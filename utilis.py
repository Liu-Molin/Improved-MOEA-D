# !/usr/bin/env python
# --------------------------------------------------------------
# File:          utilis.py
# Project:       MOEA-D
# Created:       Sunday, 5th May 2019 10:39:04 am
# @Author:       molin@live.cn
# Last Modified: Sunday, 5th May 2019 10:39:06 am
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------

import os, sys

def getOutPath(outDir, preFix, type=None):
	outDirFiles = os.listdir(outDir)
	i = 0
	if type!=None:
		tempDirName = preFix+'-'+str(i)+'.'+str(type)
	else:
		tempDirName = preFix+'-'+str(i)
	while tempDirName in outDirFiles:
		i+=1
		if type!=None:
			tempDirName = preFix+'-'+str(i)+'.'+str(type)
		else:
			tempDirName = preFix+'-'+str(i)
	tempDirName = os.path.join(outDir, tempDirName)
	return tempDirName

def getLatest(inDir, preFix, type=None):
	inDirFiles =os.listdir(inDir)
	i = 0
	tempDirName = (preFix+"-%d"%i)
	if(type!=None):
		tempDirName+=(".%s"%str(type))
	if tempDirName in inDirFiles:
		return os.path.join(inDir, tempDirName)
	
	i+=1
	tempDirName = (preFix+"-%d"%i)
	if(type!=None):
		tempDirName+=(".%s"%str(type))
	while tempDirName in inDirFiles:
		i+=1
		tempDirName = (preFix+"-%d"%i)
		if(type!=None):
			tempDirName+=(".%s"%str(type))
	tempDirName = (preFix+"-%d"%(i-1))
	if(type!=None):
		tempDirName+=(".%s"%str(type))
	return os.path.join(inDir, tempDirName)
	

