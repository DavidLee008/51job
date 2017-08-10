# -*- coding:utf-8 -*-
from pprint import pprint
import csv
import codecs
from collections import Counter
from echarts import Echart, Legend, Pie
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def locate1():
        """ 统计各个地区的招聘数 """
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        lst = []
        lst1 = []
        lst2 = []
        with codecs.open(r"E:\51job\data\locate.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            #lst = [row[1] for row in f_csv]
            #for row in f_csv:
                #if "深圳" in row[0]:
            for row in f_csv:
                lst = row[1]
                for i,rows in enumerate(lst):
                    a += int(lst[i])

            lst2.append((a,))
            pprint(a)

            #pprint(lst2)
        with codecs.open(r"E:\51job\data\test.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst2)

if __name__ == "__main__":
    locate1()
