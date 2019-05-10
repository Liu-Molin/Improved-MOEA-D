//
//  instance.cpp
//  MOEA/D
//
//  Created by Molin on 04/08/2017.
//  Copyright © 2017 merlin. All rights reserved.
//
//
#include "loader.h"
#include "randG.h"
#include "nsga2.h"
#include <iostream>
using namespace std;

int main(int argc, char *argv[]){
    clock_t start, end;
    start = clock();

    std::string id = argv[1];
    int N = atoi(argv[2]);
    
    std::string FILE_PATH = ("/Users/meow/Desktop/DP/Code/DataSet/portreb"+id+".txt");
    std::string resourceFolder = "/Users/meow/Desktop/DP/Code/Resource/";
    std::string genePath = resourceFolder+argv[2]+".txt";

    struct Constraint port1_constraint;
    double port1_correlations[31][31] = {};
    vector <struct asset> assetArray;
    bool s[4] = {0,0,0,0};
    for(int i =0; i<4; i++){
        char buffer;
    }
    if(loadItem(  FILE_PATH,
                assetArray,
                port1_constraint,
                port1_correlations)) {
        util_preprocess(assetArray);

    }

    setting(s, assetArray);
    population x;
    std::cerr<<"[Init]:\tInitial Population\n";
    init_population(x, assetArray, port1_constraint, port1_correlations, N, MM);
    gene2txt(genePath, x);
    end = clock();
    cout<<"[FINAL]: \n\tRuntime:\t"<<end-start<<endl;
}