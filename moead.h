/*
 * --------------------------------------------------------------
 * File:          moead.h
 * Project:       Code
 * Created:       Saturday, 23rd March 2019 3:51:36 pm
 * @Author:       molin@live.cn
 * Last Modified: Saturday, 23rd March 2019 3:51:39 pm
 * Copyright  © Rockface 2018 - 2019
 * --------------------------------------------------------------
 */

#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include "util_type.h"
#include <algorithm>
#include <math.h>


double max(const double a, const double b){
    if(a>b)
        return a;
    return b;
}
static int curG;
static Constraint MOP;
class MOEA_D_Solution;
struct EP_Item{
    double risk;
    double  income;
    EP_Item(double risk, double income){
        this->risk = risk;
        this->income = income;
    }
    EP_Item(MOEA_D_Solution x);
};

class Neighbor_Solution: public Solution{
public:
    Neighbor_Solution(){
        //parent = (MOEA_D*)((char*)this-offsetof(MOEA_D, MOEA_D_Solution));
        numPorts=MOP.num_assets;
        port=new int[numPorts];
    }
    ~Neighbor_Solution(){
        delete []port;
    }
    void operator=(const MOEA_D_Solution &x);
};
class MOEA_D_Solution: public Solution{
public:
    int numNeighbor;
    Neighbor_Solution*Neighbor;
    
