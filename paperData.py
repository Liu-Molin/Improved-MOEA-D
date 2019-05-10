# !/usr/bin/env python
# --------------------------------------------------------------
# File:          paperData.py
# Project:       MOEA-D
# Created:       Thursday, 9th May 2019 3:06:25 pm
# @Author:       molin@live.cn
# Last Modified: Thursday, 9th May 2019 3:06:27 pm
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------
import os, sys, fileinput, time, math, tqdm
import plot, utilis

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import pandas as pd
import matplotlib
import dataAnalysis as da
import matplotlib.font_manager as fm
import multiprocessing

def plotHV(inPath1, inPath2):
	data1 = pd.read_csv(inPath1, sep='\t')
	data2 = pd.read_csv(inPath2, sep='\t')

	gen1 = data1['Generation']
	gen2 = data2['Generation']
	hv1 = data1['HV']
	hv2 = data2['HV']
	#plt.style.available 
	dpi=50
	plt.figure(figsize=(200/dpi, 200/dpi), dpi=350)
	#plt.style.use('seaborn-paper')
	matplotlib.font_manager._rebuild()
	plt.rcParams["font.family"] = "Times New Roman"
	simsun = fm.FontProperties(fname='/Users/meow/Downloads/SimSun.ttf')
	plt.style.context('seaborn-pastel')

	plt.plot(gen2, hv2, label='NSGA-II', linewidth=1, marker='o', markersize=2)
	plt.plot(gen1, hv1, label='Modified MOEA/D', linewidth=1, marker='o', markersize=2)
	
	plt.xlabel('种群代数', fontproperties=simsun)
	plt.ylabel('超立方体', fontproperties=simsun)
	
	plt.legend()
	file_title = 'HV'
	i = 0
	outImage = os.path.join("/Users/meow/Desktop/DP/MOEA-D/Analysis/Compare", 'paper_'+file_title+ str(i)+'.png')
	while(os.path.exists(outImage)):
		i+=1
		outImage = os.path.join("/Users/meow/Desktop/DP/MOEA-D/Analysis/Compare", 'paper_'+file_title+ str(i)+'.png')
	
	plt.savefig(outImage, bbox_inches='tight')
def plot_DM(inPath1, inPath2):
	data1 = pd.read_csv(inPath1, sep='\t')
	data2 = pd.read_csv(inPath2, sep='\t')

	gen1 = data1['Generation']
	gen2 = data2['Generation']
	dm1 = data1['D-metric']
	dm2 = data2['D-metric']
	#plt.style.available 
	dpi=50
	plt.figure(figsize=(200/dpi, 200/dpi), dpi=350)
	#plt.style.use('seaborn-paper')
	matplotlib.font_manager._rebuild()
	plt.rcParams["font.family"] = "Times New Roman"
	simsun = fm.FontProperties(fname='/Users/meow/Downloads/SimSun.ttf')
	plt.style.context('seaborn-pastel')

	plt.plot(gen2, dm2, label='NSGA-II', linewidth=1, marker='o', markersize=2)
	plt.plot(gen1, dm1, label='Modified MOEA/D', linewidth=1, marker='o', markersize=2)
	
	plt.xlabel('种群代数', fontproperties=simsun)
	plt.ylabel('D-Metric', fontproperties=simsun)
	
	plt.legend()
	file_title = 'DM'

	i=0
	outImage = os.path.join("/Users/meow/Desktop/DP/MOEA-D/Analysis/Compare", 'paper_'+file_title+ str(i)+'.png')
	while(os.path.exists(outImage)):
		i+=1
		outImage = os.path.join("/Users/meow/Desktop/DP/MOEA-D/Analysis/Compare", 'paper_'+file_title+ str(i)+'.png')
	
	plt.savefig(outImage, bbox_inches='tight')
def compareHV(inPath1, inPath2):
	inPath1 = os.path.join(inPath1, 'EP.txt')
	inPath2 = os.path.join(inPath2, 'EP.txt')
	risk, income = np.loadtxt(inPath1, unpack='true')
	outFolder = "/Users/meow/Desktop/DP/MOEA-D/Output/PF"
	PFPath = utilis.getLatest(outFolder, "PF")
	PFPath = os.path.join(PFPath, "PF_conv.txt")
	risk2, income2 = np.loadtxt(inPath2, unpack='true')
	#file_title = os.path.basename(inPath)[:-4]	
	file_title = 'compare'
	outImage = os.path.join("/Users/meow/Desktop/DP/Latex/images", 'paper_'+file_title+'.png')
	dpi=50
	plt.figure(figsize=(150/dpi, 150/dpi), dpi=350)
	matplotlib.font_manager._rebuild()
	plt.rcParams["font.family"] = "Times New Roman"
	plt.style.context('seaborn-pastel')
	plt.axis([0, 120, 0, 12])
	
	plt.scatter(risk2, income2, s=1, label='Pareto Front', marker=',' )
	plt.scatter(risk, income, s=4, label='MOEA/D', marker='o')
	plt.xlabel(r'Minimize $ f_1$', fontname="Times New Roman")
	plt.ylabel(r'Minimize $ f_2$', fontname="Times New Roman")
	plt.legend()
	plt.savefig(outImage, bbox_inches='tight')
def formatDataFolder(inPath):
	#algs_type = inPath.split('/')[-2]
	#da.formatPlot_Test(inPath+'/EP.txt')
	plot.paper_EPvPF(inPath+'/EP_conv.txt')
	#da.epochValue_epoch(inPath+'/EP_epoch.txt')
	#da.epochValue_epoch(inPath+'/EP_epoch_N.txt')
	da.epochValue(inPath+'/EP_epoch.txt')


if __name__ == "__main__":
	inPath1 = "/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test110"
	inPath2 = "/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test119"
	plot_DM("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test110/EP_epoch_record.csv",
		"/Users/meow/Desktop/DP/MOEA-D/Output/NSGA-II/Test10/EP_epoch_record.csv"
			)
	#plot_DM(inPath1+'/EP_epoch_record.csv', inPath2+'/EP_epoch_record.csv')
	#plot_DM(inPath1, inPath2)