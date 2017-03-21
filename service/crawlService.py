'''
Created on 2017年2月22日

@author: test
'''

#xpath
from lxml import etree
import base64
import requests
import queue
import os

from dao.baseDataDao import BaseDataDao
from dao.pictureDao import PictureDao
from common.loggingCommon import MulLogger
logger = MulLogger()
import time
import urllib

class CrawlService(object):
    
    def __init__(self):
        self.basedata = BaseDataDao()
        self.picture = PictureDao()
    
    def to_Base64(self,picpath):
        '''把图片转换为base64编码
        @picpath:图片路径
        '''
        try:
            with open(picpath,'rb') as file:
                baseFile=base64.b64encode(file.read()) #读取文件内容，转换为base64编码
                return baseFile
        except Exception as ex:
            logger.warnning("图片编码发生异常:"+ex)
            return ''

    def download_picture(self,picture_path, url):
        '''下载图片
        @picture_path:picture存放的路径
        @url:图片url地址
        '''
        try:
            ir = requests.get(url, timeout=200)
            if ir.status_code != 200:
                return
            bs_name = os.path.basename(url)
            picpath=os.path.join(picture_path, bs_name)
            with open(picpath, 'wb') as file:
                file.write(ir.content)
            return self.to_Base64(picpath)
        except Exception as ex:
            logger.warnning("下载图片发生异常:"+ex)
            return
    
    def download_video(self,video_path,url):
        '''下载秒怕视频
        @video_path:video存放的路径
        @url:视频url地址
        '''
        try:
            ir = requests.get(url, timeout=200)
            if ir.status_code != 200:
                return
            bs_name = os.path.basename(url).split('?')[0]
            picpath=os.path.join(video_path, bs_name)
            with open(picpath, 'wb') as file:
                file.write(ir.content)
            return bs_name
        except Exception as ex:
            logger.warnning("下载视频发生异常:"+ex)
            return
        
    def getData_from_xPath(self,node, path):
        '''获取一个div下面的所有数据
        @node:需要抓取文本的节点
        @path:需要抓取文本的xpth路径
        '''
        p = node.xpath(path)
        if p is None:
            return None
        if len(p) == 0:
            return None;
        paths = path.split("/")
        last = paths[-1]
        if last.find("@")>=0 and last.find("[1]")>=0:
            return p[0]
        return  self.get_node_text(p[0])
    
    def get_node_text(self,elem):
        """获取元素节点内部全部文本
        @elem:需要抓取文件内容的节点元素
        """
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return "".join(rc)
    
    def crawl_data(self,html,endtime):
        '''数据抓取函数
        @html:需要分析抓取的原html文件
        @endtime:上一次发布消息的结束时间
        '''
        root = etree.HTML(html)
        tree = etree.ElementTree(root)
        
        mtime = []
        times = tree.xpath('//div[@class="WB_detail"]')
        #单独获取时间,通过时间判断是否跳过该条记录
        for t in times:
            mtime.append(t.xpath('div[2]/a')[0].get('title'))
        nodes = tree.xpath('//div[@class="WB_detail"]')
        i=0
        #获取内容
        for pp in nodes: 
            gg=pp.getchildren()
            #检测时间
            if endtime >= mtime[i]:
                i=i+1
                continue
            
            #检测是否是原创
            bl = False
            for dv in gg:
                if 'WB_feed_expand' in dv.attrib.get('class').split(' '):
                    bl = True
            if bl:
                i=i+1
                continue
            #原创,创建文件夹收藏
            videopath = os.getcwd()+'\\video\\'
            if not os.path.exists(videopath):
                try:
                    os.mkdir(videopath) #video统一放在一个目录
                except Exception as ex:
                    logger.warnning("创建video新文件时发生异常:"+str(ex))
                    
            picturepath = os.getcwd()+'\\picture\\'
            try:
                pth = picturepath+mtime[i].replace(':','-')+'_'+str(i)
                os.mkdir(pth) #图片分日期文件夹存放
            except Exception as ex:
                i=i+1
                logger.warnning("创建picture新文件时发生异常:"+str(ex))
                continue
            i=i+1
            
            #暂存文件
