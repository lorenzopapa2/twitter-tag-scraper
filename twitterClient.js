require('dotenv').config();
const axios = require('axios');

class TwitterClient {
    constructor(bearerToken) {
        this.bearerToken = bearerToken;
        this.baseURL = 'https://api.twitter.com/2';
        this.headers = {
            'Authorization': `Bearer ${this.bearerToken}`,
            'Content-Type': 'application/json'
        };
    }

    async searchTweets(query, maxResults = 10, nextToken = null) {
        try {
            const params = {
                query: query,
                max_results: maxResults,
                'tweet.fields': 'created_at,author_id,public_metrics,conversation_id',
                'user.fields': 'name,username,profile_image_url',
                'expansions': 'author_id'
            };

            if (nextToken) {
                params.next_token = nextToken;
            }

            const response = await axios.get(`${this.baseURL}/tweets/search/recent`, {
                headers: this.headers,
                params: params
            });

            return response.data;
        } catch (error) {
            console.error('搜索推文失败:', error.response ? error.response.data : error.message);
            throw error;
        }
    }

    async getTweetsByHashtag(hashtag, maxResults = 100) {
        const query = `#${hashtag} -is:retweet`;
        const allTweets = [];
        let nextToken = null;
        let fetchedCount = 0;

        try {
            while (fetchedCount < maxResults) {
                const batchSize = Math.min(100, maxResults - fetchedCount);
                const result = await this.searchTweets(query, batchSize, nextToken);
                
                if (result.data && result.data.length > 0) {
                    allTweets.push(...result.data);
                    fetchedCount += result.data.length;
                }

                nextToken = result.meta?.next_token;
                if (!nextToken || !result.data || result.data.length === 0) {
                    break;
                }

                await new Promise(resolve => setTimeout(resolve, 1000));
            }

            return allTweets;
        } catch (error) {
            console.error('获取标签推文失败:', error);
            return allTweets;
        }
    }
}

module.exports = TwitterClient;