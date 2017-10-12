import ROOT
import os

import numpy as np

# Load C functions
ROOT.gROOT.ProcessLine('.L {0}/utility/utility_C.h'.format(os.environ['Hbb_WORKING_DIRECTORY']))

def boost_H_index(tree, model):

  model = model['HC_e30__m15_15']

  variables = [ 'Subjet_pt_ratio','SubJet_btag_0','dR_H_SubJet_0', 'SubJet_btag_1','dR_H_SubJet_1']

  variables_eval = {
    'Subjet_pt_ratio'       : 'tree.SubjetAK08softdrop_pt[_sj_temp[_fj][0]]/tree.SubjetAK08softdrop_pt[_sj_temp[_fj][1]]',
    'SubJet_btag_0'         : 'tree.SubjetAK08softdrop_btag[_sj_temp[_fj][0]]',
    'SubJet_btag_1'         : 'tree.SubjetAK08softdrop_btag[_sj_temp[_fj][1]]',
    'dR_H_SubJet_0'         : 'ROOT.deltaR( tree.FatjetAK08ungroomed_eta[_fj], tree.FatjetAK08ungroomed_phi[_fj], tree.SubjetAK08softdrop_eta[_sj_temp[_fj][0]], tree.SubjetAK08softdrop_phi[_sj_temp[_fj][0]])',
    'dR_H_SubJet_1'         : 'ROOT.deltaR( tree.FatjetAK08ungroomed_eta[_fj], tree.FatjetAK08ungroomed_phi[_fj], tree.SubjetAK08softdrop_eta[_sj_temp[_fj][1]], tree.SubjetAK08softdrop_phi[_sj_temp[_fj][1]])',
  }

  _list_fj = {}

  # Sub jet matching
  _sj_temp = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
  for isj in xrange(tree.nSubjetAK08softdrop):

    _sj_eta = tree.SubjetAK08softdrop_eta[isj]
    _sj_phi = tree.SubjetAK08softdrop_phi[isj]

    for _fj in xrange(tree.nFatjetAK08ungroomed):

      _fj_eta = tree.FatjetAK08ungroomed_eta[_fj]
      _fj_phi = tree.FatjetAK08ungroomed_phi[_fj]

      _dR = ROOT.deltaR( _fj_eta, _fj_phi, _sj_eta, _sj_phi)

      if _dR < 0.8:

        _sj_temp[_fj].append(isj)

  # Find FJ with the best bb probability
  for _fj in xrange(tree.nFatjetAK08ungroomed):

    if not len(_sj_temp[_fj]) == 2:
      continue

    if abs(tree.FatjetAK08ungroomed_eta[_fj]) > 2.0:
      continue

    _nn_input   = np.array([ eval(variables_eval[_v]) for _v in variables])
    _nn_input   = np.reshape(_nn_input, (1,5))
    _nn_output  = model.predict(_nn_input)

    _list_fj[_fj] = _nn_output[0][0]

  # Find the index of maximum bb probability
  if len(_list_fj):
    return max(_list_fj, key=lambda k: _list_fj[k])
  else:
    return -1

def boost_H_bbv2(tree, model):

  model     = model['HC_e30__m15_15']
  fj_bbv2  = [0.0]*10

  variables = [ 'Subjet_pt_ratio','SubJet_btag_0','dR_H_SubJet_0', 'SubJet_btag_1','dR_H_SubJet_1']

  variables_eval = {
    'Subjet_pt_ratio'       : 'tree.SubjetAK08softdrop_pt[_sj_temp[_fj][0]]/tree.SubjetAK08softdrop_pt[_sj_temp[_fj][1]]',
    'SubJet_btag_0'         : 'tree.SubjetAK08softdrop_btag[_sj_temp[_fj][0]]',
    'SubJet_btag_1'         : 'tree.SubjetAK08softdrop_btag[_sj_temp[_fj][1]]',
    'dR_H_SubJet_0'         : 'ROOT.deltaR( tree.FatjetAK08ungroomed_eta[_fj], tree.FatjetAK08ungroomed_phi[_fj], tree.SubjetAK08softdrop_eta[_sj_temp[_fj][0]], tree.SubjetAK08softdrop_phi[_sj_temp[_fj][0]])',
    'dR_H_SubJet_1'         : 'ROOT.deltaR( tree.FatjetAK08ungroomed_eta[_fj], tree.FatjetAK08ungroomed_phi[_fj], tree.SubjetAK08softdrop_eta[_sj_temp[_fj][1]], tree.SubjetAK08softdrop_phi[_sj_temp[_fj][1]])',
  }

  _list_fj = {}

  # Sub jet matching
  _sj_temp = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
  for isj in xrange(tree.nSubjetAK08softdrop):

    _sj_eta = tree.SubjetAK08softdrop_eta[isj]
    _sj_phi = tree.SubjetAK08softdrop_phi[isj]

    for _fj in xrange(tree.nFatjetAK08ungroomed):

      _fj_eta = tree.FatjetAK08ungroomed_eta[_fj]
      _fj_phi = tree.FatjetAK08ungroomed_phi[_fj]

      _dR = ROOT.deltaR( _fj_eta, _fj_phi, _sj_eta, _sj_phi)

      if _dR < 0.8:

        _sj_temp[_fj].append(isj)

  # Find FJ with the best bb probability 
  for _fj in xrange(tree.nFatjetAK08ungroomed):

    if not len(_sj_temp[_fj]) == 2:
      continue

    if abs(tree.FatjetAK08ungroomed_eta[_fj]) > 2.0:
      continue

    _nn_input   = np.array([ eval(variables_eval[_v]) for _v in variables])
    _nn_input   = np.reshape(_nn_input, (1,5))
    _nn_output  = model.predict(_nn_input)

    fj_bbv2[_fj] = _nn_output[0][0]

  return fj_bbv2

def boost_2nd_b(tree, model):

  variables           = [ 'HC_J_pt_ratio', 'J_btag', 'J_eta', 'dR_HCJ']
  number_of_jets      = 25
  number_of_features  = len(variables)

  # Create input template for LSTM
  input_template = np.zeros([1, number_of_jets, number_of_features])

  # Find HC candidate
  HC_idx = boost_H_index(tree, model)

  if HC_idx == -1:
    return -1

  HC_eta = tree.FatjetAK08ungroomed_eta[HC_idx]
  HC_phi = tree.FatjetAK08ungroomed_phi[HC_idx]

  # if abs(HC_eta) < 2.0:
  #   return -1

  counter = 0

  for _j in xrange(tree.nJet):

    # Filter jets
    if abs(tree.Jet_eta[_j]) > 2.4:
      continue

    # Filter jets
    if tree.Jet_btagCSV[_j] < 0.0:
      continue

    # Filter jets
    dR_HCJ = ROOT.deltaR( HC_eta, HC_phi, tree.Jet_eta[_j], tree.Jet_phi[_j])
    if dR_HCJ < 0.8:
      continue

    variables[0] = 1.0*tree.Jet_pt[_j]/tree.FatjetAK08ungroomed_pt[HC_idx]
    variables[1] = tree.Jet_btagCSV[_j]
    variables[2] = abs(tree.Jet_eta[_j])
    variables[3] = dR_HCJ

    # Fill input template
    input_template[0][counter] = variables
    counter += 1

  prediction = model['2ndb_e1__m25_25'].predict(input_template, verbose=0)

  return prediction[0,-1,-1]