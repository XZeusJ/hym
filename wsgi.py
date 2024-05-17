### wsgi.py：手动设置环境变量并导入程序实例
### 在这个脚本中加载环境变量，并导入程序实例以供部署时使用
### 这两个环境变量的具体定义，在远程服务器环境创建新的 .env 文件写入

import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app