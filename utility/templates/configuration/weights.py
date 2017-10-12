weights = {
  'genWeight': {
    'samples' : 'all_but_data',
    'weight'  : 'genWeight' # 'sign(genWeight)' 
  },
  'pile_up'   : {
    'samples' : 'all_but_data',
    # 'mc'      : '/users/bmesic/WorkingDirectory/17_01_test_Hbb/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_PU_Gael_13fb/mcpu.root',
    # 'data'    : '/users/bmesic/WorkingDirectory/17_01_test_Hbb/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_PU_Gael_13fb/outputData.root',
    # 'C'       : 'pile_up.h',
    'weight'  : 'puWeight' # 'pile_up(nTrueInt)' user defined function not used right now
  },
  
  # 'scale_factor_bb_tag'  : {
  #   'samples' : 'all_but_data',
  #   'C'       : 'scale_factor_bb_tag.h',
  #   # 'weight'  : 'scale_factor_bb_tag(FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb])'
  #   'weight'  : 'scale_factor_bb_tag(FatjetAK08ungroomed_pt[boost_H_index])'
  # },

  'scale_factor_electron_trigger'  : {
    'samples' : 'all_but_data',
    'file'    : '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/Tight27AfterIDISO_out.py',
    'type'    : 'Tight27AfterIDISO',
    'C'       : 'scale_factor_electron_trigger.h',
    'weight'  : 'scale_factor_electron_trigger( vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  },
  'scale_factor_electron_ID'  : {
    'samples' : 'all_but_data',
    'file'    : '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/EIDISO_WH_out.py',
    'type'    : 'EIDISO_WH',
    'C'       : 'scale_factor_electron_ID.h',
    'weight'  : 'scale_factor_electron_ID( vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  },
  'scale_factor_electron_trk' : {
    'samples' : 'all_but_data',
    'file'    : '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/ScaleFactor_etracker_80x.py',
    'type'    : 'ScaleFactor_tracker_80x',
    'C'       : 'scale_factor_electron_trk.h',
    'weight'  : 'scale_factor_electron_trk( vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  },

  'scale_factor_muon_trigger'  : {
    'samples' : 'all_but_data',
    'file'  : {
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/MuTrigger_SFs_BCDEF.py' : 0.55,
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/MuTrigger_SFs_GH.py'    : 0.45},
    'type'  : 'IsoMu24_OR_IsoTkMu24_PtEtaBins',
    'C'     : 'scale_factor_muon_trigger.h',
    'weight': 'scale_factor_muon_trigger( abs(vLeptons_eta[0]), vLeptons_pt[0], vLeptons_pdgId[0])'
  },
  'scale_factor_muon_iso' : {
    'samples' : 'all_but_data',
    'file'  : {
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/MuISO_SFs_BCDEF.py' : 0.55,
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/MuISO_SFs_GH.py'    : 0.45},
    'type'  : 'TightISO_TightID_pt_eta',
    'C'     : 'scale_factor_muon_iso.h',
    'weight': 'scale_factor_muon_iso( abs(vLeptons_eta[0]), vLeptons_pt[0], vLeptons_pdgId[0])'
  },
  'scale_factor_muon_ID'  : {
    'samples' : 'all_but_data',
    'file'  : {
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/MuID_EfficienciesAndSF_BCDEF.py' : 0.55,
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/MuID_EfficienciesAndSF_GH.py'    : 0.45},
    'type'  : 'MC_NUM_TightID_DEN_genTracks_PAR_pt_eta',
    'C'     : 'scale_factor_muon_ID.h',
    'weight': 'scale_factor_muon_ID( abs(vLeptons_eta[0]), vLeptons_pt[0], vLeptons_pdgId[0])'
  },
  'scale_factor_muon_trk' : {
    'samples' : 'all_but_data',
    'file'  : {
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/trk_SF_RunBCDEF.py' : 0.55,
      '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/aux/weights/2017_04/trk_SF_RunGH.py'    : 0.45},
    'type'  : 'Graph',
    'C'     : 'scale_factor_muon_trk.h',
    'weight': 'scale_factor_muon_trk( vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  },

}