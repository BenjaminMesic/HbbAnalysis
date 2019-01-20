import ROOT
import os

import numpy as np

# Load C functions
ROOT.gROOT.ProcessLine('.L {0}/utility/utility_C.h'.format(os.environ['Hbb_WORKING_DIRECTORY']))

# ---------------------------------
# ------ Selection variables ------
def boost_HC_index(tree, global_variables):

  max_bb_index = -1
  max_bb = -1

  # Find FJ with the best bb probability
  for _fj in xrange(tree.nFatjetAK08ungroomed):

    if abs(tree.FatjetAK08ungroomed_eta[_fj]) > 2.0:
      continue

    if tree.FatjetAK08ungroomed_bbtag[_fj] > max_bb:
      max_bb = tree.FatjetAK08ungroomed_bbtag[_fj]
      max_bb_index = _fj

  return max_bb_index

def boost_n_add_jets(tree, global_variables):

  return aux_n_add_jets(tree, global_variables)

def boost_btag_veto(tree, global_variables):

  return aux_btag_veto(tree, global_variables)

def boost_ctag_veto(tree, global_variables):

  return aux_ctag_veto(tree, global_variables)

# ---------------------------------
# ------ Weights ------
def boost_weight_btag_veto(tree, global_variables, aux_files):
  
  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='b')

def boost_weight_ctag_veto(tree, global_variables, aux_files):
  
  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='c')

# ---------------------------------
# ------ Systematics ------

# bb tag systematics
def boost_sys_HC_bb_up(tree, global_variables):

  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_pt = tree.FatjetAK08ungroomed_pt[HC_idx]

  if HC_pt < 250:

    return .92*(1. + .03*2) # double uncertainty on SF

  elif HC_pt < 350:

    return .92*(1. + .03)

  elif HC_pt < 430:

    return 1.01*(1. + .03)

  elif HC_pt < 840:

    return .92*(1. + .03)

  else:

    return .92*(1. + .03*2) # double uncertainty on SF

def boost_sys_HC_bb_down(tree, global_variables):

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_pt = tree.FatjetAK08ungroomed_pt[HC_idx]

  if HC_pt < 250:

    return .92*(1. - .03*2) # double uncertainty on SF

  elif HC_pt < 350:

    return .92*(1. - .03)

  elif HC_pt < 430:

    return 1.01*(1. - .04)

  elif HC_pt < 840:

    return .92*(1. - .05)

  else:

    return .92*(1. - .05*2) # double uncertainty on SF

def boost_sys_HC_bb_mistag_up(tree, global_variables):

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_pt = tree.FatjetAK08ungroomed_pt[HC_idx]

  if HC_pt < 250:

    return 1.05*(1. + .044*2) # double uncertainty on SF

  elif HC_pt < 350:

    return 1.05*(1. + .044)

  elif HC_pt < 700:

    return 1.086*(1. + .078)

  else:

    return 1.086*(1. + .078*2) # double uncertainty on SF

def boost_sys_HC_bb_mistag_down(tree, global_variables):

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_pt = tree.FatjetAK08ungroomed_pt[HC_idx]

  if HC_pt < 250:

    return 1.05*(1. - .044*2) # double uncertainty on SF

  elif HC_pt < 350:

    return 1.05*(1. - .044)

  elif HC_pt < 700:

    return 1.086*(1. - .078)

  else:

    return 1.086*(1. - .078*2) # double uncertainty on SF

# tau2/tau1 systematics
def boost_sys_HC_tau21_up(tree, global_variables):
  
  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetWtagging#Systematic_uncertainties

  return 1.*(1.1 + .12) # Changed from 1 to 1.1 May 30th

def boost_sys_HC_tau21_down(tree, global_variables):
  
  return 1.*(1.1 - .12)

def boost_sys_HC_tau21_pt_up(tree, global_variables):
  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetWtagging#Systematic_uncertainties
  # X * ln(pt/200GeV)
  # For high-pT extrapolation of pruning+CHS use the closest corresponding SD+PUPPI working point
  # In our case: tau21(0.55): High Purity cut efficiency : 1.03, sqrt(0.04^2+0.13^2) = 0.14

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_pt = tree.FatjetAK08ungroomed_pt[HC_idx]

  return 1.*(1.03 + 0.14)*np.log(1.0*HC_pt/200)

def boost_sys_HC_tau21_pt_down(tree, global_variables):
  
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_pt = tree.FatjetAK08ungroomed_pt[HC_idx]

  return 1.*(1.03 - 0.14)*np.log(1.0*HC_pt/200)

