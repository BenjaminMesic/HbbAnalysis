task = {
  'test'        : [ 'L0', 'L1'],
  'Wen_SR'      : [ 'L0', 'L1'],
  'Wmn_SR'      : [ 'L0', 'L1'],
  'Wen_CR_TT'   : [ 'L0', 'L1'],
  'Wmn_CR_TT'   : [ 'L0', 'L1'],
  'Wen_CR_HF'   : [ 'L0', 'L1'],
  'Wmn_CR_HF'   : [ 'L0', 'L1'],
  'Wen_CR_LF'   : [ 'L0', 'L1'],
  'Wmn_CR_LF'   : [ 'L0', 'L1']
}

hierarchy   = {
  'L0' : '(Vtype==2 || Vtype==3) && nFatjetAK08ungroomed > 0',
  'L1' : 'boost_HC_index != -1 && FatjetAK08ungroomed_pt[boost_HC_index] > 250 && FatjetAK08ungroomed_mprunedcorr[boost_HC_index] > 50'
}

subsamples  = {
  # lheV_pt bin samples
  'light'     : 'ttCls<41              ',
  'c'         : 'ttCls>=41 && ttCls<=45',
  '1b'        : 'ttCls>=51 && ttCls<=52',
  '2b'        : 'ttCls>=53 && ttCls<=55',
  # # lheV_pt bin samples, NOT USED SINCE WE ARE USING RIGHT NOW ONLY NLO inclusive
  # 'light'     : 'ttCls<41               && lheNb==0 && nGenStatus2bHad==0',
  # 'c'         : 'ttCls>=41 && ttCls<=45 && lheNb==0 && nGenStatus2bHad==0',
  # '1b'        : 'ttCls>=51 && ttCls<=52 && lheNb==0 && nGenStatus2bHad==0',
  # '2b'        : 'ttCls>=53 && ttCls<=55 && lheNb==0 && nGenStatus2bHad==0',
  # Inclusive
  'lightIncl' : 'ttCls<41               && ((lheNb==0 && nGenStatus2bHad==0 && lheV_pt>40) || lheV_pt<40) && lheV_pt < 100',
  'cIncl'     : 'ttCls>=41 && ttCls<=45 && ((lheNb==0 && nGenStatus2bHad==0 && lheV_pt>40) || lheV_pt<40) && lheV_pt < 100',
  '1bIncl'    : 'ttCls>=51 && ttCls<=52 && ((lheNb==0 && nGenStatus2bHad==0 && lheV_pt>40) || lheV_pt<40) && lheV_pt < 100',
  '2bIncl'    : 'ttCls>=53 && ttCls<=55 && ((lheNb==0 && nGenStatus2bHad==0 && lheV_pt>40) || lheV_pt<40) && lheV_pt < 100',
  # BJets
  'lightB'    : 'ttCls<41               && lheNb>0',
  'cB'        : 'ttCls>=41 && ttCls<=45 && lheNb>0',
  '1bB'       : 'ttCls>=51 && ttCls<=52 && lheNb>0',
  '2bB'       : 'ttCls>=53 && ttCls<=55 && lheNb>0',
  # BFilter
  'lightBFil' : 'ttCls<41  &&              lheNb==0 && nGenStatus2bHad>0',
  'cBFil'     : 'ttCls>=41 && ttCls<=45 && lheNb==0 && nGenStatus2bHad>0 ',
  '1bBFil'    : 'ttCls>=51 && ttCls<=52 && lheNb==0 && nGenStatus2bHad>0 ',
  '2bBFil'    : 'ttCls>=53 && ttCls<=55 && lheNb==0 && nGenStatus2bHad>0 ',
  # TT samples
  'TTincl'    : 'invariant_mass( GenTop_pt[0], GenTop_eta[0], GenTop_phi[0], GenTop_mass[0], GenTop_pt[1], GenTop_eta[1], GenTop_phi[1], GenTop_mass[1]) < 700',
  # Data, trigger cuts, etc...
  # For CR
  'el'        : 'abs(vLeptons_pdgId[0]) == 11 && Vtype==3 && HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v == 1 && json',
  'mu'        : 'abs(vLeptons_pdgId[0]) == 13 && Vtype==2 && ( HLT_BIT_HLT_IsoMu22_v == 1 || HLT_BIT_HLT_IsoTkMu22_v == 1 ) && json',
  # For SR, mass blind
  # 'el'        : 'abs(vLeptons_pdgId[0]) == 11 && Vtype==3 && HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v == 1 && json && (FatjetAK08ungroomed_mprunedcorr[boost_HC_index] < 100 || FatjetAK08ungroomed_mprunedcorr[boost_HC_index] > 150)',
  # 'mu'        : 'abs(vLeptons_pdgId[0]) == 13 && Vtype==2 && ( HLT_BIT_HLT_IsoMu22_v == 1 || HLT_BIT_HLT_IsoTkMu22_v == 1 ) && json && (FatjetAK08ungroomed_mprunedcorr[boost_HC_index] < 100 || FatjetAK08ungroomed_mprunedcorr[boost_HC_index] > 150)',
}

