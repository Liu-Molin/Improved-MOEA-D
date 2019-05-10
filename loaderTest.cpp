/*
 * --------------------------------------------------------------
 * File:          loaderTest.cpp
 * Project:       Code
 * Created:       Thursday, 7th March 2019 2:10:29 pm
 * @Author:       molin@live.cn
 * Last Modified: Thursday, 7th March 2019 2:10:31 pm
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */

#include <fstream>
#include <sstream>
#include <cstring>
#include <iostream>
 
struct item{
    int id;
    int value;
};
int loadFile(struct item**outValue){
    
    *outValue = (struct item*)malloc(sizeof(struct item)*10);
    int line = 0;
    for(int i = 0; i<10; i++){
        outValue[i]->id = i;
    }
    if(*outValue== NULL) 
    {
        free(*outValue);      /* this line is completely redundant */
        printf("\nERROR: Memory allocation did not complete successfully!"); 
    }
    printf("\nPoint1: Memory allocated: %d bytes", sizeof(*outValue)); 
    return 0;
}

int main(){
    std::cout<<"Begin\n";
    struct item*passValue;
    loadFile(&passValue);
    std::cout<<"Complete allocat memory\n";
    for(int i = 0; i<10; i++){
        std::cout<<i<<std::endl;
        std::cout<<passValue[i].id<<std::endl;
    }
}