# JEC/JER AK08 systematics (mass correction)
def boost_sys_HC_AK08JEC_up(tree, global_variables):
  
  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetWtagging#Systematic_uncertainties

  return 1.*(1 + .023) # Changed from 0.0094 to current May 30th

def boost_sys_HC_AK08JEC_down(tree, global_variables):
  
  return 1.*(1 - .023)

def boost_sys_HC_AK08JER_up(tree, global_variables):
    
  # https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#Smearing_procedures
  
  SF        = 1.23
  sigma_SF  = 0.18
  # Relative sigma
  sigma_JER = aux_HC_AK08JER_sigma_mass(tree, global_variables)/125 

  return 1.0 + np.random.normal(0, sigma_JER, 1)[0]*np.sqrt( max((SF+sigma_SF)**2-1,0) )

def boost_sys_HC_AK08JER_down(tree, global_variables):

  SF        = 1.23
  sigma_SF  = 0.18
  # Relative sigma
  sigma_JER = aux_HC_AK08JER_sigma_mass(tree, global_variables)/125 

  return 1.0 + np.random.normal(0, sigma_JER, 1)[0]*np.sqrt( max((SF-sigma_SF)**2-1,0) )

# JEC/JER AK04 systematics
def boost_sys_n_add_jets_AK04JEC_up(tree, global_variables):
  
  return aux_n_add_jets(tree, global_variables, sys_type='JEC_up')

def boost_sys_n_add_jets_AK04JEC_down(tree, global_variables):
  
  return aux_n_add_jets(tree, global_variables, sys_type='JEC_down')

def boost_sys_n_add_jets_AK04JER_up(tree, global_variables):
  
  return aux_n_add_jets(tree, global_variables, sys_type='JER_up')

def boost_sys_n_add_jets_AK04JER_down(tree, global_variables):
  
  return aux_n_add_jets(tree, global_variables, sys_type='JER_down')

def boost_sys_btag_veto_AK04JEC_up(tree, global_variables):
  
  return aux_btag_veto(tree, global_variables, sys_type='JEC_up')

def boost_sys_btag_veto_AK04JEC_down(tree, global_variables):

  return aux_btag_veto(tree, global_variables, sys_type='JEC_down')

def boost_sys_btag_veto_AK04JER_up(tree, global_variables):

  return aux_btag_veto(tree, global_variables, sys_type='JER_up')

def boost_sys_btag_veto_AK04JER_down(tree, global_variables):

  return aux_btag_veto(tree, global_variables, sys_type='JER_down')

def boost_sys_ctag_veto_AK04JEC_up(tree, global_variables):

  return aux_ctag_veto(tree, global_variables, sys_type='JEC_up')

def boost_sys_ctag_veto_AK04JEC_down(tree, global_variables):

  return aux_ctag_veto(tree, global_variables, sys_type='JEC_down')

def boost_sys_ctag_veto_AK04JER_up(tree, global_variables):

  return aux_ctag_veto(tree, global_variables, sys_type='JER_up')

def boost_sys_ctag_veto_AK04JER_down(tree, global_variables):

  return aux_ctag_veto(tree, global_variables, sys_type='JER_down')

# btag AK04 systematics
def boost_sys_btag_veto_bc_up(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='b', sys_type='bc_up')

def boost_sys_btag_veto_bc_down(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='b', sys_type='bc_down')

def boost_sys_btag_veto_light_up(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='b', sys_type='light_up')

def boost_sys_btag_veto_light_down(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='b', sys_type='light_down')

# ctag AK04 systematics
def boost_sys_ctag_veto_bc_up(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='c', sys_type='bc_up')

def boost_sys_ctag_veto_bc_down(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='c', sys_type='bc_down')

def boost_sys_ctag_veto_light_up(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='c', sys_type='light_up')

def boost_sys_ctag_veto_light_down(tree, global_variables, aux_files):

  return aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type='c', sys_type='light_down')

# ---------------------------------
# aux functions which are used for each sys many times, to avoid writing same code milion times
def aux_n_add_jets(tree, global_variables, sys_type=None):

  # Choose jet correction
  if sys_type  == 'JEC_up':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JECUp[_j]/tree.Jet_corr[_j]'
  
  elif sys_type== 'JEC_down':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JECDown[_j]/tree.Jet_corr[_j]'
  
  elif sys_type== 'JER_up':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JERUp[_j]/tree.Jet_corr_JER[_j]'
  
  elif sys_type== 'JER_down':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JERDown[_j]/tree.Jet_corr_JER[_j]'
  
  else:
    jet_pt = 'tree.Jet_pt[_j]'

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_eta = tree.FatjetAK08ungroomed_eta[HC_idx]
  HC_phi = tree.FatjetAK08ungroomed_phi[HC_idx]

  counter = 0

  for _j in xrange(tree.nJet):

    # Filter jets
    if abs(tree.Jet_eta[_j]) > 2.4:
      continue

    if tree.Jet_id[_j] <= 0:
      continue

    if tree.Jet_puId[_j] <= 0:
      continue

    dR_HCJ = ROOT.deltaR( HC_eta, HC_phi, tree.Jet_eta[_j], tree.Jet_phi[_j])
    if dR_HCJ < 0.8:
      continue

    if eval(jet_pt) < 20:
      continue

    counter += 1

  return counter

def aux_btag_veto(tree, global_variables, sys_type=None):

  # Choose jet correction
  if sys_type  == 'JEC_up':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JECUp[_j]/tree.Jet_corr[_j]'
  
  elif sys_type== 'JEC_down':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JECDown[_j]/tree.Jet_corr[_j]'
  
  elif sys_type== 'JER_up':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JERUp[_j]/tree.Jet_corr_JER[_j]'
  
  elif sys_type== 'JER_down':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JERDown[_j]/tree.Jet_corr_JER[_j]'
  
  else:
    jet_pt = 'tree.Jet_pt[_j]'

  # Search for max b tag starts here
  _max_btag_value = -999

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_eta = tree.FatjetAK08ungroomed_eta[HC_idx]
  HC_phi = tree.FatjetAK08ungroomed_phi[HC_idx]

  for _j in xrange(tree.nJet):

    # Filter jets
    if ROOT.deltaR( HC_eta, HC_phi, tree.Jet_eta[_j], tree.Jet_phi[_j]) < 0.8:
      continue

    if abs(tree.Jet_eta[_j]) > 2.4:
      continue

    if tree.Jet_id[_j] <= 0:
      continue

    if tree.Jet_puId[_j] <= 0:
      continue

    if eval(jet_pt) < 20:
      continue

    _btag_value = tree.Jet_btagCSV[_j]

    if _btag_value > _max_btag_value:
      _max_btag_value = _btag_value

  # WP: L, veto on max b_tag AK04 outside HC
  if _max_btag_value > 0.5426:
    return 0

  # Veto passed
  return 1

def aux_ctag_veto(tree, global_variables, sys_type=None):

  # Choose jet correction
  if sys_type  == 'JEC_up':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JECUp[_j]/tree.Jet_corr[_j]'
  
  elif sys_type== 'JEC_down':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JECDown[_j]/tree.Jet_corr[_j]'
  
  elif sys_type== 'JER_up':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JERUp[_j]/tree.Jet_corr_JER[_j]'
  
  elif sys_type== 'JER_down':
    jet_pt = 'tree.Jet_pt[_j]*tree.Jet_corr_JERDown[_j]/tree.Jet_corr_JER[_j]'
  
  else:
    jet_pt = 'tree.Jet_pt[_j]'

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_eta = tree.FatjetAK08ungroomed_eta[HC_idx]
  HC_phi = tree.FatjetAK08ungroomed_phi[HC_idx]

  for _j in xrange(tree.nJet):

    # Filter jets
    if ROOT.deltaR( HC_eta, HC_phi, tree.Jet_eta[_j], tree.Jet_phi[_j]) > 0.8:
      continue

    if abs(tree.Jet_eta[_j]) > 2.4:
      continue

    if tree.Jet_id[_j] <= 0:
      continue

    if tree.Jet_puId[_j] <= 0:
      continue

    if eval(jet_pt) < 20:
      continue

    # WP: L, there should be no jets passing c tag selection below
    if tree.Jet_ctagVsB[_j] > -0.17 and tree.Jet_ctagVsL[_j] > -0.48:
      return 0

  # Veto passed
  return 1

