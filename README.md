# MR智能分析系统

一个用于拉取GitLab合并请求(MR)并进行AI性能分析的工具集。

## 功能特点
- 拉取指定仓库某时间段内的所有MR及代码差异
- 将MR详情和diff内容存储为JSON文件
- 使用大模型对MR进行性能诊断分析
- 支持自定义分析prompt模板

## 环境要求
- Python 3.8+
- GitLab访问令牌
- OpenAI API密钥

## 安装步骤
1. 克隆仓库
```bash
git clone <repository-url>
cd my_first_repository
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
复制环境变量示例文件并修改为实际值：
```bash
cp .env.example .env
# 编辑.env文件设置你的GitLab和OpenAI凭证
```

## 使用方法

### 1. 拉取MR数据
```bash
python mr_fetcher.py
```
MR数据将保存在`mrs/`目录下，以MR ID命名的JSON文件。

### 2. 分析MR性能
```bash
python mr_analyzer.py mrs/<mr_id>.json -s
```
- `-s`：保存分析结果到`analysis_results/`目录
- `-t`：指定自定义prompt模板（位于`prompts/`目录）

## 自定义Prompt
在`prompts/`目录下创建YAML格式的prompt模板，使用Jinja2语法引用MR数据字段。

## 文件结构
- `mr_fetcher.py`：拉取MR数据的主脚本
- `mr_analyzer.py`：AI分析主脚本
- `prompts/`：存放prompt模板
- `mrs/`：存放MR数据JSON文件
- `analysis_results/`：存放分析结果

demo仓库，练手用
