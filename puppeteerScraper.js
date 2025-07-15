require('dotenv').config();
const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

class PuppeteerScraper {
    constructor() {
        this.authToken = process.env.AUTH_TOKEN;
        this.ct0 = process.env.CT0;
        this.dataDir = path.join(__dirname, 'data');
        this.tweetsFile = path.join(this.dataDir, 'tweets.json');
    }

    async init() {
        try {
            await fs.mkdir(this.dataDir, { recursive: true });
            
            try {
                await fs.access(this.tweetsFile);
            } catch {
                await fs.writeFile(this.tweetsFile, JSON.stringify([], null, 2));
            }
        } catch (error) {
            console.error('初始化失败:', error);
        }
    }

    async setupBrowser() {
        const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        
        // 设置cookies
        await page.setCookie(
            {
                name: 'auth_token',
                value: this.authToken,
                domain: '.twitter.com',
                path: '/',
                httpOnly: true,
                secure: true,
                sameSite: 'None'
            },
            {
                name: 'ct0',
                value: this.ct0,
                domain: '.twitter.com',
                path: '/',
                httpOnly: false,
                secure: true,
                sameSite: 'Lax'
            }
        );

        // 设置User-Agent
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
        
        return { browser, page };
    }

    async scrapeHashtag(hashtag) {
        console.log(`开始使用Puppeteer抓取标签 #${hashtag} 的推文...`);
        
        let browser;
        try {
            const { browser: b, page } = await this.setupBrowser();
            browser = b;

            // 访问搜索页面
            const searchUrl = `https://twitter.com/search?q=%23${hashtag}&src=typed_query&f=live`;
            await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 30000 });

            // 等待推文加载
            await page.waitForSelector('article[data-testid="tweet"]', { timeout: 10000 }).catch(() => {
                console.log('未找到推文元素，可能需要登录或没有相关推文');
            });

            // 滚动页面以加载更多推文
            let previousHeight = 0;
            let scrollAttempts = 0;
            const maxScrollAttempts = 5;

            while (scrollAttempts < maxScrollAttempts) {
                const currentHeight = await page.evaluate(() => document.body.scrollHeight);
                
                if (currentHeight > previousHeight) {
                    previousHeight = currentHeight;
                    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    scrollAttempts = 0;
                } else {
                    scrollAttempts++;
                }
            }

            // 抓取推文数据
            const tweets = await page.evaluate(() => {
                const tweetElements = document.querySelectorAll('article[data-testid="tweet"]');
                const tweetsData = [];

                tweetElements.forEach(element => {
                    try {
                        // 提取推文文本
                        const textElement = element.querySelector('[data-testid="tweetText"]');
                        const text = textElement ? textElement.innerText : '';

                        // 提取作者信息
                        const authorElement = element.querySelector('a[href*="/status/"]');
                        const authorUrl = authorElement ? authorElement.href : '';
                        const tweetIdMatch = authorUrl.match(/\/status\/(\d+)/);
                        const tweetId = tweetIdMatch ? tweetIdMatch[1] : '';

                        const usernameMatch = authorUrl.match(/twitter\.com\/([^\/]+)\/status/);
                        const username = usernameMatch ? usernameMatch[1] : '';

                        // 提取时间
                        const timeElement = element.querySelector('time');
                        const time = timeElement ? timeElement.getAttribute('datetime') : '';

                        // 提取互动数据
                        const replyButton = element.querySelector('[data-testid="reply"]');
                        const retweetButton = element.querySelector('[data-testid="retweet"]');
                        const likeButton = element.querySelector('[data-testid="like"]');

                        const replies = replyButton ? replyButton.innerText || '0' : '0';
                        const retweets = retweetButton ? retweetButton.innerText || '0' : '0';
                        const likes = likeButton ? likeButton.innerText || '0' : '0';

                        if (tweetId && text) {
                            tweetsData.push({
                                id: tweetId,
                                text: text,
                                created_at: time,
                                author: {
                                    username: username
                                },
                                metrics: {
                                    replies: parseInt(replies.replace(/[^\d]/g, '') || 0),
                                    retweets: parseInt(retweets.replace(/[^\d]/g, '') || 0),
                                    likes: parseInt(likes.replace(/[^\d]/g, '') || 0)
                                },
                                url: authorUrl
                            });
                        }
                    } catch (error) {
                        console.error('解析推文出错:', error);
                    }
                });

                return tweetsData;
            });

            await browser.close();

            // 保存推文
            const existingTweets = await this.loadExistingTweets();
            const existingIds = new Set(existingTweets.map(t => t.id));
            
            const newTweets = tweets.filter(tweet => !existingIds.has(tweet.id));
            
            if (newTweets.length > 0) {
                const allTweets = [...newTweets, ...existingTweets];
                await this.saveTweets(allTweets);
                console.log(`发现并保存了 ${newTweets.length} 条新推文`);
            } else {
                console.log('没有发现新推文');
            }

            return newTweets;
        } catch (error) {
            console.error('抓取过程出错:', error);
            if (browser) {
                await browser.close();
            }
            return [];
        }
    }

    async loadExistingTweets() {
        try {
            const data = await fs.readFile(this.tweetsFile, 'utf-8');
            return JSON.parse(data);
        } catch (error) {
            console.error('加载现有推文失败:', error);
            return [];
        }
    }

    async saveTweets(tweets) {
        try {
            await fs.writeFile(this.tweetsFile, JSON.stringify(tweets, null, 2));
            console.log(`已保存 ${tweets.length} 条推文`);
        } catch (error) {
            console.error('保存推文失败:', error);
        }
    }
}

module.exports = PuppeteerScraper;