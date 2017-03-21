'''
Created on 2017年2月22日

@author: test
'''

from common.sqlengineCommom import session
from sqlalchemy import or_, not_, func
from model.picture import Picture

from common.loggingCommon import MulLogger
logger = MulLogger()

class PictureDao(object):

    def __init__(self):
        '''
        Constructor
        '''
        pass
    def get_data_by_id(self,id):
        '''获取表数据条目
        '''
        try:
            query = session.query(Picture)
            return query.filter(Picture.id == id).first()
        except Exception as ex:
            session.rollback()
            logger.warnning("查询picture表发生异常"+str(ex))
            return -1
        
    def get_datas_by_id(self,id):
        '''获取数据库条目
        '''
        try:
            query = session.query(Picture)
            return query.filter(Picture.id.in_((id))).all()
        except Exception as ex:
            session.rollback()
            logger.warnning("查询picture表发生异常"+str(ex))
  
    def insert_list_picture(self,mimg):
        try:
            for m in mimg:
                picture = Picture(img=m.get("data"),datatype=m.get("type"))
                session.add(picture)
            session.commit()
            return picture.id
        except Exception as ex:
            session.rollback()
            logger.warnning("插入picture表发生异常"+str(ex))
    