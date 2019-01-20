double scale_factor_muon_iso(double eta, double pt, int lepton_pdgID)
{
  if (abs(lepton_pdgID) != 13)
    return 1;

  if (pt > 60.0 && pt < 120.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.999122050405;
    if (eta > 0.0 && eta < 0.9)
      return 0.998780176044;
    if (eta > 1.2 && eta < 2.1)
      return 0.999213159084;
    if (eta > 2.1 && eta < 2.4)
      return 1.0015225172;
    else
      return 1;
  }
  if (pt > 25.0 && pt < 30.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 1.00042890608;
    if (eta > 0.0 && eta < 0.9)
      return 0.99330933094;
    if (eta > 1.2 && eta < 2.1)
      return 0.995904949307;
    if (eta > 2.1 && eta < 2.4)
      return 0.991872668266;
    else
      return 1;
  }
  if (pt > 30.0 && pt < 40.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.999431717396;
    if (eta > 0.0 && eta < 0.9)
      return 0.993782183528;
    if (eta > 1.2 && eta < 2.1)
      return 0.997964453697;
    if (eta > 2.1 && eta < 2.4)
      return 0.996224096417;
    else
      return 1;
  }
  if (pt > 20.0 && pt < 25.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.995186954737;
    if (eta > 0.0 && eta < 0.9)
      return 0.984762614965;
    if (eta > 1.2 && eta < 2.1)
      return 0.991503226757;
    if (eta > 2.1 && eta < 2.4)
      return 0.983842265606;
    else
      return 1;
  }
  if (pt > 50.0 && pt < 60.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.999143999815;
    if (eta > 0.0 && eta < 0.9)
      return 0.996805244684;
    if (eta > 1.2 && eta < 2.1)
      return 0.998344343901;
    if (eta > 2.1 && eta < 2.4)
      return 0.998602291942;
    else
      return 1;
  }
  if (pt > 40.0 && pt < 50.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.997694447637;
    if (eta > 0.0 && eta < 0.9)
      return 0.995297423005;
    if (eta > 1.2 && eta < 2.1)
      return 0.998013055325;
    if (eta > 2.1 && eta < 2.4)
      return 0.998322731256;
    else
      return 1;
  }
  else
   return 1;
}
