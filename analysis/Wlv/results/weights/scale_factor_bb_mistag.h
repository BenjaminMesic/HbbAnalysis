double scale_factor_bb_mistag( double pt )
{
  if (pt > 250 && pt < 350)
  {
    return 1.05;
  }
  if (pt > 350 && pt < 750)
  {
    return 1.086;
  }
  else
    return 1.086;
}
