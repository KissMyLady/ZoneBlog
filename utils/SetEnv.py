# coding:utf-8
# Author:mylady
# 2023/9/17 10:53
from dotenv import load_dotenv
import os


def test_1():
    # 读取配置文件
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')

    print('读取配置文件: ', dotenv_path)

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    a = os.environ.get('FLASK_COVERAGE')
    print(a)
    pass


def main():
    test_1()
    pass


if __name__ == "__main__":
    main()
