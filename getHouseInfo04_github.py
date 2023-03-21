# -- coding: utf-8 --*
# @Author : Guan Yabin 2023年2月
# 爬取链家网站郑东新区小区数据，第四步，百度地图XY坐标转换为GIS坐标的代码
# @E-mail ：guanyabin2010@163.com
import math as Math
import pandas as pd

def baiduToWgs84( bdLon,bdLat):
    PI = 3.14159265358979324;
    x_pi = 3.14159265358979324 * 3000.0 / 180.0;
    x = float(bdLon) - 0.0065;
    y = float(bdLat) - 0.006;
    z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * x_pi);
    theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * x_pi);
    gcjLon = z * Math.cos(theta);
    gcjLat = z * Math.sin(theta);
    a = 6378245.0;
    ee = 0.00669342162296594323;
    dLat = transformLat(gcjLon - 105.0, gcjLat - 35.0);
    dLon = transformLon(gcjLon - 105.0, gcjLat - 35.0);
    radLat = gcjLat / 180.0 * PI;
    magic = Math.sin(radLat);
    magic = 1 - ee * magic * magic;
    sqrtMagic = Math.sqrt(magic);
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * Math.cos(radLat) * PI);
    dLat = gcjLat - dLat;
    dLon = gcjLon - dLon;
    map={"wgs84lat":dLat,"wgs84lon": dLon}
    return map
        
def  transformLon( x,  y):
    PI = 3.14159265358979324;
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(abs(x));
    ret += (20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    ret += (20.0 * Math.sin(x * PI) + 40.0 * Math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
    ret += (150.0 * Math.sin(x / 12.0 * PI) + 300.0 * Math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
    return ret

def  transformLat ( x, y):
    PI = 3.14159265358979324;
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(abs(x));
    ret += (20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    ret += (20.0 * Math.sin(y * PI) + 40.0 * Math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
    ret += (160.0 * Math.sin(y / 12.0 * PI) + 320 * Math.sin(y * PI / 30.0)) * 2.0 / 3.0;
    return ret 

#数据源excel
excelPath="D:/HouseResult03.xlsx"
excelFile = pd.read_excel(excelPath, sheet_name = 'Sheet1')
number=len(excelFile)
listName=[]
listXData=[]
listYData=[]
for i in range(0,number):
    name=str(excelFile["name"][i])
    listName.append(name)
    x=excelFile["baiduX"][i]
    y=excelFile["baiduY"][i]
    resultXY=baiduToWgs84( x,  y)
    listXData.append(resultXY["wgs84lon"])
    listYData.append(resultXY["wgs84lat"])

writer = pd.ExcelWriter("D:/HouseResult03_GIS.xlsx")
df1 = pd.DataFrame(data={'name':listName,"gisX":listXData,"gisY":listYData})
df1.to_excel(writer,'Sheet1')
writer.save()
print("xy：baidu to gis OK")
