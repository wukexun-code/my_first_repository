import os
import json
import argparse
import jinja2
import openai
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
load_dotenv()

# 配置OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')

# 配置Jinja2模板环境
TEMPLATE_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader('prompts'),
    trim_blocks=True,
    lstrip_blocks=True
)

def load_mr_data(mr_file_path):
    """加载MR JSON文件数据"""
    try:
        with open(mr_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载MR文件失败: {e}")
        return None

def render_prompt(template_name, mr_data):
    """使用Jinja2渲染分析prompt"""
    try:
        template = TEMPLATE_ENV.get_template(f"{template_name}.yaml")
        return template.render(mr=mr_data)
    except Exception as e:
        print(f"渲染prompt失败: {e}")
        return None

def analyze_mr(mr_data, prompt):
    """调用大模型分析MR内容"""
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一位专业的代码性能分析专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"大模型分析失败: {e}")
        return None

def save_analysis_result(mr_id, analysis_result):
    """保存分析结果到文件"""
    output_dir = Path('analysis_results')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"mr_{mr_id}_analysis.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(analysis_result)
    
    print(f"分析结果已保存至: {output_path}")
    return output_path

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='MR性能分析工具')
    parser.add_argument('mr_file', help='MR JSON文件路径')
    parser.add_argument('-t', '--template', default='default', help='prompt模板名称(位于prompts目录下)')
    parser.add_argument('-s', '--save', action='store_true', help='是否保存分析结果到文件')
    args = parser.parse_args()
    
    # 加载MR数据
    mr_data = load_mr_data(args.mr_file)
    if not mr_data:
        return
    
    # 渲染prompt
    prompt = render_prompt(args.template, mr_data)
    if not prompt:
        return
    
    # 分析MR
    print(f"正在使用{MODEL_NAME}分析MR #{mr_data['iid']}...")
    analysis_result = analyze_mr(mr_data, prompt)
    
    if analysis_result:
        print("\n===== 分析结果 =====\n")
        print(analysis_result)
        
        if args.save:
            save_analysis_result(mr_data['id'], analysis_result)

if __name__ == '__main__':
    if not openai.api_key:
        print("请配置OPENAI_API_KEY环境变量")
        exit(1)
    
    main()