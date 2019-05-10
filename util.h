/*
 * --------------------------------------------------------------
 * File:          util.h
 * Project:       Code
 * Created:       Friday, 5th April 2019 2:38:40 pm
 * @Author:       molin@live.cn
 * Last Modified: Friday, 5th April 2019 2:38:57 pm
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */
#include <iostream>
#include "util_random.h"
using namespace std;

int* treNum(int len=10){
	//@Todo Need to Optimize
	cout<<endl;
	int value[3];
	int temp0 = int(randG()*(len-1));
	value[0] = temp0;
	int temp1 = int(randG()*(len-2));
	value[1] = temp1;

	if (value[1]>=temp0){
		value[1] += 1;
	}

	int temp2;
	do{
		temp2 = int(randG()*(len-1));
	}while(temp2==value[0]||temp2==value[1]);
	value[2] = temp2;

	return &value[0];
}