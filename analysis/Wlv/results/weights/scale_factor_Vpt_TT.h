// AN2016: page 43 0.000380 ± 0.000089
float scale_factor_Vpt_TT(float V_pt, float variation){
  // variation for up/down
  return 1.0 - (0.000380 + variation)*V_pt;

}