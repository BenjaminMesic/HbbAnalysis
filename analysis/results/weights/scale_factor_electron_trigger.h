double scale_factor_electron_trigger(double eta, double pt, int lepton_pdgID )
{
  if (abs(lepton_pdgID) != 11)
    return 1;

  if (eta > -2.17 && eta < -1.80)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.816;
    if (pt > 30.00 && pt < 35.00)
      return 0.97;
    if (pt > 50.00 && pt < 200.00)
      return 0.964;
    if (pt > 40.00 && pt < 50.00)
      return 0.982;
    if (pt > 35.00 && pt < 40.00)
      return 0.976;
    else
      return 1;
  }
  if (eta > -1.57 && eta < -1.44)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0;
    if (pt > 30.00 && pt < 35.00)
      return 0;
    if (pt > 50.00 && pt < 200.00)
      return 0;
    if (pt > 40.00 && pt < 50.00)
      return 0;
    if (pt > 35.00 && pt < 40.00)
      return 0;
    else
      return 1;
  }
  if (eta >  0.80 && eta <  1.44)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.831;
    if (pt > 30.00 && pt < 35.00)
      return 0.955;
    if (pt > 50.00 && pt < 200.00)
      return 0.997;
    if (pt > 40.00 && pt < 50.00)
      return 0.997;
    if (pt > 35.00 && pt < 40.00)
      return 0.985;
    else
      return 1;
  }
  if (eta >  0.00 && eta <  0.80)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.851;
    if (pt > 30.00 && pt < 35.00)
      return 0.964;
    if (pt > 50.00 && pt < 200.00)
      return 0.998;
    if (pt > 40.00 && pt < 50.00)
      return 1.008;
    if (pt > 35.00 && pt < 40.00)
      return 0.994;
    else
      return 1;
  }
  if (eta > -1.80 && eta < -1.57)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.829;
    if (pt > 30.00 && pt < 35.00)
      return 0.936;
    if (pt > 50.00 && pt < 200.00)
      return 0.967;
    if (pt > 40.00 && pt < 50.00)
      return 0.966;
    if (pt > 35.00 && pt < 40.00)
      return 0.949;
    else
      return 1;
  }
  if (eta > -1.44 && eta < -0.80)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.86;
    if (pt > 30.00 && pt < 35.00)
      return 0.963;
    if (pt > 50.00 && pt < 200.00)
      return 0.995;
    if (pt > 40.00 && pt < 50.00)
      return 1.001;
    if (pt > 35.00 && pt < 40.00)
      return 0.988;
    else
      return 1;
  }
  if (eta > -0.80 && eta <  0.00)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.863;
    if (pt > 30.00 && pt < 35.00)
      return 0.969;
    if (pt > 50.00 && pt < 200.00)
      return 1.007;
    if (pt > 40.00 && pt < 50.00)
      return 1.016;
    if (pt > 35.00 && pt < 40.00)
      return 1.001;
    else
      return 1;
  }
  if (eta >  1.44 && eta <  1.57)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0;
    if (pt > 30.00 && pt < 35.00)
      return 0;
    if (pt > 50.00 && pt < 200.00)
      return 0;
    if (pt > 40.00 && pt < 50.00)
      return 0;
    if (pt > 35.00 && pt < 40.00)
      return 0;
    else
      return 1;
  }
  if (eta >  1.80 && eta <  2.17)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.693;
    if (pt > 30.00 && pt < 35.00)
      return 0.902;
    if (pt > 50.00 && pt < 200.00)
      return 0.955;
    if (pt > 40.00 && pt < 50.00)
      return 0.958;
    if (pt > 35.00 && pt < 40.00)
      return 0.941;
    else
      return 1;
  }
  if (eta >  1.57 && eta <  1.80)
  {
    if (pt > 27.00 && pt < 30.00)
      return 0.81;
    if (pt > 30.00 && pt < 35.00)
      return 0.919;
    if (pt > 50.00 && pt < 200.00)
      return 0.969;
    if (pt > 40.00 && pt < 50.00)
      return 0.97;
    if (pt > 35.00 && pt < 40.00)
      return 0.961;
    else
      return 1;
  }
  else
    return 1; 
}