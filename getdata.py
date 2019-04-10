# 下载并处理miso上的demand 和 price 数据
import urllib.request

# 日期的遍历
import datetime

begin = datetime.date(2019,1,1)
end = datetime.date(2019,3,19)
baseurl = "https://docs.misoenergy.org/marketreports/"
"""
for i in range((end-begin).days+1):
    day = begin + datetime.timedelta(days=i)
    # print(day.strftime('%Y%m%d'))
    otherurl = day.strftime('%Y%m%d') + "_da_pr.xls"
    url = baseurl + otherurl
    downPath = "D:/0毕设/data/price/" + otherurl # 是文件名而不是文件夹
    urllib.request.urlretrieve(url, downPath)
"""
"""
# 将demand中已下载的文件提取physical demand到一个csv文件
import xlrd
import pandas as pd
from pandas import DataFrame
result_filename = "D:/0毕设/data/demand/demand.txt"
cols = []

for i in range((end-begin).days+1):
    day = begin + datetime.timedelta(days=i)
    filename = "D:/0毕设/data/demand/" + day.strftime('%Y%m%d') + "_da_ex.xls"
    df = pd.read_excel(filename)
    data = df.ix[0]
    wb = xlrd.open_workbook(filename=filename)  # 打开文件
    sheet = wb.sheet_by_index(0)  # 通过索引获取表格
    cols.append(sheet.col_values(1)) # 获取列内容
    cols[i] = cols[i][5:]
    cols[i][0] = day.strftime('%Y%m%d')

print(cols)
df = pd.DataFrame(cols,columns=['Date','Hour1', 'Hour2', 'Hour3', 'Hour4', 'Hour5', 'Hour6', 'Hour7', 'Hour8', 'Hour9', 'Hour10', 'Hour11', 'Hour12',
                                 'Hour13', 'Hour14', 'Hour15', 'Hour16', 'Hour17', 'Hour18', 'Hour19', 'Hour20', 'Hour21', 'Hour22', 'Hour23', 'Hour24'])
df.to_csv(result_filename)
"""

# 将price中已下载的文件提取system price到一个csv文件
import xlrd
import pandas as pd
from pandas import DataFrame
result_filename = "D:/0毕设/data/price/price.txt"
cols = []

for i in range((end-begin).days+1):
    day = begin + datetime.timedelta(days=i)
    filename = "D:/0毕设/data/price/" + day.strftime('%Y%m%d') + "_da_pr.xls"
    df = pd.read_excel(filename)
    data = df.ix[0]
    wb = xlrd.open_workbook(filename=filename)  # 打开文件
    sheet = wb.sheet_by_index(0)  # 通过索引获取表格
    cols.append(sheet.col_values(1)) # 获取列内容
    cols[i] = cols[i][14:39]
    cols[i][0] = day.strftime('%Y%m%d')

print(cols)
df = pd.DataFrame(cols,columns=['Date','Hour1', 'Hour2', 'Hour3', 'Hour4', 'Hour5', 'Hour6', 'Hour7', 'Hour8', 'Hour9', 'Hour10', 'Hour11', 'Hour12',
                                 'Hour13', 'Hour14', 'Hour15', 'Hour16', 'Hour17', 'Hour18', 'Hour19', 'Hour20', 'Hour21', 'Hour22', 'Hour23', 'Hour24'])
df.to_csv(result_filename)






