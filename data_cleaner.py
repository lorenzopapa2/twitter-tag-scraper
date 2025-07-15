#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter数据清洗和去重工具
用于处理抓取的推文数据，去除重复并生成干净的数据集
"""

import pandas as pd
import json
import re
from datetime import datetime
import os

class TwitterDataCleaner:
    def __init__(self):
        self.data = None
        self.original_count = 0
        self.cleaned_count = 0
        
    def load_csv(self, filepath):
        """加载CSV文件"""
        try:
            self.data = pd.read_csv(filepath, encoding='utf-8-sig')
            self.original_count = len(self.data)
            print(f"✅ 成功加载 {self.original_count} 条数据")
            return True
        except Exception as e:
            print(f"❌ 加载CSV失败: {e}")
            return False
    
    def load_json(self, filepath):
        """加载JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                if 'tweets' in json_data:
                    self.data = pd.DataFrame(json_data['tweets'])
                else:
                    self.data = pd.DataFrame(json_data)
                self.original_count = len(self.data)
                print(f"✅ 成功加载 {self.original_count} 条数据")
                return True
        except Exception as e:
            print(f"❌ 加载JSON失败: {e}")
            return False
    
    def remove_duplicates(self):
        """去除重复推文"""
        if self.data is None:
            print("❌ 没有加载数据")
            return
        
        # 方法1：基于推文ID去重
        if 'id' in self.data.columns:
            before = len(self.data)
            self.data = self.data.drop_duplicates(subset=['id'], keep='first')
            after = len(self.data)
            print(f"📌 基于ID去重: 删除了 {before - after} 条重复")
        
        # 方法2：基于推文内容去重（针对相同内容但不同ID的情况）
        if 'text' in self.data.columns or '推文内容' in self.data.columns:
            text_col = 'text' if 'text' in self.data.columns else '推文内容'
            before = len(self.data)
            
            # 清理文本：去除多余空格和换行
            self.data[text_col] = self.data[text_col].apply(lambda x: ' '.join(str(x).split()) if pd.notna(x) else '')
            
            # 基于清理后的文本去重
            self.data = self.data.drop_duplicates(subset=[text_col], keep='first')
            after = len(self.data)
            print(f"📌 基于内容去重: 删除了 {before - after} 条重复")
        
        # 方法3：基于作者和时间的组合去重（同一作者同一时间不可能发两条推文）
        author_col = None
        time_col = None
        
        if 'author_username' in self.data.columns:
            author_col = 'author_username'
        elif '作者用户名' in self.data.columns:
            author_col = '作者用户名'
        
        if 'created_at' in self.data.columns:
            time_col = 'created_at'
        elif '发布时间' in self.data.columns:
            time_col = '发布时间'
        
        if author_col and time_col:
            before = len(self.data)
            self.data = self.data.drop_duplicates(subset=[author_col, time_col], keep='first')
            after = len(self.data)
            print(f"📌 基于作者+时间去重: 删除了 {before - after} 条重复")
        
        self.cleaned_count = len(self.data)
        print(f"\n✅ 去重完成！原始数据: {self.original_count} 条 → 清理后: {self.cleaned_count} 条")
        print(f"📊 总共删除: {self.original_count - self.cleaned_count} 条重复数据")
    
    def clean_data(self):
        """清理数据"""
        if self.data is None:
            print("❌ 没有加载数据")
            return
        
        # 删除空推文
        text_col = 'text' if 'text' in self.data.columns else '推文内容'
        if text_col in self.data.columns:
            before = len(self.data)
            self.data = self.data[self.data[text_col].notna()]
            self.data = self.data[self.data[text_col].str.strip() != '']
            after = len(self.data)
            if before - after > 0:
                print(f"📌 删除了 {before - after} 条空推文")
        
        # 修复数值列
        numeric_columns = ['replies', 'retweets', 'likes', 'views', '回复数', '转发数', '点赞数', '浏览量']
        for col in numeric_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce').fillna(0).astype(int)
        
        # 重新计算互动率
        if all(col in self.data.columns for col in ['replies', 'retweets', 'likes', 'views']):
            self.data['engagement_rate'] = ((self.data['replies'] + self.data['retweets'] + self.data['likes']) / self.data['views'] * 100).round(2)
            self.data.loc[self.data['views'] == 0, 'engagement_rate'] = 0
        
        print("✅ 数据清理完成")
    
    def generate_stats(self):
        """生成统计信息"""
        if self.data is None:
            print("❌ 没有加载数据")
            return
        
        print("\n📊 数据统计:")
        print(f"   总推文数: {len(self.data)}")
        
        # 唯一作者数
        author_col = 'author_username' if 'author_username' in self.data.columns else '作者用户名'
        if author_col in self.data.columns:
            unique_authors = self.data[author_col].nunique()
            print(f"   唯一作者数: {unique_authors}")
            print(f"   平均每位作者发推数: {(len(self.data) / unique_authors):.2f}")
        
        # 互动数据统计
        if 'likes' in self.data.columns:
            print(f"   平均点赞数: {self.data['likes'].mean():.2f}")
            print(f"   最高点赞数: {self.data['likes'].max()}")
        
        if 'views' in self.data.columns:
            print(f"   平均浏览量: {self.data['views'].mean():.2f}")
            print(f"   最高浏览量: {self.data['views'].max()}")
        
        if 'engagement_rate' in self.data.columns:
            print(f"   平均互动率: {self.data['engagement_rate'].mean():.2f}%")
        
        # 图片统计
        if 'has_image' in self.data.columns:
            image_count = self.data['has_image'].sum()
            print(f"   包含图片的推文: {image_count} ({image_count/len(self.data)*100:.1f}%)")
        
        # 发推最多的作者
        if author_col in self.data.columns:
            print("\n🏆 发推最多的前10位作者:")
            top_authors = self.data[author_col].value_counts().head(10)
            for i, (author, count) in enumerate(top_authors.items(), 1):
                print(f"   {i}. {author} - {count} 条推文")
    
    def export_cleaned_data(self, output_dir='cleaned_data'):
        """导出清理后的数据"""
        if self.data is None:
            print("❌ 没有数据可导出")
            return
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 导出CSV
        csv_path = os.path.join(output_dir, f'cleaned_tweets_{self.cleaned_count}条_{timestamp}.csv')
        self.data.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ 导出CSV: {csv_path}")
        
        # 导出JSON
        json_path = os.path.join(output_dir, f'cleaned_tweets_{self.cleaned_count}条_{timestamp}.json')
        
        # 准备JSON数据
        json_data = {
            'metadata': {
                'total_tweets': len(self.data),
                'original_count': self.original_count,
                'duplicates_removed': self.original_count - self.cleaned_count,
                'cleaned_at': datetime.now().isoformat(),
                'hashtag': '#UnlockRitual'
            },
            'tweets': self.data.to_dict('records')
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 导出JSON: {json_path}")
        
        # 导出Excel（方便查看）
        excel_path = os.path.join(output_dir, f'cleaned_tweets_{self.cleaned_count}条_{timestamp}.xlsx')
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            self.data.to_excel(writer, sheet_name='推文数据', index=False)
            
            # 添加统计信息页
            stats_data = {
                '统计项': ['总推文数', '原始数据量', '删除重复数', '清理完成时间'],
                '数值': [len(self.data), self.original_count, self.original_count - self.cleaned_count, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            }
            pd.DataFrame(stats_data).to_excel(writer, sheet_name='统计信息', index=False)
        print(f"✅ 导出Excel: {excel_path}")

def main():
    """主函数"""
    print("🔧 Twitter数据清洗工具")
    print("=" * 50)
    
    cleaner = TwitterDataCleaner()
    
    # 这里可以修改为你的文件路径
    file_path = input("请输入要清理的文件路径 (CSV或JSON): ").strip()
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    # 根据文件扩展名加载数据
    if file_path.endswith('.csv'):
        if not cleaner.load_csv(file_path):
            return
    elif file_path.endswith('.json'):
        if not cleaner.load_json(file_path):
            return
    else:
        print("❌ 不支持的文件格式，请使用CSV或JSON文件")
        return
    
    # 执行清理流程
    print("\n🚀 开始清理数据...")
    cleaner.remove_duplicates()
    cleaner.clean_data()
    cleaner.generate_stats()
    
    # 导出清理后的数据
    print("\n💾 导出清理后的数据...")
    cleaner.export_cleaned_data()
    
    print("\n✅ 数据清理完成！")

if __name__ == "__main__":
    main()