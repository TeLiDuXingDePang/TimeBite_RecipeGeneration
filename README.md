# TimeBite_RecipeGeneration

AI for Code 应用赛道参赛作品-食光机小程序菜谱数据生成脚本

## 项目简介

本项目是为食光机小程序开发的菜谱数据生成工具，利用Coze智能体API自动生成结构化的菜谱数据并存储到Excel数据库中。通过这个工具，可以批量获取各种菜谱的详细信息，包括烹饪步骤、食材准备、烹饪工具、小贴士等内容，大大提高了菜谱内容创建的效率。

## 功能特点

- 批量从文本文件读取菜谱名称并自动查询
- 调用Coze智能体API获取丰富的菜谱信息
- 自动提取API响应中的结构化菜谱数据
- 支持菜谱的多个维度信息（基本信息、步骤、工具、准备步骤、小贴士等）
- 将所有菜谱数据保存到Excel表格，便于进一步处理
- 兼容现有数据结构，保留Excel中的其他工作表

## 菜谱数据结构

每个菜谱包含以下信息：

- `name`: 菜谱名称
- `cook_time`: 烹饪时间（分钟）
- `calories`: 热量信息
- `image`: 菜品图片链接
- `description`: 菜品描述
- `tools`: 烹饪工具列表
- `prep_steps`: 准备步骤列表
- `steps`: 详细烹饪步骤（包含步骤编号和内容）
- `tips`: 烹饪小贴士列表
- `difficulty`: 难度级别

## 使用方法

### 环境要求

- Python 3.7+
- 安装所需依赖：`pip install pandas openpyxl requests`

### 准备工作

1. 准备菜谱名称文件：在项目根目录创建一个文本文件（默认为`家常菜菜谱名称.txt`），每行一个菜谱名称
2. 确保`data`目录下有`database.xlsx`文件，用于存储菜谱数据

### 运行脚本

```bash
python recipe_to_excel.py
```

系统会自动读取文本文件中的菜谱名称，依次查询每个菜谱的信息，并将结果保存到Excel文件中。

### 单独查询某个菜谱

如果只想查询单个菜谱，可以使用：

```bash
python recipe_bot_client.py
```

按提示输入菜谱名称，即可获取详细的菜谱信息。

## 技术实现

本项目主要由以下几个部分组成：

1. `recipe_bot_client.py`: 提供单个菜谱查询功能
2. `recipe_to_excel.py`: 批量处理菜谱并保存到Excel
3. `家常菜菜谱名称.txt`: 待查询的菜谱名称列表
4. `data/database.xlsx`: 存储菜谱数据的Excel文件

核心实现逻辑：
- 调用Coze智能体API获取菜谱信息
- 从返回的数据中提取assistant角色的answer类型消息
- 解析JSON格式的菜谱数据
- 将数据保存到Excel表格中的recipes工作表

## 注意事项

- API调用需要有效的Coze API令牌
- 查询过于频繁可能会受到API限制
- 确保Excel文件格式正确，且有写入权限


