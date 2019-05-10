# !/usr/bin/env python
# --------------------------------------------------------------
# File:          nsga2.py
# Project:       MOEA-D
# Created:       Sunday, 5th May 2019 1:09:30 am
# @Author:       molin@live.cn
# Last Modified: Sunday, 5th May 2019 1:09:36 am
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------
import sys, os
import plot, dataAnalysis

basePath = os.path.abspath(os.path.curdir)
#basePath = "/Users/meow/Desktop/DP/Code"

def batchJob():
	id = input("Which data:\t")
	N = input("Num of solutions:\t")
	MM = input("Num of MM:\t")
	iterations = input("Num of iterations:\t")
	num_batch = int(input("Num of batches:\t"))
	exefilePath = os.path.join(os.path.abspath(os.path.curdir), "NSGAII/nsga2.o")
	for i in range(num_batch):
		outPath = getOutPath(os.path.join(basePath, 'Output/NSGA-II'))
		nsga2_command = exefilePath + " " + str(id) + " " + outPath + " " + str(iterations) + " " + str(N) + " " + str(MM)
		os.mkdir(outPath)
		os.system(nsga2_command)


		config_file = open(os.path.join(outPath, 'config.txt'), 'w')
		config_file.write("File:\t%s\n"%str(id))
		config_file.write("Iterations:\t%s\n"%str(iterations))
		config_file.write("Population:\t%s\n"%str(N))
		config_file.write("MM:\t%s"%str(MM))
		config_file.close()
		plot.plotEP(outPath)
		dataAnalysis.analysisPF(outPath)
		
def getOutPath(outDir):
	outDirFiles = os.listdir(outDir)
	i = 0
	preFix = "Test"
	tempDirName = preFix + str(i)
	while tempDirName in outDirFiles:
		i+=1
		tempDirName = preFix + str(i)
	tempDirName = os.path.join(outDir, tempDirName)
	return tempDirName

def singleRun():
	outPath = getOutPath(os.path.join(basePath, 'Output/NSGA-II'))

	id = input("Which data:\t")
	N = input("Num of solutions:\t")
	MM = input("Num of MM:\t")
	iterations = input("Num of iterations:\t")
	exefilePath = os.path.join(os.path.abspath(os.path.curdir), "NSGAII/nsga2.o")
	nsga2_command = exefilePath + " " + str(id) + " " + outPath + " " + str(iterations) + " " + str(N) + " " + str(MM)
	os.mkdir(outPath)
	os.system(nsga2_command)


	config_file = open(os.path.join(outPath, 'config.txt'), 'w')
	config_file.write("File:\t%s\n"%str(id))
	config_file.write("Iterations:\t%s\n"%str(iterations))
	config_file.write("Population:\t%s\n"%str(N))
	config_file.write("MM:\t%s\n"%str(MM))
	config_file.close()

	plot.plotEP(outPath)
if __name__ == "__main__":
	batchJob()