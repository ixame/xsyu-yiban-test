#coding:utf-8
# -*-coding:utf-8 -*-
#import cookielib
import urllib2
import urllib
import re
import MySQLdb   #֧��Python�����ݿ�Ľ�����
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
 #дë�ߵ��� ����
 
url = 'http://jwxt.xsyu.edu.cn/eams/stdSyllabus!search.action'
#����ͨ������urlpostѧ������
#Ҳ��ͨ������url��get��ʽ����
#http://jwxt.xsyu.edu.cn/eams/stdSyllabus!search.action?lesson.project.id=1&lesson.semester.id=45
postdata = urllib.urlencode({
            'lesson.project.id':'1',
			'lesson.semester.id':'45',
			'pageNo':'1',
			'pageSize':'500',
           })
#�ı�pageNo��ֵ��ҳ
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'      
headers = { 'User-Agent' : user_agent }
request = urllib2.Request(url,postdata)
response=urllib2.urlopen(request)
r = response.read()
#print r

###########################################################################
lesson=re.findall('<tbody([\s\S]*?)</tbody>',r)
#��ȡ������� ������ȫ������lesson[0]

alltr=re.findall('<tr>([\s\S]*?)</tr>',lesson[0])
#����Ϊÿ�� alltr[n]��ʾ��n+1��

#tr=str(alltr[0]).decode('string_escape')
#ÿ������ tr[i++]

alltr_len=len(alltr)
i=0
#�˴���ѭ��
while (i<alltr_len):
	td=re.findall('<td>([\s\S]*?)</td>',alltr[i])
	#��ÿ�н������� ����10+1��Ԫ��  td[n]Ϊn+1��

	name=re.findall('<a.*?href="[^"]*".*?>([\S\s]*?)</a>',td[1])
	value=re.findall('value="([\S\s]*?)"',alltr[i])
	td[1]=name[0]
	td.append(value[0])
	#������Ŀ�Ĵ��� 
	#	ÿ���±�Ϊ1��Ԫ�ؽ��ж��δ���
	#	��ȡidֵ������ÿ��

	#����ǰ ['A030216.06', '<a href="/eams/stdSyllabus!info.action?lesson.id=72376" onclick="return bg.Go(this,null)" title="�鿴������ϸ��Ϣ">ȭ��</a>', 'ͨʶ������', '�꼶:2017��,Ժϵ:�����ѧԺ ��ѧ����ѧԺ', '���', '46', '46', '1', '24/2', '1-12']

	#����� ['A030216.06', 'ȭ��', 'ͨʶ������', '�꼶:2017��,Ժϵ:�����ѧԺ ��ѧ����ѧԺ', '���', '46', '46', '1', '24/2', '1-12', '72376']

	alltr[i]=td
	#td������� ���¸�ֵ��alltr ��˫��listǶ��

	i=i+1
##########################################################################
jsobject=re.findall('Object([\s\S]*?)function',r)
#��ȡjsobject���� ������ȫ������jsobject[0]

#print alltr[0][10]
#print alltr[1][10]

allcontents=re.findall('contents([\s\S]*?);',jsobject[0])
#����Ϊÿ�� allcontents[n] ��ʾ��n+1��

#�˴���ѭ�� ��ÿ�н��д���
i=0
allcontents_len=len(allcontents)
while (i<allcontents_len):
	everyline=re.findall('\'([\S\s]*?)\'',allcontents[i])
	#ÿ������ ��������Ԫ�� no �� �ص�

	allcontents[i]=everyline
	#������� ���¸�ֵ��alltr ��˫��listǶ��

	i=i+1
#########################################################################
#����˫��list��Ƚ�id id��ͬ���address���� ��ȫ���
# len() ���������б�Ԫ�ظ�����
# len(list)
i=0
j=0
#�˴���˫��Ƕ��ѭ��  
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
        #��ʼ�������ݿ� ������д�������ݿ������,�˺�����,�ͽ�Ҫ�����������ݱ�
          host='localhost',
          port = 3306,
          user='yiban',
          passwd='Qq2017..',
          charset='utf8',
          db ='yiban',
           ) 
cur = conn.cursor()   
sqli="insert into Class_schedule values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

#ʾ�����ݣ�
#['A010001.04', '�ߵ���ѧ��1��', 'ѧ�ƻ�����', '�༶:ʯ��(��ѧ��EN)1801 ����(��ѧ��EN)1801 Ӫ��(��ѧ��EN)1801 ��ľ(��ѧ��EN)1801', '¬ѧ��', '49', '120', '5.5', '88/6', '1-10,13-17', '71575', '¬ѧ�� ����һ 1-2 [1-10],[13-17]  2#806  <br>¬ѧ�� ������ 1-2 [1-10],[13-17]  2#806  <br>¬ѧ�� ������ 1-2 [1-10],[13-17]  2#806  ']
 

# print alltr[0][2]
# print type(alltr[0][2])
# print str(alltr[0][2])
# print type(str(alltr[0][2]))
i=0
while (i<alltr_len):
	print "The "+str(i+1)+" Working on it......"
	cur.execute(sqli,(alltr[i][0],alltr[i][1],alltr[i][2],alltr[i][3],alltr[i][4],int(alltr[i][5]),int(alltr[i][6]),float(alltr[i][7]),alltr[i][8],alltr[i][9],int(alltr[i][10]),alltr[i][11]))
	i=i+1
#���ݿ����  ��ֵ�������ݿ�


cur.close()
conn.commit()                        
#�����иĶ��������ݿ���  Pythonȥ�������ݿ����Ҫ��������̵ġ�
conn.close()                        
#�رպ����ݿ������

