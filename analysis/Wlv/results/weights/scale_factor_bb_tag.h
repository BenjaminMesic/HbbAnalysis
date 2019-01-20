double scale_factor_bb_tag( double pt )
{
  if (pt > 250 && pt < 350)
  {
    return 0.92;
  }
  if (pt > 350 && pt < 430)
  {
    return 1.01;
  }
  if (pt > 430 && pt < 840)
  {
    return 0.92;
  }
  else
    return 0.92;
}
