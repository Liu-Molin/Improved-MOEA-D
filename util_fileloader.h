/*
 * --------------------------------------------------------------
 * File:          util_fileloader.h
 * Project:       Code
 * Created:       Thursday, 28th February 2019 10:58:31 am
 * @Author:       molin@live.cn
 * Last Modified: Thursday, 28th February 2019 10:58:33 am
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */
#ifndef FILE_LOADER
#define FILE_LOADER
#include <vector>
#include <fstream>
#include "util_type.h"

void load_portreb(std::string path, struct Constraint &constraint, struct asset **outAsset){
    std::fstream data(path, std::ios::in);
    std::string input_cache;
    int line = 0;
    if (!data.is_open()){
        std::cout<<"CANNOT OPEN FILE\n";
        std::cout<<"\t FILE PATH: "<<path<<std::endl;
        return;
    }
    while( std::getline(data, input_cache)){
        if(input_cache.length()<=1){
            //std::cerr<<("Line: %d\n", line);
            //std::cerr<<"Content:\t"<<input_cache<<std::endl;
            continue;
        }
        std::istringstream line_cache(input_cache);
        if(line == 0){
            line_cache>>
            constraint.num_assets>>
            constraint.max_assets>>
            constraint.transaction_limit>>
            constraint.cash_change;
            *outAsset = (struct asset*)malloc(constraint.num_assets*sizeof(struct asset));
        }

        else{
            if(line <= constraint.num_assets){
                (*outAsset)[line-1].init(line_cache);
            }
            if(constraint.num_assets<line && line<=(2*constraint.num_assets)){
                int tran = line - constraint.num_assets - 1;
                line_cache>>(*outAsset)[tran].mean_income>>(*outAsset)[tran].diviation_r;
            }
        }
        line++;
    }       
}
std::string Trim(std::string& str)
{
	//str.find_first_not_of(" \t\r\n"),在字符串str中从索引0开始，返回首次不匹配"\t\r\n"的位置
	str.erase(0,str.find_first_not_of(" \t\r\n"));
	str.erase(str.find_last_not_of(" \t\r\n") + 1);
	return str;
}



#endif