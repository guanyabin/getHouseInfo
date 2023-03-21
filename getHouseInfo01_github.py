# -- coding: utf-8 --*
# @Author : Guan Yabin 2023年2月
# 爬取链家网站郑东新区小区数据，第一步，获取小区名称和对应详情页面href
# @E-mail ：guanyabin2010@163.com
'''
01：第一个文件，爬取郑州市郑东新区小区数据
第一页的两个链接均可访问
https://zz.fang.lianjia.com/loupan/zhengdongxinqu/#zhengdongxinqu
https://zz.fang.lianjia.com/loupan/zhengdongxinqu/pg1/#zhengdongxinqu
剩余页面链接，pg后参数不同
https://zz.fang.lianjia.com/loupan/zhengdongxinqu/pg11/#zhengdongxinqu
获取小区名称的xPath
/html/body/div[3]/ul[2]/li[1]/div/div[1]/a
获取小区地址的xPath
/html/body/div[3]/ul[2]/li[2]/div/div[1]/a
进入小区详情页面：
https://zz.fang.lianjia.com/loupan/p_drcabmxc/
XY坐标对应的xpath，获取小区的X和Y坐标
//*[@id="mapWrapper"]
第二层详情页面
https://zz.fang.lianjia.com/loupan/p_drcabmxc/xiangqing/
户数的xpath，获取户数信息
/html/body/div[4]/div[1]/ul[3]/li[7]/span[2]
'''
from base64 import decode
import requests
import io
import sys
import importlib
from lxml import etree
import pandas as pd
#importlib.reload(sys)

#首先定义一个Spider类
class Spider():
    def __init__(self):
        self.domain = 'https://zz.lianjia.com/xiaoqu/zhengdongxinqu/'
    #接下来定义一个download_page方法，用于下载一个页面,获取小区的名称和对应详情页面的链接地址
    # 获取已有的已建成已居住的小区
    def download_page(self, url, page):
        res = requests.get(url)
        content = res.text
        selector = etree.HTML(content)
        # 获取li数量
        path = '/html/body/div[4]/div[1]/ul/li'
        size = len(selector.xpath(path))
        print("size=",size)
        # 遍历li节点
        listName=[]
        listHref=[]
        for i in range(1, size + 1):
            li_path = '/html/body/div[4]/div[1]/ul/li[%s]' % i
            # 获取小区名
            path = li_path + '/div[1]/div[1]/a'               
            name = selector.xpath(path)[0].text
            # 获取详情页面路径
            infoUrl = selector.xpath(path)[0].attrib['href']
            listName.append(name)
            listHref.append(infoUrl)                         
        writer = pd.ExcelWriter("D:/lianjia_page{0}.xlsx".format(page))
        df1 = pd.DataFrame(data={'name':listName, 'href':listHref})
        df1.to_excel(writer,'Sheet1')
        writer.save()
        print(page,"完成")

    # 郑东新区新房(当前在售楼盘)数据下载,获取小区名称和详情页面的链接。测试完成。
    def download_pageNewHouse(self, url, page):
        res = requests.get(url)
        content = res.text
        selector = etree.HTML(content)
        #       /html/body/div[3]/ul[2]/li[1]/div/div[1]/a
        #       /html/body/div[3]/ul[2]/li[1]
        #       /html/body/div[3]/ul[2]
        path = '/html/body/div[3]/ul[2]/li'
        size = len(selector.xpath(path))
        print("size=",size)
        # 遍历li节点
        listName=[]
        listAddress=[]
        listHref=[]
        listX=[]
        listY=[]
        for i in range(1, size + 1):
            li_path = '/html/body/div[3]/ul[2]/li[%s]' % i
            # 获取小区名
            path = li_path + '/div/div[1]/a'               
            name = selector.xpath(path)[0].text
            # 获取小区的详细地址
            pathAd = li_path + '/div/div[2]/a'               
            address = selector.xpath(pathAd)[0].text
            # 获取详情页面路径，有坐标 https://zz.fang.lianjia.com/loupan/p_hrzdblhrfbmrfi/
            # //*[@id="mapWrapper"]  span 属性coord有XY坐标
            # 第二页详情页面，有户数信息 https://zz.fang.lianjia.com/loupan/p_hrzdblhrfbmrfi/xiangqing/ 
            # /html/body/div[4]/div[1]/ul[3]/li[7]/span[2] span的text是户数
            infoUrl = "https://zz.fang.lianjia.com"+selector.xpath(path)[0].attrib['href']
            listName.append(name)
            listAddress.append(address)
            listHref.append(infoUrl)  
            listXY=self.download_pageNewHouseXY(infoUrl)    
            listX.append(listXY[1])
            listY.append(listXY[0])                
        writer = pd.ExcelWriter("D:/lianjiaNewHouse_page{0}.xlsx".format(page))
        df1 = pd.DataFrame(data={'name':listName, 'address':listAddress,'href':listHref,'baiduX':listX,'baiduY':listY})
        df1.to_excel(writer,'Sheet1')
        writer.save()
        print(page,"完成")


    # 郑东新区新房数据下载,获取小区名称和详情页面的链接。
    def download_pageNewHouseXY(self, url):
        res = requests.get(url)
        content = res.text
        selector = etree.HTML(content)
        path = '//*[@id="mapWrapper"]'
        xySpan=selector.xpath(path)[0].attrib
        xyStr=xySpan["data-coord"] #'data-coord': '34.838105072104,113.73887707302'
        xyList=xyStr.split(",") 
        print(xyList[1],xyList[0])    
        return xyList 


def main():
    spider = Spider()
    # 采集已有的小区数据，获取第一页，不需要增加pg1后缀，每页30条数据
    spider.download_page('https://zz.lianjia.com/xiaoqu/zhengdongxinqu/',1)   
    # 获取第2页-16页，20230215,455个小区，根据具体的地区进行更换,例如某地区小区数据总共20页，则修改为range（2，21）
    for i in range(2,17):
        page = 'pg{0}'.format(i)
        url = spider.domain+page
        spider.download_page(url,i)
main()
# 结果默认存放在D:/lianjia_page{0}.xlsx
