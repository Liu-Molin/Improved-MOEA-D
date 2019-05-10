/*
 * --------------------------------------------------------------
 * File:          util_type.h
 * Project:       Code
 * Created:       Wednesday, 6th March 2019 9:36:58 am
 * @Author:       molin@live.cn
 * Last Modified: Wednesday, 6th March 2019 9:37:01 am
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */

#ifndef TYPEDEF
#define TYPEDEF
#include <iostream>
#include <sstream>
#include <cstring>
#include "util_random.h"
struct Lamb{
    double lamb[2];
    int *neighbor;
    ~Lamb(){
        delete []neighbor;
    }
};
struct Constraint{
    //Problem's info
    unsigned int num_assets = 0;
    unsigned int max_assets = 0;
    unsigned int transaction_limit = 0;
    unsigned int cash_change = 0;
    
    
    unsigned int N = 100;//The number of population.
    unsigned int T = 10; //The size of neighborhood.
    
    int* maxBuy;
    int* minBuy;
    int fundLimit;
    //@Todo Specific criteria
    int stopCriteria; //
    //Overwrite operators
    Constraint(){

    };
    Constraint(int N, int T){
        this->N = N;
        this->T = T;
    }
    struct Constraint&operator=(struct Constraint x){
        this->num_assets = x.num_assets;
        this->max_assets = x.max_assets;
        this->transaction_limit = x.transaction_limit;
        this->cash_change = x.cash_change;
        this->N = x.N;
        this->T = x.T;
        this->maxBuy=x.maxBuy;
        this->minBuy=x.minBuy;
        this->fundLimit=x.fundLimit;
        return *this;
    }
};

struct asset{
    asset(){
        
    }
    double current_price = 0;
    double holding = 0;
    double cost_buy = 0;
    double cost_sell = 0;
    double vcost_buy = 0;
    double vcost_sell = 0;
    int min_buy = 0;
    int min_sell = 0;
    int max_buy = 0;
    double max_sell = 0;

    double mean_income = 0;
    double diviation_r = 0;
    unsigned int id = 0;

    void init(std::istringstream&line_cache){
        line_cache>>this->current_price>>
                      this->holding>>
                      this->cost_buy>>
                      this->cost_sell>>
                      this->vcost_buy>>
                      this->vcost_sell>>   
                      this->min_buy>>
                      this->min_sell>>
                      this->max_buy>>
                      this->max_sell;
    }
    struct asset &operator=(struct asset x){
        this->current_price = x.current_price;
        this->holding = x.holding;
        this->cost_buy = x.cost_buy;
        this->cost_sell = x.cost_sell;
        this->vcost_buy = x.vcost_buy;
        this->vcost_sell = x.vcost_sell;
        this->min_buy = x.min_buy;
        this->min_sell = x.min_sell;
        this->max_buy = x.max_buy;
        this->max_sell = x.max_sell;
        this->id = x.id;
        return *this;
    }
    
};

class Solution{
public:
    double risk;
    double income;
    int numPorts;
    int *port = nullptr;
    
    Solution(){

    };
    Solution(Solution const &x){
        this->risk = x.risk;
        this->income = x.income;
        this->numPorts = x.numPorts;
        if(port == nullptr){
            this->port = new int[numPorts];
        }
        for(int i = 0; i<numPorts; i++){
            this->port[i] = x.port[i];
        }
    }
    Solution(int length){
        numPorts=length;
        port=new int[length];
    }
    ~Solution(){
    }
    void operator=(Solution const &x){
        this->risk = x.risk;
        this->income = x.income;
        this->numPorts = x.numPorts;
        if(port == nullptr){
            this->port = new int[numPorts];
        }
        for(int i = 0; i<numPorts; i++){
            this->port[i] = x.port[i];
        }
    }
    /*
    class Solution&operator=(Solution&x){
        this->risk = x.risk;
        this->income = x.income;
        this->numPorts = x.numPorts;
        for(int i = 0; i<numPorts; i++){
            this->port[i] = x.port[i];
        }
    }*/

    void list(){
        for(int i = 0; i<numPorts; i++){
            std::cout<<port[i]<<" ";
        }
        std::cout<<"\n";
    }
};

#endif