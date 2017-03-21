'''
Created on 2016年12月5日

@author: xiaochuan
'''

import os
import json

from common.loggingCommon import MulLogger
logger = MulLogger()


'''
封装单列模式
'''
def singleton(cls, *args):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls()  
        return instances[cls]  
    return _singleton 
 
@singleton
class Config(object):
    '''
    app配置文件类，单例模式，动态装载配置文件参数，全局使用
    '''
    def __init__(self):
        '''
        fileName 配置文件名字
        '''
        self.filePath = os.getcwd()+"/conf/appconfig.json";       
        self.conf = self._get_file_content_()


    def _get_file_content_(self):
        '''
        根据文件路径获取文件内容
        '''  
        if not self.filePath:
            logger.error("配置文件路径不存在")
        try:
            with open(self.filePath,'r',encoding="utf-8") as fileHanld:
                content = fileHanld.read()
        except Exception as ex:
            logger.error("打开配置文件发生异常; Exception:"+str(ex))
            return False
        else:
            return json.loads(content)
    