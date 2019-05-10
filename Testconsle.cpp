/*
 * --------------------------------------------------------------
 * File:          Testconsle.cpp
 * Project:       Code
 * Created:       Saturday, 23rd March 2019 11:05:48 am
 * @Author:       molin@live.cn
 * Last Modified: Saturday, 23rd March 2019 11:05:55 am
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */


 #include <iostream>
 #include "util_type.h"
 #include "util_random.h"
 using namespace std;
 int main(){
	 Solution pre = Solution(32);
	 pre.init();
	 Solution pre1 = Solution(1000);
	 pre1.init();
	 cout<<sizeof(pre)<<endl;

	 //pre.list();
	 //cout<<"Pre1:\n";
	 //pre1.list();
	 int num;
	 cin>>num;
	 Solution *ptr = (Solution*)malloc(sizeof(Solution*)*num);
	 for(int i = 0; i<num; i++){
		 ptr[i].init(32);
	 }
	 for(int i = 0; i<num; i++){
		 cout<<"ptr:"<<i<<endl;
		 ptr[i].list();
	 }
 }