def aux_bctag_veto_weight(tree, global_variables, aux_files, flavour_type=None, sys_type=None):

  # setup systematics, btag (jetFlavor (B = 0, C = 1, UDSG = 2))
  if sys_type   == 'bc_up':
    systematics = ['up', 'up', 'central']

  elif sys_type == 'bc_down':
    systematics = ['down', 'down', 'central']

  elif sys_type == 'light_up':
    systematics = ['central', 'central', 'up']

  elif sys_type == 'light_down':
    systematics = ['central', 'central', 'down']

  else:
    systematics = ['central', 'central', 'central']

  # setup selection
  if flavour_type == 'b':
    selection = 'tree.Jet_btagCSV[_j] > 0.5426'
    dR        = 'ROOT.deltaR( HC_eta, HC_phi, tree.Jet_eta[_j], tree.Jet_phi[_j]) < 0.8' # If inside, continue for loop

  elif flavour_type == 'c':
    selection = 'tree.Jet_ctagVsB[_j] > -0.17 and tree.Jet_ctagVsL[_j] > -0.48'
    dR        = 'ROOT.deltaR( HC_eta, HC_phi, tree.Jet_eta[_j], tree.Jet_phi[_j]) > 0.8' # If outside, continue for loop

  # Load all external files with MC eff
  _root_name  = 'boost_weight_{0}tag_veto_eff_root'.format(flavour_type)
  _hist_eff_b = aux_files[_root_name].Get('efficiency_b')
  _hist_eff_c = aux_files[_root_name].Get('efficiency_c')
  _hist_eff_l = aux_files[_root_name].Get('efficiency_udsg')

  _reader_name= 'boost_weight_{0}tag_veto_SF_{0}tagcal'.format(flavour_type)  
  _reader     = aux_files[_reader_name]

  _hist_eff_xaxis = _hist_eff_b.GetXaxis()
  _hist_eff_yaxis = _hist_eff_b.GetYaxis()

  # Heppy -> btag (jetFlavor (B = 0, C = 1, UDSG = 2))
  _jet_flavour_converter = {
    0 : 2,
    4 : 1,
    5 : 0
  }

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return -1

  HC_eta = tree.FatjetAK08ungroomed_eta[HC_idx]
  HC_phi = tree.FatjetAK08ungroomed_phi[HC_idx]

  total_weight = 1

  # Loop over all jets
  for _j in xrange(tree.nJet):

    # Filter jets
    if abs(tree.Jet_eta[_j]) > 2.4:
      continue

    if tree.Jet_pt[_j] < 20:
      continue

    if tree.Jet_id[_j] <= 0:
      continue

    if tree.Jet_puId[_j] <= 0:
      continue

    if eval(dR):
      continue

    # Find eff bin 
    _hist_eff_binx = _hist_eff_b.FindBin(tree.Jet_pt[_j])
    _hist_eff_biny = _hist_eff_b.FindBin(tree.Jet_eta[_j])

    # Eff's
    _jet_flavour = _jet_flavour_converter[tree.Jet_hadronFlavour[_j]]

    if _jet_flavour == 0:
      efficiency = _hist_eff_b.GetBinContent(_hist_eff_binx, _hist_eff_biny)
      systematic = systematics[0]
    
    elif _jet_flavour == 1:
      efficiency = _hist_eff_c.GetBinContent(_hist_eff_binx, _hist_eff_biny)
      systematic = systematics[1]
    
    elif _jet_flavour == 2:
      efficiency = _hist_eff_l.GetBinContent(_hist_eff_binx, _hist_eff_biny)
      systematic = systematics[2]
 
    SF = _reader.eval_auto_bounds(
      systematic,                   # systematic (here also 'up'/'down' possible)
      _jet_flavour,                 # jet flavor
      tree.Jet_eta[_j],             # eta
      tree.Jet_pt[_j]               # pt
    )

    # Check b-tag condition
    if eval(selection):
      p_data  = 1.0*efficiency*SF
      p_mc    = 1.0*efficiency
    else:
      p_data = 1 - 1.0*SF*efficiency
      p_mc   = 1 - 1.0*efficiency

    # compute weight
    total_weight *= 1.0*p_data/p_mc

    values = [
      str(sys_type), 
      flavour_type,
      '{:06.4f}'.format(_j),
      '{:06.4f}'.format(_jet_flavour),
      '{:06.4f}'.format(tree.Jet_pt[_j]),
      '{:06.4f}'.format(tree.Jet_eta[_j]),
      '{:06.4f}'.format(total_weight),
      '{:06.4f}'.format(SF),
      '{:06.4f}'.format(efficiency),
      '{:06.4f}'.format(1.0*p_data/p_mc),
      systematic,
      str(eval(selection))
    ]

    x = '{:12s}'*len(values)
    # print values
    print x.format(*values)

  return total_weight

def aux_HC_AK08JER_sigma_mass(tree, global_variables):

  # All numbers given by Vuko

  # # Result of fit without pt bins
  # return 13.18 

  # Find HC candidate
  HC_idx = global_variables['boost_HC_index']

  if HC_idx == -1:
    return 10.0

  HC_pt = tree.FatjetAK08ungroomed_pt[HC_idx]

  if HC_pt < 350:
    return 13.05

  elif HC_pt < 450:
    return 13.11

  elif HC_pt < 550:
    return 12.18

  else:
    return 10.14
