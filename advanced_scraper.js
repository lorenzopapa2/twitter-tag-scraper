// 高级Twitter推文抓取脚本 - 解决重复问题
// 在Twitter页面的控制台中运行此脚本

class TwitterScraper {
    constructor() {
        this.allTweets = new Map(); // 使用Map存储，key为推文ID
        this.targetCount = 2000;
        this.scrollAttempts = 0;
        this.maxScrollAttempts = 100;
        this.lastHeight = 0;
        this.duplicateCount = 0;
        this.uniqueAuthors = new Set();
    }

    // 提取推文唯一ID
    extractTweetId(element) {
        const linkElement = element.querySelector('a[href*="/status/"]');
        if (!linkElement) return null;
        
        const href = linkElement.href;
        const idMatch = href.match(/\/status\/(\d+)/);
        return idMatch ? idMatch[1] : null;
    }

    // 提取单条推文数据
    extractTweetData(element) {
        try {
            const tweetId = this.extractTweetId(element);
            if (!tweetId) return null;

            // 如果已存在，跳过
            if (this.allTweets.has(tweetId)) {
                this.duplicateCount++;
                return null;
            }

            // 提取文本
            const textElement = element.querySelector('[data-testid="tweetText"]');
            const text = textElement ? textElement.innerText.trim() : '';

            // 跳过空文本
            if (!text) return null;

            // 提取作者信息
            const linkElement = element.querySelector('a[href*="/status/"]');
            const href = linkElement ? linkElement.href : '';
            const usernameMatch = href.match(/\/([^\/]+)\/status/);
            const username = usernameMatch ? usernameMatch[1] : '';

            // 查找作者名称 - 更精确的选择器
            let authorName = username;
            const nameElement = element.querySelector('div[data-testid="User-Name"] span:first-child');
            if (nameElement) {
                authorName = nameElement.innerText.trim();
            }

            // 提取时间
            const timeElement = element.querySelector('time');
            const datetime = timeElement ? timeElement.getAttribute('datetime') : '';
            const relativeTime = timeElement ? timeElement.innerText : '';

            // 提取互动数据 - 更准确的方法
            const getMetricValue = (testId) => {
                const button = element.querySelector(`[data-testid="${testId}"]`);
                if (!button) return 0;
                
                const ariaLabel = button.getAttribute('aria-label') || '';
                const match = ariaLabel.match(/(\d+)/);
                if (match) return parseInt(match[1]);
                
                const span = button.querySelector('span');
                if (span && span.innerText) {
                    const text = span.innerText.trim();
                    if (text === '') return 0;
                    
                    // 处理K/M后缀
                    if (text.includes('K')) return Math.round(parseFloat(text) * 1000);
                    if (text.includes('M')) return Math.round(parseFloat(text) * 1000000);
                    return parseInt(text) || 0;
                }
                return 0;
            };

            const replies = getMetricValue('reply');
            const retweets = getMetricValue('retweet');
            const likes = getMetricValue('like');

            // 查找浏览量
            let views = 0;
            const viewsElement = Array.from(element.querySelectorAll('a')).find(a => 
                a.href && a.href.includes('/analytics')
            );
            if (viewsElement) {
                const viewsText = viewsElement.innerText || '0';
                if (viewsText.includes('K')) views = Math.round(parseFloat(viewsText) * 1000);
                else if (viewsText.includes('M')) views = Math.round(parseFloat(viewsText) * 1000000);
                else views = parseInt(viewsText) || 0;
            }

            // 计算互动率
            const totalEngagement = replies + retweets + likes;
            const engagementRate = views > 0 ? ((totalEngagement / views) * 100).toFixed(2) : '0.00';

            // 检查是否有图片
            const hasImage = element.querySelector('img[src*="pbs.twimg.com/media"]') !== null;

            // 检查是否是认证账号
            const isVerified = element.querySelector('svg[aria-label*="Verified"]') !== null;

            // 记录唯一作者
            this.uniqueAuthors.add(username);

            return {
                id: tweetId,
                author_name: authorName,
                author_username: `@${username}`,
                text: text,
                created_at: datetime,
                relative_time: relativeTime,
                replies: replies,
                retweets: retweets,
                likes: likes,
                views: views,
                engagement_rate: engagementRate,
                has_image: hasImage,
                is_verified: isVerified,
                url: `https://x.com/${username}/status/${tweetId}`,
                scraped_at: new Date().toISOString()
            };
        } catch (error) {
            console.error('提取推文数据时出错:', error);
            return null;
        }
    }

