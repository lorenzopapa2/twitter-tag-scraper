require('dotenv').config();
const axios = require('axios');

class TwitterWebClient {
    constructor(authToken, ct0) {
        this.authToken = authToken;
        this.ct0 = ct0;
        this.baseURL = 'https://api.twitter.com/1.1';
        this.graphqlURL = 'https://twitter.com/i/api/graphql';
        this.headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-csrf-token': this.ct0,
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'cookie': `auth_token=${this.authToken}; ct0=${this.ct0}`
        };
    }

    async searchTweets(query, cursor = null) {
        try {
            const variables = {
                rawQuery: query,
                count: 20,
                querySource: 'typed_query',
                product: 'Latest'
            };

            if (cursor) {
                variables.cursor = cursor;
            }

            const features = {
                rweb_lists_timeline_redesign_enabled: true,
                responsive_web_graphql_exclude_directive_enabled: true,
                verified_phone_label_enabled: false,
                creator_subscriptions_tweet_preview_api_enabled: true,
                responsive_web_graphql_timeline_navigation_enabled: true,
                responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
                tweetypie_unmention_optimization_enabled: true,
                responsive_web_edit_tweet_api_enabled: true,
                graphql_is_translatable_rweb_tweet_is_translatable_enabled: true,
                view_counts_everywhere_api_enabled: true,
                longform_notetweets_consumption_enabled: true,
                responsive_web_twitter_article_tweet_consumption_enabled: false,
                tweet_awards_web_tipping_enabled: false,
                freedom_of_speech_not_reach_fetch_enabled: true,
                standardized_nudges_misinfo: true,
                tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled: true,
                longform_notetweets_rich_text_read_enabled: true,
                longform_notetweets_inline_media_enabled: true,
                responsive_web_media_download_video_enabled: false,
                responsive_web_enhance_cards_enabled: false
            };

            const params = new URLSearchParams({
                variables: JSON.stringify(variables),
                features: JSON.stringify(features)
            });

            const response = await axios.get(
                `${this.graphqlURL}/nK1dw4oV3k4w5TdtcAdSww/SearchTimeline?${params.toString()}`,
                { headers: this.headers }
            );

            return this.parseSearchResponse(response.data);
        } catch (error) {
            console.error('搜索推文失败:', error.response ? error.response.data : error.message);
            throw error;
        }
    }

    parseSearchResponse(data) {
        const tweets = [];
        
        try {
            const instructions = data?.data?.search_by_raw_query?.search_timeline?.timeline?.instructions || [];
            
            for (const instruction of instructions) {
                if (instruction.type === 'TimelineAddEntries') {
                    const entries = instruction.entries || [];
                    
                    for (const entry of entries) {
                        if (entry.entryId?.startsWith('tweet-')) {
                            const tweetResult = entry.content?.itemContent?.tweet_results?.result;
                            
                            if (tweetResult && tweetResult.legacy) {
                                const tweet = tweetResult.legacy;
                                const user = tweetResult.core?.user_results?.result?.legacy;
                                
                                tweets.push({
                                    id: tweetResult.rest_id,
                                    text: tweet.full_text,
                                    created_at: tweet.created_at,
                                    author: {
                                        id: user?.id_str,
                                        name: user?.name,
                                        username: user?.screen_name
                                    },
                                    metrics: {
                                        likes: tweet.favorite_count || 0,
                                        retweets: tweet.retweet_count || 0,
                                        replies: tweet.reply_count || 0,
                                        quotes: tweet.quote_count || 0
                                    },
                                    url: `https://twitter.com/${user?.screen_name}/status/${tweetResult.rest_id}`
                                });
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('解析响应数据失败:', error);
        }

        return tweets;
    }

    async getTweetsByHashtag(hashtag, maxResults = 100) {
        const query = `#${hashtag} -filter:retweets`;
        const allTweets = [];
        let cursor = null;
        let fetchedCount = 0;

        try {
            while (fetchedCount < maxResults) {
                const result = await this.searchTweets(query, cursor);
                
                if (result && result.length > 0) {
                    allTweets.push(...result);
                    fetchedCount += result.length;
                }

                if (!result || result.length === 0 || fetchedCount >= maxResults) {
                    break;
                }

                await new Promise(resolve => setTimeout(resolve, 1000));
            }

            return allTweets.slice(0, maxResults);
        } catch (error) {
            console.error('获取标签推文失败:', error);
            return allTweets;
        }
    }
}

module.exports = TwitterWebClient;