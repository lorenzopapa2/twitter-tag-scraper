#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载数据"""
    # 读取CSV数据
    df = pd.read_csv('tweets_analysis.csv')
    
    # 转换timestamp为datetime对象
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

def create_engagement_visualization(df):
    """创建互动指标可视化"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Twitter推文互动指标分析', fontsize=16)
    
    # 1. 点赞数分布
    axes[0, 0].hist(df['likes'], bins=30, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('点赞数分布')
    axes[0, 0].set_xlabel('点赞数')
    axes[0, 0].set_ylabel('推文数量')
    axes[0, 0].axvline(df['likes'].mean(), color='red', linestyle='dashed', linewidth=2, label=f'平均值: {df["likes"].mean():.1f}')
    axes[0, 0].legend()
    
    # 2. 浏览量分布
    axes[0, 1].hist(df['views'], bins=30, edgecolor='black', alpha=0.7, color='green')
    axes[0, 1].set_title('浏览量分布')
    axes[0, 1].set_xlabel('浏览量')
    axes[0, 1].set_ylabel('推文数量')
    axes[0, 1].axvline(df['views'].mean(), color='red', linestyle='dashed', linewidth=2, label=f'平均值: {df["views"].mean():.1f}')
    axes[0, 1].legend()
    
    # 3. 互动率分布
    axes[1, 0].hist(df['engagement_rate'].astype(float), bins=30, edgecolor='black', alpha=0.7, color='orange')
    axes[1, 0].set_title('互动率分布 (%)')
    axes[1, 0].set_xlabel('互动率 (%)')
    axes[1, 0].set_ylabel('推文数量')
    axes[1, 0].axvline(df['engagement_rate'].astype(float).mean(), color='red', linestyle='dashed', linewidth=2, 
                      label=f'平均值: {df["engagement_rate"].astype(float).mean():.1f}%')
    axes[1, 0].legend()
    
    # 4. 各指标的箱线图
    metrics_data = [df['replies'], df['reposts'], df['likes']]
    axes[1, 1].boxplot(metrics_data, labels=['回复', '转发', '点赞'])
    axes[1, 1].set_title('互动指标箱线图')
    axes[1, 1].set_ylabel('数量')
    
    plt.tight_layout()
    plt.savefig('engagement_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("已保存: engagement_analysis.png")

def create_time_analysis(df):
    """创建时间分析图表"""
    # 按小时聚合数据
    df['hour'] = df['timestamp'].dt.hour
    hourly_tweets = df.groupby('hour').size()
    
    # 创建24小时分布图
    plt.figure(figsize=(12, 6))
    plt.bar(hourly_tweets.index, hourly_tweets.values, edgecolor='black', alpha=0.7, color='skyblue')
    plt.title('推文发布时间分布（24小时）')
    plt.xlabel('小时')
    plt.ylabel('推文数量')
    plt.xticks(range(24))
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('time_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("已保存: time_distribution.png")

def create_correlation_matrix(df):
    """创建相关性矩阵热图"""
    # 选择数值列
    numeric_cols = ['replies', 'reposts', 'likes', 'views', 'engagement_rate', 'text_length', 'hashtag_count', 'mention_count']
    correlation_data = df[numeric_cols].astype(float)
    
    # 计算相关性矩阵
    corr_matrix = correlation_data.corr()
    
    # 创建热图
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('各指标之间的相关性分析')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("已保存: correlation_matrix.png")

def create_top_performers_chart(df):
    """创建表现最佳的推文图表"""
    # 获取前10条最受欢迎的推文
    top_by_likes = df.nlargest(10, 'likes')[['author_username', 'likes', 'views', 'engagement_rate']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 点赞数最多的前10条
    y_pos = np.arange(len(top_by_likes))
    ax1.barh(y_pos, top_by_likes['likes'], alpha=0.7, color='crimson')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(top_by_likes['author_username'])
    ax1.set_xlabel('点赞数')
    ax1.set_title('点赞数最多的前10条推文')
    ax1.invert_yaxis()
    
    # 互动率最高的前10条
    top_by_engagement = df.nlargest(10, 'engagement_rate')[['author_username', 'engagement_rate']]
    y_pos2 = np.arange(len(top_by_engagement))
    ax2.barh(y_pos2, top_by_engagement['engagement_rate'].astype(float), alpha=0.7, color='darkgreen')
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(top_by_engagement['author_username'])
    ax2.set_xlabel('互动率 (%)')
    ax2.set_title('互动率最高的前10条推文')
    ax2.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('top_performers.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("已保存: top_performers.png")

def create_image_analysis(df):
    """分析有图片vs无图片的推文表现"""
    # 按是否有图片分组
    grouped = df.groupby('has_image').agg({
        'likes': 'mean',
        'views': 'mean',
        'engagement_rate': lambda x: x.astype(float).mean(),
        'replies': 'mean',
        'reposts': 'mean'
    })
    
    # 创建对比图
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('有图片 vs 无图片推文表现对比', fontsize=16)
    
    metrics = [('likes', '平均点赞数'), ('views', '平均浏览量'), 
               ('engagement_rate', '平均互动率(%)'), ('reposts', '平均转发数')]
    
    for idx, (metric, title) in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]
        values = grouped[metric]
        bars = ax.bar(['无图片', '有图片'], values, color=['lightblue', 'lightcoral'])
        ax.set_title(title)
        ax.set_ylabel('数值')
        
        # 在柱子上添加数值
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('image_impact_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("已保存: image_impact_analysis.png")

def generate_summary_stats(df):
    """生成汇总统计信息"""
    print("\n=== 数据汇总统计 ===")
    print(f"总推文数: {len(df)}")
    print(f"平均点赞数: {df['likes'].mean():.1f}")
    print(f"平均浏览量: {df['views'].mean():.1f}")
    print(f"平均互动率: {df['engagement_rate'].astype(float).mean():.1f}%")
    print(f"包含图片的推文比例: {df['has_image'].sum() / len(df) * 100:.1f}%")
    print(f"平均文本长度: {df['text_length'].mean():.1f} 字符")
    print(f"平均标签数: {df['hashtag_count'].mean():.1f}")
    print(f"平均@提及数: {df['mention_count'].mean():.1f}")

def main():
    """主函数"""
    print("开始生成数据可视化...")
    
    # 加载数据
    df = load_data()
    
    # 生成各种可视化
    create_engagement_visualization(df)
    create_time_analysis(df)
    create_correlation_matrix(df)
    create_top_performers_chart(df)
    create_image_analysis(df)
    
    # 生成汇总统计
    generate_summary_stats(df)
    
    print("\n所有可视化图表已生成完成！")
    print("生成的图表文件:")
    print("- engagement_analysis.png: 互动指标分析")
    print("- time_distribution.png: 时间分布分析")
    print("- correlation_matrix.png: 相关性矩阵")
    print("- top_performers.png: 表现最佳的推文")
    print("- image_impact_analysis.png: 图片影响分析")

if __name__ == "__main__":
    main()