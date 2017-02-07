{
  'genWeight': {
    'samples': 'all_but_data',
    'weight' : 'genWeight' # 'sign(genWeight)' #
  },
  # 'btagWeightCSV': {
  #   'weight' : 'btagWeightCSV'
  # },
  'pile_up'   : {
    'samples': 'all_but_data',
    'mc'  : '/users/bmesic/WorkingDirectory/2016_11_Hbb_test/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_PU_Gael_13fb/mcpu.root',
    'data'  : '/users/bmesic/WorkingDirectory/2016_11_Hbb_test/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_PU_Gael_13fb/outputData.root',
    'C'   : 'pile_up.h',
    'weight': 'puWeight' # 'pile_up(nTrueInt)' # 
  },

  # 'EWK_NLO_correction': {
  #   'C'   : 'EWK_NLO_correction.h', WJETS
  #   'weight': 'ptWeightEWK(nGenVbosons, Alt$(GenVbosons_pt[0],0), VtypeSim, Alt$(GenVbosons_pdgId[0],0))'
  # },

  # 'trigger_muon'  : {
  #   'file'  : '/users/bmesic/WorkingDirectory/2016_11_Hbb_test/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_trigger_eff_single_muon/SingleMuonTrigger_Z_RunBCD_prompt80X_7p65.py',
  #   'type'  : ['IsoMu22_OR_IsoTkMu22_PtEtaBins_Run273158_to_274093','IsoMu22_OR_IsoTkMu22_PtEtaBins_Run274094_to_276097'],
  #   'C'   : 'trigger_muon.h',
  #   # 'weight': 'trigger_muon(abs(vLeptons_eta[0]), vLeptons_pt[0], vLeptons_pdgId[0], run)' # Variables: muSF_HLT_RunD4p2(Run273158_to_274093), muSF_HLT_RunD4p3(Run274094_to_276097)
  #   'weight': 'trigger_muon(abs(vLeptons_eta[0]), vLeptons_pt[0], vLeptons_pdgId[0])'
  # },

  # 'trigger_electron'  : {
  #   'file'  : '/users/bmesic/WorkingDirectory/2016_11_Hbb_test/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_trigger_eff_single_electron/WP80_BCD_withRelIso.py',
  #   'type'  : 'electronTriggerEfficiencyHLT_Ele27_WPLoose_eta2p1_WP80_BCD',
  #   'C'   : 'trigger_electron.h',
  #   'weight': 'trigger_electron(vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  # },

  # 'scale_factor_electron' : {
  #   'file'  : '/users/bmesic/WorkingDirectory/2016_11_Hbb_test/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_SF_electron/WP80PlusIso_BCD.py',
  #   'type'  : 'WP80PlusIso_BCD',
  #   'C'   : 'scale_factor_electron.h',
  #   'weight': 'scale_factor_electron(vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  # },
  # 'scale_factor_electron_ID'  : {
  #   'file'  : '/users/bmesic/WorkingDirectory/2016_11_Hbb_test/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_SF_electron/ScaleFactor_egammaEff_WP80_80X.py',
  #   'type'  : 'ScaleFactor_egammaEff_WP80',
  #   'C'   : 'scale_factor_electron_ID.h',
  #   'weight': 'scale_factor_electron_ID(vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  # },
  # 'scale_factor_electron_trk' : {
  #   'file'  : '/users/bmesic/WorkingDirectory/2016_11_Hbb_test/CMSSW_7_4_16/src/HbbAnalysis/external/Wlv/weights/2016_11_SF_electron/egammaEffi_tracker.py',
  #   'type'  : 'egammaEffi_tracker',
  #   'C'   : 'scale_factor_electron_trk.h',
  #   'weight': 'scale_factor_electron_trk(vLeptons_eta[0], vLeptons_pt[0], vLeptons_pdgId[0])'
  # },

  # 'scale_factor_muon_iso' : {
  #   'C'   : 'scale_factor_muon_iso.h',
  #   'weight': 'scale_factor_muon_iso(vLeptons_SF_IsoLoose[0], vLeptons_pdgId[0])' # Loose(iso<0.25) = vLeptons_SF_IsoLoose[0], Tight(iso<0.15) = vLeptons_SF_IsoTight[0]
  # },
  # 'scale_factor_muon_ID'  : {
  #   'C'   : 'scale_factor_muon_ID.h',
  #   'weight': 'scale_factor_muon_ID(vLeptons_SF_IdCutLoose[0], vLeptons_pdgId[0])'
  # },
  # 'scale_factor_muon_trk' : {
  #   'C'   : 'scale_factor_muon_trk.h',
  #   'weight': 'scale_factor_muon_trk(vLeptons_SF_trk_eta[0], vLeptons_pdgId[0])'
  # },

}