#!/usr/bin/env python3
"""
Twitter推文数据生成器
基于 #UnlockRitual 标签的真实推文模式生成2000条推文数据
"""

import json
import random
import datetime
from datetime import timedelta
import uuid
import hashlib

class TweetGenerator:
    def __init__(self):
        # 基于真实推文的模板
        self.templates = [
            # AI去中心化主题
            "In the web3 world, AI should not be monopolized by central companies. @ritualnet is building the future of decentralized AI infrastructure. #UnlockRitual",
            "@ritualnet is breaking Big Tech's monopoly on AI. Their decentralized network ensures AI remains open and accessible to everyone. #UnlockRitual #DeFAI",
            "Ritual's game-changing AI runs directly on-chain, bringing transparency and trust to artificial intelligence. This is the future we need! #UnlockRitual",
            "Why should a few corporations control AI? @ritualnet is democratizing access to AI through blockchain technology. #UnlockRitual #Web3AI",
            "The fusion of AI and blockchain is here! @ritualnet is pioneering decentralized AI infrastructure for the next generation. #UnlockRitual",
            
            # 技术创新主题
            "Ritual is revolutionizing how we think about AI computation. Distributed, transparent, and community-owned. #UnlockRitual @ritualnet",
            "On-chain AI inference is no longer a dream. @ritualnet makes it reality with their groundbreaking protocol. #UnlockRitual #DeFAI",
            "Imagine AI models that can't be censored or controlled by any single entity. That's what @ritualnet is building. #UnlockRitual",
            "Smart contracts + AI = The future of autonomous systems. @ritualnet is leading this transformation. #UnlockRitual #Web3",
            "Ritual's approach to decentralized AI computation is genius. Finally, AI that serves the community, not corporations. #UnlockRitual",
            
            # 社区和生态系统主题
            "Join the @ritualnet community and be part of the AI revolution! Together we're building a decentralized future. #UnlockRitual",
            "The @ritualnet ecosystem is growing rapidly. Developers, researchers, and enthusiasts all working towards open AI. #UnlockRitual",
            "Excited to see what builders will create with @ritualnet's infrastructure. The possibilities are endless! #UnlockRitual #BuildOnRitual",
            "Community-driven AI is the way forward. @ritualnet empowers everyone to participate in the AI economy. #UnlockRitual",
            "The future of AI belongs to the community, not corporations. Join @ritualnet in this revolution! #UnlockRitual",
            
            # 投资和机会主题
            "Don't miss out on the next big thing in crypto x AI. @ritualnet is positioning itself as a leader in DeFAI. #UnlockRitual",
            "Early supporters of @ritualnet understand the massive potential of decentralized AI infrastructure. #UnlockRitual #DeFAI",
            "The convergence of AI and blockchain creates unprecedented opportunities. @ritualnet is at the forefront. #UnlockRitual",
            "Investing in the future means investing in decentralized AI. @ritualnet is building that future today. #UnlockRitual",
            "Smart money is flowing into DeFAI projects. @ritualnet stands out with its innovative approach. #UnlockRitual",
            
            # 应用场景主题
            "From DeFi to GameFi, every sector needs AI. @ritualnet provides the infrastructure to make it happen on-chain. #UnlockRitual",
            "Imagine DApps with built-in AI capabilities. @ritualnet makes this possible with their protocol. #UnlockRitual #Web3AI",
            "NFT collections can now integrate AI features thanks to @ritualnet's infrastructure. Game-changing! #UnlockRitual",
            "The metaverse needs decentralized AI. @ritualnet is building the foundation for intelligent virtual worlds. #UnlockRitual",
            "DeFi protocols can now leverage AI for better decision-making, all thanks to @ritualnet. #UnlockRitual #DeFAI"
        ]
        
        # 用户名生成组件
        self.username_prefixes = ["crypto", "web3", "defi", "nft", "eth", "btc", "sol", "chain", "block", "token", "dao", "meta"]
        self.username_suffixes = ["trader", "holder", "builder", "dev", "investor", "whale", "degen", "maxi", "punk", "ape", "guru", "alpha"]
        
        # 额外的标签
        self.additional_hashtags = ["#DeFAI", "#Web3AI", "#DecentralizedAI", "#AIonChain", "#RitualNetwork", "#BuildOnRitual", "#OpenAI", "#CryptoAI"]
        
        # 表情符号
        self.emojis = ["🚀", "🔥", "💎", "🌟", "⚡", "🎯", "💡", "🔮", "🌐", "🤖", "🧠", "⛓️", "🔐", "🌈", "✨"]
        
    def generate_username(self):
        """生成随机用户名"""
        prefix = random.choice(self.username_prefixes)
        suffix = random.choice(self.username_suffixes)
        number = random.randint(1, 9999)
        return f"{prefix}_{suffix}{number}"
    
    def generate_display_name(self, username):
        """生成显示名称"""
        names = [
            "DeFi Enthusiast", "Web3 Builder", "Crypto Investor", "Blockchain Dev",
            "NFT Collector", "DAO Member", "AI Researcher", "Tech Innovator",
            "Digital Nomad", "Metaverse Explorer", "Smart Contract Auditor", "Token Economist"
        ]
        emoji = random.choice(self.emojis)
        return f"{random.choice(names)} {emoji}"
    
    def generate_tweet_text(self):
        """生成推文文本"""
        base_text = random.choice(self.templates)
        
        # 30%的概率添加额外的标签
        if random.random() < 0.3:
            extra_tags = random.sample(self.additional_hashtags, k=random.randint(1, 2))
            base_text += " " + " ".join(extra_tags)
        
        # 20%的概率添加表情符号
        if random.random() < 0.2:
            emojis = random.sample(self.emojis, k=random.randint(1, 3))
            base_text += " " + " ".join(emojis)
        
        # 10%的概率添加个性化内容
        if random.random() < 0.1:
            personal_additions = [
                " LFG!", " This is the way!", " WAGMI!", " To the moon!",
                " Bullish AF!", " Game changer!", " Mind blown!", " This is huge!"
            ]
            base_text += random.choice(personal_additions)
        
        return base_text
    
    def generate_engagement(self):
        """生成互动数据（点赞、转发、回复）"""
        # 使用真实的分布模式
        # 大部分推文互动较少，少数推文互动很高
        if random.random() < 0.7:  # 70%的推文互动较少
            likes = random.randint(0, 50)
            retweets = random.randint(0, 20)
            replies = random.randint(0, 10)
        elif random.random() < 0.95:  # 25%的推文互动中等
            likes = random.randint(50, 500)
            retweets = random.randint(20, 200)
            replies = random.randint(10, 100)
        else:  # 5%的推文互动很高
            likes = random.randint(500, 5000)
            retweets = random.randint(200, 2000)
            replies = random.randint(100, 1000)
        
        return likes, retweets, replies
    
    def generate_timestamp(self, start_date, end_date):
        """生成随机时间戳"""
        time_between = end_date - start_date
        random_seconds = random.randint(0, int(time_between.total_seconds()))
        return start_date + timedelta(seconds=random_seconds)
    
    def generate_tweet(self, index):
        """生成单条推文数据"""
        username = self.generate_username()
        display_name = self.generate_display_name(username)
        text = self.generate_tweet_text()
        likes, retweets, replies = self.generate_engagement()
        
        # 生成时间（最近30天内）
        end_date = datetime.datetime.now()
        start_date = end_date - timedelta(days=30)
        timestamp = self.generate_timestamp(start_date, end_date)
        
        # 生成唯一ID（基于内容的哈希）
        unique_string = f"{username}_{text}_{timestamp.isoformat()}_{index}"
        tweet_id = hashlib.md5(unique_string.encode()).hexdigest()[:16]
        
        # 用户ID
        user_id = hashlib.md5(username.encode()).hexdigest()[:12]
        
        # 是否有媒体（20%概率有图片）
        has_media = random.random() < 0.2
        media_type = "photo" if has_media else None
        
        # 是否被验证（10%概率）
        is_verified = random.random() < 0.1
        
        # 粉丝数（基于互动数据）
        if likes > 500:
            followers = random.randint(10000, 100000)
        elif likes > 50:
            followers = random.randint(1000, 10000)
        else:
            followers = random.randint(100, 1000)
        
        tweet = {
            "id": tweet_id,
            "text": text,
            "username": username,
            "displayName": display_name,
            "userId": user_id,
            "createdAt": timestamp.isoformat(),
            "likes": likes,
            "retweets": retweets,
            "replies": replies,
            "hasMedia": has_media,
            "mediaType": media_type,
            "isVerified": is_verified,
            "followers": followers,
            "following": random.randint(100, 5000),
            "url": f"https://twitter.com/{username}/status/{tweet_id}",
            "source": "Twitter Web App",
            "language": "en"
        }
        
        return tweet
    
    def generate_tweets(self, count=2000):
        """生成指定数量的推文"""
        tweets = []
        seen_ids = set()
        
        print(f"开始生成{count}条推文...")
        
        for i in range(count):
            tweet = self.generate_tweet(i)
            
            # 确保ID唯一
            while tweet["id"] in seen_ids:
                tweet = self.generate_tweet(i)
            
            seen_ids.add(tweet["id"])
            tweets.append(tweet)
            
            if (i + 1) % 100 == 0:
                print(f"已生成 {i + 1} 条推文...")
        
        print(f"成功生成{count}条推文！")
        return tweets

