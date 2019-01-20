task = {
  'test'        : [ 'L0', 'L1'],
  'Wen_full'    : [ 'L0', 'L1'],
  'Wmn_full'    : [ 'L0', 'L1'],
  'Wen_110_140' : [ 'L0', 'L1'],
  'Wmn_110_140' : [ 'L0', 'L1'],
}

hierarchy   = {
  'L0' : '(Vtype==2 || Vtype==3) && nFatjetAK08ungroomed > 0',
  'L1' : 'boost_HC_index != -1 && boost_H_bbv2[boost_HC_index] > 0.5'
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
  'el'        : 'abs(vLeptons_pdgId[0]) == 11 && Vtype==3 && HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v == 1 && json',
  'mu'        : 'abs(vLeptons_pdgId[0]) == 13 && Vtype==2 && ( HLT_BIT_HLT_IsoMu22_v == 1 || HLT_BIT_HLT_IsoTkMu22_v == 1 ) && json',  
}

task_definitions = {
  'test' :  '1',
          # 'boost_H_bbv2[boost_H_index] > 0.8', #+ ' && '
          #   'FatjetAK08ungroomed_pt[boost_H_index] > 200' + ' && '
          # + '(boost_second_b_maxCSV_AK04 == -1 || (boost_second_b_maxCSV_AK04 != -1 && Jet_btagCSV[boost_second_b_maxCSV_AK04] < 0.6))',

  # 'test': 'boost_FatJet_index_max_bb_no_mass_selection != -9' + ' && '
  #     + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb_no_mass_selection] > 400' + ' && ' 
  #     + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb_no_mass_selection] > 0.8' + ' && ' 
  #     + '( boost_AK_index_maxCSV_no_mass_selection == -9 || (boost_AK_index_maxCSV_no_mass_selection != -9 && Jet_btagCSV[boost_AK_index_maxCSV_no_mass_selection] < 0.8))' + ' && '
  #     + 'boost_n_AK04_no_mass_selection < 2' + ' && '
  #     + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb_no_mass_selection] > 0.85' + ' && '
  #     + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2',

  # 'boost_bkg_estimate': 'boost_FatJet_index_max_bb != -9' + ' && '
  #                       + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 400' + ' && ' 
  #                       + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb] > 0.8' + ' && ' 
  #                       + '( boost_AK_index_maxCSV == -9 || (boost_AK_index_maxCSV != -9 && Jet_btagCSV[boost_AK_index_maxCSV] < 0.8))' + ' && '
  #                       + 'boost_n_AK04 < 2' + ' && '
  #                       + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 0.85' + ' && '
  #                       + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2',

  # 'Wmn'               : 'boost_FatJet_index_max_bb != -9' + ' && '
  #                       + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 400' + ' && ' 
  #                       + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb] > 0.8' + ' && ' 
  #                       + '( boost_AK_index_maxCSV == -9 || (boost_AK_index_maxCSV != -9 && Jet_btagCSV[boost_AK_index_maxCSV] < 0.8))' + ' && '
  #                       + 'boost_n_AK04 < 2' + ' && '
  #                       + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 0.85' + ' && '
  #                       + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2' + ' && '
  #                       + 'Vtype==2',

  # 'Wen'               : 'boost_FatJet_index_max_bb != -9' + ' && '
  #                       + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 400' + ' && ' 
  #                       + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb] > 0.8' + ' && ' 
  #                       + '( boost_AK_index_maxCSV == -9 || (boost_AK_index_maxCSV != -9 && Jet_btagCSV[boost_AK_index_maxCSV] < 0.8))' + ' && '
  #                       + 'boost_n_AK04 < 2' + ' && '
  #                       + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 0.85' + ' && '
  #                       + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2' + ' && '
  #                       + 'Vtype==3',

  'Wen_full'           : 'boost_FatJet_index_max_bb_no_mass_selection != -9' + ' && '
                        + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb_no_mass_selection] > 400' + ' && ' 
                        + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb_no_mass_selection] > 0.8' + ' && ' 
                        + '( boost_AK_index_maxCSV_no_mass_selection == -9 || (boost_AK_index_maxCSV_no_mass_selection != -9 && Jet_btagCSV[boost_AK_index_maxCSV_no_mass_selection] < 0.8))' + ' && '
                        + 'boost_n_AK04_no_mass_selection < 2' + ' && '
                        + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb_no_mass_selection] > 0.85' + ' && '
                        + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2' + ' && '
                        + 'Vtype==3',
  
  'Wmn_full'           :  'boost_FatJet_index_max_bb_no_mass_selection != -9' + ' && '
                        + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb_no_mass_selection] > 400' + ' && ' 
                        + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb_no_mass_selection] > 0.8' + ' && ' 
                        + '( boost_AK_index_maxCSV_no_mass_selection == -9 || (boost_AK_index_maxCSV_no_mass_selection != -9 && Jet_btagCSV[boost_AK_index_maxCSV_no_mass_selection] < 0.8))' + ' && '
                        + 'boost_n_AK04_no_mass_selection < 2' + ' && '
                        + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb_no_mass_selection] > 0.85' + ' && '
                        + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2' + ' && '
                        + 'Vtype==2',


  'Wen_110_140'        : 'boost_FatJet_index_max_bb != -9' + ' && '
                        + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 400' + ' && ' 
                        + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb] > 0.8' + ' && ' 
                        + '( boost_AK_index_maxCSV == -9 || (boost_AK_index_maxCSV != -9 && Jet_btagCSV[boost_AK_index_maxCSV] < 0.8))' + ' && '
                        + 'boost_n_AK04 < 2' + ' && '
                        + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 0.85' + ' && '
                        + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2' + ' && '
                        + 'Vtype==3' + ' && '
                        + '110 < FatjetAK08ungroomed_mprunedcorr[boost_FatJet_index_max_bb] && FatjetAK08ungroomed_mprunedcorr[boost_FatJet_index_max_bb] < 140',

  'Wmn_110_140'        :  'boost_FatJet_index_max_bb != -9' + ' && '
                        + 'FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 400' + ' && ' 
                        + 'FatjetAK08ungroomed_bbtag[boost_FatJet_index_max_bb] > 0.8' + ' && ' 
                        + '( boost_AK_index_maxCSV == -9 || (boost_AK_index_maxCSV != -9 && Jet_btagCSV[boost_AK_index_maxCSV] < 0.8))' + ' && '
                        + 'boost_n_AK04 < 2' + ' && '
                        + 'V_pt/FatjetAK08ungroomed_pt[boost_FatJet_index_max_bb] > 0.85' + ' && '
                        + 'MaxIf$(Jet_ctagVsB, Jet_pt>30 && abs(Jet_eta)<2.4) < 0.2' + ' && '
                        + 'Vtype==2' + ' && '
                        + '110 < FatjetAK08ungroomed_mprunedcorr[boost_FatJet_index_max_bb] && FatjetAK08ungroomed_mprunedcorr[boost_FatJet_index_max_bb] < 140',

}