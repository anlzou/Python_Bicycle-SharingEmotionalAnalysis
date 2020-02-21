def readData(path,File):
	fname = path + File
	F1 = open(fname, "r",encoding='utf-8')
	List_row = F1.readlines()

	list_source = []
	list_Pos = []
	list_Neg = []
	list_AvgPos = []
	list_AvgNeg = []
	list_StdPos = []
	list_StdNeg = []
	for i in range(1,len(List_row)):
		column_list = List_row[i].strip().split(" ")
		list_source.append(column_list)

		list_Pos.append(float(column_list[0]))
		list_Neg.append(float(column_list[1]))
		list_AvgPos.append(float(column_list[2]))
		list_AvgNeg.append(float(column_list[3]))
		list_StdPos.append(float(column_list[4]))
		list_StdNeg.append(float(column_list[5]))

	return list_source,list_Pos,list_Neg,list_AvgPos,list_AvgNeg,list_StdPos,list_StdNeg

list_source1,list_Pos1,list_Neg1,list_AvgPos1,list_AvgNeg1,list_StdPos1,list_StdNeg1 = readData('./data/','小黄车数据处理结果.txt')#
list_source2,list_Pos2,list_Neg2,list_AvgPos2,list_AvgNeg2,list_StdPos2,list_StdNeg2 = readData('./data/','小蓝车数据处理结果.txt')
list_source3,list_Pos3,list_Neg3,list_AvgPos3,list_AvgNeg3,list_StdPos3,list_StdNeg3 = readData('./data/','共享单车 - 副本数据处理结果.txt')


###以下数据求和处理
data1 = []   #保存积极分值, 消极分值，积极情感均值，消极情感均值，积极情感方差，消极情感方差，的各个和
data2 = []
data3 = []
#Pos求和
def sum_Pos(list_Pos):
	sum = 0
	for i in list_Pos:
		if int(i)>10000:
			continue
		sum += i
	return sum
data1.append(int(sum_Pos(list_Pos1)))
data2.append(int(sum_Pos(list_Pos2)))
data3.append(int(sum_Pos(list_Pos3)))


#Neg求和
def sum_Neg(list_Neg):
	sum = 0
	for i in list_Neg:
		if int(i)>10000:
			continue
		sum += i
	return sum
data1.append(int(sum_Neg(list_Neg1)))
data2.append(int(sum_Neg(list_Neg2)))
data3.append(int(sum_Neg(list_Neg3)))

#AvgPos求和
def sum_AvgPos(list_AvgPos):
	sum = 0
	for i in list_AvgPos:
		if int(i)>10000:
			continue
		sum += i
	return sum
data1.append(int(sum_AvgPos(list_AvgPos1)))
data2.append(int(sum_AvgPos(list_AvgPos2)))
data3.append(int(sum_AvgPos(list_AvgPos3)))

#AvgNeg求和
def sum_AvgNeg(list_AvgNeg):
	sum = 0
	for i in list_AvgNeg:
		if int(i)>10000:
			continue
		sum += i
	return sum
data1.append(int(sum_AvgNeg(list_AvgNeg1)))
data2.append(int(sum_AvgNeg(list_AvgNeg2)))
data3.append(int(sum_AvgNeg(list_AvgNeg3)))

#StdPos求和
def sum_StdPos(list_StdPos):
	sum = 0
	for i in list_StdPos:
		if int(i)>10000:
			continue
		sum += i
	return sum
data1.append(int(sum_StdPos(list_StdPos1)))
data2.append(int(sum_StdPos(list_StdPos2)))
data3.append(int(sum_StdPos(list_StdPos3)))

#StdNeg求和
def sum_StdNeg(list_StdNeg):
	sum = 0
	for i in list_StdNeg:
		if int(i)>10000:
			continue
		sum += i
	return sum
data1.append(int(sum_StdNeg(list_StdNeg1)))
data2.append(int(sum_StdNeg(list_StdNeg2)))
data3.append(int(sum_StdNeg(list_StdNeg3)))


import tkinter
import numpy  as np
import matplotlib.pyplot as plt

def dataGram1():
	plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

	plt.bar(range(len(data1)), data1, align='center', color='purple', alpha=0.5)
	plt.ylabel(u'分值')
	plt.title(u'小黄车数据图')
	plt.xticks(range(6), [u'积极分值',u'消极分值',u'积极均值',u'消极均值',u'积极方差',u'消极方差'])
	plt.ylim([100, 70000])
	for x, y in enumerate(data1):
		plt.text(x, y + 100, '%s' % round(y, 1), ha='center')
	plt.show()

def dataGram2():
	plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

	plt.bar(range(len(data2)), data2, align='center', color='purple', alpha=0.5)
	plt.ylabel(u'分值')
	plt.title(u'小蓝车数据图')
	plt.xticks(range(6), [u'积极分值',u'消极分值',u'积极均值',u'消极均值',u'积极方差',u'消极方差'])
	plt.ylim([100, 200000])
	for x, y in enumerate(data2):
		plt.text(x, y + 100, '%s' % round(y, 1), ha='center')
	plt.show()

def dataGram3():
	plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

	plt.bar(range(len(data3)), data3, align='center', color='purple', alpha=0.5)
	plt.ylabel(u'分值')
	plt.title(u'共享单车数据图')
	plt.xticks(range(6), [u'积极分值',u'消极分值',u'积极均值',u'消极均值',u'积极方差',u'消极方差'])
	plt.ylim([100, 300000])
	for x, y in enumerate(data3):
		plt.text(x, y + 100, '%s' % round(y, 1), ha='center')
	plt.show()



#主窗口
root = tkinter.Tk()
but1 = tkinter.Button(root,text = "小黄车数据图",command = dataGram1)
but2 = tkinter.Button(root,text = "小蓝车数据图",command = dataGram2)
but3 = tkinter.Button(root,text = "共享单车数据图",command = dataGram3)

but1.pack(side = 'left')
but2.pack(side = 'left')
but3.pack(side = 'left')
root.mainloop()