resolved = ' && '.join([
    '((vLeptons_pt[0] > 30 && abs(vLeptons_pdgId[0]) == 11) || (vLeptons_pt[0] > 25 && abs(vLeptons_pdgId[0]) == 13) )',
    'Jet_pt_reg[hJCidx[0]] > 25',
    'Jet_pt_reg[hJCidx[1]] > 25',
    'HCSV_reg_pt > 100',
    'HCSV_reg_mass > 90',
    'HCSV_reg_mass < 150',
    'Jet_btagCSV[hJCidx[0]] > 0.935',
    'Jet_btagCSV[hJCidx[1]] > 0.46',
    'Sum$(Jet_pt > 25 && abs(Jet_eta) < 2.9 && Jet_puId > 0 && Jet_id > 0 && Iteration$ != hJCidx[0] && Iteration$ != hJCidx[1]) < 2',
    # 'Sum$(aLeptons_pt > 15 && abs(aLeptons_eta) < 2.5 && aLeptons_relIso03 < 0.1) == 0',
    'abs(deltaPhi(V_phi, HCSV_reg_phi)) > 2.5',
    'abs(deltaPhi(met_phi, vLeptons_phi[0])) < 2.0' ,
    '((abs(vLeptons_pdgId[0]) == 11 && vLeptons_relIso03[0] < 0.15) || (abs(vLeptons_pdgId[0]) == 13 && vLeptons_relIso04[0] < 0.06))'
  ])

# L selection + SR/CR
SR    = ' && '.join([
  'FatjetAK08ungroomed_bbtag[boost_HC_index] > 0.8', 
  'FatjetAK08ungroomed_tau2[boost_HC_index]/FatjetAK08ungroomed_tau1[boost_HC_index] < 0.45',
  'V_pt/FatjetAK08ungroomed_pt[boost_HC_index] > 0.8 && V_pt/FatjetAK08ungroomed_pt[boost_HC_index] < 1.2',
  'boost_n_add_jets < 2',
  'boost_btag_veto == 1',
  'boost_ctag_veto == 1',
  '(FatjetAK08ungroomed_mprunedcorr[boost_HC_index] > 50 && FatjetAK08ungroomed_mprunedcorr[boost_HC_index] < 190)'
])

CR_TT = ' && '.join([
  'FatjetAK08ungroomed_bbtag[boost_HC_index] > 0.8', 
  'FatjetAK08ungroomed_tau2[boost_HC_index]/FatjetAK08ungroomed_tau1[boost_HC_index] < 0.45',
  'V_pt/FatjetAK08ungroomed_pt[boost_HC_index] > 0.8 && V_pt/FatjetAK08ungroomed_pt[boost_HC_index] < 1.2',
  'boost_n_add_jets > 1',
  'boost_btag_veto == 1',
  'boost_ctag_veto == 1',
  '(FatjetAK08ungroomed_mprunedcorr[boost_HC_index] > 50 && FatjetAK08ungroomed_mprunedcorr[boost_HC_index] < 190)'
])

CR_LF = ' && '.join([
  'FatjetAK08ungroomed_bbtag[boost_HC_index] < 0.8', 
  'FatjetAK08ungroomed_tau2[boost_HC_index]/FatjetAK08ungroomed_tau1[boost_HC_index] > 0.45',
  'V_pt/FatjetAK08ungroomed_pt[boost_HC_index] > 0.8 && V_pt/FatjetAK08ungroomed_pt[boost_HC_index] < 1.2',
  'boost_n_add_jets < 2',
  'boost_btag_veto == 1',
  'boost_ctag_veto == 1',
  '(FatjetAK08ungroomed_mprunedcorr[boost_HC_index] > 50 && FatjetAK08ungroomed_mprunedcorr[boost_HC_index] < 190)'
])

