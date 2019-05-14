import pandas as pd
from pandas import Series,DataFrame
d1=pd.read_csv("2012Transcript.csv",encoding="gbk")
def clear(n):
    
    data=d1.loc[d1["TeamID"]==n]
    g1=data['成绩'].groupby(data['学号'])
    s=g1.agg(["sum"]+["mean"]+["max"]+["min"]+["count"]+["std"])
    s['TeamID']=n
    
    data1=data.loc[data["课程类别_显示值"]=='学科基础必修课']
    group1=data1['成绩'].groupby(data1['学号'])
    jibi=group1.mean()
    s['学科基础必修课平均成绩']=jibi

    data2=data.loc[data["课程类别_显示值"]=='公共必修课']
    group2=data2['成绩'].groupby(data2['学号'])
    gongbi=group2.mean()
    s['公共必修课平均成绩']=gongbi

    data3=data.loc[data["课程类别_显示值"]=='专业必修课']
    group3=data3['成绩'].groupby(data3['学号'])
    zhuanbi=group3.mean()
    s['专业必修课平均成绩']=zhuanbi


    data4=data[data['成绩']<60]
    group4=data4['成绩'].groupby(data4['学号'])

    s['不及格门数']=group4.size()
    return  s   
s1=clear(1)
s2=clear(2)
s3=clear(3)
s4=clear(4)
s5=clear(5)
s6=clear(6)
s7=clear(7)
s8=clear(8)

s=[s1,s2,s3,s4,s5,s6,s7,s8]
f=pd.concat(s)
f
