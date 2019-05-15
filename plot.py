import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import os
import plotly.graph_objs as go
import numpy as np
from plotly.graph_objs import Scatter, Layout
import plotly.io as pio
import matplotlib.pyplot as plt
from matplotlib import rc
import dataAnalysis, utilis

import matplotlib
import pandas as pd
maxY = 15
maxX = 120

def mat_plotConv(inPath):
	risk, income = np.loadtxt(inPath, unpack='true')
	outImage = os.path.join(os.path.dirname(inPath), os.path.basename(inPath)[:-4]+'_paper.png')
	dpi=50
	plt.figure(figsize=(150/dpi, 150/dpi), dpi=350)
	matplotlib.font_manager._rebuild()
	plt.rcParams["font.family"] = "Times New Roman"
	#plt.rc('font', family='serif')
	plt.style.use('seaborn-pastel')
	plt.axis([0, 120, 0, 12])
	plt.scatter(risk, income, s=1, label='Pareto front', color='darkorange')
	plt.xlabel(r'Minimize $ f_1$', fontname="Times New Roman")
	plt.ylabel(r'Minimize $ f_2$', fontname="Times New Roman")
	plt.legend()
	#plt.show()
	plt.savefig(outImage, bbox_inches='tight')
def mat_plotFormate(inPath):
	risk, income = np.loadtxt(inPath, unpack='true')
	outImage = os.path.join(os.path.dirname(inPath), os.path.basename(inPath)[:-4]+'_paper.png')
	dpi=50
	plt.figure(figsize=(150/dpi, 150/dpi), dpi=350)
	matplotlib.font_manager._rebuild()
	plt.rcParams["font.family"] = "Times New Roman"
	#plt.rc('font', family='serif')
	plt.style.use('seaborn-pastel')
	plt.axis([0, 120, 0, 12])
	plt.scatter(risk, income, s=1, label='Pareto front', color='darkorange')
	plt.xlabel('Risk', fontname="Times New Roman")
	plt.ylabel('Return', fontname="Times New Roman")
	plt.legend()
	#plt.show()
	plt.savefig(outImage, bbox_inches='tight')
def mat_plotLine(inPath):
	data = pd.read_csv(inPath, sep='\t')
	gen = data['Generation']
	hv = data['HV']
	d_metric = data['D-metric']
	#plt.style.available 
	dpi=50
	fig = plt.figure(figsize=(250/dpi, 250/dpi), dpi=350)
	ax1 = fig.add_subplot(111)
	ax1.plot(gen, hv, label='Hypervolume', linewidth=1, marker='o', markersize=2)
	ax1.legend(loc=1)
	ax1.set_ylabel("Hypervolume")
	ax1.set_ylim([0, 600])
	ax2 = ax1.twinx()
	ax2.plot(gen, d_metric, label='D-metric', color ='darkorange' ,linewidth=1, marker='o', markersize=2)
	ax2.legend(loc=2)
	plt.style.use('seaborn-paper')
	outImage = inPath[:-4]+'.png'
	plt.savefig(outImage, bbox_inches='tight')
def paper_EPvPF(inPath):
	risk, income = np.loadtxt(inPath, unpack='true')
	outFolder = "/Users/meow/Desktop/DP/MOEA-D/Output/PF"
	PFPath = utilis.getLatest(outFolder, "PF")
	PFPath = os.path.join(PFPath, "PF_conv.txt")
	pf_risk, pf_income = np.loadtxt(PFPath, unpack='true')
	file_title = os.path.basename(inPath)[:-4]	
	outImage = os.path.join(os.path.dirname(inPath), 'paper_'+file_title+'.png')
	label_title = inPath.split('/')[-3]
	id_title = inPath.split('/')[-2][4:]
	dpi=50
	plt.figure(figsize=(150/dpi, 150/dpi), dpi=350)
	matplotlib.font_manager._rebuild()
	plt.rcParams["font.family"] = "Times New Roman"
	plt.style.context('seaborn-pastel')
	plt.axis([0, 120, 0, 12])
	
	plt.scatter(pf_risk, pf_income, s=1, label='Pareto Front', marker=',' )
	plt.scatter(risk, income, s=4, label='MOEA/D', marker='o')
	plt.xlabel(r'Minimize $ f_1$', fontname="Times New Roman")
	plt.ylabel(r'Minimize $ f_2$', fontname="Times New Roman")
	plt.legend()
	#plt.show()
	plt.savefig(outImage, bbox_inches='tight')