CR_HF = ' && '.join([
  'FatjetAK08ungroomed_bbtag[boost_HC_index] > 0.8', 
  'FatjetAK08ungroomed_tau2[boost_HC_index]/FatjetAK08ungroomed_tau1[boost_HC_index] > 0.45',
  'V_pt/FatjetAK08ungroomed_pt[boost_HC_index] > 0.8 && V_pt/FatjetAK08ungroomed_pt[boost_HC_index] < 1.2',
  'boost_n_add_jets < 2',
  'boost_btag_veto == 1',
  'boost_ctag_veto == 1',
  '(FatjetAK08ungroomed_mprunedcorr[boost_HC_index] > 50 && FatjetAK08ungroomed_mprunedcorr[boost_HC_index] < 190)'
])

# ------- Not used -------
# 'MaxIf$( Jet_ctagVsB, (Jet_ctagVsB > 0.0 && Jet_ctagVsL < 0.0) && deltaR( FatjetAK08ungroomed_eta[boost_HC_index], FatjetAK08ungroomed_phi[boost_HC_index], Jet_eta, Jet_phi)<0.8) == 0'
# 'MaxIf$( Jet_ctagVsB + 1, (Jet_ctagVsB > -0.17 && Jet_ctagVsL < 0.69 && Jet_ctagVsL > -0.48) && deltaR( FatjetAK08ungroomed_eta[boost_HC_index], FatjetAK08ungroomed_phi[boost_HC_index], Jet_eta, Jet_phi)<0.8) == 0'
# 'MaxIf$(Jet_ctagVsB, Jet_pt>20 && abs(Jet_eta)<2.4 && Jet_id>0 && Jet_puId>0) < 0.2',
# '(boost_max_ctag_index == -1 || (Jet_ctagVsB[boost_max_ctag_index]< 0.08 || Jet_ctagVsL[boost_max_ctag_index] < -0.1))', # Medium WP veto
# '(boost_max_ctag_index == -1 || (Jet_ctagVsB[boost_max_ctag_index] > 0.69 && Jet_ctagVsL[boost_max_ctag_index] > -0.45))', # Tight WP
# '(boost_max_ctag_index == -1 || ( (Jet_ctagVsB[boost_max_ctag_index] < 0.0 || Jet_ctagVsL[boost_max_ctag_index] > 0.0) && deltaR( FatjetAK08ungroomed_eta[boost_HC_index], FatjetAK08ungroomed_phi[boost_HC_index], Jet_eta[boost_max_ctag_index], Jet_phi[boost_max_ctag_index])<0.8))', # Temp WP
# '(Jet_ctagVsB[boost_max_ctag_index] < 0.0 || Jet_ctagVsL[boost_max_ctag_index] > 0.0) && deltaR( FatjetAK08ungroomed_eta[boost_HC_index], FatjetAK08ungroomed_phi[boost_HC_index], Jet_eta[boost_max_ctag_index], Jet_phi[boost_max_ctag_index])<0.8))'
  

task_definitions = {

  # 'test'        :  SR + ' && ' + resolved,
  'test'        :  SR,
  # 'test'          : 'abs(vLeptons_pdgId[0]) == 11' + ' && ' + SR,

  # Signal and control regions 
  'Wen_SR'      : 'abs(vLeptons_pdgId[0]) == 11' + ' && ' + SR,
  'Wmn_SR'      : 'abs(vLeptons_pdgId[0]) == 13' + ' && ' + SR,
  'Wen_CR_TT'   : 'abs(vLeptons_pdgId[0]) == 11' + ' && ' + CR_TT,
  'Wmn_CR_TT'   : 'abs(vLeptons_pdgId[0]) == 13' + ' && ' + CR_TT,
  'Wen_CR_HF'   : 'abs(vLeptons_pdgId[0]) == 11' + ' && ' + CR_HF,
  'Wmn_CR_HF'   : 'abs(vLeptons_pdgId[0]) == 13' + ' && ' + CR_HF,
  'Wen_CR_LF'   : 'abs(vLeptons_pdgId[0]) == 11' + ' && ' + CR_LF,
  'Wmn_CR_LF'   : 'abs(vLeptons_pdgId[0]) == 13' + ' && ' + CR_LF
}