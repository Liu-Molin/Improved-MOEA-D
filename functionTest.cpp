/*
 * --------------------------------------------------------------
 * File:          functionTest.cpp
 * Project:       Code
 * Created:       Friday, 5th April 2019 1:52:54 pm
 * @Author:       molin@live.cn
 * Last Modified: Friday, 5th April 2019 1:53:02 pm
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */
#include "util_random.h"
#include "util.h"
#include <iostream>
#include <vector>
#include <sstream>
#include <cstring>
#include <fstream>
#include <algorithm>
class Example{
public:
	int *port;
	Example(){
		port = new int[10];
	}
	double risk;
	double income;
	void assign(double risk, double income){
		this->risk = risk;
		this->income = income;
	}
	void echo(){
		std::cout<<risk<<"\t"<<income<<std::endl;
	}
	~Example(){
		delete []port;
		std::cout<<"Example, de\n";
	}
	void operator=(Example const &x){
		risk = x.risk;
		income = x.income;
		for(int i = 0; i<10; i++){
			port[i] = x.port[i];
		}
	}
};
class moead_Example: public Example{
public:
	moead_Example(){

	}
	~moead_Example(){
		std::cout<<"moead_Example, de\n";
	}
};
bool dom(Example&x, Example&y){
	if((x.risk<y.risk)and(x.income>y.income)){
		return true;
	}
	return false;
}
void testDom(){
	fstream inFile("Output/MOEA-D/Test4/initEP.txt", ios::in);
	std::string input_cache;
	int line = 0;
	std::vector<class Example*>population;
	while( std::getline(inFile, input_cache)){
		std::istringstream line_cache(input_cache);
		double risk, income;
		line_cache>>risk>>income;
		Example*tempExample = new Example();
		tempExample->assign(risk, income);
		population.push_back(tempExample);
	}
	std::cout<<"Population:"<<population.size()<<std::endl;
	std::vector<class Example*>outPopulation;
	for(int i = 0; i<population.size(); i++){
		bool dominated = false;
		for(int j = 0; j<population.size(); j++){
			if(dom(*population[j], *population[i])){
				dominated = true;
				break;
			}
		}
		if(!dominated){
			population[i]->echo();
			outPopulation.push_back(population[i]);
		}
	}
	std::cout<<"Population:"<<outPopulation.size()<<std::endl;
	ofstream outFile;
	outFile.open("Output/MOEA-D/Test4/initEP1.txt");
}


int main(int argc, char *argv[]){
	std::vector<class Example>x;
	for(int i = 0; i<10; i++){
		Example tempX;
		x.push_back(tempX);
	}
	x.erase(x.begin()+3);
	//testDom();
	/*
	Example x;
	x.assign(18.715, 1.17502);

	Example y;
	y.assign(17.0082, 1.77234);

	if(dom(x,y)){
		std::cout<<"ok\n";
	}*/
}