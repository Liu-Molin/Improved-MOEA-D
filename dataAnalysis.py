# !/usr/bin/env python
# --------------------------------------------------------------
# File:          dataAnalysis.py
# Project:       Code
# Created:       Saturday, 4th May 2019 9:47:02 pm
# @Author:       molin@live.cn
# Last Modified: Saturday, 4th May 2019 9:47:05 pm
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------

import os, sys, fileinput, time, math
import plot, utilis
import pandas as pd
import tqdm

import multiprocessing
z_risk = 0.0
z_income =0.0
ParetoFront = []

pbar = None
def callback_tqdm(*v):
	pbar.update()
class Point:
	def __init__(self, line):
		line = line.strip()
		line = line.split('\t')
		self.risk = float(line[0])
		self.income = float(line[1])
		if len(line)==3:
			self.epoch = float(line[2])
	def __str__(self):
		return str(str(self.risk)+"\t"+str(self.income))
	def __repr__(self):
		return str(str(self.risk)+"\t"+str(self.income))
	def __eq__(self, other):
		return (self.risk==other.risk)and(self.income==other.income)
	def __hash__(self):
		return hash(('risk', self.risk, 'income', self.income))

class PF:
	def __init__(self, EP):
		self.EP = EP
def loadEP(inPath):
	EP_set = set()
	if not os.path.exists(inPath):
		print("File Not Exists:\t%s"%inPath)
		pass
	EP = []
	for line in fileinput.input(inPath):
		tempPoint = Point(line)
		if tempPoint not in EP_set:
			EP_set.add(tempPoint)
			EP.append(tempPoint)
	fileinput.close()
	return EP

def loadEP_epoch(inPath):
	if not os.path.exists(inPath):
		print("File Not Exists:\t%s"%inPath)
		pass
	EP = []
	for line in fileinput.input(inPath):
		tempPoint = Point(line)
		EP.append(tempPoint)
	fileinput.close()
	return EP
def removeDuplicate(EP):
	EP_set = set()
	temp_EP=[]
	for item in EP:
		if item not in EP_set:
			EP_set.add(item)
			temp_EP.append(item)
	return temp_EP

def dominate(p1, p2):
	if p1.risk<=p2.risk:
		if p1.income>p2.income:
			return True
	return False

def insertPoint(EP, index, tempPoint):
	EP.pop(index)
	EP.insert(index, tempPoint)
	if index>0 and index < len(EP)-1:
		while(EP[index+1].income<tempPoint.income):
			EP.pop(index+1)
			if len(EP)<index+2:
				break
def getPF(EP, tempEP):
	for i in range(len(tempEP)):
		appendFlag = True
		insertList = []
		for j in range(len(EP)):
			if tempEP[i].risk>EP[j].risk:
				continue
			else:
				appendFlag = False
				if tempEP[i].income>EP[j].risk:
					insertList.append([j, tempEP[i]])
		for i in range(len(insertList)):
			insertPoint(EP, insertList[i][0]-i, insertList[i][1])
		if appendFlag:
			EP.append(tempEP[i])
	return EP

def getPFv2(EP, tempEP):
	for i in range(len(tempEP)):
		isAppend = True
		for item in EP:
			if item==tempEP[i]:
				isAppend = False
				break
			if dominate(tempEP[i], item):
				EP.remove(item)
			if dominate(item, tempEP[i]):
				isAppend = False
				break
		if isAppend:
			EP.append(tempEP[i])
	return EP
def to_csv(outPath, EP):
	outFile = open(outPath, 'w')
	for i in range(len(EP)):
		outFile.write(str(EP[i].risk)+'\t'+ str(EP[i].income) +'\n')
	outFile.close()
