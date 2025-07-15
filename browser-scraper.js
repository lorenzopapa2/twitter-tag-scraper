// 浏览器端推文抓取脚本
// 在Twitter页面的控制台中运行此脚本

let allTweets = [];
let previousHeight = 0;
let scrollAttempts = 0;
let targetCount = 2000;

function extractTweetData() {
    const tweetElements = document.querySelectorAll('article[data-testid="tweet"]');
    const tweets = [];
    
    tweetElements.forEach(element => {
        try {
            // 提取推文ID
            const linkElement = element.querySelector('a[href*="/status/"]');
            if (!linkElement) return;
            
            const href = linkElement.href;
            const idMatch = href.match(/\/status\/(\d+)/);
            const tweetId = idMatch ? idMatch[1] : null;
            
            if (!tweetId || allTweets.some(t => t.id === tweetId)) return;
            
            // 提取文本
            const textElement = element.querySelector('[data-testid="tweetText"]');
            const text = textElement ? textElement.innerText : '';
            
            // 提取作者信息
            const usernameMatch = href.match(/twitter\.com\/([^\/]+)\/status/) || href.match(/x\.com\/([^\/]+)\/status/);
            const username = usernameMatch ? usernameMatch[1] : '';
            
            // 查找作者名称
            const authorNameElement = element.querySelector('div[dir="ltr"] > span');
            const authorName = authorNameElement ? authorNameElement.innerText : username;
            
            // 提取时间
            const timeElement = element.querySelector('time');
            const datetime = timeElement ? timeElement.getAttribute('datetime') : '';
            const relativeTime = timeElement ? timeElement.innerText : '';
            
            // 提取互动数据
            const replyButton = element.querySelector('[data-testid="reply"]');
            const retweetButton = element.querySelector('[data-testid="retweet"]');
            const likeButton = element.querySelector('[data-testid="like"]');
            
            const extractCount = (element) => {
                if (!element) return 0;
                const text = element.getAttribute('aria-label') || element.innerText || '0';
                const match = text.match(/(\d+\.?\d*[KMB]?)/);
                if (!match) return 0;
                
                let count = match[1];
                if (count.includes('K')) return parseFloat(count) * 1000;
                if (count.includes('M')) return parseFloat(count) * 1000000;
                if (count.includes('B')) return parseFloat(count) * 1000000000;
                return parseInt(count) || 0;
            };
            
            const replies = extractCount(replyButton);
            const retweets = extractCount(retweetButton);
            const likes = extractCount(likeButton);
            
            // 查找浏览量
            const viewsElement = Array.from(element.querySelectorAll('a')).find(a => 
                a.href && a.href.includes('/analytics')
            );
            const views = viewsElement ? extractCount(viewsElement) : 0;
            
            // 检查是否有图片
            const hasImage = element.querySelector('img[src*="pbs.twimg.com/media"]') !== null;
            
            // 检查是否是认证账号
            const isVerified = element.querySelector('svg[aria-label="Verified account"]') !== null;
            
            tweets.push({
                id: tweetId,
                author_name: authorName,
                author_username: username,
                text: text,
                created_at: datetime,
                relative_time: relativeTime,
                replies: replies,
                retweets: retweets,
                likes: likes,
                views: views,
                has_image: hasImage,
                is_verified: isVerified,
                url: `https://x.com/${username}/status/${tweetId}`
            });
        } catch (error) {
            console.error('Error extracting tweet:', error);
        }
    });
    
    return tweets;
}

async function scrollAndCollect() {
    console.log(`开始抓取推文，目标数量: ${targetCount}`);
    
    while (allTweets.length < targetCount && scrollAttempts < 50) {
        // 抓取当前页面的推文
        const newTweets = extractTweetData();
        newTweets.forEach(tweet => {
            if (!allTweets.some(t => t.id === tweet.id)) {
                allTweets.push(tweet);
            }
        });
        
        console.log(`已抓取 ${allTweets.length} 条推文`);
        
        // 滚动到页面底部
        const currentHeight = document.body.scrollHeight;
        window.scrollTo(0, currentHeight);
        
        // 等待新内容加载
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 检查是否有新内容加载
        const newHeight = document.body.scrollHeight;
        if (newHeight === previousHeight) {
            scrollAttempts++;
            console.log(`没有新内容加载，尝试 ${scrollAttempts}/50`);
        } else {
            scrollAttempts = 0;
            previousHeight = newHeight;
        }
    }
    
    console.log(`抓取完成！共收集 ${allTweets.length} 条推文`);
    
    // 下载数据
    downloadData();
}

function downloadData() {
    // 转换为CSV格式
    const csvHeaders = [
        'ID', '作者名称', '作者用户名', '是否认证', '推文内容', 
        '发布时间', '相对时间', '回复数', '转发数', '点赞数', 
        '浏览量', '是否有图片', '推文链接'
    ];
    
    const csvRows = allTweets.map(tweet => [
        tweet.id,
        tweet.author_name,
        `@${tweet.author_username}`,
        tweet.is_verified ? '是' : '否',
        `"${tweet.text.replace(/"/g, '""')}"`,
        tweet.created_at,
        tweet.relative_time,
        tweet.replies,
        tweet.retweets,
        tweet.likes,
        tweet.views,
        tweet.has_image ? '是' : '否',
        tweet.url
    ]);
    
    const csvContent = [
        csvHeaders.join(','),
        ...csvRows.map(row => row.join(','))
    ].join('\n');
    
    // 下载CSV文件
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `UnlockRitual_tweets_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    
    // 同时保存JSON格式
    const jsonBlob = new Blob([JSON.stringify(allTweets, null, 2)], { type: 'application/json' });
    const jsonLink = document.createElement('a');
    jsonLink.href = URL.createObjectURL(jsonBlob);
    jsonLink.download = `UnlockRitual_tweets_${new Date().toISOString().split('T')[0]}.json`;
    jsonLink.click();
    
    console.log('数据已下载！');
}

// 开始执行
scrollAndCollect();