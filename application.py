'''
Created on 2017年2月22日

@author: test
'''
#打包多进程参数设置,必须写在第一行
import common.packgeMultiprocess

from common.sqlengineCommom import *

import time
#phantomjs导入包
from selenium import webdriver
#xpath
from lxml.html.clean import Cleaner 
from service.crawlService import CrawlService
from common.configCommon import Config
config = Config().conf

from common.loggingCommon import MulLogger
logger = MulLogger()

import random

if __name__ == '__main__':
    
    driver = webdriver.PhantomJS()
    driver.maximize_window() #设置浏览器窗口最大话
    url = config.get('login').get('loginUrl')
    logger.info("程序开始启动")
    driver.implicitly_wait(20); #设置等待时间
    #登录
    while(True):
        driver.get(url)
        logger.info("登录页面:"+driver.current_url)
    
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        username.send_keys(config.get("login").get("name"))
        password.send_keys(config.get("login").get("pwd"))
        sbtn = driver.find_element_by_css_selector('.btn_mod .W_btn_a') 
        sbtn.submit()
        time.sleep(20)
        if driver.current_url != url: #做一次简单的对比
            break
        
    logger.info("个人主页:"+driver.current_url)
    try:
        #跳转到微博页面
        weibo = driver.find_element_by_css_selector(".l_pdt a")
        url=weibo.get_attribute('href')
        driver.get(url)
        # time.sleep(10)
        logger.info("微博页面:"+driver.current_url)
        
        #跳转到搞笑类
        mtarget = config.get('target')
        car = driver.find_element_by_partial_link_text(mtarget)
        url=car.get_attribute("href")
        driver.get(url)
        logger.info("专栏页面:"+driver.current_url)
        
        #跳转到原创
        yy = driver.find_element_by_partial_link_text('原创')
        url=yy.get_attribute("href")
        driver.get(url)
        logger.info("原创页面:"+driver.current_url)
    except Exception as ex:
        logger.error("主程序登录异常,程序退出:"+str(ex))
        driver.quit()
       
#     with open('temp.html','rb') as file:
#         html = file.read()
        
    times = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    cs = CrawlService()
    while(True):
        #清理html
        page = driver.page_source
        cleaner = Cleaner(safe_attrs_only=False)
        html = cleaner.clean_html(page)
        
        logger.info('爬取时间:'+time.strftime("%Y-%m-%d %H:%M", time.localtime()))
        #爬取内容
        temptime = cs.crawl_data(html,times)
        if temptime:
            times = temptime
        logger.info("最后一次发表时间为:"+times)
        #如果配置文件有配置值,则配置文件优先
        steps = config.get('steps')
        if steps:
            logger.info("间隔%s分钟抓取一次网页"%steps)
            time.sleep(steps*60)
        else:
            logger.info("间隔(3-5)分钟抓取一次网页")
            time.sleep(random.randint(3,5)*60) 
        #刷新网页
        driver.refresh()
    driver.quit()
    logger.info("程序已关闭")
    
    
