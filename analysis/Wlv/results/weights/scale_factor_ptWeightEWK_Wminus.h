// Vuko gave on 5 Sep, 2018
// WmH:
// p0                        =     0.954747   +/-   0.190121    
// p1                        =  -0.00039735   +/-   0.000640062 

float scale_factor_ptWeightEWK_Wminus(float GenVbosons_pt){

  return 0.9547 - 0.000397*GenVbosons_pt;

}