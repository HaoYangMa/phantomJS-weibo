


----------新浪微博网页爬虫--------------
时间：2017/3/21
版本：V1.0
功能描述：
@1.配置用户名和密码动态登录新浪微博
@2.配置要爬取得专栏,可以动态爬取以下内容：
a.发布者
b.发布时间
c.描述文本
d.图片 or 视频


----------配置文件说明----------------
@1.mysqldb:mysql数据库链接配置
@2.login：新浪微博登录配置
@3.steps：实时爬取的时候，间隔多少时间刷新一次网页。为0的时候,默认是3-5分钟
@4.target：需要爬取得关注栏目（原创板块）


-----------数据库创建-----------------
-- ----------------------------
-- Table structure for jokedata
-- ----------------------------
DROP TABLE IF EXISTS `jokedata`;
CREATE TABLE `jokedata` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `addtime` int(11) NOT NULL,
  `name` varchar(60) NOT NULL COMMENT '发表者',
  `keyworld` varchar(60) DEFAULT NULL COMMENT '关键字,暂时没有用',
  `content` varchar(255) NOT NULL COMMENT '文本内容',
  `pictureid` varchar(120) DEFAULT NULL COMMENT '图片or视频id',
  `datatype` tinyint(4) NOT NULL COMMENT '1:图片,2:视频',
  `other` varchar(255) DEFAULT '/0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for jokepicture
-- ----------------------------
DROP TABLE IF EXISTS `jokepicture`;
CREATE TABLE `jokepicture` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `img` longtext COMMENT 'base64图片 or 视频路径',
  `datatype` tinyint(4) NOT NULL COMMENT '1:图片,2:视频',
  `other` varchar(255) DEFAULT '/0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;



