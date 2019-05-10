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
    std::string outFolder = argv[2];
    int gener = atoi(argv[3]);
    int N = atoi(argv[4]);
    int MM = atoi(argv[5]);
    std::string FILE_PATH = ("/Users/meow/Desktop/DP/Code/DataSet/portreb"+id+".txt");
    std::string resourceFolder = "/Users/meow/Desktop/DP/Code/Resource/";
    std::string genePath = resourceFolder+argv[4]+".txt";
    ofstream epochFile;
    std::string outPath = outFolder + "/EP_epoch.txt";
    epochFile.open(outPath);

    ofstream outEP;
    std::string outEPPath = outFolder + "/EP.txt";
    outEP.open(outEPPath);

    ofstream initEP;
    std::string outInitPath = outFolder +"/initEP.txt";
    initEP.open(outInitPath);

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
    for(auto item:x.xi){
        initEP<<item.objectives[1]<<"\t"<<item.objectives[0]<<"\n";
        epochFile<<item.objectives[1]<<"\t"<<item.objectives[0]<<"\t"<<"0"<<"\n";
    }
    std::cerr<<"[Update]:\tFast Nondominated Sort\n";
    process_Fast_Nondominated(x);
    for(auto item:x.xi){
        epochFile<<item.objectives[1]<<"\t"<<item.objectives[0]<<"\t"<<"1"<<"\n";
    }
    for(int i = 0; i<gener; i++){
        process_selection(x);
        process_updateP(x, assetArray);
        process_fast_nondominated_lite(x);
        //shrink
        if (i<20){
            for(auto item:x.xi){
                epochFile<<item.objectives[1]<<"\t"<<item.objectives[0]<<"\t"<<i+2<<"\n";
            }
        }
        else if(i<50){
            if(i%2==0){
                for(auto item:x.xi){
                    epochFile<<item.objectives[1]<<"\t"<<item.objectives[0]<<"\t"<<i+2<<"\n";
                }
            }
        }
        else{
            if(i%5==0){
                for(auto item:x.xi){
                    epochFile<<item.objectives[1]<<"\t"<<item.objectives[0]<<"\t"<<i+2<<"\n";
                }
            }
        }
        
        std::cerr.width(4);
        std::cerr<<int(100*i/gener)+2<<"%";
        std::cerr<<"\b\b\b\b\b";
    }
    for(auto item:x.xi){
        outEP<<item.objectives[1]<<"\t"<<item.objectives[0]<<"\n";
    }
    outEP.close();
    epochFile.close();
    end = clock();
    cout<<"[FINAL]: \n\tRuntime:\t"<<end-start<<endl;
}