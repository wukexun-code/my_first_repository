import os
import json
import gitlab
from datetime import datetime
from dateutil.parser import parse
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
load_dotenv()

# 配置GitLab连接
GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.com')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
PROJECT_ID = os.getenv('PROJECT_ID')
START_DATE = parse(os.getenv('START_DATE'))
END_DATE = parse(os.getenv('END_DATE'))

# 创建存储目录
OUTPUT_DIR = Path('mrs')
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_mrs():    
    # 初始化GitLab客户端
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
    
    try:
        project = gl.projects.get(PROJECT_ID)
    except gitlab.exceptions.GitlabGetError as e:
        print(f"无法获取项目: {e}")
        return
    
    # 获取符合时间范围的MR
    mrs = project.mergerequests.list(
        state='all',
        updated_after=START_DATE.isoformat(),
        updated_before=END_DATE.isoformat(),
        order_by='updated_at',
        sort='asc',
        per_page=100,
        pagination='keyset'
    )
    
    for mr in mrs:
        try:
            # 获取MR详情
            mr_details = project.mergerequests.get(mr.id)
            
            # 获取MR diff
            diff = mr_details.diff()
            
            # 构建MR数据
            mr_data = {
                'id': mr.id,
                'iid': mr.iid,
                'title': mr.title,
                'description': mr.description,
                'state': mr.state,
                'author': mr.author['username'],
                'created_at': mr.created_at,
                'updated_at': mr.updated_at,
                'merged_at': mr.merged_at,
                'source_branch': mr.source_branch,
                'target_branch': mr.target_branch,
                'diff': diff,
                'changes_count': mr.changes_count,
                'web_url': mr.web_url
            }
            
            # 保存为JSON文件
            output_path = OUTPUT_DIR / f"{mr.id}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mr_data, f, indent=2, ensure_ascii=False)
                
            print(f"已保存MR #{mr.iid}: {mr.title} ({output_path})")
            
        except Exception as e:
            print(f"处理MR #{mr.iid}时出错: {e}")
            continue

if __name__ == '__main__':
    if not all([GITLAB_TOKEN, PROJECT_ID]):
        print("请配置GITLAB_TOKEN和PROJECT_ID环境变量")
        exit(1)
    
    fetch_mrs()