# !/usr/bin/env python
# --------------------------------------------------------------
# File:          ExpConfig.py
# Project:       MOEA-D
# Created:       Friday, 10th May 2019 8:25:21 am
# @Author:       molin@live.cn
# Last Modified: Friday, 10th May 2019 8:25:27 am
# Copyright  © Rockface 2019 - 2019
# --------------------------------------------------------------

import os, sys, multiprocessing, tqdm, shutil
import pandas as pd
from numba import jit
import utilis
import moead

pbar = None
def callback_tqdm(*v):
	pbar.update()

PATH_EXP = "ExpConfig"
def getLatestExp():
    configFile = pd.DataFrame(columns=['Data id', 'Algorithm Type', 'N', 'T', 'MM', 'Generation', 'Mix rate'])
    configPath = utilis.getOutPath(PATH_EXP, 'Experiment', 'csv')
    print(configPath)
    configFile.to_csv(configPath, sep=',', index=False)

def loadConfig():
    configPath = utilis.getLatest(PATH_EXP, 'Experiment', 'csv')
    experimentFolder = os.path.join('Out', os.path.basename(configPath)[:-4])
    print(experimentFolder)
    os.mkdir(experimentFolder)
    config = pd.read_csv(configPath)
    list_moead = []
    list_nsga2 = []
    for i in tqdm.tqdm(range(len(config['Algorithm Type']))):
        subExpFolder = "Exp"+'-'+str(i)
        subExpFolder = os.path.join(experimentFolder, subExpFolder)
        print(subExpFolder)
        os.mkdir(subExpFolder)
        if config['Algorithm Type'].iloc[i]=='moead':
            experiment_moead(
                subExpFolder,
                config['Data id'].iloc[i], 
                config['N'].iloc[i], 
                config['T'].iloc[i],
                config['Generation'].iloc[i],
                config['Mix rate'].iloc[i]
                )
@jit(parallel=True)
def experiment_moead(outPath, dataid, N, T, G, MR):
    print(dataid, N, T, G, MR)
    p = multiprocessing.Pool(os.cpu_count())
    subTest_list = []
    num_subTest = 4

    for i in range(num_subTest):
        subTestFolder = "Test-"+str(i)
        subTestFolder = os.path.join(outPath, subTestFolder)
        os.mkdir(subTestFolder)
        subTest_list.append(subTestFolder)

    for i in range(num_subTest):
        p.apply_async(moead.batchJob, args=(dataid, N, T, G, MR, subTest_list[i]))
    p.close()
    p.join()

@jit(parallel=True)
def analysisExp():
    pass
def experiment_nsga2(dataid, N, MM, G, MR):
    pass
if __name__ == "__main__":
    #getLatestExp()
    
    loadConfig()
    #moead.batchJob(1, 500, 10, 100, 0.2, "/home/lusso/Documents/MOEA-D/Out/Experiment-1/Exp-0/Test-0")