#             tt = time.strftime("%Y-%m-%d %H:%M", time.localtime())
#             with open(str(tt.replace(':','-'))+'.html','wb') as file:
#                 file.write(bytes(html,'utf-8'))
    
            #获取数据，以下部分通过分析html网页进行数据提取
            data = {}
            picture = []
            base64picture = []
            datatype = 1 #1:图片 or 2:视频
            for dv in gg:
                if 'WB_from' in dv.attrib.get('class').split(' '):#时间
                    ntime = dv.getchildren()
                    if not ntime:
                        ntime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
                        data['ntime'] = ntime
                        continue
                    ntime = ntime[0].get('title')
                    data['ntime'] = ntime
                    logger.info('time: '+ntime)
                if 'WB_info' in dv.attrib.get('class').split(' '):#发布人
                    name = dv.getchildren()[0].text.replace(' ','')
                    data['name'] = name
                    logger.info('name: '+name)
                if 'WB_text' in dv.attrib.get('class').split(' '):#介绍
                    content = self.getData_from_xPath(dv,'.')
					#此处可以写个正则子函数，单独做匹配。这里我偷工减料了
                    data['content'] = content.replace(' ','').replace("’",'"').replace("‘",'"').replace("“",'"').replace("”",'"').replace("，",",").replace("。",".")
                    logger.info('content: '+content)
                if 'WB_media_wrap' in dv.attrib.get('class').split(' '):#图片
                    lis = dv.xpath('div[1]/ul')
                    if not lis: 
                        continue
                    lis = lis[0].getchildren()
                    try:
                        for li in lis:
                            if 'WB_video' in li.attrib.get('class'):#为视频资源
                                mlist = li.attrib.get('action-data').split('&')
                                dics = [m.split('=') for m in mlist]
                                for vio in dics:
                                    if len(vio) == 2:
                                        if vio[0] == 'video_src':#是视频资源
                                            ur = urllib.parse.unquote(vio[1])
                                            videoname=self.download_video(videopath ,ur)
                                            if not videoname:
                                                continue
                                            picture.append(ur)
                                            base64picture.append({"data":videoname,"type":2})
                                            datatype = 2
                                        if vio[0] == 'cover_img':#是视频封面图资源
                                            ur = urllib.parse.unquote(vio[1])
                                            picture_souce = self.download_picture(videopath,ur)
                                            if not picture_souce:
                                                continue
                                            base64picture.append({"data":str(picture_souce),"type":1})
                                            picture.append(ur)
                                break #跳出循环
                            else:#为图片资源
                                ur = li.getchildren()[0].attrib.get('src')
                                if not ur:
                                    continue
                                ur = ur.replace('thumb150','mw1024')
                                picture.append(ur)
                                video_souce = self.download_picture(videopath,ur)
                                if not video_souce:
                                    continue
                                base64picture.append({"data":str(video_souce),"type":1})
                    except Exception as ex:
                        logger.warnning("图片下载出现异常:"+str(ex))
                    data['picture'] = picture
                    logger.info('picture: '+str(picture))
            try:
                if base64picture:#有图片or视频才存数据库
                    idnum = self.picture.insert_list_picture(base64picture)
                    picid = [id for id in range(idnum-len(base64picture)+1,idnum+1)]
                    tt = time.mktime(time.strptime(data.get('ntime'),'%Y-%m-%d %H:%M'))
                    self.basedata.insert_baseData(data.get('name'),tt,'key',data.get('content'),str(picid),datatype)
#               else:
#                    os.rmdir(pth) #删除空文件夹
            except Exception as ex:
                logger.warnning("数据库入库发生异常"+str(ex))
            try:
                if base64picture: #由于编码问题，有时候会写入文件失败
                    with open('data.json','a+') as file:
                        file.write(str(data))
                        file.write(str(',\n\r'))
                        file.close()
            except Exception as ex:
                try:
                    del data['content']
                    with open('data.json','a+') as file: #由于编码问题，第一次写入文件失败，尝试再次写入
                            file.write(str(data))
                            file.write(str(',\n\r'))
                            file.close()
                except Exception as ex:
                    logger.warnning("数据写入文件失败"+str(ex))
        return mtime[0] if mtime else False



        
