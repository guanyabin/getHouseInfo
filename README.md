# getHouseInfo
# guanyabin2010@163.com,2023年3月
python代码实现爬取链家网站小区信息，共四个python文件，基于Python3.8.13运行，需要安装代码中对应的第三方库。
1、第一步，运行getHouseInfo01_github.py，获取小区的名称和对应详情页面的href。
注意：不同地区的数据需要修改页面的访问路径，结果文件的保存路径。生成的execl默认会追加一列ID，可自行处理，保留或者删除。
2、第二步，在第一步基础上，整合多个页面的小区数据，运行combineHouseInfo02_github.py。例如本实验在2023年2月15日采集郑东新区小区数据，共455个小区，16页，得到16个excel文件，此步骤将直接把16个excel文件合并为一个文件。
3、第三步，运行getHouseInfo03_github.py，读取第二步整合文件中的href，进入小区的详情页面获取小区的楼栋数、总户数和百度地图的X和Y坐标（需要转换为GIS系统下的坐标）。
4、第四步，将百度地图坐标系统下的XY坐标转换为GIS坐标，运行getHouseInfo04_github.py文件，转换坐标，注意其余字段的处理，可自行定义。
