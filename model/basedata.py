'''
Created on 2017年2月22日

@author: test
'''

from common.sqlengineCommom import *

from common.configCommon import Config
config = Config().conf

class BaseData(BaseModel):
    '''用户表
    '''
    __tablename__ = 'jokedata'
    id          = Column(BigInteger, primary_key = True)
    name  = Column(VARCHAR(60))
    content   = Column(VARCHAR(255))
    keyworld  = Column(VARCHAR(60))
    addtime = Column(Integer)
    pictureid = Column(VARCHAR(120))
    datatype = Column(SmallInteger)
    other = Column(VARCHAR(60))

init_db()
    
