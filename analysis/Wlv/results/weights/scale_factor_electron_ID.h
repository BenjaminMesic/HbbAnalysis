double scale_factor_electron_ID(double eta, double pt, int lepton_pdgID)
{
  if (abs(lepton_pdgID) != 11)
    return 1;

  if (eta >  1.57 && eta <  1.80)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.83;
    if (pt > 32.00 && pt < 35.00)
      return 0.864;
    if (pt > 35.00 && pt < 40.00)
      return 0.882;
    if (pt > 27.00 && pt < 30.00)
      return 0.856;
    if (pt > 40.00 && pt < 50.00)
      return 0.9;
    if (pt > 30.00 && pt < 32.00)
      return 0.851;
    if (pt > 50.00 && pt < 200.00)
      return 0.917;
    else
      return 1;
  }
  if (eta >  1.44 && eta <  1.57)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0;
    if (pt > 32.00 && pt < 35.00)
      return 0;
    if (pt > 35.00 && pt < 40.00)
      return 0;
    if (pt > 27.00 && pt < 30.00)
      return 0;
    if (pt > 40.00 && pt < 50.00)
      return 0;
    if (pt > 30.00 && pt < 32.00)
      return 0;
    if (pt > 50.00 && pt < 200.00)
      return 0;
    else
      return 1;
  }
  if (eta > -2.17 && eta < -1.80)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.771;
    if (pt > 32.00 && pt < 35.00)
      return 0.801;
    if (pt > 35.00 && pt < 40.00)
      return 0.824;
    if (pt > 27.00 && pt < 30.00)
      return 0.766;
    if (pt > 40.00 && pt < 50.00)
      return 0.853;
    if (pt > 30.00 && pt < 32.00)
      return 0.799;
    if (pt > 50.00 && pt < 200.00)
      return 0.889;
    else
      return 1;
  }
  if (eta >  0.80 && eta <  1.44)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.867;
    if (pt > 32.00 && pt < 35.00)
      return 0.892;
    if (pt > 35.00 && pt < 40.00)
      return 0.903;
    if (pt > 27.00 && pt < 30.00)
      return 0.886;
    if (pt > 40.00 && pt < 50.00)
      return 0.913;
    if (pt > 30.00 && pt < 32.00)
      return 0.886;
    if (pt > 50.00 && pt < 200.00)
      return 0.919;
    else
      return 1;
  }
  if (eta > -1.57 && eta < -1.44)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0;
    if (pt > 32.00 && pt < 35.00)
      return 0;
    if (pt > 35.00 && pt < 40.00)
      return 0;
    if (pt > 27.00 && pt < 30.00)
      return 0;
    if (pt > 40.00 && pt < 50.00)
      return 0;
    if (pt > 30.00 && pt < 32.00)
      return 0;
    if (pt > 50.00 && pt < 200.00)
      return 0;
    else
      return 1;
  }
  if (eta > -1.44 && eta < -0.80)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.851;
    if (pt > 32.00 && pt < 35.00)
      return 0.889;
    if (pt > 35.00 && pt < 40.00)
      return 0.893;
    if (pt > 27.00 && pt < 30.00)
      return 0.882;
    if (pt > 40.00 && pt < 50.00)
      return 0.904;
    if (pt > 30.00 && pt < 32.00)
      return 0.883;
    if (pt > 50.00 && pt < 200.00)
      return 0.909;
    else
      return 1;
  }
  if (eta > -2.50 && eta < -2.17)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.788;
    if (pt > 32.00 && pt < 35.00)
      return 0.774;
    if (pt > 35.00 && pt < 40.00)
      return 0.791;
    if (pt > 27.00 && pt < 30.00)
      return 0.774;
    if (pt > 40.00 && pt < 50.00)
      return 0.828;
    if (pt > 30.00 && pt < 32.00)
      return 0.797;
    if (pt > 50.00 && pt < 200.00)
      return 0.864;
    else
      return 1;
  }
  if (eta > -0.80 && eta <  0.00)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.862;
    if (pt > 32.00 && pt < 35.00)
      return 0.889;
    if (pt > 35.00 && pt < 40.00)
      return 0.895;
    if (pt > 27.00 && pt < 30.00)
      return 0.875;
    if (pt > 40.00 && pt < 50.00)
      return 0.899;
    if (pt > 30.00 && pt < 32.00)
      return 0.886;
    if (pt > 50.00 && pt < 200.00)
      return 0.904;
    else
      return 1;
  }
  if (eta >  2.17 && eta <  2.50)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.709;
    if (pt > 32.00 && pt < 35.00)
      return 0.748;
    if (pt > 35.00 && pt < 40.00)
      return 0.771;
    if (pt > 27.00 && pt < 30.00)
      return 0.713;
    if (pt > 40.00 && pt < 50.00)
      return 0.792;
    if (pt > 30.00 && pt < 32.00)
      return 0.72;
    if (pt > 50.00 && pt < 200.00)
      return 0.848;
    else
      return 1;
  }
  if (eta > -1.80 && eta < -1.57)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.836;
    if (pt > 32.00 && pt < 35.00)
      return 0.859;
    if (pt > 35.00 && pt < 40.00)
      return 0.869;
    if (pt > 27.00 && pt < 30.00)
      return 0.844;
    if (pt > 40.00 && pt < 50.00)
      return 0.892;
    if (pt > 30.00 && pt < 32.00)
      return 0.869;
    if (pt > 50.00 && pt < 200.00)
      return 0.917;
    else
      return 1;
  }
  if (eta >  1.80 && eta <  2.17)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.791;
    if (pt > 32.00 && pt < 35.00)
      return 0.828;
    if (pt > 35.00 && pt < 40.00)
      return 0.852;
    if (pt > 27.00 && pt < 30.00)
      return 0.793;
    if (pt > 40.00 && pt < 50.00)
      return 0.87;
    if (pt > 30.00 && pt < 32.00)
      return 0.814;
    if (pt > 50.00 && pt < 200.00)
      return 0.904;
    else
      return 1;
  }
  if (eta >  0.00 && eta <  0.80)
  {
    if (pt > 25.00 && pt < 27.00)
      return 0.903;
    if (pt > 32.00 && pt < 35.00)
      return 0.926;
    if (pt > 35.00 && pt < 40.00)
      return 0.933;
    if (pt > 27.00 && pt < 30.00)
      return 0.921;
    if (pt > 40.00 && pt < 50.00)
      return 0.935;
    if (pt > 30.00 && pt < 32.00)
      return 0.924;
    if (pt > 50.00 && pt < 200.00)
      return 0.94;
    else
      return 1;
  }
  else
    return 1; 
}