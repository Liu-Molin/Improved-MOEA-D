# !/usr/bin/env python
# --------------------------------------------------------------
# File:          dataAnalysis.py
# Project:       Code
# Created:       Saturday, 4th May 2019 6:36:33 pm
# @Author:       molin@live.cn
# Last Modified: Saturday, 4th May 2019 6:36:35 pm
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------

import os, sys, fileinput
import pandas as pd
import numpy as np
PATH_output = "/Users/meow/Desktop/DP/Code/Output"

def loadEP(inPath):
	data = pd.read_csv(inPath, sep='\t', header=None, names=['Risk', 'Income'])
	return data

def dominate(x, y):
	if float(x['Risk'])<=float(y['Risk']):
		if float(x['Income'])>=float(y['Income']):
			return True
	return False

def getPF(inPath, EP):
	tempEP = loadEP(inPath)
	dropList = []
	for i in range(len(tempEP.index)):
		addFlag = True
		for j in range(len(EP.index)):
			if dominate(EP.iloc[j], tempEP.iloc[i]):
				#print(EP.iloc[j])
				#print(tempEP.iloc[i])
				addFlag = False
				dropList.append(i)
				break
	indexes_to_keep = set(range(tempEP.shape[0])) - set(dropList)
	tempEP_sliced = tempEP.take(list(indexes_to_keep))
	#print(len(tempEP.index))
	#print(len(tempEP_sliced.index))
	#tempEP.drop(tempEP.index[dropList], inplace=True)
	EP = EP.append(tempEP_sliced,  ignore_index=True)

def collectPF(outputPath):
	EP = pd.DataFrame()
	for algorithmType in os.listdir(outputPath):
		if not os.path.isdir(os.path.join(outputPath, algorithmType)):
			continue
		for testFolder in os.listdir(os.path.join(outputPath, algorithmType)):
			tempPath = os.path.join(os.path.join(outputPath, algorithmType), testFolder)
			#print("Processing:%s"%tempPath)
			tempPath = os.path.join(tempPath, "EP.txt")
			if not os.path.exists(tempPath):
				continue
			#if type(EP)!=
			if EP.empty:
				EP = loadEP(tempPath)
				continue
			tempEP = loadEP(tempPath)
			dropList = []
			for i in range(len(tempEP.index)):
				addFlag = True
				for j in range(len(EP.index)):
					if dominate(EP.iloc[j], tempEP.iloc[i]):
						addFlag = False
						dropList.append(i)
						break
			indexes_to_keep = set(range(tempEP.shape[0])) - set(dropList)
			tempEP_sliced = tempEP.take(list(indexes_to_keep))
			#tempEP.drop(tempEP.index[dropList], inplace=True)
			EP = EP.append(tempEP_sliced,  ignore_index=True)
			print(len(EP.index))
	outputPath = os.path.join(outputPath, 'PF.txt')
	EP.to_csv(outputPath, sep='\t', index = False)
	

if __name__ == "__main__":
	#loadEP("/Users/meow/Desktop/DP/Code/Output/MOEA-D/Test29/EP.txt")
	collectPF("/Users/meow/Desktop/DP/Code/Output")
	'''
	t1 = loadEP("/Users/meow/Desktop/DP/Code/Output/test1.txt")
	t2 = loadEP("/Users/meow/Desktop/DP/Code/Output/test2.txt")
	getPF("/Users/meow/Desktop/DP/Code/Output/test2.txt", t1)
	'''