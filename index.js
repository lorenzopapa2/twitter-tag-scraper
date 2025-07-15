require('dotenv').config();
const TwitterWebClient = require('./twitterWebClient');
const TweetScraper = require('./tweetScraper');

async function main() {
    const authToken = process.env.AUTH_TOKEN;
    const ct0 = process.env.CT0;
    const hashtag = process.env.HASHTAG || 'UnlockRitual';

    if (!authToken || !ct0) {
        console.error('错误: 请在 .env 文件中设置 AUTH_TOKEN 和 CT0');
        process.exit(1);
    }

    console.log(`初始化 Twitter 推文抓取器...`);
    console.log(`目标标签: #${hashtag}`);

    const twitterClient = new TwitterWebClient(authToken, ct0);
    const scraper = new TweetScraper(twitterClient);

    await scraper.init();

    const args = process.argv.slice(2);
    
    if (args.includes('--once')) {
        console.log('执行单次抓取...');
        await scraper.scrapeHashtag(hashtag, 100);
    } else {
        const intervalMinutes = parseInt(args.find(arg => arg.startsWith('--interval='))?.split('=')[1]) || 5;
        await scraper.startPeriodicScraping(hashtag, intervalMinutes);
        
        console.log('按 Ctrl+C 停止程序');
    }
}

process.on('SIGINT', () => {
    console.log('\n程序已停止');
    process.exit(0);
});

main().catch(error => {
    console.error('程序出错:', error);
    process.exit(1);
});