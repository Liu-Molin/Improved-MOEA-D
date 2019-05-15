# !/usr/bin/env python
# --------------------------------------------------------------
# File:          moead.py
# Project:       Code
# Created:       Tuesday, 9th April 2019 4:34:48 pm
# @Author:       molin@live.cn
# Last Modified: Saturday, 4th May 2019 6:21:46 pm
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------

import sys, os
import plot, dataAnalysis
import utilis
import multiprocessing
basePath = os.path.abspath(os.path.curdir)
#basePath = "/Users/meow/Desktop/DP/Code"
def batchJob(id, N, T, iterations, mix_percentage, outPath):
	moead_command = ("./portfolio.o" + " " + 
					outPath + " " +
					str(id) + " " + 
					str(N) + " " + 
					str(T) + " " + 
					str(iterations) +" "
					+ str(mix_percentage)
					)
	#print(moead_command)
	os.system(moead_command)
	config_file = open(os.path.join(outPath, 'config.txt'), 'w')
	config_file.write("File:\t%s\n"%str(id))
	config_file.write("Iterations:\t%s\n"%str(iterations))
	config_file.write("Population:\t%s\n"%str(N))
	config_file.write("Neighbor:\t%s\n"%str(T))
	config_file.write("Percentage:\t%s%%"%str(float(mix_percentage)*100))
	config_file.close()
	#plot.plotMOEAD(outPath)
	#dataAnalysis.analysisPF(outPath)
	#dataAnalysis.formatPlot_Test(outPath+'/EP.txt') 
if __name__ == "__main__":
	#singleRun()
	id = input("Which data:\t")
	N = input("Num of solutions:\t")
	T = input("Num of neighbors:\t")
	N = N.strip().split()
	T = T.strip().split()
	iterations = input("Num of iterations:\t")
	mix_percentage = input("Low assets %:\t")
	
	if len(N)>len(T):
		num_batch = len(N)
		for i in range(num_batch):
			batchJob(id, N[i], T[0], iterations, mix_percentage)
	else:
		for i in range(len(T)):
			batchJob(id, N[0], T[i], iterations, mix_percentage)