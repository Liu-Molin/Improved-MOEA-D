/*
 * --------------------------------------------------------------
 * File:          highLand.cpp
 * Project:       Code
 * Created:       Friday, 12th April 2019 8:13:39 pm
 * @Author:       molin@live.cn
 * Last Modified: Friday, 12th April 2019 8:13:45 pm
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */
#include "util_type.h"
#include "moead.h"
class Highland: public Solution{
public:
	Highland(){

	}
private:
	double fundpool;
	Constraint problem;
	int *assetMax;
	int *assetMin;
	double *price;

	void fundDistribute(int*port, double&fund, std::vector<int>toBuy){
		for(int i = 0; i<toBuy.size(); i++){
			int buyNum = int(randG()*(assetMax[toBuy[i]] - port[toBuy[i]]));
			if(buyNum*price[toBuy[i]]>fund){
				if(fund/price[toBuy[i]]>assetMin[toBuy[i]]){
					buyNum = fund/price[toBuy[i]];
					port[toBuy[i]]+=buyNum;
					fund = 0;
					break;
				}
			}

			port[toBuy[i]]+=buyNum;
			fund-=buyNum*price[toBuy[i]];
		}
	}
	void randomHighland(MOEA_D_Solution*x){
		double localFund = fundpool;
		std::vector<int>toBuy;
		for(int i = 0; i<problem.max_assets; i++){
			int buyID = int(randG()*(problem.num_assets+1));
			if(buyID>=problem.num_assets){
				buyID = -1;
			}
			std::vector<int>::iterator it = std::find(toBuy.begin(), toBuy.end(),buyID);
			if(it==toBuy.end()){
				toBuy.push_back(buyID);
			}
		}
		for(auto item:toBuy){
			int buyNum = int(randG()*(assetMax[item]- assetMin[item]))+assetMin[item];
			if(localFund-buyNum*price[item]){
				localFund-=static_cast<double>(buyNum)*price[item];
			}
			x->port[item]=buyNum;
		}
		fundDistribute(x->port, localFund, toBuy);
	}
};