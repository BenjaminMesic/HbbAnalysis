import ROOT
import os

# Load C functions
ROOT.gROOT.ProcessLine('.L {0}/utility/utility_C.h'.format(os.environ['Hbb_WORKING_DIRECTORY']))

def boost_FatJet_index_max_bb(tree):

  _jet_list = {}

  if tree.nvLeptons == 0:
    return -9

  _v_eta  = tree.vLeptons_eta[0]
  _v_phi  = tree.vLeptons_phi[0]

  for _n in xrange(tree.nFatjetAK08ungroomed):

    _fj_eta = tree.FatjetAK08ungroomed_eta[_n]
    _fj_phi = tree.FatjetAK08ungroomed_phi[_n]

    _dR     = ROOT.deltaR( _fj_eta, _fj_phi, _v_eta, _v_phi)
    _fj_pt  = tree.FatjetAK08ungroomed_pt[_n]

    if _dR > 0.8 and _fj_pt > 200 and 95 < tree.FatjetAK08ungroomed_mpruned[_n] < 155:
      _jet_list[_n] = tree.FatjetAK08ungroomed_bbtag[_n]
    else:
      pass  

  if len(_jet_list) == 0:
    return -9.0
  else:
    return max( _jet_list, key=_jet_list.get)

def boost_AK_index_maxCSV(tree):

  _index_FJ  = boost_FatJet_index_max_bb(tree)

  if _index_FJ == -9:
    return -9.0

  _index_AK  = -9.0
  _max_btagCSV = -9.0

  _fj_eta = tree.FatjetAK08ungroomed_eta[_index_FJ]
  _fj_phi = tree.FatjetAK08ungroomed_phi[_index_FJ]

  for _cj in xrange(tree.nJet):
    
    _ak_eta = tree.Jet_eta[_cj]
    _ak_phi = tree.Jet_phi[_cj]
    _ak_pt  = tree.Jet_pt[_cj]

    if tree.Jet_btagCSV[_cj] > _max_btagCSV:

      _dR = ROOT.deltaR( _fj_eta, _fj_phi, _ak_eta, _ak_phi)

      if abs(_ak_eta) < 2.5 and _ak_pt > 30 and _dR > 0.8:

        _max_btagCSV  = tree.Jet_btagCSV[_cj]
        _index_AK     = _cj

  return _index_AK

def boost_n_AK04(tree):

  _counter = 0.0

  _index_FJ  = boost_FatJet_index_max_bb(tree)

  if _index_FJ == -9:
    return -9.0

  _fj_eta = tree.FatjetAK08ungroomed_eta[_index_FJ]
  _fj_phi = tree.FatjetAK08ungroomed_phi[_index_FJ]

  for _cj in xrange(tree.nJet):

    _ak_phi = tree.Jet_phi[_cj]   
    _ak_eta = tree.Jet_eta[_cj]
    _ak_pt  = tree.Jet_pt[_cj]

    _dR = ROOT.deltaR( _fj_eta, _fj_phi, _ak_eta, _ak_phi)

    if abs(_ak_eta) < 2.5 and _ak_pt > 30 and _dR > 0.8:
      _counter += 1

  return _counter
