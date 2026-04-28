#include <stdio.h>
#include "constant.h"
#include "particle.h"
#include "formulae.h"


int
main()
{
    /*
    make_particle("name"             , "symbol"  ,eps, k , P , Q ,kap, x , m_exp      );
     */

    make_particle("neutral electron" , "e_0"     , 1 , 1 , 1 , 1 , 0 , 0 ,   0.00000000);
    make_particle("electron"         , "e_-"     , 1 , 1 , 1 , 1 , 0 , 1 ,   0.51099907);
    make_particle("muon"             , "miu_-"   , 1 , 1 , 1 , 1 , 1 , 0 ,  105.6583890);

    make_particle("eta"              , "eta"     , 1 , 1 , 0 , 0 , 0 , 0 ,  547.3000000);
    make_particle("charged kaon"     , "KAPPA_+" , 1 , 1 , 1 , 0 , 1 , 0 ,  493.6770000);
    make_particle("neutral kaon"     , "KAPPA_0" , 1 , 1 , 1 , 0 , 1 , 1 ,  497.6720000);
    make_particle("charged pion"     , "pi_+-"   , 1 , 1 , 2 , 0 , 0 , 0 ,  139.5701800);
    make_particle("neutral pion"     , "pi_0"    , 1 , 1 , 2 , 0 , 0 , 1 ,  134.9766000);

    make_particle("lambda"           , "LAMBDA"  , 1 , 2 , 0 , 1 , 0 , 0 , 1115.6830000);
    make_particle("omega"            , "OMEGA_-" , 1 , 2 , 0 , 3 , 0 , 0 , 1672.4500000);
    make_particle("proton"           , "p"       , 1 , 2 , 1 , 1 , 0 , 0 ,  938.2723100);
    make_particle("neutron"          , "n"       , 1 , 2 , 1 , 1 , 0 , 1 ,  939.5656300);
    make_particle("neutral xi"       , "XI_0"    , 1 , 2 , 1 , 1 , 1 , 0 , 1314.9000000);
    make_particle("charged xi"       , "XI_-"    , 1 , 2 , 1 , 1 , 1 , 1 , 1321.3200000);
    make_particle("positive sigma"   , "SIGMA_+" , 1 , 2 , 2 , 1 , 0 , 0 , 1189.3700000);
    make_particle("neutral sigma"    , "SIGMA_0" , 1 , 2 , 2 , 1 , 0 , 1 , 1192.6420000);
    make_particle("negative sigma"   , "SIGMA_-" , 1 , 2 , 2 , 1 , 0 , 2 , 1197.4490000);
    make_particle("2 charged delta"  , "DELTA_++", 1 , 2 , 3 , 3 , 0 , 0 , 1232.0000000);
    make_particle("positive delta"   , "DELTA_+" , 1 , 2 , 3 , 3 , 0 , 1 , 1232.0000000);
    make_particle("neutral delta"    , "DELTA_0" , 1 , 2 , 3 , 3 , 0 , 2 , 1232.0000000);
    make_particle("negative delta"   , "DELTA_-" , 1 , 2 , 3 , 3 , 0 , 3 , 1232.0000000);

    stat_constants(stdout);
    stat_formulaes(stdout, particle_list);
    stat_particles(stdout);

    return 0;
}
