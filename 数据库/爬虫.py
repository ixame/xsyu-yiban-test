#coding:utf-8
# -*-coding:utf-8 -*-
#import cookielib
import urllib2
import urllib
import re
import MySQLdb   #支持Python和数据库的交换。
#import sys
#import smtplib                               
#from email.mime.text import MIMEText
#from email.header import Header
#import gzip
#import StringIO
import chardet
 
# class Employee:
 
   # def __init__(no, name, type, classname, teacher, stdCount, credits, Period, weekstate):
      # self.name = name
      # self.=
	  # self.=
	  # self.=
	  # self.=
	  # self.=
	  # self.=
	  # self.=
	  # self.=
 #写毛线的类 渣渣
 
url = 'http://jwxt.xsyu.edu.cn/eams/stdSyllabus!search.action'
#爬虫通过上述urlpost学期数据
#也可通过下面url以get方式访问
#http://jwxt.xsyu.edu.cn/eams/stdSyllabus!search.action?lesson.project.id=1&lesson.semester.id=45
postdata = urllib.urlencode({
            'lesson.project.id':'1',
			'lesson.semester.id':'45',
			'pageNo':'1',
			'pageSize':'500',
           })
#改变pageNo的值翻页
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'      
headers = { 'User-Agent' : user_agent }
request = urllib2.Request(url,postdata)
response=urllib2.urlopen(request)
r = response.read()
#print r

###########################################################################
lesson=re.findall('<tbody([\s\S]*?)</tbody>',r)
#抽取表格主体 所有行全部存在lesson[0]

alltr=re.findall('<tr>([\s\S]*?)</tr>',lesson[0])
#整理为每行 alltr[n]表示第n+1行

#tr=str(alltr[0]).decode('string_escape')
#每行整理 tr[i++]

alltr_len=len(alltr)
i=0
#此处加循环
while (i<alltr_len):
	td=re.findall('<td>([\s\S]*?)</td>',alltr[i])
	#对每行进行整理 包含10+1个元素  td[n]为n+1列

	name=re.findall('<a.*?href="[^"]*".*?>([\S\s]*?)</a>',td[1])
	value=re.findall('value="([\S\s]*?)"',alltr[i])
	td[1]=name[0]
	td.append(value[0])
	#特殊项目的处理 
	#	每行下标为1的元素进行二次处理
	#	提取id值并加入每行

	#处理前 ['A030216.06', '<a href="/eams/stdSyllabus!info.action?lesson.id=72376" onclick="return bg.Go(this,null)" title="查看任务详细信息">拳击</a>', '通识教育课', '年级:2017级,院系:计算机学院 化学化工学院', '李海林', '46', '46', '1', '24/2', '1-12']

	#处理后 ['A030216.06', '拳击', '通识教育课', '年级:2017级,院系:计算机学院 化学化工学院', '李海林', '46', '46', '1', '24/2', '1-12', '72376']

	alltr[i]=td
	#td整理结束 重新赋值回alltr 即双重list嵌套

	i=i+1
##########################################################################
jsobject=re.findall('Object([\s\S]*?)function',r)
#抽取jsobject主体 所有行全部存在jsobject[0]

#print alltr[0][10]
#print alltr[1][10]

allcontents=re.findall('contents([\s\S]*?);',jsobject[0])
#整理为每行 allcontents[n] 表示第n+1行

#此处加循环 对每行进行处理
i=0
allcontents_len=len(allcontents)
while (i<allcontents_len):
	everyline=re.findall('\'([\S\s]*?)\'',allcontents[i])
	#每行整理 包含两个元素 no 和 地点

	allcontents[i]=everyline
	#整理结束 重新赋值回alltr 即双重list嵌套

	i=i+1
#########################################################################
#两个双重list间比较id id相同则把address加入 补全完成
# len() 方法返回列表元素个数。
# len(list)
i=0
j=0
#此处加双重嵌套循环  
while (j<alltr_len):
    while (i<allcontents_len):
	#print "contents"+allcontents[i][0]
	#print alltr[j][10]
	#print "in"+str(j)
	if allcontents[i][0]==alltr[j][10]:
		alltr[j].append(allcontents[i][1])
	i=i+1	
    j=j+1
    i=0
    #print "out"+str(j)
    #print alltr[j][10]
#print alltr[1][10]
#print alltr[2][10]
decode=str(alltr[0]).decode('string_escape')
print "\nSample data:\n"+decode
print "\nThe chardet is "+str(chardet.detect(alltr[20][2])["encoding"])

print "\n\nTotal "+str(alltr_len)+" Group & "+str(allcontents_len)+" Addres Informatio\n\n"



conn= MySQLdb.connect(    
        #开始连接数据库 下面填写的是数据库的配置,账号密码,和将要被操作的数据表。
          host='localhost',
          port = 3306,
          user='yiban',
          passwd='Qq2017..',
          charset='utf8',
          db ='yiban',
           ) 
cur = conn.cursor()   
sqli="insert into Class_schedule values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

#示例数据：
#['A010001.04', '高等数学Ⅰ（1）', '学科基础课', '班级:石工(留学生EN)1801 地质(留学生EN)1801 营销(留学生EN)1801 土木(留学生EN)1801', '卢学飞', '49', '120', '5.5', '88/6', '1-10,13-17', '71575', '卢学飞 星期一 1-2 [1-10],[13-17]  2#806  <br>卢学飞 星期三 1-2 [1-10],[13-17]  2#806  <br>卢学飞 星期五 1-2 [1-10],[13-17]  2#806  ']
 

# print alltr[0][2]
# print type(alltr[0][2])
# print str(alltr[0][2])
# print type(str(alltr[0][2]))
i=0
while (i<alltr_len):
	print "The "+str(i+1)+" Working on it......"
	cur.execute(sqli,(alltr[i][0],alltr[i][1],alltr[i][2],alltr[i][3],alltr[i][4],int(alltr[i][5]),int(alltr[i][6]),float(alltr[i][7]),alltr[i][8],alltr[i][9],int(alltr[i][10]),alltr[i][11]))
	i=i+1
#数据库语句  将值插入数据库


cur.close()
conn.commit()                        
#将所有改动行入数据库中  Python去操作数据库必须要有这个过程的。
conn.close()                        
#关闭和数据库的链接

