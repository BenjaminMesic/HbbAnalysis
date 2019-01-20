double scale_factor_muon_trigger(double eta, double pt, int lepton_pdgID)
{
  if (abs(lepton_pdgID) != 13)
    return 1;

  if (pt > 60.0 && pt < 120.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.964894166589;
    if (eta > 0.0 && eta < 0.9)
      return 0.983891037107;
    if (eta > 1.2 && eta < 2.1)
      return 0.998933911324;
    if (eta > 2.1 && eta < 2.4)
      return 0.952402967215;
    else
      return 1;
  }
  if (pt > 30.0 && pt < 40.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.965955582261;
    if (eta > 0.0 && eta < 0.9)
      return 0.984091502428;
    if (eta > 1.2 && eta < 2.1)
      return 0.995479756594;
    if (eta > 2.1 && eta < 2.4)
      return 0.944552755356;
    else
      return 1;
  }
  if (pt > 200.0 && pt < 500.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.949587833881;
    if (eta > 0.0 && eta < 0.9)
      return 0.983277073503;
    if (eta > 1.2 && eta < 2.1)
      return 0.982793581486;
    if (eta > 2.1 && eta < 2.4)
      return 0.91809155941;
    else
      return 1;
  }
  if (pt > 120.0 && pt < 200.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.946718859673;
    if (eta > 0.0 && eta < 0.9)
      return 0.976027205586;
    if (eta > 1.2 && eta < 2.1)
      return 1.00552132726;
    if (eta > 2.1 && eta < 2.4)
      return 0.977005371451;
    else
      return 1;
  }
  if (pt > 26.0 && pt < 30.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.956332758069;
    if (eta > 0.0 && eta < 0.9)
      return 0.980353054404;
    if (eta > 1.2 && eta < 2.1)
      return 0.982502600551;
    if (eta > 2.1 && eta < 2.4)
      return 0.906210771203;
    else
      return 1;
  }
  if (pt > 50.0 && pt < 60.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.968170365691;
    if (eta > 0.0 && eta < 0.9)
      return 0.985117459297;
    if (eta > 1.2 && eta < 2.1)
      return 0.99911839962;
    if (eta > 2.1 && eta < 2.4)
      return 0.960392948985;
    else
      return 1;
  }
  if (pt > 40.0 && pt < 50.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.967854008079;
    if (eta > 0.0 && eta < 0.9)
      return 0.984899061918;
    if (eta > 1.2 && eta < 2.1)
      return 0.999197807908;
    if (eta > 2.1 && eta < 2.4)
      return 0.957528609037;
    else
      return 1;
  }
  else
   return 1;
}
