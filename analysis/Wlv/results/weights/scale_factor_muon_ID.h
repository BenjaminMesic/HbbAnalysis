double scale_factor_muon_ID(double eta, double pt, int lepton_pdgID)
{
  if (abs(lepton_pdgID) != 13)
    return 1;

  if (pt > 60.0 && pt < 120.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.974912124872;
    if (eta > 0.0 && eta < 0.9)
      return 0.992158982158;
    if (eta > 1.2 && eta < 2.1)
      return 0.988777202368;
    if (eta > 2.1 && eta < 2.4)
      return 0.963148453832;
    else
      return 1;
  }
  if (pt > 25.0 && pt < 30.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.970736426115;
    if (eta > 0.0 && eta < 0.9)
      return 0.983006241918;
    if (eta > 1.2 && eta < 2.1)
      return 0.986154904962;
    if (eta > 2.1 && eta < 2.4)
      return 0.973938322067;
    else
      return 1;
  }
  if (pt > 30.0 && pt < 40.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.973600694537;
    if (eta > 0.0 && eta < 0.9)
      return 0.984384050965;
    if (eta > 1.2 && eta < 2.1)
      return 0.987878718972;
    if (eta > 2.1 && eta < 2.4)
      return 0.969469454885;
    else
      return 1;
  }
  if (pt > 20.0 && pt < 25.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.972429051995;
    if (eta > 0.0 && eta < 0.9)
      return 0.986356261373;
    if (eta > 1.2 && eta < 2.1)
      return 0.986309170723;
    if (eta > 2.1 && eta < 2.4)
      return 0.975301507115;
    else
      return 1;
  }
  if (pt > 50.0 && pt < 60.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.974562454224;
    if (eta > 0.0 && eta < 0.9)
      return 0.981909179688;
    if (eta > 1.2 && eta < 2.1)
      return 0.98543818891;
    if (eta > 2.1 && eta < 2.4)
      return 0.967713272572;
    else
      return 1;
  }
  if (pt > 40.0 && pt < 50.0)
  {
    if (eta > 0.9 && eta < 1.2)
      return 0.974862366915;
    if (eta > 0.0 && eta < 0.9)
      return 0.985897368193;
    if (eta > 1.2 && eta < 2.1)
      return 0.990529999137;
    if (eta > 2.1 && eta < 2.4)
      return 0.97257258594;
    else
      return 1;
  }
  else
   return 1;
}