def mat_plotEP_PF(inPath):
	risk, income = np.loadtxt(inPath, unpack='true')
	outFolder = "/home/lusso/Documents/MOEA-D/Resource/PF"
	PFPath = utilis.getLatest(outFolder, "PF")
	PFPath = os.path.join(PFPath, "PF_conv.txt")
	pf_risk, pf_income = np.loadtxt(PFPath, unpack='true')
	file_title = os.path.basename(inPath)[:-4]	
	outImage = os.path.join(os.path.dirname(inPath), file_title+'_paper.png')
	print(outImage)
	label_title = inPath.split('/')[-3]
	id_title = inPath.split('/')[-2][4:]
	
	dpi=50
	plt.figure(figsize=(150/dpi, 150/dpi), dpi=350)
	matplotlib.font_manager._rebuild()
	plt.rcParams["font.family"] = "Times New Roman"
	plt.style.context('seaborn-pastel')
	plt.axis([0, 120, 0, 12])
	plt.scatter(pf_risk, pf_income, s=1, marker='s', label='Pareto Front', )
	plt.scatter(risk, income, s=3, label=label_title)
	plt.xlabel(r'Minimize $f_1$')
	plt.ylabel(r'Minimize $f_2$')
	plt.legend()
	#plt.show()
	plt.savefig(outImage, bbox_inches='tight')
	os.system("cp "+outImage+" /Users/meow/Desktop/DP/MOEA-D/Analysis/"+str(label_title)+str(id_title)+'.png')
def getLayout(file_title, maxX, maxY, x_title="", y_titile=""):
	Playout = go.Layout(
		title = file_title,
		xaxis=dict(
			zeroline=True,
			gridwidth=1,
			range=[0, maxX],
			title=dict(text=x_title)
		),
		yaxis=dict(
			zeroline=True,
			gridwidth=1,
			range=[0, maxY],
			title=dict(text=y_titile)
		),
		showlegend=True
	)
	return Playout
def plotEP_PF(inPath):
	mat_plotEP_PF(inPath)
	risk, income = np.loadtxt(inPath, unpack='true')
	outFolder = "/Users/meow/Desktop/DP/MOEA-D/Output/PF"
	PFPath = utilis.getLatest(outFolder, "PF")
	PFPath = os.path.join(PFPath, "PF_conv.txt")
	pf_risk, pf_income = np.loadtxt(PFPath, unpack='true')
	inPath = inPath[:-4]
	file_title = os.path.basename(inPath)
	#file_title = inPath.split('/')[-1][:-4]
	max_X=120
	max_Y=12
	x_title = r"$\text{Minimize} f_1$"
	y_title = r"$\text{Minimize} f_2$"
	Playout = getLayout(file_title, max_X, max_Y, x_title, y_title)
	EP = go.Scatter(x=risk, y=income, mode = 'markers',name = "EP", marker=dict(size=8, color='rgb(241, 75, 75)'))
	PF_EP = go.Scatter(x=pf_risk, y=pf_income, mode = 'markers',name = "PF", marker=dict(size=4, color='rgb(253, 127, 40)', symbol="square-open"))
	data = [PF_EP, EP]
	fig = dict(data=data, layout=Playout)
	outfile = os.path.join(os.path.dirname(inPath), file_title+'.html')
	outImage = os.path.join(os.path.dirname(inPath), file_title+'.jpeg')
	print(outImage)
	imgFig = go.Figure(data=data, layout=Playout)
	pio.write_image(imgFig, outImage, width=600, height=600, scale=4)
	plot(fig, filename=outfile, auto_open=False)
def plotPoints(inPath, max_X, max_Y):
	risk, income = np.loadtxt(inPath, unpack='true')
	inPath = inPath[:-4]
	file_title = os.path.basename(inPath)
	#file_title = inPath.split('/')[-1][:-4]
	if max_X==100 and max_Y==10:
		x_title = "Minimize f1"
		y_title = "Minimize f2"
	else:
		x_title = "Risk"
		y_title = "Income"
	Playout = getLayout(file_title, max_X, max_Y, x_title, y_title)
	EP = go.Scatter(x=risk, y=income, mode = 'markers',name = "EP", marker=dict(size=4, color='rgb(253, 127, 40)', symbol="square-open"))
	data = [EP]
	fig = dict(data=data, layout=Playout)
	outfile = os.path.join(os.path.dirname(inPath), file_title+'.html')
	outImage = os.path.join(os.path.dirname(inPath), file_title+'.jpeg')
	print(outImage)
	imgFig = go.Figure(data=data, layout=Playout)
	pio.write_image(imgFig, outImage, width=600, height=600, scale=4)
	plot(fig, filename=outfile, auto_open=False)
