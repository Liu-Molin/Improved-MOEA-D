# !/usr/bin/env python
# --------------------------------------------------------------
# File:          dataClean.py
# Project:       Code
# Created:       Friday, 3rd May 2019 11:04:14 am
# @Author:       molin@live.cn
# Last Modified: Friday, 3rd May 2019 11:04:17 am
# Copyright  © Rockface 2018 - 2019
# --------------------------------------------------------------

import os
import numpy as np

def formatFile(inPath):
	income, risk, gen = np.loadtxt(inPath, unpack='true')
	np.savetxt(inPath, np.c_[risk, income, gen])
	print(income)


if __name__ == "__main__":
	inPath = input("filePath:\t")
	formatFile(inPath)