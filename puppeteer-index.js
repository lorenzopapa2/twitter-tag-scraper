require('dotenv').config();
const PuppeteerScraper = require('./puppeteerScraper');

async function main() {
    const hashtag = process.env.HASHTAG || 'UnlockRitual';

    console.log(`初始化 Puppeteer Twitter 推文抓取器...`);
    console.log(`目标标签: #${hashtag}`);

    const scraper = new PuppeteerScraper();
    await scraper.init();

    const args = process.argv.slice(2);
    
    if (args.includes('--once')) {
        console.log('执行单次抓取...');
        await scraper.scrapeHashtag(hashtag);
    } else {
        const intervalMinutes = parseInt(args.find(arg => arg.startsWith('--interval='))?.split('=')[1]) || 5;
        
        console.log(`开始定期抓取，间隔: ${intervalMinutes} 分钟`);
        
        // 首次抓取
        await scraper.scrapeHashtag(hashtag);
        
        // 定期抓取
        setInterval(async () => {
            console.log(`\n[${new Date().toLocaleString()}] 执行定期抓取...`);
            await scraper.scrapeHashtag(hashtag);
        }, intervalMinutes * 60 * 1000);
        
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