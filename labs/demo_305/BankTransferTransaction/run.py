import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from database.init_db import create_tables
from database.db_connection import get_cursor

if __name__ == "__main__":
    with get_cursor() as (cursor, conn):
        create_tables(cursor)
        print("Create database success!") 