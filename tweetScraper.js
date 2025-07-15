const TwitterClient = require('./twitterClient');
const fs = require('fs').promises;
const path = require('path');

class TweetScraper {
    constructor(twitterClient) {
        this.twitterClient = twitterClient;
        this.dataDir = path.join(__dirname, 'data');
        this.tweetsFile = path.join(this.dataDir, 'tweets.json');
        this.lastCheckFile = path.join(this.dataDir, 'lastCheck.json');
    }

    async init() {
        try {
            await fs.mkdir(this.dataDir, { recursive: true });
            
            try {
                await fs.access(this.tweetsFile);
            } catch {
                await fs.writeFile(this.tweetsFile, JSON.stringify([], null, 2));
            }

            try {
                await fs.access(this.lastCheckFile);
            } catch {
                await fs.writeFile(this.lastCheckFile, JSON.stringify({ lastCheckTime: null, lastTweetId: null }, null, 2));
            }
        } catch (error) {
            console.error('初始化失败:', error);
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

    async updateLastCheck(tweetId) {
        try {
            const lastCheck = {
                lastCheckTime: new Date().toISOString(),
                lastTweetId: tweetId
            };
            await fs.writeFile(this.lastCheckFile, JSON.stringify(lastCheck, null, 2));
        } catch (error) {
            console.error('更新最后检查时间失败:', error);
        }
    }

    formatTweet(tweet, author) {
        return {
            id: tweet.id,
            text: tweet.text,
            created_at: tweet.created_at,
            author: {
                id: author?.id,
                name: author?.name,
                username: author?.username
            },
            metrics: {
                likes: tweet.public_metrics?.like_count || 0,
                retweets: tweet.public_metrics?.retweet_count || 0,
                replies: tweet.public_metrics?.reply_count || 0,
                quotes: tweet.public_metrics?.quote_count || 0
            },
            url: `https://twitter.com/${author?.username}/status/${tweet.id}`
        };
    }

    async scrapeHashtag(hashtag, maxResults = 100) {
        console.log(`开始抓取标签 #${hashtag} 的推文...`);
        
        try {
            const result = await this.twitterClient.getTweetsByHashtag(hashtag, maxResults);
            
            if (!result || result.length === 0) {
                console.log('未找到新推文');
                return [];
            }

            const existingTweets = await this.loadExistingTweets();
            const existingIds = new Set(existingTweets.map(t => t.id));
            
            const newTweets = [];
            for (const tweet of result) {
                if (!existingIds.has(tweet.id)) {
                    const author = tweet.author || {};
                    const formattedTweet = this.formatTweet(tweet, author);
                    newTweets.push(formattedTweet);
                }
            }

            if (newTweets.length > 0) {
                const allTweets = [...newTweets, ...existingTweets];
                await this.saveTweets(allTweets);
                await this.updateLastCheck(newTweets[0].id);
                console.log(`发现并保存了 ${newTweets.length} 条新推文`);
            } else {
                console.log('没有发现新推文');
            }

            return newTweets;
        } catch (error) {
            console.error('抓取推文时出错:', error);
            return [];
        }
    }

    async startPeriodicScraping(hashtag, intervalMinutes = 5) {
        console.log(`开始定期抓取，间隔: ${intervalMinutes} 分钟`);
        
        await this.scrapeHashtag(hashtag);
        
        setInterval(async () => {
            console.log(`\n[${new Date().toLocaleString()}] 执行定期抓取...`);
            await this.scrapeHashtag(hashtag);
        }, intervalMinutes * 60 * 1000);
    }
}

module.exports = TweetScraper;