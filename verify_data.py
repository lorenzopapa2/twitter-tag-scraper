#!/usr/bin/env python3
"""
验证生成的推文数据质量
"""

import json
from collections import Counter

def verify_data(filename="generated_tweets.json"):
    """验证数据质量"""
    print("=== 数据验证报告 ===\n")
    
    # 读取数据
    with open(filename, 'r', encoding='utf-8') as f:
        tweets = json.load(f)
    
    print(f"1. 数据数量：{len(tweets)} 条推文")
    
    # 检查唯一ID
    ids = [tweet['id'] for tweet in tweets]
    unique_ids = set(ids)
    print(f"2. 唯一ID检查：{len(unique_ids)} 个唯一ID（应该等于 {len(tweets)}）")
    if len(unique_ids) != len(tweets):
        print("   ⚠️ 发现重复ID！")
    else:
        print("   ✅ 所有ID都是唯一的")
    
    # 检查用户唯一性
    users = [tweet['username'] for tweet in tweets]
    unique_users = set(users)
    print(f"3. 用户数量：{len(unique_users)} 个独立用户")
    
    # 互动数据统计
    total_likes = sum(tweet['likes'] for tweet in tweets)
    total_retweets = sum(tweet['retweets'] for tweet in tweets)
    total_replies = sum(tweet['replies'] for tweet in tweets)
    
    print(f"\n4. 互动数据统计：")
    print(f"   - 总点赞数：{total_likes:,}")
    print(f"   - 总转发数：{total_retweets:,}")
    print(f"   - 总回复数：{total_replies:,}")
    print(f"   - 平均点赞：{total_likes/len(tweets):.2f}")
    print(f"   - 平均转发：{total_retweets/len(tweets):.2f}")
    print(f"   - 平均回复：{total_replies/len(tweets):.2f}")
    
    # 媒体统计
    media_tweets = [tweet for tweet in tweets if tweet['hasMedia']]
    print(f"\n5. 媒体统计：{len(media_tweets)} 条推文包含媒体 ({len(media_tweets)/len(tweets)*100:.1f}%)")
    
    # 认证用户统计
    verified_tweets = [tweet for tweet in tweets if tweet['isVerified']]
    print(f"6. 认证用户：{len(verified_tweets)} 条推文来自认证用户 ({len(verified_tweets)/len(tweets)*100:.1f}%)")
    
    # 检查必需标签
    missing_hashtag = [tweet for tweet in tweets if '#UnlockRitual' not in tweet['text']]
    print(f"\n7. 标签检查：")
    if missing_hashtag:
        print(f"   ⚠️ {len(missing_hashtag)} 条推文缺少 #UnlockRitual 标签")
    else:
        print("   ✅ 所有推文都包含 #UnlockRitual 标签")
    
    # 检查@ritualnet提及
    ritual_mentions = [tweet for tweet in tweets if '@ritualnet' in tweet['text']]
    print(f"8. @ritualnet 提及：{len(ritual_mentions)} 条推文 ({len(ritual_mentions)/len(tweets)*100:.1f}%)")
    
    # 高互动推文示例
    print(f"\n9. 高互动推文示例（前5条）：")
    sorted_tweets = sorted(tweets, key=lambda x: x['likes'] + x['retweets'] + x['replies'], reverse=True)
    for i, tweet in enumerate(sorted_tweets[:5], 1):
        engagement = tweet['likes'] + tweet['retweets'] + tweet['replies']
        print(f"   {i}. @{tweet['username']} - {engagement:,} 互动")
        print(f"      {tweet['text'][:80]}...")
    
    print("\n=== 验证完成 ===")

if __name__ == "__main__":
    verify_data()