def collectPF(outputPath):
	EP = loadEP(getLatestPF())
	for algorithmType in os.listdir(outputPath):
		if not os.path.isdir(os.path.join(outputPath, algorithmType)):
			continue
		for testFolder in os.listdir(os.path.join(outputPath, algorithmType)):
			tempPath = os.path.join(os.path.join(outputPath, algorithmType), testFolder)
			#print("Processing:%s"%tempPath)
			tempPath = os.path.join(tempPath, "EP.txt")
			if not os.path.exists(tempPath): 
				continue
			if EP == []:
				EP = loadEP(tempPath)
				EP.sort(key=lambda x:x.risk)
				continue
			tempEP = loadEP(tempPath)
			EP = getPFv2(EP, tempEP)

	print("\tNum of points:\t%d"%len(EP))
	EP.sort(key=lambda x:x.risk)
	EP = getPFv2(EP, EP)
	EP = removeDuplicate(EP)
	EP.sort(key=lambda x:x.risk)
	return EP

def formatPlot(inPath):
	EP = loadEP(inPath)
	EP.sort(key=lambda x:x.risk)
	EP = convert2min(EP)
	outPath = inPath[:-4] +"_conv.txt"
	to_csv(outPath, EP)
	plot.plotPoints(outPath, 120, 12)

def formatPlot_Test(inPath):
	EP = loadEP(inPath)
	EP.sort(key=lambda x:x.risk)
	PF_EP = loadEP(getLatestPF())
	z_risk = PF_EP[0].risk
	z_income = PF_EP[-1].income
	for i in range(len(EP)):
		EP[i].risk = EP[i].risk-z_risk
		EP[i].income = z_income-EP[i].income

	outPath = inPath[:-4] +"_conv.txt"
	to_csv(outPath, EP)
	plot.mat_plotEP_PF(outPath)
def getLatestZ():
	outPath = "/Users/meow/Desktop/DP/MOEA-D/Output/PF"
	PFPath = utilis.getLatest(outPath, "PF")
	zPath = os.path.join(PFPath, "z.txt")
	value = None
	for line in fileinput.input(zPath):
		line = line.split('\t')
		value = (float(line[0]), float(line[1]))
	return value

def getLatestPF():
	outPath = "/Users/meow/Desktop/DP/MOEA-D/Output/PF"
	PFPath = utilis.getLatest(outPath, "PF")
	PFPath = os.path.join(PFPath, "PF.txt")
	return PFPath
def getTestInfo(inPath):
	if not os.path.exists(inPath):
		raise Exception("Config file not exists.\n\t%s"%inPath)
	for line in fileinput.input(inPath):
		pass

def convert2min(EP):
	EP.sort(key=lambda x:x.risk)
	z_risk = EP[0].risk
	z_income = EP[-1].income
	for i in range(len(EP)):
		EP[i].risk = EP[i].risk-z_risk
		EP[i].income = z_income-EP[i].income
	return EP
def calEpoch_HV(EP):
	global z_risk
	global z_income
	EP.sort(key=lambda x:x.risk)
	hv = 0.0
	for i in range(len(EP)):
		widght = z_risk-EP[i].risk
		if i == 0:
			height = EP[i].income - z_income
		else:
			height = EP[i].income - EP[i-1].income
		hv += float(height)*float(widght)
	return hv
def calEP_HV(tempEP, z_risk, z_income, start_index, end_index):
	hv = 0.0
	EP = tempEP[start_index:end_index]
	EP.sort(key=lambda x:x.risk)
	for i in range(end_index-start_index):
		try:
			widght = z_risk-EP[i].risk
		except:
			print("Len EP:"+str(len(EP)))
			EP = tempEP[start_index:end_index]
			print("Len tempEP:"+str(len(tempEP)))
			print("Start:"+str(start_index))
			print("End:"+str(end_index))
			print(str(i)+'\t'+str(end_index-start_index))
			exit
		if i == 0:
			height = EP[i].income - z_income
		else:
			height = EP[i].income - EP[i-1].income
		hv += float(height)*float(widght)
	return hv
