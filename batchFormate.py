# !/usr/bin/env python
# --------------------------------------------------------------
# File:          batchFormate.py
# Project:       MOEA-D
# Created:       Friday, 10th May 2019 9:29:24 am
# @Author:       molin@live.cn
# Last Modified: Friday, 10th May 2019 9:29:57 am
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

def plotCSV(inPath):
	for test in os.listdir(inPath):
		if not test[0]=='.':
			Path_test = os.path.join(inPath, test)
			for file in os.listdir(Path_test):
				if file[-4:] == '.csv':
					plot.mat_plotLine(os.path.join(Path_test, file))

if __name__ == "__main__":
	NSGA='/Users/meow/Desktop/DP/MOEA-D/Output/NSGA-II'
	plotCSV(NSGA)