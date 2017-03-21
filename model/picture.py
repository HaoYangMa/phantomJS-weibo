'''
Created on 2017年2月22日

@author: test
'''



from common.sqlengineCommom import *

from common.configCommon import Config
config = Config().conf
    
class Picture(BaseModel):
    '''用户表
    '''
    __tablename__ = 'jokepicture'
    id    = Column(BigInteger, primary_key = True)
    img   = Column(Text)
    datatype = Column(SmallInteger)
    other = Column(VARCHAR(60))


init_db()
    
