double scale_factor_electron_trk(double eta, double pt, int lepton_pdgID)
{
  if (abs(lepton_pdgID) != 11)
    return 1;

  if (eta > 1.8 && eta < 2.0)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.992;
    else
      return 1;
  }
  if (eta > 2.2 && eta < 2.3)
  {
    if (pt > 25.0 && pt < 500.0)
      return 1.001;
    else
      return 1;
  }
  if (eta > -2.3 && eta < -2.2)
  {
    if (pt > 25.0 && pt < 500.0)
      return 1.014;
    else
      return 1;
  }
  if (eta > 1.2 && eta < 1.444)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.988;
    else
      return 1;
  }
  if (eta > 2.3 && eta < 2.4)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.99;
    else
      return 1;
  }
  if (eta > -2.2 && eta < -2.0)
  {
    if (pt > 25.0 && pt < 500.0)
      return 1.007;
    else
      return 1;
  }
  if (eta > 1.63 && eta < 1.8)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.993;
    else
      return 1;
  }
  if (eta > -0.6 && eta < -0.4)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.985;
    else
      return 1;
  }
  if (eta > -2.5 && eta < -2.45)
  {
    if (pt > 25.0 && pt < 500.0)
      return 1.318;
    else
      return 1;
  }
  if (eta > 0.0 && eta < 0.2)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.985;
    else
      return 1;
  }
  if (eta > 0.6 && eta < 1.0)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.988;
    else
      return 1;
  }
  if (eta > -2.4 && eta < -2.3)
  {
    if (pt > 25.0 && pt < 500.0)
      return 1.025;
    else
      return 1;
  }
  if (eta > -1.444 && eta < -1.2)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.99;
    else
      return 1;
  }
  if (eta > 2.4 && eta < 2.45)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.971;
    else
      return 1;
  }
  if (eta > -2.0 && eta < -1.8)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.995;
    else
      return 1;
  }
  if (eta > 1.566 && eta < 1.63)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.99;
    else
      return 1;
  }
  if (eta > 0.2 && eta < 0.4)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.989;
    else
      return 1;
  }
  if (eta > -1.566 && eta < -1.444)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.963;
    else
      return 1;
  }
  if (eta > 1.444 && eta < 1.566)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.968;
    else
      return 1;
  }
  if (eta > -1.63 && eta < -1.566)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.992;
    else
      return 1;
  }
  if (eta > -1.2 && eta < -1.0)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.986;
    else
      return 1;
  }
  if (eta > -2.45 && eta < -2.4)
  {
    if (pt > 25.0 && pt < 500.0)
      return 1.114;
    else
      return 1;
  }
  if (eta > 2.45 && eta < 2.5)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.907;
    else
      return 1;
  }
  if (eta > -0.4 && eta < -0.2)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.982;
    else
      return 1;
  }
  if (eta > -1.8 && eta < -1.63)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.995;
    else
      return 1;
  }
  if (eta > 0.4 && eta < 0.6)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.988;
    else
      return 1;
  }
  if (eta > -1.0 && eta < -0.6)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.982;
    else
      return 1;
  }
  if (eta > -0.2 && eta < 0.0)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.98;
    else
      return 1;
  }
  if (eta > 2.0 && eta < 2.2)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.998;
    else
      return 1;
  }
  if (eta > 1.0 && eta < 1.2)
  {
    if (pt > 25.0 && pt < 500.0)
      return 0.988;
    else
      return 1;
  }
  else
    return 1; 
}