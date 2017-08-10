# -*- coding:utf-8 -*-
from pprint import pprint
import csv
import codecs
from collections import Counter
from echarts import Echart, Legend, Pie
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Jobspider1():

    def beijing_salary(self):
        """ 北京工资范围分布 """
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        lst = []
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if "北京" in row[1]:
                    if 0 <= float(row[0]) <= 1.0 :
                        i1 += 1
                    elif 1.1 <= float(row[0]) <= 1.5 :
                        i2 += 1
                    elif 1.6 <= float(row[0]) <= 2.0 :
                        i3 += 1
                    elif 2.1 <= float(row[0]) <= 2.5 :
                        i4 += 1
                    else:
                        i5 += 1
            lst.append((i1,i2,i3,i4,i5))

        with codecs.open(r"E:\51job\data\beijing.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)


    def shanghai_salary(self):
        """ 上海工资范围分布 """
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        lst = []
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if "上海" in row[1]:
                    if 0 <= float(row[0]) <= 1.0 :
                        i1 += 1
                    elif 1.1 <= float(row[0]) <= 1.5 :
                        i2 += 1
                    elif 1.6 <= float(row[0]) <= 2.0 :
                        i3 += 1
                    elif 2.1 <= float(row[0]) <= 2.5 :
                        i4 += 1
                    else:
                        i5 += 1
            lst.append((i1,i2,i3,i4,i5))

        with codecs.open(r"E:\51job\data\shanghai.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)

    def shenzhen_salary(self):
        """ 深圳工资范围分布 """
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        lst = []
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if "深圳" in row[1]:
                    if 0 <= float(row[0]) <= 1.0 :
                        i1 += 1
                    elif 1.1 <= float(row[0]) <= 1.5 :
                        i2 += 1
                    elif 1.6 <= float(row[0]) <= 2.0 :
                        i3 += 1
                    elif 2.1 <= float(row[0]) <= 2.5 :
                        i4 += 1
                    else:
                        i5 += 1
            lst.append((i1,i2,i3,i4,i5))

        with codecs.open(r"E:\51job\data\shenzhen.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)

    def guangzhou_salary(self):
        """ 广州工资范围分布 """
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        lst = []
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if "广州" in row[1]:
                    if 0 <= float(row[0]) <= 1.0 :
                        i1 += 1
                    elif 1.1 <= float(row[0]) <= 1.5 :
                        i2 += 1
                    elif 1.6 <= float(row[0]) <= 2.0 :
                        i3 += 1
                    elif 2.1 <= float(row[0]) <= 2.5 :
                        i4 += 1
                    else:
                        i5 += 1
            lst.append((i1,i2,i3,i4,i5))

        with codecs.open(r"E:\51job\data\guangzhou.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)

    def yidi_salary(self):
        """ 广州工资范围分布 """
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        lst = []
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if "异地招聘" in row[1]:
                    if 0 <= float(row[0]) <= 1.0 :
                        i1 += 1
                    elif 1.1 <= float(row[0]) <= 1.5 :
                        i2 += 1
                    elif 1.6 <= float(row[0]) <= 2.0 :
                        i3 += 1
                    elif 2.1 <= float(row[0]) <= 2.5 :
                        i4 += 1
                    else:
                        i5 += 1
            lst.append((i1,i2,i3,i4,i5))

        with codecs.open(r"E:\51job\data\yidi.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)

    def beijing_salary_dis(self):
        lst = []
        with codecs.open(r"E:\51job\data\beijing.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for i in range(5):
                    lst.append(int(row[i]))
            chart = Echart(u'北京-工资范围分布', '[x,y]包含边界值x和y')
            chart.use(Pie('Beijing', [{'value': lst[0], 'name': '[0,1.0]: %d'% (lst[0])},
                          {'value': lst[1], 'name': '[1.1,1.5]: %d'% (lst[1])},
                          {'value': lst[2], 'name': '[1.6,2.0]: %d'% (lst[2])},
                          {'value': lst[3], 'name': '[2.1,2.5]: %d'% (lst[3])},
                          {'value': lst[4], 'name': '>2.5: %d'% (lst[4])}],
                            radius=["50%", "70%"]))
            #chart.use(Legend(['Beijing']))
            del chart.json["xAxis"]
            del chart.json["yAxis"]
            chart.plot()

    def shanghai_salary_dis(self):
        lst = []
        with codecs.open(r"E:\51job\data\shanghai.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for i in range(5):
                    lst.append(int(row[i]))
            chart = Echart(u'上海-工资范围分布', '[x,y]包含边界值x和y')
            chart.use(Pie('Shanghai', [{'value': lst[0], 'name': '[0,1.0]: %d'% (lst[0])},
                          {'value': lst[1], 'name': '[1.1,1.5]: %d'% (lst[1])},
                          {'value': lst[2], 'name': '[1.6,2.0]: %d'% (lst[2])},
                          {'value': lst[3], 'name': '[2.1,2.5]: %d'% (lst[3])},
                          {'value': lst[4], 'name': '>2.5: %d'% (lst[4])}],
                            radius=["50%", "70%"]))
            #chart.use(Legend(['Beijing']))
            del chart.json["xAxis"]
            del chart.json["yAxis"]
            chart.plot()

    def shenzhen_salary_dis(self):
        lst = []
        with codecs.open(r"E:\51job\data\shenzhen.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for i in range(5):
                    lst.append(int(row[i]))
            chart = Echart(u'深圳-工资范围分布', '[x,y]包含边界值x和y')
            chart.use(Pie('Shenzhen', [{'value': lst[0], 'name': '[0,1.0]: %d'% (lst[0])},
                          {'value': lst[1], 'name': '[1.1,1.5]: %d'% (lst[1])},
                          {'value': lst[2], 'name': '[1.6,2.0]: %d'% (lst[2])},
                          {'value': lst[3], 'name': '[2.1,2.5]: %d'% (lst[3])},
                          {'value': lst[4], 'name': '>2.5: %d'% (lst[4])}],
                            radius=["50%", "70%"]))
            #chart.use(Legend(['Beijing']))
            del chart.json["xAxis"]
            del chart.json["yAxis"]
            chart.plot()

    def guangzhou_salary_dis(self):
        lst = []
        with codecs.open(r"E:\51job\data\guangzhou.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for i in range(5):
                    lst.append(int(row[i]))
            chart = Echart(u'广州-工资范围分布', '[x,y]包含边界值x和y')
            chart.use(Pie('Guangzhou', [{'value': lst[0], 'name': '[0,1.0]: %d'% (lst[0])},
                          {'value': lst[1], 'name': '[1.1,1.5]: %d'% (lst[1])},
                          {'value': lst[2], 'name': '[1.6,2.0]: %d'% (lst[2])},
                          {'value': lst[3], 'name': '[2.1,2.5]: %d'% (lst[3])},
                          {'value': lst[4], 'name': '>2.5: %d'% (lst[4])}],
                            radius=["50%", "70%"]))
            #chart.use(Legend(['Beijing']))
            del chart.json["xAxis"]
            del chart.json["yAxis"]
            chart.plot()

    def yidi_salary_dis(self):
        lst = []
        with codecs.open(r"E:\51job\data\yidi.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for i in range(5):
                    lst.append(int(row[i]))
            chart = Echart(u'异地招聘-工资范围分布', '[x,y]包含边界值x和y')
            chart.use(Pie('Guangzhou', [{'value': lst[0], 'name': '[0,1.0]: %d'% (lst[0])},
                          {'value': lst[1], 'name': '[1.1,1.5]: %d'% (lst[1])},
                          {'value': lst[2], 'name': '[1.6,2.0]: %d'% (lst[2])},
                          {'value': lst[3], 'name': '[2.1,2.5]: %d'% (lst[3])},
                          {'value': lst[4], 'name': '>2.5: %d'% (lst[4])}],
                            radius=["50%", "70%"]))
            #chart.use(Legend(['Beijing']))
            del chart.json["xAxis"]
            del chart.json["yAxis"]
            chart.plot()

if __name__ == "__main__":
    spider1 = Jobspider1()
    spider1.beijing_salary()
    spider1.shanghai_salary()
    spider1.shenzhen_salary()
    spider1.guangzhou_salary()
    spider1.yidi_salary()
    spider1.beijing_salary_dis()
    spider1.shanghai_salary_dis()
    spider1.shenzhen_salary_dis()
    spider1.guangzhou_salary_dis()
    spider1.yidi_salary_dis()
