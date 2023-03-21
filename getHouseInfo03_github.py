# -- coding: utf-8 --*
# @Author : Guan Yabin 2023年2月
# 爬取链家网站郑东新区小区数据，第三步，获取小区的楼栋数、总户数和百度地图下的XY坐标信息
# @E-mail ：guanyabin2010@163.com
import pandas as pd
import requests
from lxml import etree

#第二步的数据源excel
excelPath="D:/lianjia_AllHouse02.xlsx"
excelFile = pd.read_excel(excelPath, sheet_name = 'Sheet1')
number=len(excelFile)#得到总行数
listName=[]
listBulidingNum=[]
listHouseNum=[]
listType=[]
listXData=[]
listYData=[]
for i in range(0,number):
    name=str(excelFile["name"][i])
    listName.append(name)
    href=str(excelFile["href"][i])
    # 访问页面，获取页面HTML-得到小区的栋数和户数
    res = requests.get(href)
    content = res.text
    selector = etree.HTML(content)    
    try:
        # 获取楼栋数
        bulidingNumPath="/html/body/div[6]/div[2]/div[2]/div[5]/span[2]"
        bulidNum= selector.xpath(bulidingNumPath)[0].text
        bulidNum=bulidNum.replace("栋","")
        listBulidingNum.append(bulidNum)       
    except Exception as e:
        #print(name)
        listBulidingNum.append("无数据")
        continue
    try:
        # 获取小区户数
        houseNumPath= '/html/body/div[6]/div[2]/div[2]/div[6]/span[2]'             
        houseNum= selector.xpath(houseNumPath)[0].text   
        houseNum=houseNum.replace("户","")
        listHouseNum.append(houseNum)
    except Exception as e:
        #print(name)
        listHouseNum.append("无数据")
        continue
    try:
        # 获取小区的百度地图XY坐标
        # <span mendian="113.752385,34.766342" xiaoqu="[113.755911,34.76678]" class="actshowMap">永威东棠店</span> 
        xyDataPath="/html/body/div[6]/div[2]/div[2]/div[7]/span[2]/span"
        xyData= selector.xpath(xyDataPath)[0].attrib
        xyStr=xyData["xiaoqu"]
        xyStr=xyStr.replace("[","")
        xyStr=xyStr.replace("]","")
        xyList=xyStr.split(",") # 结果是['113.75895742018', '34.78830592162']
        listXData.append(xyList[0])
        listYData.append(xyList[1])
    except Exception as e:
        print("getXY error:",name)
        listXData.append(0)
        listYData.append(0)
        continue
writer = pd.ExcelWriter("D:/HouseResult03.xlsx")
df1 = pd.DataFrame(data={'name':listName, 'buliding':listBulidingNum,"house":listHouseNum,"baiduX":listXData,"baiduY":listYData})
df1.to_excel(writer,'Sheet1')
writer.save()
print("完成小区的数据采集")
