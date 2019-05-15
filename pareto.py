# !/usr/bin/env python
# --------------------------------------------------------------
# File:          pareto.py
# Project:       MOEA-D
# Created:       Thursday, 9th May 2019 2:26:20 pm
# @Author:       molin@live.cn
# Last Modified: Thursday, 9th May 2019 2:26:25 pm
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------
import os, sys, time
import dataAnalysis, utilis, plot

if __name__ == "__main__":
	start_s1 = time.time()
	print("[Start]\tCollecting Pareto Front")
	
	basePath = os.path.curdir
	outPath = os.path.join(basePath, "Output")
	outPF = dataAnalysis.collectPF(outPath)
	outPath = utilis.getOutPath("/home/lusso/Documents/MOEA-D/Resource/PF", "PF")
	os.mkdir(outPath)
	outPF_file = os.path.join(outPath, "PF.txt")

	dataAnalysis.to_csv(outPF_file, outPF)
	outZ = open(os.path.join(outPath, "z.txt"), 'w')
	outZ.write(str(outPF[0].risk)+"\t"+str(outPF[-1].income))
	outZ.close()
	
	plot.plotPoints(outPF_file, 120, 15)
	#dataAnalysis.formatPlot(outPF_file)
	end_s1 = time.time()
	print("[End]\t%s"%(end_s1-start_s1))