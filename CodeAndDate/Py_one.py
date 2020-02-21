import xlrd
from xlutils.copy import copy
def readExcel(path,File,col):    #从excel中提取评论数据保存到txt；只支持读取'.xlsx'后缀文件
	fname = path + File
	filename = xlrd.open_workbook(fname)
	sheet = filename.sheets()[0]
	nrows = sheet.nrows-1
	File = File.replace(".xlsx", "数据提取.txt")
	path_txt = path + File
	file = open(path_txt, "w", encoding="utf-8")
	file.write('评论数据(行|人)：' + str(nrows) + '\n')
	for i in range(1,nrows):
		cell_value = sheet.cell_value(i, col)
		file.write(str(cell_value)+'\n')
	print(File, "ok")
	file.close()

readExcel('./data/','小黄车.xlsx',2)
readExcel('./data/','小蓝车.xlsx',2)
readExcel('./data/',"共享单车 - 副本.xlsx",1)



import jieba
import numpy as np
#打开词典文件，返回列表
def open_dict(Dict = 'name', path=r'./data/字典/'):
    path = path + '%s.txt' % Dict
    dictionary = open(path, 'r',encoding="utf-8")
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        dict.append(word)
    return dict


def judgeodd(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'


#path路径为相对路径。
deny_word = open_dict(Dict = '否定词', path= r'./data/字典/')
posdict = open_dict(Dict = 'positive', path= r'./data/字典/')
negdict = open_dict(Dict = 'negative', path= r'./data/字典/')

degree_word = open_dict(Dict = '程度级别词语', path= r'./data/字典/')
mostdict = degree_word[degree_word.index('extreme')+1 : degree_word.index('very')]#权重4，即在情感词前乘以4
verydict = degree_word[degree_word.index('very')+1 : degree_word.index('more')]#权重3
moredict = degree_word[degree_word.index('more')+1 : degree_word.index('ish')]#权重2
ishdict = degree_word[degree_word.index('ish')+1 : degree_word.index('last')]#权重0.5



def sentiment_score_list(dataset):
    seg_sentence = dataset.split('。')

    count1 = []
    count2 = []
    for sen in seg_sentence: #循环遍历每一个评论
        segtmp = jieba.lcut(sen, cut_all=False)  #把句子进行分词，以列表的形式返回
        i = 0 #记录扫描到的词的位置
        a = 0 #记录情感词的位置
        poscount = 0 #积极词的第一次分值
        poscount2 = 0 #积极词反转后的分值
        poscount3 = 0 #积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word in posdict:  # 判断词语是否是情感词
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w in mostdict:
                        poscount *= 4.0
                    elif w in verydict:
                        poscount *= 3.0
                    elif w in moredict:
                        poscount *= 2.0
                    elif w in ishdict:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化

            elif word in negdict:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in degree_word:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '！' or word == '!':  ##判断句子是否有感叹号
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1 # 扫描词位置前移


            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []

    return count2

def sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        AvgPos = np.mean(score_array[:, 0])
        AvgPos = float('%.1f'%AvgPos)
        AvgNeg = np.mean(score_array[:, 1])
        AvgNeg = float('%.1f'%AvgNeg)
        StdPos = np.std(score_array[:, 0])
        StdPos = float('%.1f'%StdPos)
        StdNeg = np.std(score_array[:, 1])
        StdNeg = float('%.1f'%StdNeg)
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])    #[积极分值, 消极分值，积极情感均值，消极情感均值，积极情感方差，消极情感方差]
    return score[0]



def readText(path,File): #从评论数据文件txt提取数据处理后保存到新的txt
	fname = path + File
	file = open(fname, "r",encoding="utf-8")
	readlines = file.readlines()
	File = File.replace("数据提取.txt", "数据处理结果.txt")
	path_txt = path + File
	filewrite = open(path_txt, "w", encoding="utf-8")

	i = 1
	for line in readlines:
		line_one = line
		line = line.replace('。','，')    #每条数据不留’。‘
		line = line.replace('\n','匹配符。匹配符')   #末尾加’。‘
		if i == 1:
			nrow = line_one[line_one.find("：")+1:len(line_one)].rstrip("\n")
			print(nrow)
			filewrite.write(line_one)
			i = i + 1
			continue
		data = sentiment_score(sentiment_score_list(line))

		s = str(data).replace('[', '').replace(']','')  # 去除[],这两行按数据不同，可以选择
		s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
		filewrite.write(s)
		i = i + 1
	print(File,"ok")

readText('./data/','小黄车数据提取.txt')
readText('./data/','小蓝车数据提取.txt')
readText('./data/','共享单车 - 副本数据提取.txt')
