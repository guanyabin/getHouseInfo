# -- coding: utf-8 --*
# @Author : Guan Yabin 2023年2月
# 爬取链家网站郑东新区小区数据，第二步，在第一步生成多个excel文件基础上，合并所有的excel为一个最终的excel
# @E-mail ：guanyabin2010@163.com
import pandas as pd
import os
data_list=[]
# 循环当前文件夹下的所有excel，读取全部数据，追加到data_list中
path = "D:/"
for fname in os.listdir(path):
    print(fname)
    if fname.startswith("lianjia_page")  and fname.endswith(".xlsx"):
        data_list.append(pd.read_excel(path+fname))
data_all=pd.concat(data_list)
# 生成新的汇总文件
data_all.to_excel("D:/lianjia_AllHouse02.xlsx",index=False)
print("OK!combine excel。")