def plotEP(inPath):
	fileEP = os.path.join(inPath, 'EP.txt')
	fileInitEP = os.path.join(inPath, 'initEP.txt')
	file_title = inPath.split('/')
	file_title = file_title[-2]
	print(fileEP)
	print(fileInitEP)
	risk, income = np.loadtxt(fileEP, unpack='true')
	initRisk, initIncome = np.loadtxt(fileInitEP, unpack='true')

	Playout = getLayout(file_title, maxX, maxY)
	EP = go.Scatter(x=risk, y=income, mode = 'markers',name = "EP", marker=dict(size=4, color='rgb(253, 127, 40)'))
	initEP = go.Scatter(x=initRisk, y=initIncome, mode='markers', name='Init Ep', marker=dict(size=4, color='rgb(124, 122, 121)'))
	data = [initEP, EP]
	fig = dict(data=data, layout=Playout)
	file_title = os.path.join(inPath, file_title+'.html')
	plot(fig, filename=file_title, auto_open=False)

def plotMOEAD(inPath):
	fileEP = os.path.join(inPath, 'EP.txt')
	fileInitEP = os.path.join(inPath, 'initEP.txt')
	fileZ = os.path.join(inPath, 'z.txt')
	file_title = inPath.split('/')
	file_title = file_title[-2]
	risk, income = np.loadtxt(fileEP, unpack='true')
	initRisk, initIncome = np.loadtxt(fileInitEP, unpack='true')
	z_risk, z_income, gen = np.loadtxt(fileZ, unpack='true')

	Playout = go.Layout(
		title = file_title,
		xaxis=dict(
			zeroline=True,
			gridwidth=1,
			range=[0, maxX],
			title=dict(text="Risk")
		),
		yaxis=dict(
			zeroline=True,
			gridwidth=1,
			range=[0, maxY],
			title=dict(text="Income")
		),
		showlegend=True
	)
	EP = go.Scatter(x=risk, y=income, mode = 'markers',name = "EP", marker=dict(size=4, color='rgb(253, 127, 40)'))
	initEP = go.Scatter(x=initRisk, y=initIncome, mode='markers', name='Init Ep', marker=dict(size=4, color='rgb(124, 122, 121)'))
	graph_z = go.Scatter(x=z_risk, y=z_income, mode='markers', name='z points', marker=dict(size=4, color=gen, colorscale='Viridis', showscale=False))
	data = [initEP, EP,  graph_z]
	fig = dict(data=data, layout=Playout)
	file_title = os.path.join(inPath, file_title+'.html')
	plot(fig, filename=file_title, auto_open=False)
def plotSimple(inPath):
	plot_title = os.path.basename(os.path.dirname(inPath))
	risk, income = np.loadtxt(inPath, unpack='true')



def plotRawEP(inPath):
	##fileEP = os.path.join(inPath, 'EP.txt')
	##fileInitEP = os.path.join(inPath, 'initEP.txt')
	file_title = inPath.split('/')
	file_title = file_title[-3]
	risk, income, gen = np.loadtxt(inPath, unpack='true')

	Playout = go.Layout(
		title = file_title,
		xaxis=dict(
			zeroline=True,
			gridwidth=1,
			range=[0, maxX],
			title=dict(text='Risk')
		),
		yaxis=dict(
			zeroline=True,
			gridwidth=1,
			range=[0, maxY],
			title=dict(text='Income')
		),
		showlegend=True
	)
	EP = go.Scatter(
		x=risk, 
		y=income, 
		mode = 'markers',
		name = "EP", 
		marker=dict(
			size=4, 
			color=gen,
			colorscale='Viridis',
			showscale=True ))
	data = [EP]
	fig = dict(data=data, layout=Playout)
	file_title = os.path.join(inPath, file_title+'.html')
	outFile = '/Users/meow/Downloads/moea_d报告/plot.html'
	plot(fig, filename=outFile, auto_open=False)

if __name__ == "__main__":
	'''
	type = input("Algorithm type:\n 1. MOEA\D\t2. NSGA-II\n")
	if type=="1":
		type = "MOEA-D"
	else:
		type = "NSGA-II"
	inFilePath = os.path.join(os.path.abspath(os.path.curdir), "Output/"+type)
	whichTest = input("Which test:")
	inFilePath = os.path.join(inFilePath, "Test"+str(whichTest))
	plotEP(inFilePath)
	'''
	#plotRawEP(inPath)
	#mat_plotEP_PF("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test34/EP_conv.txt")
	#dataAnalysis.formatPlot_Test(inPath)
	#mat_plotEP_PF("")
	#mat_plotLine("/Users/meow/Desktop/DP/MOEA-D/Output/MOEA-D/Test97/EpochRecord.csv")
	inPath = input("Path:")
	paper_EPvPF(inPath)