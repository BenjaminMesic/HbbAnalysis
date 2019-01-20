CR_SF = {  
  # --------------------------
  # Computed on Oct 27th, 
  # /afs/cern.ch/work/b/bmesic/public/18_09_Hbb_datacards/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/Hbb_datacards/18_10_25_seminar/CRSR
  # SF_TT_Wln   = 0.789345   +/-  0.126243  (limited)
  # SF_Wj0b_Wln   = 1.00508  +/-  0.125597  (limited)
  # SF_Wj1b_Wln   = 1.72578  +/-  0.447216  (limited)
  # SF_Wj2b_Wln   = 0.170879   +/-  2.76971 (limited)
  'TT'    : .78,
  'Wj0b'  : 1.00,
  'Wj1b'  : 1.72,
  'Wj2b'  : .17,

}

weights = {
  'genWeight': {
    'samples' : 'all_but_data',
    # 'weight'  : 'genWeight' #
    'weight'  : 'sign(genWeight)' 
  },
  'pile_up'   : {
    'samples' : 'all_but_data',
    # 'mc'      : '/users/bmesic/WorkingDirectory/17_01_test_Hbb/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_PU_Gael_13fb/mcpu.root',
    # 'data'    : '/users/bmesic/WorkingDirectory/17_01_test_Hbb/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_PU_Gael_13fb/outputData.root',
    # 'C'       : 'pile_up.h',
    'weight'  : 'puWeight' # 'pile_up(nTrueInt)' user defined function not used right now
  },
  
  'scale_factor_bb_tag'  : {
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    'samples' : [ 'WminusHPOWPYT', 'WplusHPOWPYT'],
    'C'       : 'scale_factor_bb_tag.h',
    'weight'  : 'scale_factor_bb_tag(FatjetAK08ungroomed_pt[boost_HC_index])'
  },

  'scale_factor_bb_mistag'  : {
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    'samples' : ['TT'],
    'C'       : 'scale_factor_bb_mistag.h',
    'weight'  : 'scale_factor_bb_mistag(FatjetAK08ungroomed_pt[boost_HC_index])'
  },

  'scale_factor_tau21'  : {
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetWtagging
    'samples' : [ 'WminusHPOWPYT', 'WplusHPOWPYT'],
    'C'       : 'scale_factor_tau21.h',
    'weight'  : 'scale_factor_tau21()'
  },

  'scale_factor_tau21_pt'  : {
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetWtagging
    'samples' : [ 'WminusHPOWPYT', 'WplusHPOWPYT'],
    'C'       : 'scale_factor_tau21_pt.h',
    'weight'  : 'scale_factor_tau21_pt(FatjetAK08ungroomed_pt[boost_HC_index])'
  },

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

  # 'scale_factor_ptWeightEWK' : {
  #   'samples' : ['WJet100', 'WJet250', 'WJet400', 'WJet600', 'WJet100_light', 'WJet100_c', 'WJet100_1b', 'WJet100_2b', 'WJet250_light', 'WJet250_c', 'WJet250_1b', 'WJet250_2b', 'WJet400_light', 'WJet400_c', 'WJet400_1b', 'WJet400_2b','WJet600_light', 'WJet600_c', 'WJet600_1b', 'WJet600_2b'],
  #   'C'       : 'scale_factor_ptWeightEWK.h',
  #   'weight'  : 'scale_factor_ptWeightEWK( nGenVbosons, GenVbosons_pt[0], Vtype, GenVbosons_pdgId[0])'
  # },
  # 'scale_factor_Vpt_TT' : {
  #   'samples' : ['TT'],
  #   'C'       : 'scale_factor_Vpt_TT.h',
  #   'weight'  : 'scale_factor_Vpt_TT(V_pt, 0)'
  # },
  'scale_factor_ptWeightEWK_Wminus' : {
    'samples' : ['WminusHPOWPYT'],
    'C'       : 'scale_factor_ptWeightEWK_Wminus.h',
    'weight'  : 'scale_factor_ptWeightEWK_Wminus(GenVbosons_pt[0])'
  },
  'scale_factor_ptWeightEWK_Wplus' : {
    'samples' : ['WplusHPOWPYT'],
    'C'       : 'scale_factor_ptWeightEWK_Wplus.h',
    'weight'  : 'scale_factor_ptWeightEWK_Wplus(GenVbosons_pt[0])'
  },

  # ------------------------
  # Requires boosted ntuples
  'btag_veto': {
    'samples' : 'all_but_data',
    'weight'  : 'boost_weight_btag_veto'
  },

  'ctag_veto': {
    'samples' : 'all_but_data',
    'weight'  : 'boost_weight_ctag_veto'
  },

}