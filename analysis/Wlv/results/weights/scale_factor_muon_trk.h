double scale_factor_muon_trk(double eta, double pt, int lepton_pdgID)
{
  if (abs(lepton_pdgID) != 13)
    return 1;

  if (pt > 0.0 && pt < 10000.0)
  {
    if (eta > 0.3 && eta < 0.6)
      return 0.998722302055;
    if (eta > 1.2 && eta < 1.6)
      return 0.995418297975;
    if (eta > 0.9 && eta < 1.2)
      return 0.997707970249;
    if (eta > 0.2 && eta < 0.3)
      return 0.997948453688;
    if (eta > -2.4 && eta < -2.1)
      return 0.992280202395;
    if (eta > 1.6 && eta < 2.1)
      return 0.995424535176;
    if (eta > -0.6 && eta < -0.3)
      return 0.997773737047;
    if (eta > -0.2 && eta < 0.2)
      return 0.997287521598;
    if (eta > -0.3 && eta < -0.2)
      return 0.997067189539;
    if (eta > 2.1 && eta < 2.4)
      return 0.988594618646;
    if (eta > -1.6 && eta < -1.2)
      return 0.996584599672;
    if (eta > -0.9 && eta < -0.6)
      return 0.997698801389;
    if (eta > 0.6 && eta < 0.9)
      return 0.99843744821;
    if (eta > -2.1 && eta < -1.6)
      return 0.995300493513;
    if (eta > -1.2 && eta < -0.9)
      return 0.997201612548;
    else
      return 1;
  }
  else
   return 1;
}
