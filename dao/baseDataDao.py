'''
Created on 2017年2月22日

@author: test
'''

from common.sqlengineCommom import session
from sqlalchemy import or_, not_, func
from model.basedata import BaseData

from common.loggingCommon import MulLogger
logger = MulLogger()

class BaseDataDao(object):

    def __init__(self):
        '''
        Constructor
        '''
        pass
    def get_data_by_id(self,id):
        '''获取表数据条目
        '''
        try:
            query = session.query(BaseData)
            return query.filter(BaseData.id == id).first()
        except Exception as ex:
            session.rollback()
            logger.warnning("查询basedata表发生异常"+str(ex))
            return -1
        
    def get_datas_by_id(self,id):
        '''获取数据库条目
        '''
        try:
            query = session.query(BaseData)
            return query.filter(BaseData.id.in_((id))).all()
        except Exception as ex:
            session.rollback()
            logger.warnning("查询basedata表发生异常"+str(ex))
  
    def insert_baseData(self,mname,maddtime,mkeyworld,mcontent,mpictureid,mdatatype):
        try:
            basedata = BaseData(name=mname,addtime=maddtime,keyworld=mkeyworld,content=mcontent,pictureid=mpictureid,datatype=mdatatype)
            session.add(basedata)
            session.commit()
            return basedata.id
        except Exception as ex:
            session.rollback()
            logger.warnning("插入basedata表发生异常"+str(ex))
    