def calHV(inPath):
	PF = loadEP(getLatestPF())
	PF.sort(key=lambda x:x.risk)
	z_risk = PF[-1].risk
	z_income = PF[0].income
	hv = 0.0
	EP = loadEP(inPath)
	EP.sort(key=lambda x:x.risk)
	for i in range(len(EP)):
		widght = z_risk-EP[i].risk
		if i == 0:
			height = EP[i].income - z_income
		else:
			height = EP[i].income - EP[i-1].income
		hv += float(height)*float(widght)
	print("Hypervolume:\t%s"%str(hv))
	inPath = os.path.dirname(inPath)
	addConfig(inPath, "Hypervolume", hv)

def cal_Distance(x, y):
	return math.sqrt(math.pow((x.risk-y.risk), 2)+math.pow((x.income-y.income), 2))
def calEpoch_D(EP):
	global ParetoFront
	PF = ParetoFront
	sum_minD = 0.0
	for item in PF:
		minD = cal_Distance(item, EP[0])
		for subItem in EP:
			temp_minD = cal_Distance(item, subItem)
			if temp_minD<minD:
				minD = temp_minD
		sum_minD+=minD
	D_metric = float(sum_minD)/float(len(EP))
	return D_metric
def calEP_D(tempEP, start_index, end_index):
	global ParetoFront
	PF = ParetoFront
	sum_minD = 0.0
	EP = tempEP[start_index:end_index]
	for item in PF:
		minD = cal_Distance(item, EP[0])
		for i in range(len(EP)):
			temp_minD = cal_Distance(item, EP[i])
			if temp_minD<minD:
				minD = temp_minD
		sum_minD+=minD
	D_metric = float(sum_minD)/float(len(EP))
	return D_metric
def cal_D_Metric(inPath):
	EP = loadEP(getLatestPF())
	Test_EP = loadEP(inPath)
	sum_minD = 0.0
	for item in EP:
		minD = cal_Distance(item, Test_EP[0])
		for subItem in Test_EP:
			temp_minD = cal_Distance(item, subItem)
			if temp_minD<minD:
				minD = temp_minD
		sum_minD+=minD
	D_metric = float(sum_minD)/float(len(EP))
	inPath = os.path.dirname(inPath)
	addConfig(inPath, "D-mectric", D_metric)
def addConfig(inPath, tag, value):
	config = open(os.path.join(inPath, 'config.txt'), 'a')
	config.write("\n"+tag+":\t"+str(value))
	config.close()
def epochValue_epoch(inPath):
	global ParetoFront
	EP = loadEP_epoch(inPath)
	print("Num of points:\t"+str(len(EP)))
	epochRecord = pd.DataFrame()
	ParetoFront = loadEP(getLatestPF())
	z_risk = ParetoFront[-1].risk
	z_income = ParetoFront[0].income

	HV_list = []
	D_metric_list = []

	gen = []
	tempP = []
	sliceStart = []
	sliceEnd = []
	sliceStart.append(0)
	tempP.append(EP[0])
	for i in range(len(EP)):
		if i != 0:
			if EP[i].epoch==EP[i-1].epoch:
				tempP.append(EP[i])
			else:
				sliceEnd.append(i)
				sliceStart.append(i)
				gen.append(int(EP[i-1].epoch))
				tempP.append(EP[i])
				tempP.clear()
	sliceEnd.append(len(EP))
	gen.append(int(EP[-1].epoch))
	p=multiprocessing.Pool(os.cpu_count())
	for i in range(len(sliceEnd)):
		#print(len(i))
		HV = p.apply_async(calEP_HV, args=(EP, z_risk, z_income, sliceStart[i], sliceEnd[i]))
		D_metric = p.apply_async(calEP_D, args=(EP, sliceStart[i], sliceEnd[i]))
		HV_list.append(HV)
		D_metric_list.append(D_metric)

	for i in range(len(D_metric_list)):
		D_metric_list[i] = D_metric_list[i].get()
		HV_list[i] = HV_list[i].get()
	p.close()
	p.join()
	epochRecord["Generation"] = gen
	epochRecord["HV"] = HV_list
	epochRecord["D-metric"] = D_metric_list
	filename = inPath[:-4]+'_record_epoch.csv'
	epochRecord.to_csv(filename, sep='\t')
	plot.mat_plotLine(filename)


