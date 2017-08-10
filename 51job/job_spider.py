# -*- coding:utf-8 -*-
from pprint import pprint
import csv
from collections import Counter
import requests
from bs4 import BeautifulSoup
import jieba
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
import codecs
import numpy as np
from scipy.interpolate import spline
from salary import Jobspider1

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体

class JobSpider():

    def __init__(self):
        self.company = []
        self.text = ""
        self.headers = {'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/56.0.2924.87 Safari/537.36'}

    def job_spider(self):
        """ 爬虫入口 """
       # url = "http://search.51job.com/list/010000%252C020000%252C030200%252C040000,000000,0000,00,9,99,Python,2,{}.html?" \
       #       "lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0" \
       #       "&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="

        url = "http://search.51job.com/jobsearch/search_result.php?"\
              "fromJs=1&jobarea=040000%2C010000%2C020000%2C030200&keyword=Python" \
              "&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"

        urls = [url.format(p) for p in range(1, 14)]
        for url in urls:
            r = requests.get(url, headers=self.headers).content.decode('gbk')
            bs = BeautifulSoup(r, 'lxml').find("div", class_="dw_table").find_all("div", class_="el")
            for b in bs:
                try:
                    href, post = b.find('a')['href'], b.find('a')['title']
                    locate = b.find('span', class_='t3').text
                    salary = b.find('span', class_='t4').text
                    d = {'href':href, 'post':post, 'locate':locate, 'salary':salary}
                    self.company.append(d)
                except Exception:
                    pass

    def post_require(self):
        """ 爬取职位描述 """
        for c in self.company:
            r = requests.get(c.get('href'), headers=self.headers).content.decode('gbk')
            bs = BeautifulSoup(r, 'lxml').find("div", class_="bmsg job_msg inbox").text
            s = bs.replace("举报", "").replace("分享", "").replace("\t", "").strip()
            self.text += s
        #print self.text
        with codecs.open(r"E:\51job\data\post_require.txt", "w+", encoding="utf-8") as f:
            f.write(self.text)

    def post_desc_counter(self):
        """ 职位描述统计 """
        post = codecs.open(r"E:\51job\data\post_require.txt", "r", encoding="utf-8").read()
        #使用jieba分词
        jieba.load_userdict(r"E:\51job\data\user_dict.txt")
        seg_list = jieba.cut(post, cut_all=False)
        counter = dict()
        for seg in seg_list:
            counter[seg] = counter.get(seg, 1) + 1
        counter_sort = sorted(counter.items(), key=lambda value: value[1], reverse=True)
        #pprint(counter_sort)
        with codecs.open(r"E:\51job\data\post_pre_desc_counter.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(counter_sort)

    def post_counter(self):
        """ 职位统计 """
        lst = [c.get('post') for c in self.company]
        counter = Counter(lst)
        counter_most = counter.most_common()
        #pprint(counter_most)
        with codecs.open(r"E:\51job\data\post_pre_counter.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(counter_most)

    def post_salary_locate(self):
        """ 招聘大概信息，职位，薪酬以及工作地点 """
        lst = []
        for c in self.company:
            lst.append((c.get('salary'), c.get('post'), c.get('locate')))
        #pprint(lst)
        with codecs.open(r"E:\51job\data\post_salary_locate.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)


    def post_salary(self):
        """ 薪酬统一处理 """
        lst1 = []
        lst2 = []
        lst3 = []
        month = []
        year = []
        thouand = []
        with codecs.open(r"E:\51job\data\post_salary_locate.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if "万/月" in row[0]:
                    #使用正则表达式匹配数字，去除中文
                    #lst1 = re.match(r'^[0-9]\.([0-9]+|[0-9])\-[0-9]\.([0-9]+|[0-9])', row[0])
                    #if lst1:
                        #month.append((lst1.group(), row[2], row[1]))
                    month.append((row[0][:-7], row[2], row[1]))
                elif "万/年" in row[0]:
                    #lst2 = re.match(r'^[0-9]\.([0-9]+|[0-9])\-[0-9]\.([0-9]+|[0-9])', row[0])
                    #if lst2:
                        #year.append((lst2.group(), row[2], row[1]))
                    year.append((row[0][:-7], row[2], row[1]))
                elif "千/月" in row[0]:
                    #lst3 = re.match(r'^[0-9]\.([0-9]+|[0-9])\-[0-9]\.([0-9]+|[0-9])', row[0])
                    #if lst3:
                        #thouand.append((lst3.group(), row[2], row[1]))
                    thouand.append((row[0][:-7], row[2], row[1]))
        pprint(month)
        calc = []
        for m in month:
            pprint(m[0])
            s = m[0].split("-")
            calc.append((round((float(s[1]) - float(s[0])) * 0.4 + float(s[0]), 1), m[1], m[2]))

        for y in year:
            s = y[0].split("-")
            calc.append((round(((float(s[1]) - float(s[0])) * 0.4 + float(s[0])) / 12, 1), y[1], y[2]))

        for t in thouand:
            s = t[0].split("-")
            calc.append((round(((float(s[1]) - float(s[0])) * 0.4 + float(s[0])) / 10, 1), t[1], t[2]))

        pprint(calc)
        with codecs.open(r"E:\51job\data\post_salary.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(calc)

    def post_salary_counter(self):
        """ 薪酬统计 """
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            lst = [row[0] for row in f_csv]
        counter = Counter(lst).most_common()
        #pprint(counter)
        with codecs.open(r"E:\51job\data\post_salary1.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(counter)


    def word_cloud(self):
        """ 生成词云 """
        counter = {}
        with codecs.open(r"E:\51job\data\post_pre_desc_counter.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                counter[row[0]] = counter.get(row[0], int(row[1]))
            pprint(counter)
        wordcloud = WordCloud(font_path=r"E:\51job\font\msyh.ttf",
                              max_words=2000, height=1000, width=1500).generate_from_frequencies(counter)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        wordcloud.to_file('E:\51job\images\wordcloud.jpg')

    def insert_into_db(self):
        """ 插入数据到数据库
            creat table jobpost(
                j_salary float(3, 1),
                j_locate text,
                j_post text
            );
        """
        import pymysql
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="lee", charset="utf8")
        cur = conn.cursor()
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            sql = "insert into jobpost(j_salary, j_locate, j_post) values(%s, %s, %s)"
            for row in f_csv:
                value = (row[0], row[1], row[2])
                try:
                    cur.execute(sql, value)
                    conn.commit()
                except Exception as e:
                    print e
        cur.close()

    def locate(self):
        """ 统计总招聘数 """
        lst = [c.get('locate') for c in self.company]
        counter = Counter(lst)
        counter_most = counter.most_common()
        #pprint(counter_most)
        with codecs.open(r"E:\51job\data\locate.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(counter_most)

    def locate1(self):
        """ 统计各个地区的招聘数 """
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        lst = []
        with codecs.open(r"E:\51job\data\locate.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if "深圳" in row[0]:
                    a += 1

                elif "上海" in row[0]:
                    b += 1

                elif "北京" in row[0]:
                    c += 1

                elif "广州" in row[0]:
                    d += 1

                else:
                    e += 1
            lst.append((a, b, c, d, e, f))
        with codecs.open(r"E:\51job\data\locate1.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)


    """def locate_counter1(self):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
        sum = []
        #统计深圳
        with codecs.open(r"E:\51job\data\locate1.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            column = [row[1] for row in f_csv]
            print column
        for i,rows in enumerate(column):
            sum1 += int(column[i])
        sum.append(str(sum1))
        print sum1

        #统计上海
        with codecs.open(r"E:\51job\data\locate2.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            column = [row[1] for row in f_csv]
            print column
        for i,rows in enumerate(column):
            sum2 += int(column[i])
        sum.append(str(sum2))
        print sum2

        with codecs.open(r"E:\51job\data\locate3.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            column = [row[1] for row in f_csv]
            print column
        for i,rows in enumerate(column):
            sum3 += int(column[i])
        sum.append(str(sum3))
        print sum3

        with codecs.open(r"E:\51job\data\locate4.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            column = [row[1] for row in f_csv]
            print column
        for i,rows in enumerate(column):
            sum4 += int(column[i])
        sum.append(str(sum4))
        print sum4

        with codecs.open(r"E:\51job\data\locate5.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            column = [row[1] for row in f_csv]
            print column
        for i,rows in enumerate(column):
            sum5 += int(column[i])
        sum.append(str(sum5))
        print sum5

        pprint(sum)
        with codecs.open(r"E:\51job\data\locate_sum.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows([sum])"""

    def employment_counter(self):
        """ 显示各地招聘数量的散点图 """
        T = np.array([1, 2, 3, 4, 5])
        y = []
        with codecs.open(r"E:\51job\data\locate1.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for i in range(5):
                    y.append(int(row[i]))

        power = np.array(y)
        xnew = np.linspace(T.min(),T.max())
        smooth = spline(T, power, xnew)
        plt.plot(xnew, smooth)
        plt.plot(T, y,"og", label=u"招聘数量", )
        plt.xlabel(u'招聘地点')
        plt.ylabel(u'招聘数量')
        plt.xticks((1,2,3,4,5), (u'深圳', u'上海', u'北京', u'广州', u'异地招聘'))
        for i in range(5):
            text(T[i]-0.05, y[i]-10, y[i], fontsize=12)
        plt.title(u'招聘职位的各地的数量')
        plt.legend()
        plt.show()

    def tech_counter(self):
        """ 过滤掉中文的关键词，统计出前20的英文词汇 """
        lst = []
        match = []
        with codecs.open(r"E:\51job\data\post_desc_counter.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                lst = re.search(r'^[a-zA-Z]+$', row[0])
                #匹配到非字母的时候返回None，因此用if判断，不然会报错
                if lst:
                    pprint(lst.group())
                    match.append((lst.group(), row[1]))

        with codecs.open(r"E:\51job\data\match_counter.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(match)

    def tech_counter1(self):
        """ 展示出前20的英文词汇 """
        i = 2
        x = []
        y = []
        x1 = []
        with codecs.open(r"E:\51job\data\match_counter.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                x1.append(row[0])
                y.append(row[1])

        for i in range(17):
            i += 2
            x.append(i)

        plt.bar(x, y, label=u'掌握的能力')
        plt.xticks(x,x1)
        for i in range(17):
            text(x[i]-0.15, int(y[i])+10, y[i], fontsize=12)
        plt.legend()
        plt.xlabel(u'能力')
        plt.ylabel(u'提及的次数')
        plt.title(u'所需掌握的技术')
        plt.show()

    def post_counter_dis(self):
        i = 2
        y = []
        x = []
        y1 =[]
        with codecs.open(r"E:\51job\data\post_pre_counter1.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                x.append(row[1])
                y1.append(row[0])

        for i in range(22):
            i = i + 2
            y.append(i)

        #plt.barh:横着显示条形图的函数
        plt.barh(y, x, label=u'职位')
        plt.yticks(y, y1)
        for i in range(22):
            text(int(x[i])+2, y[i]-0.2, x[i], fontsize=12)
        plt.legend()
        plt.title(u'职位统计')
        plt.show()

    def salary_distribution(self):
        i1 = 0
        i2 = 0
        i3 = 0
        i4 = 0
        i5 = 0
        lst = []
        with codecs.open(r"E:\51job\data\post_salary.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if 0 <= float(row[0]) <= 1.0:
                    i1 += 1
                elif 1.1 <= float(row[0]) <=1.5:
                    i2 += 1
                elif 1.6 <= float(row[0]) <= 2.0:
                    i3 += 1
                elif 2.1 <= float(row[0]) <= 2.5:
                    i4 += 1
                else:
                    i5 += 1
            lst.append((i1,i2,i3,i4,i5))


        with codecs.open(r"E:\51job\data\salary_distribution.csv", "w+", encoding="utf-8") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lst)

    def salary_distribution_dis(self):
        T = np.array([1, 2, 3, 4, 5])
        y = []
        with codecs.open(r"E:\51job\data\salary_distribution.csv", "r", encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for i in range(5):
                    y.append(int(row[i]))
        #pprint(y)
        power = np.array(y)
        x1 = np.linspace(T.min(),T.max())
        smooth = spline(T, power, x1)
        plt.plot(x1, smooth)
        plt.plot(T, y, "og", label=u"工资分布数量")
        plt.xlabel(u'工资分布范围')
        plt.ylabel(u'工资分布数量')
        plt.xticks((1,2,3,4,5), (u'[0,1.0]万/月', u'[1.1,1.5]万/月', u'[1.6,2.0]万/月', u'[2.1,2.5]万/月', u'>2.5万/月'))
        for i in range(5):
            text(T[i]-0.05, y[i]-10, y[i], fontsize=12)
        plt.title(u'工资分布折线图')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    spider = JobSpider()
    spider.job_spider()
    #spider.post_require()
    spider.post_desc_counter()
    spider.post_salary_locate()
    spider.post_salary()
    spider.insert_into_db()
    spider.post_salary_counter()
    spider.post_counter()
    spider.employment_counter()
    spider.tech_counter()
    spider.tech_counter1()
    #spider.word_cloud()
    spider.locate()
    spider.locate1()
    #spider.locate_counter1()
    spider.post_counter_dis()
    spider.salary_distribution()
    spider.salary_distribution_dis()

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