    // 抓取当前可见的所有推文
    scrapeVisibleTweets() {
        const tweetElements = document.querySelectorAll('article[data-testid="tweet"]');
        let newTweetsCount = 0;

        tweetElements.forEach(element => {
            const tweetData = this.extractTweetData(element);
            if (tweetData) {
                this.allTweets.set(tweetData.id, tweetData);
                newTweetsCount++;
            }
        });

        return newTweetsCount;
    }

    // 滚动页面
    async scrollPage() {
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 2000));
    }

    // 主抓取函数
    async startScraping() {
        console.log(`🚀 开始抓取推文，目标数量: ${this.targetCount}`);
        console.log('----------------------------------------');

        while (this.allTweets.size < this.targetCount && this.scrollAttempts < this.maxScrollAttempts) {
            // 抓取当前页面的推文
            const newTweets = this.scrapeVisibleTweets();
            
            console.log(`✅ 已抓取: ${this.allTweets.size} 条唯一推文 | 新增: ${newTweets} 条 | 重复: ${this.duplicateCount} 条`);
            console.log(`👥 唯一作者数: ${this.uniqueAuthors.size}`);

            // 检查是否达到目标
            if (this.allTweets.size >= this.targetCount) {
                break;
            }

            // 滚动页面
            const currentHeight = document.body.scrollHeight;
            await this.scrollPage();

            // 检查是否有新内容加载
            const newHeight = document.body.scrollHeight;
            if (newHeight === this.lastHeight) {
                this.scrollAttempts++;
                console.log(`⚠️ 没有新内容加载，尝试 ${this.scrollAttempts}/${this.maxScrollAttempts}`);
                
                // 尝试向上滚动一点再向下
                window.scrollBy(0, -500);
                await new Promise(resolve => setTimeout(resolve, 500));
                window.scrollTo(0, document.body.scrollHeight);
                await new Promise(resolve => setTimeout(resolve, 2000));
            } else {
                this.scrollAttempts = 0;
                this.lastHeight = newHeight;
            }

            // 每50条推文暂停一下，避免请求过快
            if (this.allTweets.size % 50 === 0 && this.allTweets.size > 0) {
                console.log('⏸️ 暂停3秒，避免请求过快...');
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
        }

        console.log('----------------------------------------');
        console.log(`✅ 抓取完成！共收集 ${this.allTweets.size} 条唯一推文`);
        console.log(`📊 统计信息:`);
        console.log(`   - 唯一推文数: ${this.allTweets.size}`);
        console.log(`   - 重复推文数: ${this.duplicateCount}`);
        console.log(`   - 唯一作者数: ${this.uniqueAuthors.size}`);
        console.log(`   - 平均每位作者发推数: ${(this.allTweets.size / this.uniqueAuthors.size).toFixed(2)}`);

        return Array.from(this.allTweets.values());
    }

    // 生成统计报告
    generateStats(tweets) {
        const stats = {
            total: tweets.length,
            withImages: tweets.filter(t => t.has_image).length,
            verified: tweets.filter(t => t.is_verified).length,
            avgLikes: (tweets.reduce((sum, t) => sum + t.likes, 0) / tweets.length).toFixed(2),
            avgRetweets: (tweets.reduce((sum, t) => sum + t.retweets, 0) / tweets.length).toFixed(2),
            avgReplies: (tweets.reduce((sum, t) => sum + t.replies, 0) / tweets.length).toFixed(2),
            avgViews: (tweets.reduce((sum, t) => sum + t.views, 0) / tweets.length).toFixed(2),
            avgEngagement: (tweets.reduce((sum, t) => sum + parseFloat(t.engagement_rate), 0) / tweets.length).toFixed(2),
            topAuthors: this.getTopAuthors(tweets, 10)
        };

        return stats;
    }

    // 获取发推最多的作者
    getTopAuthors(tweets, limit = 10) {
        const authorCounts = {};
        tweets.forEach(tweet => {
            const author = tweet.author_username;
            authorCounts[author] = (authorCounts[author] || 0) + 1;
        });

        return Object.entries(authorCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([author, count]) => ({ author, count }));
    }

    // 导出为CSV
    exportToCSV(tweets) {
        const headers = [
            'ID', '作者名称', '作者用户名', '是否认证', '推文内容', 
            '发布时间', '相对时间', '回复数', '转发数', '点赞数', 
            '浏览量', '互动率%', '是否有图片', '推文链接', '抓取时间'
        ];

        const csvRows = [headers.join(',')];
        
        tweets.forEach((tweet, index) => {
            const row = [
                index + 1,
                `"${tweet.author_name}"`,
                tweet.author_username,
                tweet.is_verified ? '是' : '否',
                `"${tweet.text.replace(/"/g, '""')}"`,
                tweet.created_at,
                tweet.relative_time,
                tweet.replies,
                tweet.retweets,
                tweet.likes,
                tweet.views,
                tweet.engagement_rate,
                tweet.has_image ? '是' : '否',
                tweet.url,
                tweet.scraped_at
            ];
            csvRows.push(row.join(','));
        });

        const csvContent = '\ufeff' + csvRows.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `Twitter_UnlockRitual_${this.allTweets.size}条_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
    }

    // 导出为JSON
    exportToJSON(tweets) {
        const data = {
            metadata: {
                total_tweets: tweets.length,
                unique_authors: this.uniqueAuthors.size,
                duplicate_removed: this.duplicateCount,
                scraped_at: new Date().toISOString(),
                hashtag: '#UnlockRitual'
            },
            stats: this.generateStats(tweets),
            tweets: tweets
        };

        const jsonContent = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonContent], { type: 'application/json' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `Twitter_UnlockRitual_${this.allTweets.size}条_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    }

    // 导出数据
    async exportData() {
        const tweets = Array.from(this.allTweets.values());
        
        // 按时间排序（最新的在前）
        tweets.sort((a, b) => {
            if (a.created_at && b.created_at) {
                return new Date(b.created_at) - new Date(a.created_at);
            }
            return 0;
        });

        // 显示统计信息
        const stats = this.generateStats(tweets);
        console.log('\n📊 数据统计:');
        console.log(`   - 总推文数: ${stats.total}`);
        console.log(`   - 包含图片: ${stats.withImages} (${(stats.withImages/stats.total*100).toFixed(1)}%)`);
        console.log(`   - 认证账号: ${stats.verified} (${(stats.verified/stats.total*100).toFixed(1)}%)`);
        console.log(`   - 平均点赞: ${stats.avgLikes}`);
        console.log(`   - 平均转发: ${stats.avgRetweets}`);
        console.log(`   - 平均回复: ${stats.avgReplies}`);
        console.log(`   - 平均浏览: ${stats.avgViews}`);
        console.log(`   - 平均互动率: ${stats.avgEngagement}%`);
        console.log('\n🏆 发推最多的作者:');
        stats.topAuthors.forEach((author, index) => {
            console.log(`   ${index + 1}. ${author.author} - ${author.count} 条推文`);
        });

        // 导出文件
        this.exportToCSV(tweets);
        this.exportToJSON(tweets);
        
        console.log('\n✅ 数据已导出为CSV和JSON格式！');
    }
}

// 执行抓取
async function runScraper() {
    const scraper = new TwitterScraper();
    await scraper.startScraping();
    await scraper.exportData();
}

// 启动
console.log('🔧 Twitter推文抓取器已准备就绪！');
console.log('📌 当前页面应该是 #UnlockRitual 标签搜索结果');
console.log('⚡ 开始抓取...\n');
runScraper();