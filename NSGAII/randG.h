//
// Created by molin on 17-11-6.
//

#ifndef RANDG_H
#define RANDG_H

#include <ctime>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
//Debug scope

double randG(){
    clock_t t;
    t = clock();
    //std::cout<<t<<std::endl;
    static int counter = 3;
    int seed = counter+t;
    gsl_rng * engine = gsl_rng_alloc(gsl_rng_taus);

    gsl_rng_set( engine, seed);
    double lambda = gsl_rng_uniform(engine);
    gsl_rng_free(engine);
    counter ++;

    //@Todo: Consider parallism computing
    return lambda;
}


#endif //MOEA_D_RANDG_H
