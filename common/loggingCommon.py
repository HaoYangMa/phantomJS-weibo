#!urs/bin/env python
#coding:utf-8

# 日志记录模块，用于记录程序运行时的错误等日志

import json
import logging.config

import os
        
class MulLogger(object):
    '''多个进程写日志
    BUG：未测试是否真的进程安全
    '''
    def __init__(self, category='console'):
        try:
            config_file = os.getcwd()+'/conf/logging.conf'
            f = open(config_file, 'r')
        except:
            raise "日志配置文件不存在"
        data = f.read()
        f.close()
        config = json.loads(data)
        logging.config.dictConfig(config)
        self.logger = logging.getLogger(category)
        
    #   
    # 下面的五个方法为logging的五个日志级别，不再一一赘述
    #    
    def debug(self, msg):
        self.logger.debug(msg)
        
    def info(self, msg):
        self.logger.info(msg)
        
    def warnning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
        
    def critical(self, msg):
        self.logger.critical(msg)
    
    
def test():
    # 运行测试时将配置文件的路径修改一下
    logger = MulLogger()
    logger.debug('asdasd')
    logger.info('zxczxc')


if __name__ == '__main__':
    test()