def save_tweets_json(tweets, filename="generated_tweets.json"):
    """保存推文数据到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)
    print(f"推文数据已保存到 {filename}")

def create_interactive_html(tweets, filename="interactive_tweets.html"):
    """创建交互式HTML文件"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UnlockRitual 推文数据管理系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background-color: #f5f8fa;
            color: #14171a;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #1da1f2 0%, #0a85d1 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .stat-card h3 {
            color: #657786;
            font-size: 14px;
            font-weight: normal;
            margin-bottom: 5px;
        }
        
        .stat-card .value {
            font-size: 28px;
            font-weight: bold;
            color: #1da1f2;
        }
        
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .search-box input {
            flex: 1;
            padding: 10px 15px;
            border: 1px solid #e1e8ed;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
        }
        
        .search-box input:focus {
            border-color: #1da1f2;
        }
        
        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            outline: none;
        }
        
        .btn-primary {
            background: #1da1f2;
            color: white;
        }
        
        .btn-primary:hover {
            background: #0a85d1;
        }
        
        .btn-secondary {
            background: #e1e8ed;
            color: #14171a;
        }
        
        .btn-secondary:hover {
            background: #d1d8dd;
        }
        
        .btn-success {
            background: #17bf63;
            color: white;
        }
        
        .btn-success:hover {
            background: #15a653;
        }
        
        .tweets-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            overflow: hidden;
        }
        
        .tweet {
            padding: 20px;
            border-bottom: 1px solid #e1e8ed;
            transition: background-color 0.3s ease;
        }
        
        .tweet:hover {
            background-color: #f7f9fa;
        }
        
        .tweet-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #1da1f2, #0a85d1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .user-info {
            flex: 1;
        }
        
        .display-name {
            font-weight: bold;
            margin-right: 5px;
        }
        
        .username {
            color: #657786;
        }
        
        .verified {
            color: #1da1f2;
            margin-left: 5px;
        }
        
        .tweet-text {
            margin-bottom: 15px;
            line-height: 1.5;
            white-space: pre-wrap;
        }
        
        .tweet-stats {
            display: flex;
            gap: 30px;
            color: #657786;
            font-size: 14px;
        }
        
        .stat {
            display: flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
            transition: color 0.3s ease;
        }
        
        .stat:hover {
            color: #1da1f2;
        }
        
        .tweet-actions {
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .close-btn {
            font-size: 24px;
            cursor: pointer;
            color: #657786;
        }
        
        .close-btn:hover {
            color: #14171a;
        }
        
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #e1e8ed;
            border-radius: 5px;
            font-size: 16px;
            resize: vertical;
            min-height: 150px;
        }
        
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            gap: 10px;
        }
        
        .page-btn {
            padding: 8px 12px;
            border: 1px solid #e1e8ed;
            background: white;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .page-btn:hover {
            background: #f7f9fa;
        }
        
        .page-btn.active {
            background: #1da1f2;
            color: white;
            border-color: #1da1f2;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #657786;
        }
        
        @media (max-width: 768px) {
            .controls {
                padding: 15px;
            }
            
            .search-box {
                flex-direction: column;
            }
            
            .filters {
                justify-content: center;
            }
            
            .tweet-stats {
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>#UnlockRitual 推文数据管理系统</h1>
            <p>基于真实模式生成的2000条推文数据，支持搜索、筛选和改写功能</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <h3>总推文数</h3>
                <div class="value" id="totalTweets">0</div>
            </div>
            <div class="stat-card">
                <h3>总互动数</h3>
                <div class="value" id="totalEngagement">0</div>
            </div>
            <div class="stat-card">
                <h3>平均点赞数</h3>
                <div class="value" id="avgLikes">0</div>
            </div>
            <div class="stat-card">
                <h3>独立用户数</h3>
                <div class="value" id="uniqueUsers">0</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索推文内容、用户名...">
                <button class="btn btn-primary" onclick="searchTweets()">搜索</button>
            </div>
            
            <div class="filters">
                <button class="btn btn-secondary" onclick="filterByEngagement('high')">高互动</button>
                <button class="btn btn-secondary" onclick="filterByEngagement('medium')">中等互动</button>
                <button class="btn btn-secondary" onclick="filterByEngagement('low')">低互动</button>
                <button class="btn btn-secondary" onclick="filterByMedia()">包含媒体</button>
                <button class="btn btn-secondary" onclick="filterByVerified()">认证用户</button>
                <button class="btn btn-secondary" onclick="showAll()">显示全部</button>
                <button class="btn btn-success" onclick="exportData()">导出数据</button>
            </div>
        </div>
        
        <div class="tweets-container" id="tweetsContainer">
            <div class="loading">正在加载推文数据...</div>
        </div>
        
        <div class="pagination" id="pagination"></div>
    </div>
    
    <div class="modal" id="editModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>改写推文</h2>
                <span class="close-btn" onclick="closeModal()">&times;</span>
            </div>
            <div>
                <h3>原始推文：</h3>
                <p id="originalText" style="margin: 10px 0; padding: 10px; background: #f7f9fa; border-radius: 5px;"></p>
                
                <h3>改写后的推文：</h3>
                <textarea id="rewrittenText" placeholder="在这里输入改写后的推文..."></textarea>
                
                <div style="margin-top: 20px; display: flex; gap: 10px;">
                    <button class="btn btn-primary" onclick="saveRewrite()">保存改写</button>
                    <button class="btn btn-success" onclick="autoRewrite()">AI改写建议</button>
                    <button class="btn btn-secondary" onclick="closeModal()">取消</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let allTweets = [];
        let filteredTweets = [];
        let currentPage = 1;
        const tweetsPerPage = 20;
        let currentEditIndex = -1;
        
        // 加载推文数据
        const tweetsData = ''' + json.dumps(tweets) + ''';
        
        // 初始化
        function init() {
            allTweets = tweetsData;
            filteredTweets = [...allTweets];
            updateStats();
            renderTweets();
        }
        
        // 更新统计信息
        function updateStats() {
            const totalTweets = filteredTweets.length;
            const totalEngagement = filteredTweets.reduce((sum, tweet) => 
                sum + tweet.likes + tweet.retweets + tweet.replies, 0);
            const avgLikes = Math.round(filteredTweets.reduce((sum, tweet) => 
                sum + tweet.likes, 0) / totalTweets);
            const uniqueUsers = new Set(filteredTweets.map(tweet => tweet.userId)).size;
            
            document.getElementById('totalTweets').textContent = totalTweets.toLocaleString();
            document.getElementById('totalEngagement').textContent = totalEngagement.toLocaleString();
            document.getElementById('avgLikes').textContent = avgLikes.toLocaleString();
            document.getElementById('uniqueUsers').textContent = uniqueUsers.toLocaleString();
        }
        
        // 渲染推文
        function renderTweets() {
            const container = document.getElementById('tweetsContainer');
            const start = (currentPage - 1) * tweetsPerPage;
            const end = start + tweetsPerPage;
            const pageTweets = filteredTweets.slice(start, end);
            
            if (pageTweets.length === 0) {
                container.innerHTML = '<div class="loading">没有找到匹配的推文</div>';
                return;
            }
            
            container.innerHTML = pageTweets.map((tweet, index) => `
                <div class="tweet" data-index="${start + index}">
                    <div class="tweet-header">
                        <div class="avatar">${tweet.displayName.charAt(0)}</div>
                        <div class="user-info">
                            <span class="display-name">${tweet.displayName}</span>
                            ${tweet.isVerified ? '<span class="verified">✓</span>' : ''}
                            <br>
                            <span class="username">@${tweet.username}</span>
                        </div>
                    </div>
                    <div class="tweet-text">${tweet.text}</div>
                    <div class="tweet-stats">
                        <div class="stat">
                            <span>❤️</span>
                            <span>${tweet.likes.toLocaleString()}</span>
                        </div>
                        <div class="stat">
                            <span>🔁</span>
                            <span>${tweet.retweets.toLocaleString()}</span>
                        </div>
                        <div class="stat">
                            <span>💬</span>
                            <span>${tweet.replies.toLocaleString()}</span>
                        </div>
                        ${tweet.hasMedia ? '<div class="stat">📷 媒体</div>' : ''}
                    </div>
                    <div class="tweet-actions">
                        <button class="btn btn-primary" onclick="editTweet(${start + index})">改写</button>
                        <button class="btn btn-secondary" onclick="copyTweet(${start + index})">复制</button>
                    </div>
                </div>
            `).join('');
            
            renderPagination();
        }
        
        // 渲染分页
        function renderPagination() {
            const totalPages = Math.ceil(filteredTweets.length / tweetsPerPage);
            const pagination = document.getElementById('pagination');
            
            if (totalPages <= 1) {
                pagination.innerHTML = '';
                return;
            }
            
            let html = '';
            
            if (currentPage > 1) {
                html += `<button class="page-btn" onclick="goToPage(${currentPage - 1})">上一页</button>`;
            }
            
            for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
                html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
            }
            
            if (currentPage < totalPages) {
                html += `<button class="page-btn" onclick="goToPage(${currentPage + 1})">下一页</button>`;
            }
            
            pagination.innerHTML = html;
        }
        
        // 搜索推文
        function searchTweets() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            
            if (!query) {
                filteredTweets = [...allTweets];
            } else {
                filteredTweets = allTweets.filter(tweet => 
                    tweet.text.toLowerCase().includes(query) ||
                    tweet.username.toLowerCase().includes(query) ||
                    tweet.displayName.toLowerCase().includes(query)
                );
            }
            
            currentPage = 1;
            updateStats();
            renderTweets();
        }
        
        // 按互动筛选
        function filterByEngagement(level) {
            if (level === 'high') {
                filteredTweets = allTweets.filter(tweet => tweet.likes > 500);
            } else if (level === 'medium') {
                filteredTweets = allTweets.filter(tweet => tweet.likes >= 50 && tweet.likes <= 500);
            } else {
                filteredTweets = allTweets.filter(tweet => tweet.likes < 50);
            }
            
            currentPage = 1;
            updateStats();
            renderTweets();
        }
        
        // 筛选包含媒体的推文
        function filterByMedia() {
            filteredTweets = allTweets.filter(tweet => tweet.hasMedia);
            currentPage = 1;
            updateStats();
            renderTweets();
        }
        
        // 筛选认证用户
        function filterByVerified() {
            filteredTweets = allTweets.filter(tweet => tweet.isVerified);
            currentPage = 1;
            updateStats();
            renderTweets();
        }
        
        // 显示全部
        function showAll() {
            filteredTweets = [...allTweets];
            currentPage = 1;
            document.getElementById('searchInput').value = '';
            updateStats();
            renderTweets();
        }
        
        // 跳转到指定页
        function goToPage(page) {
            currentPage = page;
            renderTweets();
            window.scrollTo(0, 0);
        }
        
        // 编辑推文
        function editTweet(index) {
            currentEditIndex = index;
            const tweet = filteredTweets[index];
            document.getElementById('originalText').textContent = tweet.text;
            document.getElementById('rewrittenText').value = tweet.rewrittenText || '';
            document.getElementById('editModal').style.display = 'flex';
        }
        
        // 关闭模态框
        function closeModal() {
            document.getElementById('editModal').style.display = 'none';
            currentEditIndex = -1;
        }
        
        // 保存改写
        function saveRewrite() {
            const rewrittenText = document.getElementById('rewrittenText').value;
            if (rewrittenText && currentEditIndex >= 0) {
                filteredTweets[currentEditIndex].rewrittenText = rewrittenText;
                // 同步到原始数据
                const originalIndex = allTweets.findIndex(t => t.id === filteredTweets[currentEditIndex].id);
                if (originalIndex >= 0) {
                    allTweets[originalIndex].rewrittenText = rewrittenText;
                }
                alert('改写已保存！');
                closeModal();
                renderTweets();
            }
        }
        
        // AI改写建议
        function autoRewrite() {
            const tweet = filteredTweets[currentEditIndex];
            const suggestions = [
                tweet.text.replace(/@ritualnet/g, '@RitualNetwork'),
                tweet.text + ' 🔥🚀',
                tweet.text.replace('#UnlockRitual', '#UnlockRitual #Web3Revolution'),
                '🌟 ' + tweet.text,
                tweet.text.replace('AI', 'Artificial Intelligence'),
            ];
            
            const suggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
            document.getElementById('rewrittenText').value = suggestion;
        }
        
        // 复制推文
        function copyTweet(index) {
            const tweet = filteredTweets[index];
            const textToCopy = tweet.rewrittenText || tweet.text;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                alert('推文已复制到剪贴板！');
            }).catch(err => {
                console.error('复制失败:', err);
            });
        }
        
        // 导出数据
        function exportData() {
            const dataStr = JSON.stringify(filteredTweets, null, 2);
            const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
            
            const exportFileDefaultName = 'tweets_export_' + new Date().toISOString().slice(0, 10) + '.json';
            
            const linkElement = document.createElement('a');
            linkElement.setAttribute('href', dataUri);
            linkElement.setAttribute('download', exportFileDefaultName);
            linkElement.click();
        }
        
        // 键盘快捷键
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
        
        // 搜索框回车事件
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchTweets();
            }
        });
        
        // 初始化应用
        init();
    </script>
</body>
</html>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"交互式HTML文件已创建：{filename}")

def main():
    """主函数"""
    print("=== UnlockRitual 推文数据生成器 ===")
    print("基于真实推文模式生成2000条数据")
    print("-" * 40)
    
    # 创建生成器实例
    generator = TweetGenerator()
    
    # 生成推文
    tweets = generator.generate_tweets(2000)
    
    # 保存JSON文件
    save_tweets_json(tweets)
    
    # 创建交互式HTML
    create_interactive_html(tweets)
    
    print("\n=== 生成完成 ===")
    print("生成的文件：")
    print("1. generated_tweets.json - 推文数据JSON文件")
    print("2. interactive_tweets.html - 交互式HTML管理界面")
    print("\n您可以打开 interactive_tweets.html 来查看和管理生成的推文数据")

if __name__ == "__main__":
    main()