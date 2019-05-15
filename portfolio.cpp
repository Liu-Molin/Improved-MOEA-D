/*
 * --------------------------------------------------------------
 * File:          portfolio.cpp
 * Project:       Code
 * Created:       Wednesday, 6th March 2019 10:29:56 am
 * @Author:       molin@live.cn
 * Last Modified: Wednesday, 6th March 2019 10:29:59 am
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */

#include "util_fileloader.h"
#include "moead.h"
int main(int argc, char *argv[]){
    //std::cerr<<"[Start]:\tMOEA/D\n";
    std::string outPath = argv[1];
    std::string id = argv[2];
    int input_N = atoi(argv[3]);
    int input_T = atoi(argv[4]);
    int numGen = atoi(argv[5]);
    double input_mix = std::stod(argv[6]);
    //outPath +="/Output";
    
    std::string initEP_raw = outPath+"/EP_raw.txt";
    std::string initEP = outPath+"/initEP.txt";
    ///std::cout<<initEP<<std::endl;
    std::string dataPath = ("DataSet/portreb"+id+".txt");
    std::string zPath = outPath + "/z.txt";
    std::ofstream output;

    //Portfolio Start here.
    Constraint portfolioProblem = Constraint(input_N, input_T);
    //std::cerr<<"[Init]:\tStart Initial Lamb\n";
    struct Lamb*lamb = init_lamb(input_N, input_T);
    
    //std::cerr<<"[Init]:\tInitial Lamb Complete\n";
    //Parameters setting.

    struct asset*portfolioAsset;
    //I. Load data set
    //std::cerr<<"[Init]:\tLoad Complete\n";
    load_portreb(dataPath, portfolioProblem, &portfolioAsset);

    //II. Initialization
    //  1. Initialize population.
    //std::cout<<"[Init]:\tStart MOP Initialization\n";
    MOEA_D mop(portfolioProblem, &portfolioAsset, lamb, input_mix);
    //std::cout<<"[Init]:\tMOP Initialization Complete\n";
    mop.ep2Txt(initEP);
    
    //III. Update
    //std::cout<<"[Update]:\tIteration Start\n[Processing]:\t";
    
    for(int i = 0; i<numGen; i++){
        if(i<30){

            if(i>15){
                if(i%2==0){
                    mop.epochEP(outPath+"/EP_epoch.txt");
                    mop.epochEP_N(outPath+"/EP_epoch_N.txt");
                }
            }
            else{
                mop.epochEP(outPath+"/EP_epoch.txt");
                mop.epochEP_N(outPath+"/EP_epoch_N.txt");
            }    
        }
        else{
            if(i%5==0){
                mop.epochEP(outPath+"/EP_epoch.txt");
                mop.epochEP_N(outPath+"/EP_epoch_N.txt");
            }
        }
        mop.production(i);
        mop.z2txt(zPath);
        //std::cerr.width(4);
        //std::cerr<<int(100*i/numGen)+1<<"%";
        //std::cerr<<"\b\b\b\b\b";
    }
    //std::cout<<std::endl;
    mop.epochEP(outPath+"/EP_epoch.txt");
    mop.epochEP_N(outPath+"/EP_epoch_N.txt");
    mop.ep2Txt(outPath+"/EP_old.txt");
    mop.vEP2txt(outPath+"/EP.txt");
    mop.epGene2txt(outPath+"/EP_gene.txt");
    //Deconstruction
    //std::cout<<"\n[END]:\tEnd of Portfolio.\n";
    free(portfolioAsset);
}