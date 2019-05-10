# !/usr/bin/env python
# --------------------------------------------------------------
# File:          testFlight.py
# Project:       Code
# Created:       Friday, 3rd May 2019 10:56:10 am
# @Author:       molin@live.cn
# Last Modified: Friday, 3rd May 2019 10:56:32 am
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------

import os, sys
import fileinput
import dataAnalysis
import pandas as pd
import numpy as np
import time
import plot
inPath = "/Users/meow/Desktop/DP/Code/Output/MOEA-D/Test28/EP.txt"

def formatConfig(outPath):
	for algorithmType in os.listdir(outPath):
		if not os.path.isdir(os.path.join(outPath, algorithmType)):
			continue
		for testFolder in os.listdir(os.path.join(outPath, algorithmType)):
			tempPath = os.path.join(os.path.join(outPath, algorithmType), testFolder)
			#print("Processing:%s"%tempPath)
			tempPath = os.path.join(tempPath, "EP.txt")
			if not os.path.exists(tempPath):
				continue

#print(inPath[:-4])

def deleteHV(inPath):
	
	print(inPath)
	i = 0
	addList=[]
	for line in fileinput.input(inPath):
		if i < 5:
			addList.append(line)
			i+=1
		else:
			fileinput.close()
			break
	f = open(inPath, 'w')
	for line in addList:
		f.write(line)

def deleteHVOP(inPath):
	for folder in os.listdir(inPath):
		if folder[0]=='.':
			continue
		tempConfig = os.path.join(inPath, folder)
		Config = os.path.join(tempConfig, 'config.txt')
		if not os.path.exists(tempConfig):
			continue
		deleteHV(Config)
def hvOp(inPath):
	for folder in os.listdir(inPath):
		if folder[0]=='.':
			continue
		tempConfig = os.path.join(inPath, folder)
		Config = os.path.join(tempConfig, 'config.txt')
		if not os.path.exists(tempConfig):
			continue
		dataAnalysis.analysisPF(tempConfig)
		

#hvOp("/Users/meow/Desktop/DP/MOEA-D/Output/NSGA-II")

def formatResource(inPath):
	data = pd.read_csv(inPath, sep='\t')
	outPath = inPath[:-4]+'_risk.txt'
	data.sort_values(by='Risk', ascending=False).to_csv(outPath, sep='\t', index=False)
#formatResource("/Users/meow/Desktop/DP/MOEA-D/Resource/10000.csv")
start_s1 = time.time()
print("[Start]\tCollecting Pareto Front")
#dataAnalysis.epochValue("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test110/EP_epoch.txt")
#plot.mat_plotLine("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test110/EP_epoch_record.csv")
dataAnalysis.analysisPF("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test91")
end_s1 = time.time()
print("[End]\t%s"%(end_s1-start_s1))