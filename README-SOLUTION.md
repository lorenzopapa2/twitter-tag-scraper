# Twitter标签推文抓取解决方案

由于Twitter API的认证复杂性，我为你提供几种可行的解决方案：

## 方案1：使用第三方服务（推荐）

### 1. RapidAPI Twitter服务
- 访问 https://rapidapi.com/marketplace 搜索Twitter API
- 注册获取API密钥
- 使用提供的端点进行标签搜索

### 2. Twitter官方API v2
你需要申请Twitter开发者账号：
1. 访问 https://developer.twitter.com/
2. 申请开发者访问权限
3. 创建项目获取Bearer Token
4. 使用提供的代码框架

## 方案2：使用现有工具

### 1. Twint（开源工具）
```bash
pip install twint
twint -s "#UnlockRitual" --json -o tweets.json
```

### 2. Snscrape
```bash
pip install snscrape
snscrape --jsonl --max-results 100 twitter-search "#UnlockRitual" > tweets.json
```

## 方案3：使用浏览器扩展

1. 安装Twitter数据导出扩展
2. 手动搜索标签
3. 使用扩展导出数据

## 当前代码说明

我已经为你创建了三种不同的实现：

1. **twitterClient.js** - 使用官方API v2（需要有效的Bearer Token）
2. **twitterWebClient.js** - 模拟浏览器请求（需要有效的认证）
3. **puppeteerScraper.js** - 使用Puppeteer自动化（可能需要处理登录）

## 获取有效的Bearer Token

### 方法1：申请开发者账号
1. 访问 https://developer.twitter.com/
2. 完成申请流程
3. 创建App获取Bearer Token

### 方法2：使用第三方服务
考虑使用付费的Twitter数据服务，它们提供：
- 稳定的API访问
- 无需复杂认证
- 更高的速率限制

## 注意事项

1. **速率限制**：Twitter API有严格的速率限制
2. **数据使用**：确保遵守Twitter的服务条款
3. **账号安全**：不要在公开场合分享认证信息

## 建议

对于你的需求（抓取#UnlockRitual标签），我建议：
1. 使用Python的snscrape工具（最简单）
2. 或申请官方开发者账号（最稳定）
3. 考虑使用付费API服务（最便捷）

如需其他帮助，请告诉我你倾向于哪种方案。