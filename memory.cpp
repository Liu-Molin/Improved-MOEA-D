/*
 * --------------------------------------------------------------
 * File:          memory.cpp
 * Project:       Code
 * Created:       Monday, 4th March 2019 10:39:16 am
 * @Author:       molin@live.cn
 * Last Modified: Monday, 4th March 2019 10:39:19 am
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */
 
#include <iostream>
#include "util_type.h"
void initAsset(struct asset*x, struct asset*y){
    x->current_price = y->current_price;
    x->holding = y->holding;
    x->cost_buy = y->cost_buy;
    x->cost_sell = y->cost_sell;
    x->vcost_buy = y->vcost_buy;
    x->vcost_sell = y->vcost_sell;
    x->min_buy = y->min_buy;
    x->min_sell = y->min_sell;
    x->max_buy = y->max_buy;
    x->max_sell = y->max_sell;
    x->id = y->id;
}
int main(){
    struct asset *assetInput = (struct asset*) malloc(sizeof(struct asset));
    struct asset assetCache;
    struct asset *assetSet = (struct asset*) malloc(10 * sizeof(struct asset));
    int *t = (int*)malloc(10*sizeof(int));
    for(int i = 0; i<10; i++){
        assetSet[i] = assetCache;
    }
    for(int i = 0; i<10; i++){
        std::cout<<assetSet[i].id<<std::endl;
    }
    std::cout<<sizeof(assetInput)<<std::endl;
    std::cout<<sizeof(assetSet)<<std::endl;
    std::cout<<sizeof(int)<<std::endl;
    free(assetInput);
    free(assetSet);
    free(t);
}