def epochValue(inPath):
	global pbar
	global ParetoFront

	EP = loadEP_epoch(inPath)
	print(len(EP))
	epochRecord = pd.DataFrame()
	ParetoFront = loadEP(getLatestPF())
	z_risk = ParetoFront[-1].risk
	z_income = ParetoFront[0].income

	HV_list = []
	D_metric_list = []

	gen = []
	tempP = []
	sliceI = []
	tempP.append(EP[0])
	for i in range(len(EP)):
		if i != 0:
			if EP[i].epoch==EP[i-1].epoch:
				tempP.append(EP[i])
			else:
				#tempHV = calEP_HV(tempP, z_risk, z_income)
				#tempDM = calEP_D(tempP, PF)
				#HV_list.append(tempHV)
				#D_metric_list.append(tempDM)
				gen.append(int(EP[i-1].epoch))
				tempP.append(EP[i])
				sliceI.append(i)
	
	sliceI.append(len(EP))
	gen.append(int(EP[-1].epoch))
	print(len(gen))
	pbar=tqdm.tqdm(total=len(sliceI))
	p=multiprocessing.Pool(os.cpu_count())
	for i in range(len(sliceI)):
		#print(len(i))
		HV = p.apply_async(calEP_HV, args=(tempP, z_risk, z_income, 0, int(sliceI[i])), callback=callback_tqdm)
		D_metric = p.apply_async(calEP_D, args=(tempP, 0, int(sliceI[i])))
		HV_list.append(HV)
		D_metric_list.append(D_metric)

	for i in range(len(D_metric_list)):
		D_metric_list[i] = D_metric_list[i].get()
		HV_list[i] = HV_list[i].get()
	p.close()
	p.join()
	#for i in HV_list:
		#print(i.get())
	
	epochRecord["Generation"] = gen
	epochRecord["HV"] = HV_list
	epochRecord["D-metric"] = D_metric_list
	filename = inPath[:-4]+'_record.csv'
	print(filename)
	epochRecord.to_csv(filename, sep='\t')
	plot.mat_plotLine(filename)
def readConfig(inPath):
	
	exp_record = pd.DataFrame()
	algs_type = inPath.split('/')[-2]
	exp_record['Test No.'] = [algs_type[4:]]
	for line in fileinput.input(inPath):
		if len(line)>2:
			line = line.strip()
			line = line.split('\t')
			exp_record[line[0][:-1]]=[line[1]]
	return exp_record

def analysisPF(inPath):
	'''
	inPath: folder
	'''
	algs_type = inPath.split('/')[-2]
	formatPlot_Test(inPath+'/EP.txt')
	calHV(inPath+'/EP_conv.txt') 
	cal_D_Metric(inPath+'/EP_conv.txt')
	exp_record = readConfig(inPath+'/config.txt')
	ANALYSIS_PATH = "/Users/meow/Desktop/DP/MOEA-D/Analysis"
	report_name = ANALYSIS_PATH+'/%s_report.csv'%algs_type
	if os.path.exists(report_name):
		exp_record.to_csv(report_name , header=False, mode='a')
	else:
		exp_record.to_csv(report_name)
	#epochValue_epoch(inPath)


if __name__ == "__main__":
	start_s1 = time.time()
	print("[Start]\tCollecting Pareto Front")
	
	basePath = os.path.curdir
	outPath = os.path.join(basePath, "Output")
	outPF = collectPF(outPath)
	outPath = utilis.getOutPath(os.path.join(outPath, "PF"), "PF")
	os.mkdir(outPath)
	outPF_file = os.path.join(outPath, "PF.txt")

	to_csv(outPF_file, outPF)
	outZ = open(os.path.join(outPath, "z.txt"), 'w')
	outZ.write(str(outPF[0].risk)+"\t"+str(outPF[-1].income))
	outZ.close()
	
	plot.plotPoints(outPF_file, 120, 15)
	formatPlot(outPF_file)
	end_s1 = time.time()
	print("[End]\t%s"%(end_s1-start_s1))
	'''
	#analysisPF("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test35")
	epochValue("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test83")
	
	

'''