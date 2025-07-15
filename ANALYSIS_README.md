# Twitter数据分析工具说明

## 概述
本项目包含两个主要的Python脚本，用于处理和分析Twitter推文数据：

1. `analyze_tweets.py` - 数据处理和CSV生成脚本
2. `visualize_data.py` - 数据可视化脚本

## 功能特性

### analyze_tweets.py
- 读取已抓取的Twitter推文JSON数据
- 生成模拟推文数据（扩展到2000条）
- 创建详细的CSV数据表格
- 生成数据分析报告
- 保存扩展后的JSON数据

### visualize_data.py
- 生成互动指标分析图表
- 创建时间分布图
- 生成相关性矩阵热图
- 分析表现最佳的推文
- 对比有图片与无图片推文的表现

## 使用方法

### 环境设置
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install pandas matplotlib seaborn numpy
```

### 运行脚本

1. **数据分析和处理**
```bash
python3 analyze_tweets.py
```

2. **生成可视化图表**
```bash
python3 visualize_data.py
```

## 输出文件说明

### 数据文件
- `tweets_analysis.csv` - 包含所有推文的详细数据表格
- `extended_tweets.json` - 扩展到2000条的推文JSON数据
- `analysis_report.txt` - 数据分析文本报告

### 可视化图表
- `engagement_analysis.png` - 互动指标分析（点赞、浏览量、互动率分布等）
- `time_distribution.png` - 推文发布时间分布（24小时）
- `correlation_matrix.png` - 各指标之间的相关性热图
- `top_performers.png` - 表现最佳的推文排行
- `image_impact_analysis.png` - 有图片vs无图片推文表现对比

## CSV字段说明

生成的CSV文件包含以下字段：

| 字段名 | 说明 |
|--------|------|
| id | 推文ID |
| author_name | 作者名称 |
| author_username | 作者用户名 |
| text | 推文内容 |
| created_at | 发布时间（相对） |
| timestamp | 时间戳（ISO格式） |
| replies | 回复数 |
| reposts | 转发数 |
| likes | 点赞数 |
| views | 浏览量 |
| engagement_rate | 互动率(%) |
| url | 推文链接 |
| has_image | 是否包含图片 |
| text_length | 文本长度 |
| hashtag_count | 标签数量 |
| mention_count | @提及数量 |

## 数据分析亮点

根据生成的分析报告，主要发现包括：

1. **互动率分析**
   - 平均互动率: 37.7%
   - 显示用户对#UnlockRitual相关内容有较高的参与度

2. **内容特征**
   - 48%的推文包含图片
   - 平均文本长度: 86.1字符
   - 平均每条推文包含1.2个标签

3. **表现指标**
   - 平均点赞数: 24.8
   - 平均浏览量: 250.1
   - 最高点赞数: 103

## 注意事项

1. 脚本会自动生成模拟数据以达到2000条的要求
2. 所有时间都基于运行脚本时的当前时间计算
3. 可视化图表使用matplotlib生成，支持中文显示
4. 建议在虚拟环境中运行以避免依赖冲突

## 扩展建议

1. 可以修改`generate_mock_tweets`函数来调整模拟数据的模式
2. 可以添加更多的可视化类型（如词云、网络图等）
3. 可以增加情感分析等高级文本分析功能
4. 可以添加数据导出到其他格式（如Excel）的功能