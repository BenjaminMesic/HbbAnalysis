// Vuko gave on 5 Sep, 2018
// Wph:
// p0                        =     0.949331   +/-   0.289202    
// p1                        = -0.000381705   +/-   0.000884053 

float scale_factor_ptWeightEWK_Wplus(float GenVbosons_pt){

  return 0.9493 - 0.000381*GenVbosons_pt;

}