    MOEA_D_Solution(){
        //parent = (MOEA_D*)((char*)this-offsetof(MOEA_D, MOEA_D_Solution));
        numPorts=MOP.num_assets;
        port=new int[numPorts];
        Neighbor=new Neighbor_Solution[MOP.T];
    }
    void assign(MOEA_D_Solution&x){
        this->income = x.income;
        this->risk = x.risk;
        this->numPorts = x.numPorts;
        for(int i = 0; i<numPorts; i++){
            this->port[i] = x.port[i];
        }
        
        for(int i = 0; i<MOP.T; i++){
            this->Neighbor[i] = x.Neighbor[i];
        }
    }
    void operator=(MOEA_D_Solution const &x){
        this->income = x.income;
        this->risk = x.risk;
        this->numPorts = x.numPorts;
        if(this->port == nullptr){
            this->port = new int[MOP.num_assets];
        }
        if(this->Neighbor == nullptr){
            this->Neighbor = new Neighbor_Solution[MOP.T];
        }
        for(int i = 0; i<numPorts; i++){
            this->port[i] = x.port[i];
        }
        for(int i = 0; i<MOP.T; i++){
            this->Neighbor[i] = x.Neighbor[i];
        }
    }
    ~MOEA_D_Solution(){
        delete []port;
        //delete []Neighbor;
    }
    
};
class MOEA_D{
public:
    MOEA_D(struct Constraint &problem, struct asset **dataAsset, struct Lamb*lamb, double mixP){
        this->problem = problem;
        this->assetMin = new int [problem.num_assets];
        this->assetMax = new int [problem.num_assets];
        this->price = new double [problem.num_assets];
        this->pRisk = new double [problem.num_assets];
        this->pIncome = new double [problem.num_assets];
        this->lamb = lamb;
        
        for(int i = 0; i<problem.num_assets; i++){
            this->fundpool+=(*dataAsset)[i].current_price*(*dataAsset)[i].holding;
            assetMax[i] = (*dataAsset)[i].holding+(*dataAsset)[i].max_buy;
            assetMin[i] = (*dataAsset)[i].min_buy;
            totalAsset += assetMax[i];
            price[i] = (*dataAsset)[i].current_price;
            pRisk[i] = (*dataAsset)[i].diviation_r;
            pIncome[i] = (*dataAsset)[i].mean_income;
        }
        this->mix = mixP;
        problem.maxBuy=assetMax;
        problem.minBuy=assetMin;
        MOP=problem;
        generatePartition();
        generatePopulation();
    }
    ~MOEA_D(){
        delete []assetMax;
        delete []assetMin;
        delete []seg;
    }
    void ep2Txt(std::string outPath){
        std::ofstream output;
        output.open(outPath);
        for(int i = 0; i<problem.N; i++){
            output<<EP[i].risk<<"\t"<<EP[i].income<<"\n";
        }
        output.close();
    }
    void epGene2txt(std::string outPath){
        std::ofstream output;
        output.open(outPath);
        for(int i = 0; i<problem.N; i++){
            for(int j = 0; j<EP[i].numPorts; j++){
                output<<EP[i].port[j]<<"\t";
            }
            output<<EP[i].risk<<"\t"<<EP[i].income<<"\n";
        }
        output.close();
    }
    void productionRF(){
        
    }
    void production(int currentG){
        curG = currentG;
        for(int i = 0; i<problem.N; i++){
            int a, b, c;
            a = int(randG()*(problem.T-1));
            b = int(randG()*(problem.T-2));
            if (b>=a){
                b+=1;
            }
            do{
                c=int(randG()*(problem.T-1));
            }while(c==a||c==b);
            MOEA_D_Solution*solution_a = new MOEA_D_Solution();
            *solution_a = EP[lamb[i].neighbor[a]];
            MOEA_D_Solution*solution_b = new MOEA_D_Solution();
            *solution_b = EP[lamb[i].neighbor[b]];
            MOEA_D_Solution*solution_c = new MOEA_D_Solution();
            *solution_c = EP[lamb[i].neighbor[c]];
            
            MOEA_D_Solution*trail = new MOEA_D_Solution();
            //*trail = EP[i];
            
            trail->assign(EP[i]);
            DE(*solution_a, *solution_b, *solution_c, *trail);
            
            //Update Neighbor
            updateNeighbor(trail, lamb[i], z);
            //Update EP
            updateEP(trail);
            //updateEP(trail);
            
            delete solution_a;
            delete solution_b;
            delete solution_c;
        }
    }
    void updateNeighbor(MOEA_D_Solution*x, Lamb&lamb, double z[]){
        double tcheVal = util_tchebycheff(*x, lamb, z);
        double NP=0.7;
        for(int i = 0; i<problem.T; i++){
            if (randG()<NP){
                double tempTche = util_tchebycheff(x->Neighbor[i], lamb, z);
                if(tempTche<=tcheVal){
                    x->Neighbor[i] = *x;
                }
            }
            
        }
    }
    void vEP2txt(std::string outPath){
        std::ofstream output;
        output.open(outPath);
        for(int i = 0; i<vEP.size(); i++){
            output<<vEP[i].risk<<"\t"<<vEP[i].income<<"\n";
        }
        output.close();
    }
    void z2txt(std::string outPath){
        std::ifstream f(outPath.c_str());
        std::ofstream output;
        if(f.good()){
            output.open(outPath, std::ios_base::app);
        }
        else{
            output.open(outPath);
        }
        output<<z[0]<<"\t"<<z[1]<<"\t"<<curG<<"\n";
        output.close();
    }
    void epochEP(std::string outPath){
        epochoutput.open(outPath, std::ofstream::out | std::ofstream::app);
        for(int i = 0; i<vEP.size(); i++){
            epochoutput<<vEP[i].risk<<"\t"<<vEP[i].income<<"\t"<<curG<<"\n";
        }
        epochoutput.close();
    }
    void epochEP_N(std::string outPath){
        epochoutput.open(outPath, std::ofstream::out | std::ofstream::app);
        for(int i = 0; i<problem.N; i++){
            epochoutput<<EP[i].risk<<"\t"<<EP[i].income<<"\t"<<curG<<"\n";
        }
        epochoutput.close();
    }
private:
    struct Constraint problem;
    struct Lamb*lamb;
    double fundpool;
    int totalAsset;
    int *assetMax;
    int *assetMin;
    int *seg;
    double *price;
    double *pRisk;
    double *pIncome;
    MOEA_D_Solution *EP;
    double z[2];
    std::vector<struct EP_Item>vEP;
    std::ofstream epochoutput;
    double mix = 1;
    
