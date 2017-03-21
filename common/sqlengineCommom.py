'''
Created on 2017年1月5日

@author: test
'''

'''
数据库引擎全局公共配置文件
完成数据库表映射，数据库对象链接
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import randint
import pymysql

from common.configCommon import Config
config = Config().conf


DB_CONNECT_STRING = config.get("mysqldb").get("connectStr")
engine = create_engine(DB_CONNECT_STRING, echo = False, pool_recycle=3)
DB_Session = sessionmaker(bind = engine)
session = DB_Session()

#ORM使用方式
from sqlalchemy import Column
from sqlalchemy.types import CHAR,VARCHAR, Integer, String, DECIMAL,Date,BigInteger,SmallInteger,DATETIME,Text, INT
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def init_db():
    BaseModel.metadata.create_all(engine)   #自动找到BaseModel子类并创建表
    
def drop_db():
    BaseModel.metadata.drop_all(engine)
    
    
    
    
    
    
    
    