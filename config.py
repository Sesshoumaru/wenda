import os

# 调试模式
DEBUG = True

# session cookie 加密密匙
SECRET_KEY = os.urandom(24)

# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'wenda'
USERNAME = 'root'
PASSWORD = '9527'
DB_URL = 'mysql+mysqldb://{}:{}@{}:{}/{}charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URL = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = True