    inline void updateZ(MOEA_D_Solution &x){
        if(x.risk<z[0]){
            z[0] = x.risk;
            if(curG<20){
                //z[0] = 0.5*x.risk;
            }
        }
        if(x.income>z[1]){
            z[1] = x.income;
            if(curG<20){
                //z[1] = 2*x.income;
            }
        }
        
    }
    
    void DE(MOEA_D_Solution&a, MOEA_D_Solution&b, MOEA_D_Solution&c, MOEA_D_Solution&trail){
        double CR = 0.2;
        double F = 0.7;
        int R = randG()*problem.num_assets;
        for(int i = 0; i<problem.num_assets; i++){
            double dice = randG();
            if(dice<CR||i==R){
                int geneBuffer;
                geneBuffer = c.port[i] + F * static_cast<double>(a.port[i] - b.port[i]);
                if(geneBuffer<0){
                    geneBuffer = c.port[i] + F * static_cast<double>(b.port[i] - a.port[i]);
                }
                trail.port[i] = geneBuffer;
            }
        }
        //trail.list();
        //std::cout<<"Repair:\n";
        repair(trail);
        //trail.list();
        calFitness(trail);
        updateZ(trail);
    }
    void repair(MOEA_D_Solution&x){
        //Constraint check:
        int baseC = 0;
        for(int i = 0; i<problem.num_assets; i++){
            if(x.port[i]!=0) {
                baseC++;
                if(x.port[i]<assetMin[i]){
                    x.port[i] = assetMin[i];
                }
                if(x.port[i] > assetMax[i]){
                    x.port[i] = assetMax[i];
                }
            }
        }
        if(baseC>problem.max_assets){
            for(int i = 0; i<baseC-problem.max_assets; i++){
                repair_champion(x);
            }
        }
        if(!selfCheck(x)){
            std::cout<<"Not ok\n";
        }
    }
    void repair_champion(MOEA_D_Solution&x){
        std::vector<int>id_localAsset;
        for(int i = 0; i<problem.num_assets; i++){
            if(x.port[i]!=0){
                id_localAsset.push_back(i);
            }
        }
        std::vector<double*>champion;
        for(int i = 0; i<id_localAsset.size(); i++){
            int *localPort = new int[problem.num_assets];
            for(int j = 0; j<problem.num_assets; j++){
                if(j==id_localAsset[i]){
                    localPort[j] = 0;
                    continue;
                }
                localPort[j] = x.port[j];
            }
            double*val=calFitnessMeta(localPort, id_localAsset[i]);
            if(champion.size()==0){
                champion.push_back(val);
                continue;
            }
            bool admission = false;
            for(int j = 0; j<champion.size(); j++){
                if(dominate(val, champion[j])){
                    delete []champion[j];
                    champion.erase(champion.begin()+j);
                    admission = true;
                }
                else{
                    delete [] val;
                    break;
                }
            }
            if(admission)
                champion.push_back(val);
            delete [] localPort;
        }
        //std::cout<<"Champion num: "<<champion.size()<<std::endl;
        int dice = randG()*champion.size();
        for(int i = 0; i<problem.num_assets; i++){
            if(i == int(champion[dice][2])){
                x.port[i] = 0;
                break;
            }
        }
    }
    bool dominate(double*x, double*y){
        if(x[0]<=y[0]&&x[1]>=y[1]) return true;
        return false;
    }
    bool dom(MOEA_D_Solution*x, MOEA_D_Solution*y){
        if((x->risk<y->risk)and(x->income>y->income)){
            return true;
        }
        return false;
    }
    double*calFitnessMeta(int*port, int id){
        double*val = new double[3];
        //val[0] = risk
        //val[1] = income
        for(int i = 0; i<problem.num_assets; i++){
            val[0] += double(port[i])*pRisk[i];
            val[1] += double(port[i])*pIncome[i];
        }
        val[2] = double(id);
        return val;
    }
    bool buyAsset(int*port, double&fund, int id, int num){
        if(num*price[id]>fund){
            if(fund/price[id]>assetMin[id]){
                num = fund/price[id];
            }
        }
        if(num==0){
            return false;
        }
        port[id] +=num;
        fund-=num*price[id];
        return true;
    }
    void nsga_fundDistribute(int*p, std::vector<int>&toBuy, double&fund, int n, int mode){
        int id = toBuy[n];
        if(p[id]==assetMax[id]){
            bool buyable;
        check:
            std::vector<int>tempBuy;
            buyable = false;
            for(int i = 0; i<toBuy.size(); i++){
                if((p[toBuy[i]]<assetMax[toBuy[i]])and(fund>0)){
                    tempBuy.push_back(toBuy[i]);
                    buyable = true;
                }
            }
            if(tempBuy.size()>0){
                for(int i = 0; i<tempBuy.size(); i++){
                    nsga_fundDistribute(p, toBuy, fund, tempBuy[i], 0);
                }
            }
            if(buyable) goto check;
            return;
        }
        
        int numBuy = randG()*(assetMax[id]-p[id]);
        if(fund<numBuy*price[id]){
            numBuy=fund/price[id];
        }
        fund-=numBuy*price[id];
        p[id]+=numBuy;
        if(n<=0||mode==1){
        rn:
            nsga_fundDistribute(p, toBuy, fund, int(randG()*(toBuy.size()-1)), 1);
        }
        else{
            nsga_fundDistribute(p, toBuy, fund, n-1, 0);
        }
    }
    void fundDistribute(int*port, double&fund, std::vector<int>toBuy){
        std::vector<int>flag;
        for(int i = 0; i<toBuy.size(); i++){
            flag.push_back(1);
        }
        for(int i = 0; i<toBuy.size(); i++){
            int buyNum = int(randG()*(assetMax[toBuy[i]] - port[toBuy[i]]));
            buyAsset(port, fund, toBuy[i], buyNum);
            if(port[toBuy[i]]==assetMax[toBuy[i]]){
                flag[i] = 0;
            }
        }
        std::vector<int>::iterator stop = std::find(flag.begin(), flag.end(), 1);
        while(stop!=flag.end() and fund>0){
            int id = std::distance(flag.begin(), stop);
            int buyID = toBuy[id];
            int buyNum = int(randG()*(assetMax[buyID] - port[buyID]));
            if(buyAsset(port, fund, buyID, buyNum)){
                if(port[buyID]==assetMax[buyID]){
                    flag[id] = 0;
                }
            }
            else
            {
                flag[id] = 0;
            }
            stop = std::find(flag.begin(), flag.end(), 1);
        }
    }
    void randomHighland(MOEA_D_Solution*x){
        double localFund = fundpool;
        std::vector<int>toBuy;
        for(int i = 0; i<problem.max_assets; i++){
            int buyID = int(randG()*(problem.num_assets+1));
            if(buyID>=problem.num_assets){
                buyID = -1;
                continue;
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
        nsga_fundDistribute(x->port, toBuy, localFund, toBuy.size()-1, 0);
        //fundDistribute(x->port, localFund, toBuy);
    }
    void generatePopulation(){
        int size = problem.N;
        //std::cout<<"Population: "<<size<<std::endl;
        MOEA_D_Solution *population = new MOEA_D_Solution[size];

        for(int i = 0; i<int(size*mix); i++){
            selectedRandom(population[i]);
            //population[i].list();
            calFitness(population[i]);
            
            //Initialize Z
            if(i == 0){
                z[0] = population[0].risk;
                z[1] = population[0].income;
            }
            if(z[0]<2){
                z[0] = population[i+1].risk;
            }
            updateZ(population[i]);
        }
        std::string resourcePath = "/Users/meow/Desktop/DP/MOEA-D/Resource/10000.txt";
        loadGene(resourcePath, population, int(size*mix), size);
        for(int i = int(size*mix); i<size; i++){
            //randomHighland(&population[i]);
            
            calFitness(population[i]);
            updateZ(population[i]);
        }
        initNeighbor(population);
        this->EP = population;
        initEP(population);
    }
    void mixPopulation(){
        
    }
    void initNeighbor(MOEA_D_Solution*population){
        for(int i = 0; i<problem.N; i++){
            for(int j = 0; j<problem.T; j++){
                population[i].Neighbor[j] = population[lamb[i].neighbor[j]];
            }
        }
    }
    void initEP(MOEA_D_Solution*population){
        for(int i = 0; i<problem.N; i++){
            EP_Item tempEP = EP_Item(population[i]);
            vEP.push_back(tempEP);
        }
    }
    void updateEP(MOEA_D_Solution*x){
        bool dominated = false;
        for (std::vector<EP_Item>::iterator it=vEP.begin(); it!=vEP.end();)
        {
            if((it->risk>x->risk)and(it->income<x->income)){
                it = vEP.erase(it);
            }
            else{
                if((it->risk<x->risk)and(it->income>x->income)) {
                    dominated = true;
                    break;
                }
                ++it;
                }
            
        }
        if(!dominated){
            vEP.push_back(EP_Item(*x));
        }
        for(int i = 0; i<problem.N; i++){
            if(dom(x, &EP[i])){
                EP[i] = *x;
            }
        }
    }
    void generatePartition(){
        seg = new int[problem.num_assets];
        for(int i = 0; i<problem.num_assets; i++){
            if(i>0){
                seg[i] = seg[i-1] + assetMax[i];
            }
            else{
                seg[i] = assetMax[i];
            }
            //std::cout<<seg[i]<<" ";
        }
        //std::cout<<"\n";
    }
    
    bool selfCheck(const MOEA_D_Solution&x){
        for(int i = 0; i<MOP.num_assets; i++){
            if(x.port[i] == 0)    continue;
            if(x.port[i]>MOP.maxBuy[i]||x.port[i]<MOP.minBuy[i]){
                std::cout<<x.port[i]<<" MAX: "<<MOP.maxBuy[i]<<" MIN: "<< MOP.minBuy[i]<<std::endl;
                return false;
            }
        }
        return true;
    }
    void loadGene(std::string path, MOEA_D_Solution*extendGene, int startid, int numP);
    void calFitness(MOEA_D_Solution&x){
        double local_risk = 0;
        double local_income = 0;
        for(int i = 0; i<problem.num_assets; i++){
            local_risk += double(x.port[i])*pRisk[i];
            local_income += double(x.port[i])*pIncome[i];
        }
        x.income = local_income;
        x.risk = local_risk;
    }
    double util_tchebycheff(const struct Solution &x, const struct Lamb&lb, const double z[]){
        double result;
        double*temp = new double[2];
        temp[0] = pow((x.risk-z[0]), 0.3)*lb.lamb[0];
        temp[1] = (x.income-z[1])*lb.lamb[1];
        
        if(temp[0]<0) temp[0] = -temp[0];
        if(temp[1]<0) temp[1] = -temp[1];
        result = max(temp[0], temp[1]);
        delete [] temp;
        return result;
    }
    //@Note Plan I
    //Generate a number for overall.
    //Distribute fund respected to partition.
    void random(MOEA_D_Solution&x){
        for(int i = 0; i<problem.max_assets; i++){
            int dice = static_cast<int>(randG()*double(totalAsset));
            int buyWhich;
            int buyNum;
            for(int j = 0; j<problem.num_assets; j++){
                if(dice>seg[j])    continue;
                else{
                    buyWhich = j;
                    buyNum = dice-seg[j-1];
                    if(buyNum<assetMin[j]){
                        buyWhich = j-1;
                        buyNum = assetMax[j-1];
                    }
                    x.port[buyWhich] = buyNum;
                    break;
                }
            }
        }
    };
    void selectedRandom(MOEA_D_Solution&x){
        int localFund = fundpool;
        
        for(int i = 0; i<problem.max_assets; i++){
            int buyWhich, buyNum;
            //Choose which to buy.
            int dice = static_cast<int>(randG()*double(problem.num_assets+1));
            if(dice == problem.num_assets)    continue;//Not buy;
            buyWhich = dice;
            
            //Decide how many to buy.
            int numBuy = static_cast<int>(randG()*double(assetMax[buyWhich]));
            
            if (numBuy<assetMin[buyWhich])    numBuy = assetMin[buyWhich];
            
            if (x.port[buyWhich]+numBuy>assetMax[buyWhich]){
                numBuy = assetMax[buyWhich]-x.port[buyWhich];
            }
            
            if (localFund-numBuy*price[i]<0){
                numBuy = localFund/price[i];
            }
            localFund -=numBuy*price[i];
            if (x.port[buyWhich]!=0)
                numBuy +=x.port[buyWhich];
            x.port[buyWhich] = numBuy;
        }
    }
};

void lamb2txt(Lamb*x, int sizeLamb, int sizeNeighbor){
    std::ofstream output;
    std::string outPath = "/Users/meow/Desktop/DP/Code/Output/lamb.txt";
    output.open(outPath);
    for(int i = 0; i<sizeLamb; i++){
        output<<x[i].lamb[0]<<std::setw(12)<<x[i].lamb[1]<<"\t";
        for(int j = 0; j<sizeNeighbor; j++){
            output<<x[i].neighbor[j]<<"\t";
        }
        output<<"\n";
    }
    output.close();
}
//MOEA_D Operation
int * calDistance(int index, int sizeLamb, int sizeNeighbor){
    int *neighbor = new int[sizeNeighbor];
    if(index<sizeNeighbor/2){
        for(int i = 0; i<sizeNeighbor; i++){
            neighbor[i] = i;
        }
        return neighbor;
    }
    else{
        if (index<sizeLamb-sizeNeighbor){
            for(int i = 0; i<sizeNeighbor; i++){
                neighbor[i] = index-sizeNeighbor/2+i;
            }
            return neighbor;
        }
        else{
            for(int i = 0; i<sizeNeighbor; i++){
                neighbor[i] = sizeLamb - sizeNeighbor + i;
            }
            return neighbor;
        }
    }
}
EP_Item::EP_Item(MOEA_D_Solution x){
    this->risk = x.risk;
    this->income = x.income;
}
struct Lamb* init_lamb(int sizeLamb, int sizeNeighbor){
    //@Todo Uniform sample
    struct Lamb*lptr = new struct Lamb[sizeLamb];
    for(int i = 0; i<sizeLamb; i++){
        lptr[i].lamb[0] = static_cast<double>(i)/static_cast<double>(sizeLamb-1);
        lptr[i].lamb[1] = 1-lptr[i].lamb[0];
        lptr[i].neighbor = calDistance(i, sizeLamb, sizeNeighbor);
    }
    //lamb2txt(lptr, sizeLamb, sizeNeighbor);
    return lptr;
}

void Neighbor_Solution::operator=(const MOEA_D_Solution &x){
    this->numPorts = x.numPorts;
    if(this->port == nullptr){
        port = new int[numPorts];
    }
    for(int i = 0; i<numPorts; i++){
        this->port[i] = x.port[i];
    }
}
void MOEA_D::loadGene(std::string path, MOEA_D_Solution*extendGene, int startid, int numP){
    std::fstream data(path, std::ios::in);
    std::string input_cache;
    int line = 0;
    if (!data.is_open()){
        std::cout<<"[Error]:\tCANNOT OPEN FILE\n";
        std::cout<<"\t FILE PATH: "<<path<<std::endl;
        std::exit(9);
    }
    int index = startid;
    while( std::getline(data, input_cache) and index<numP){
        if(input_cache.length()<=1){
            continue;
        }
        std::istringstream line_cache(input_cache);
        if(line == 0){
            line+=1;
            continue;
        }
        else if(line%20==0){
            std::string field;
            std::vector<int>gene;
            while(std::getline(line_cache, field, '\t')){
                gene.push_back(std::stoi(field));
            }
            for(int i = 0; i<gene.size()-2; i++){
                extendGene[index].port[i] = gene[i];
            }
            index+=1;
        }
        line++;
    }
}
