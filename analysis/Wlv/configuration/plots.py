task = {

  'test':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : [], # ['WminusHPOWPYT', 'WplusHPOWPYT'], # PlotTool line 852
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
       'Higgs candidate mass' : {
        'n_bin' : 16,
        'x_min' : 80,
        'x_max' : 160,
        'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      }
    },
  },
  # Numberofaddjets
  'Wen_SR':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
       'Higgs candidate mass [GeV]' : {
        'n_bin' : 16,
        'x_min' : 50,
        'x_max' : 190,
        'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      },
      #  'Higgs candidate pt' : {
      #   'n_bin' : 16,
      #   'x_min' : 250,
      #   'x_max' : 1200,
      #   'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      # },
      # 'Higgs candidate bb-tag' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
      # 'Higgs candidate tau21' : {
      #   'n_bin' : 16,
      #   'x_min' : 0,
      #   'x_max' : 1.0,
      #   'eval'  : 'FatjetAK08ungroomed_tau2[boost_HC_index]/FatjetAK08ungroomed_tau1[boost_HC_index]'
      # },
      # 'V and Higgs Candidate Pt ratio' : {
      #   'n_bin' : 16,
      #   'x_min' : 0,
      #   'x_max' : 1.4,
      #   'eval'  : 'V_pt/FatjetAK08ungroomed_pt[boost_HC_index]'
      # },
      # '# add. jets' : {
      #   'n_bin' : 5,
      #   'x_min' : -0.5,
      #   'x_max' : 4.5,
      #   'eval'  : 'boost_n_add_jets'
      # },
      # 'b-tag veto' : {
      #   'n_bin' : 2,
      #   'x_min' : -0.5,
      #   'x_max' : 1.5,
      #   'eval'  : 'boost_btag_veto'
      # },
      # 'c-tag veto' : {
      #   'n_bin' : 2,
      #   'x_min' : -0.5,
      #   'x_max' : 1.5,
      #   'eval'  : 'boost_ctag_veto'
      # },
    },
  },

  'Wmn_SR':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
      'Higgs candidate mass [GeV]' : {
        'n_bin' : 16,
        'x_min' : 50,
        'x_max' : 190,
        'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      },
      # 'Higgs candidate pt [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 250,
      #   'x_max' : 1200,
      #   'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      # },
      # 'Higgs candidate bb-tag' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
      # 'Higgs candidate tau21' : {
      #   'n_bin' : 16,
      #   'x_min' : 0,
      #   'x_max' : 1.0,
      #   'eval'  : 'FatjetAK08ungroomed_tau2[boost_HC_index]/FatjetAK08ungroomed_tau1[boost_HC_index]'
      # },
      # 'V and Higgs Candidate Pt ratio'  : {
      #   'n_bin' : 16,
      #   'x_min' : 0,
      #   'x_max' : 1.4,
      #   'eval'  : 'V_pt/FatjetAK08ungroomed_pt[boost_HC_index]'
      # },
      # '# add. jets' : {
      #   'n_bin' : 5,
      #   'x_min' : -0.5,
      #   'x_max' : 4.5,
      #   'eval'  : 'boost_n_add_jets'
      # },
      # 'b-tag veto' : {
      #   'n_bin' : 2,
      #   'x_min' : -0.5,
      #   'x_max' : 1.5,
      #   'eval'  : 'boost_btag_veto'
      # },
      # 'c-tag veto' : {
      #   'n_bin' : 2,
      #   'x_min' : -0.5,
      #   'x_max' : 1.5,
      #   'eval'  : 'boost_ctag_veto'
      # },
      # 'Higgs candidate mass [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 50,
      #   'x_max' : 190,
      #   'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      #   # 'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]*boost_sys_HC_AK08JEC_up'
      #   # 'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]*boost_sys_HC_AK08JEC_down'
      # },
    },
  },

  'Wen_CR_TT':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
      # 'Higgs candidate mass [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 50,
      #   'x_max' : 190,
      #   'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      # },
      'Higgs candidate pt [GeV]' : {
        'n_bin' : 16,
        'x_min' : 250,
        'x_max' : 1200,
        'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      },
      # 'Higgs candidate bb' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
    },
  },

  'Wmn_CR_TT':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
      # 'Higgs candidate mass [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 50,
      #   'x_max' : 190,
      #   'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      # },
      'Higgs candidate pt [GeV]' : {
        'n_bin' : 16,
        'x_min' : 250,
        'x_max' : 1200,
        'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      },
      # 'Higgs candidate bb' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
      # 'c veto weight' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_weight_ctag_veto'   
      # },
      # 'c veto weight bc up' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_bc_up'   
      # },
      # 'c veto weight bc down' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_bc_down'   
      # },
      # 'c veto weight light up' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_light_up'   
      # },
      # 'c veto weight light down' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_light_down'
      # }
    }
  },

  'Wen_CR_HF':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
       # 'Higgs candidate mass [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 50,
      #   'x_max' : 190,
      #   'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      # },
      'Higgs candidate pt [GeV]' : {
        'n_bin' : 16,
        'x_min' : 250,
        'x_max' : 1200,
        'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      },
      # 'Higgs candidate bb' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
    },
  },

  'Wmn_CR_HF':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
       # 'Higgs candidate mass [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 50,
      #   'x_max' : 190,
      #   'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      # },
      'Higgs candidate pt [GeV]' : {
        'n_bin' : 16,
        'x_min' : 250,
        'x_max' : 1200,
        'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      },
      # 'Higgs candidate bb' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
      # 'c veto weight' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_weight_ctag_veto'   
      # },
      # 'c veto weight bc up' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_bc_up'   
      # },
      # 'c veto weight bc down' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_bc_down'   
      # },
      # 'c veto weight light up' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_light_up'   
      # },
      # 'c veto weight light down' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'boost_sys_ctag_veto_light_down'
      # }
    },
  },

  'Wen_CR_LF':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
       # 'Higgs candidate mass [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 50,
      #   'x_max' : 190,
      #   'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      # },
      'Higgs candidate pt [GeV]' : {
        'n_bin' : 16,
        'x_min' : 250,
        'x_max' : 1200,
        'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      },
      # 'Higgs candidate bb' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
    },
  },

  'Wmn_CR_LF':{
    'split_samples'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'], # [], # 
    'ratio_plot'      : 'Data_MC_DooDMC', #'Data_MC',  # 'SigBkg'
    'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['all'],
    'variables' :{
       # 'Higgs candidate mass [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 50,
      #   'x_max' : 190,
      #   'eval'  : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'
      # },
      'Higgs candidate pt [GeV]' : {
        'n_bin' : 16,
        'x_min' : 250,
        'x_max' : 1200,
        'eval'  : 'FatjetAK08ungroomed_pt[boost_HC_index]'
      },
      # 'Higgs candidate bb' : {
      #   'n_bin' : 16,
      #   'x_min' : -1,
      #   'x_max' : 1,
      #   'eval'  : 'FatjetAK08ungroomed_bbtag[boost_HC_index]'
      # },
      # 'V pt [GeV]' : {
      #   'n_bin' : 16,
      #   'x_min' : 250,
      #   'x_max' : 1200,
      #   'eval'  : 'V_pt'
      # },      
    },
  },
}

# -----------------------------------------------------------------------------
postfit_plot = {
  'input_file'      : 'fitDiagnostics.root',
  'root_dir'        : 'shapes_fit_s', #'shapes_prefit', #
  'process'         : ['data', 'TT', 'VV', 'WH', 'Wj0b', 'Wj1b', 'Wj2b', 's_Top'],
  'process_type'    : {'data':'data', 'TT':'mc', 'VV':'mc', 'WH':'mc', 'Wj0b':'mc', 'Wj1b':'mc', 'Wj2b':'mc', 's_Top':'mc'},
  # 'variable'        : 'Higgs candidate pt [GeV]',
  'variable'        : 'Higgs candidate mass [GeV]',
  'sample_x100'     : ['WH'],
  'ratio_plot'      : 'Data_MC_DooDMC', # 'Data_MC',  # 'SigBkg'
  'ratio_plot_sig'  : [],         # ['WplusHPOWPYT', 'WminusHPOWPYT'],
  'ratio_plot_bgk'  : ['all'],
  # 'n_bin'           : 16,
  # 'x_min'           : 250,
  # 'x_max'           : 1200,

  # # new
  # SR
  'n_bin'           : 16,
  'x_min'           : 50,
  'x_max'           : 190
  # # CR
  # 'n_bin'           : 13,
  # 'x_min'           : 250,
  # 'x_max'           : 900


}

# -----------------------------------------------------------------------------

definitions = {
  'legend': {
    'SE'                    :'Data',
    'SM'                    :'Data',
    'SE_el'                 :'Data',
    'SM_mu'                 :'Data',
    'data'                  :'Data',
    'WZ'                    :'VV',
    'WZ_light'              :'VVLF',
    'WZ_c'                  :'VVLF',
    'WZ_1b'                 :'VVHF',
    'WZ_2b'                 :'VVHF',
    'WW'                    :'VV',
    'VV'                    :'VV',
    'WW_light'              :'VVLF',
    'WW_c'                  :'VVLF',
    'WW_1b'                 :'VVHF',
    'WW_2b'                 :'VVHF',
    'ZZ'                    :'VV',
    'ZZ_light'              :'VVLF',
    'ZZ_c'                  :'VVLF',
    'ZZ_1b'                 :'VVHF',
    'ZZ_2b'                 :'VVHF',
    'ZH'                    :'ZH',
    'WH'                    :'WH',
    'WminusHPOWPYT'         :'WH',
    'WplusHPOWPYT'          :'WH',
    'TT'                    :'t#bar{t}',
    'TT_TTincl'             :'t#bar{t}',
    'TTMtt700'              :'t#bar{t}',
    'TTMtt1000'             :'t#bar{t}',
    'TbarToLeptonst'        :'Single top',
    'TToLeptonst'           :'Single top',
    'TToLeptonss'           :'Single top',
    'TtW'                   :'Single top',
    'TbartW'                :'Single top',
    's_Top'                 :'Single top',
    'QCD100'                :'QCD',
    'QCD200'                :'QCD',
    'QCD300'                :'QCD',
    'QCD400'                :'QCD',
    'QCD500'                :'QCD',
    'QCD700'                :'QCD',
    'QCD1000'               :'QCD',
    'QCD1500'               :'QCD',
    'QCD2000'               :'QCD',
    # WJets
    # 'WJets'               :'W + jets',
    # 'WJets_light'         :'W + udscg',
    # 'WJets_c'             :'W + udscg', # 'W + c#bar{c}'
    # 'WJets_1b'            :'W + b',
    # 'WJets_2b'            :'W + b#bar{b}',
    'WBJets_light'          :'W + udscg',
    'WBJets_c'              :'W + udscg', # 'W + c#bar{c}'
    'WBJets_1b'             :'W + b',
    'WBJets_2b'             :'W + b#bar{b}',
    'WJetsBGen_light'       :'W + udscg',
    'WJetsBGen_c'           :'W + udscg', # 'W + c#bar{c}'
    'WJetsBGen_1b'          :'W + b',
    'WJetsBGen_2b'          :'W + b#bar{b}',
    'WJet100'               :'W + jets',
    'WJet100_light'         :'W + udscg',
    'WJet100_c'             :'W + udscg',
    'WJet100_1b'            :'W + b',
    'WJet100_2b'            :'W + b#bar{b}',
    'WJet250'               :'W + jets',
    'WJet250_light'         :'W + udscg',
    'WJet250_c'             :'W + udscg',
    'WJet250_1b'            :'W + b',
    'WJet250_2b'            :'W + b#bar{b}',
    'WJet400'               :'W + jets',
    'WJet400_light'         :'W + udscg',
    'WJet400_c'             :'W + udscg',
    'WJet400_1b'            :'W + b',
    'WJet400_2b'            :'W + b#bar{b}',
    'WJet600'               :'W + jets',
    'WJet600_light'         :'W + udscg',
    'WJet600_c'             :'W + udscg',
    'WJet600_1b'            :'W + b',
    'WJet600_2b'            :'W + b#bar{b}',
    'WBJets100'             :'W + jets',
    'WBJets100_lightB'      :'W + udscg',
    'WBJets100_cB'          :'W + udscg',
    'WBJets100_1bB'         :'W + b',
    'WBJets100_2bB'         :'W + b#bar{b}',
    'WBJets200'             :'W + jets',
    'WBJets200_lightB'      :'W + udscg',
    'WBJets200_cB'          :'W + udscg',
    'WBJets200_1bB'         :'W + b',
    'WBJets200_2bB'         :'W + b#bar{b}',
    'WBJetsFilter100'       :'W + jets',
    'WBJetsFilter100_lightB':'W + udscg',
    'WBJetsFilter100_cB'    :'W + udscg',
    'WBJetsFilter100_1bB'   :'W + b',
    'WBJetsFilter100_2bB'   :'W + b#bar{b}',
    'WBJetsFilter200'       :'W + jets',
    'WBJetsFilter200_lightB':'W + udscg',
    'WBJetsFilter200_cB'    :'W + udscg',
    'WBJetsFilter200_1bB'   :'W + b',
    'WBJetsFilter200_2bB'   :'W + b#bar{b}',
    'WJetsNLO'              :'W + jets',
    'WJetsNLO_lightIncl'    :'W + udscg',
    'WJetsNLO_cIncl'        :'W + udscg',
    'WJetsNLO_1bIncl'       :'W + b',
    'WJetsNLO_2bIncl'       :'W + b#bar{b}',
    # 'WJet800'     :'W + jets',
    # 'WJet800_light':'W + udscg',
    # 'WJet800_c'   :'W + udscg',
    # 'WJet800_1b'  :'W + b',
    # 'WJet800_2b'  :'W + b#bar{b}',
    # 'WJet1200'    :'W + jets',
    # 'WJet1200_light':'W + udscg',
    # 'WJet1200_c'  :'W + udscg',
    # 'WJet1200_1b' :'W + b',
    # 'WJet1200_2b' :'W + b#bar{b}',
    # 'WJet2500'    :'W + jets',
    # 'WJet2500_light':'W + udscg',
    # 'WJet2500_c'  :'W + udscg',
    # 'WJet2500_1b' :'W + b',
    # 'WJet2500_2b' :'W + b#bar{b}',
    'Wj0b'                  : 'W + udscg',
    'Wj1b'                  : 'W + b',
    'Wj2b'                  : 'W + b#bar{b}',

    'ZJets'                 :'Z + jets',
    'ZJets_light'           :'Z + udscg',
    'ZJets_c'               :'Z + udscg',
    'ZJets_1b'              :'Z + b',
    'ZJets_2b'              :'Z + b#bar{b}',
    'ZJet100'               :'Z + jets',
    'ZJet100_light'         :'Z + udscg',
    'ZJet100_c'             :'Z + udscg',
    'ZJet100_1b'            :'Z + b',
    'ZJet100_2b'            :'Z + b#bar{b}',
    'ZJet200'               :'Z + jets',
    'ZJet200_light'         :'Z + udscg',
    'ZJet200_c'             :'Z + udscg',
    'ZJet200_1b'            :'Z + b',
    'ZJet200_2b'            :'Z + b#bar{b}',
    'ZJet400'               :'Z + jets',
    'ZJet400_light'         :'Z + udscg',
    'ZJet400_c'             :'Z + udscg',
    'ZJet400_1b'            :'Z + b',
    'ZJet400_2b'            :'Z + b#bar{b}',
    'ZJet600'               :'Z + jets',
    'ZJet600_light'         :'Z + udscg',
    'ZJet600_c'             :'Z + udscg',
    'ZJet600_1b'            :'Z + b',
    'ZJet600_2b'            :'Z + b#bar{b}',
    'sample_x100'           :'WHx10 SM expected'
  },

  'colors': {
    'SE'                    :1,
    'SM'                    :1,
    'SE_el'                 :1,
    'SM_mu'                 :1,
    'data'                  :1,

    'VV'                    :920,
    'WZ'                    :920,
    'WZ_light'              :920,
    'WZ_c'                  :920,
    'WZ_1b'                 :921,
    'WZ_2b'                 :921,
    'WW'                    :920,
    'WW_light'              :920,
    'WW_c'                  :920,
    'WW_1b'                 :921,
    'WW_2b'                 :921,
    'ZZ'                    :920,
    'ZZ_light'              :920,
    'ZZ_c'                  :920,
    'ZZ_1b'                 :921,
    'ZZ_2b'                 :921,
    'ZH'                    :632,
    'WH'                    :634,

    'WminusHPOWPYT'         :634,  # 96
    'WplusHPOWPYT'          :634,  # 94    
    'TT'                    :596,  # 600
    'TT_TTincl'             :596,
    'TTMtt700'              :596,
    'TTMtt1000'             :596,
    'TbarToLeptonst'        :840,
    'TToLeptonst'           :840,
    'TToLeptonss'           :840,
    'TtW'                   :840,
    'TbartW'                :840,
    's_Top'                 :840,

    'QCD'                   :613,
    'QCD100'                :613,
    'QCD200'                :613,
    'QCD300'                :613,
    'QCD400'                :613,
    'QCD500'                :613,
    'QCD700'                :613,
    'QCD1000'               :613,
    'QCD1500'               :613,
    'QCD2000'               :613,
    # WJets
    'WBJets100'             :814,
    'WBJets100_lightB'      :814,
    'WBJets100_cB'          :814,
    'WBJets100_1bB'         :815,
    'WBJets100_2bB'         :820,
    'WBJets200'             :814,
    'WBJets200_lightB'      :814,
    'WBJets200_cB'          :814,
    'WBJets200_1bB'         :815,
    'WBJets200_2bB'         :820,
    'WBJetsFilter100'       :814,
    'WBJetsFilter100_lightB':814,
    'WBJetsFilter100_cB'    :814,
    'WBJetsFilter100_1bB'   :815,
    'WBJetsFilter100_2bB'   :820,
    'WBJetsFilter200'       :814,
    'WBJetsFilter200_lightB':814,
    'WBJetsFilter200_cB'    :814,
    'WBJetsFilter200_1bB'   :815,
    'WBJetsFilter200_2bB'   :820,
    # 'WJets'                 : 814,
    # 'WJets_light'           : 814,
    # 'WJets_c'               : 815,
    # 'WJets_1b'              : 815,
    # 'WJets_2b'              : 820,
    'WJetsNLO'              :814,
    'WJetsNLO_lightIncl'    :814,
    'WJetsNLO_cIncl'        :814,
    'WJetsNLO_1bIncl'       :815,
    'WJetsNLO_2bIncl'       :820,      
    # 'WBJets_light'          : 814,
    # 'WBJets_c'              : 815,
    # 'WBJets_1b'             : 815,
    # 'WBJets_2b'             : 820,
    # 'WJetsBGen_light'       : 814,
    # 'WJetsBGen_c'           : 815,
    # 'WJetsBGen_1b'          : 815,
    # 'WJetsBGen_2b'          : 820,
    'WJet100'               :814,
    'WJet100_light'         :814,
    'WJet100_c'             :814,
    'WJet100_1b'            :815,
    'WJet100_2b'            :820,
    'WJet250'               :814,
    'WJet250_light'         :814,
    'WJet250_c'             :814,
    'WJet250_1b'            :815,
    'WJet250_2b'            :820,
    'WJet400'               :814,
    'WJet400_light'         :814,
    'WJet400_c'             :814,
    'WJet400_1b'            :815,
    'WJet400_2b'            :820,
    'WJet600'               :814,
    'WJet600_light'         :814,
    'WJet600_c'             :814,
    'WJet600_1b'            :815,
    'WJet600_2b'            :820,
    # 'WJet800'               : 814,
    # 'WJet800_light'         : 814,
    # 'WJet800_c'             : 815,
    # 'WJet800_1b'            : 815,
    # 'WJet800_2b'            : 820,
    # 'WJet1200'              : 814,
    # 'WJet1200_light'        : 814,
    # 'WJet1200_c'            : 815,
    # 'WJet1200_1b'           : 815,
    # 'WJet1200_2b'           : 820,
    # 'WJet2500'              : 814,
    # 'WJet2500_light'        : 814,
    # 'WJet2500_c'            : 815,
    # 'WJet2500_1b'           : 815,
    # 'WJet2500_2b'           : 820,
    'Wj0b'                  :814,
    'Wj1b'                  :815,
    'Wj2b'                  :820,

    'ZJets'                 :402,
    'ZJets_light'           :402,
    'ZJets_c'               :397,
    'ZJets_1b'              :397,
    'ZJets_2b'              :400,
    'ZJet100'               :402,
    'ZJet100_light'         :402,
    'ZJet100_c'             :397,
    'ZJet100_1b'            :397,
    'ZJet100_2b'            :400,
    'ZJet200'               :402,
    'ZJet200_light'         :402,
    'ZJet200_c'             :397,
    'ZJet200_1b'            :397,
    'ZJet200_2b'            :400,
    'ZJet400'               :402,
    'ZJet400_light'         :402,
    'ZJet400_c'             :397,
    'ZJet400_1b'            :397,
    'ZJet400_2b'            :400,
    'ZJet600'               :402,
    'ZJet600_light'         :402,
    'ZJet600_c'             :397,
    'ZJet600_1b'            :397,
    'ZJet600_2b'            :400,
    'sample_x100'           :634
  },

  'plot_order': [
    'SE',
    'SM',
    'SE_el',
    'SM_mu',
    'data',

    'TT',
    'TT_TTincl',
    'TTMtt700',
    'TTMtt1000',

    'WJetsNLO',
    'WJets',
    'WBJets100',
    'WBJets200', 
    'WBJetsFilter100',
    'WBJetsFilter200',
    'WJet100',
    'WJet250',
    'WJet400',
    'WJet600',
    'WJet800',
    'WJet1200',
    'WJet2500',
    'WJetsNLO_lightIncl',
    'WJets_light',
    'WBJets_light',
    'WBJets200_lightB',
    'WBJets100_lightB',
    'WBJetsFilter100_lightB',
    'WBJetsFilter200_lightB',
    'WJetsBGen_light',
    'WJet100_light',
    'WJet250_light',
    'WJet400_light',
    'WJet600_light',
    'WJet800_light',
    'WJet1200_light',
    'WJet2500_light',
    'Wj0b',
    'WJetsNLO_cIncl',
    'WJets_c',
    'WBJets_c',
    'WBJets100_cB',
    'WBJets200_cB',
    'WBJetsFilter100_cB',
    'WBJetsFilter200_cB',
    'WJetsBGen_c',
    'WJet100_c',
    'WJet250_c',
    'WJet400_c',
    'WJet600_c',
    'WJet800_c',
    'WJet1200_c',
    'WJet2500_c',
    'WJetsNLO_1bIncl',
    'WJets_1b',
    'WBJets_1b',
    'WBJets100_1bB',
    'WBJets200_1bB',
    'WBJetsFilter100_1bB',
    'WBJetsFilter200_1bB',      
    'Wj1b',
    'WJetsBGen_1b',
    'WJet100_1b',
    'WJet250_1b',
    'WJet400_1b',
    'WJet600_1b',
    'WJet800_1b',
    'WJet1200_1b',
    'WJet2500_1b',
    'WJetsNLO_2bIncl',
    'Wj2b',
    'WJets_2b',
    'WBJets_2b',
    'WBJets100_2bB',
    'WBJets200_2bB',
    'WBJetsFilter100_2bB',
    'WBJetsFilter200_2bB',
    'WJetsBGen_2b',
    'WJet100_2b',
    'WJet250_2b',
    'WJet400_2b',
    'WJet600_2b',
    'WJet800_2b',
    'WJet1200_2b',
    'WJet2500_2b',

    'TbarToLeptonst',
    'TToLeptonst',
    'TToLeptonss',
    'TtW',
    'TbartW',
    's_Top',
    'WZ',
    'WZ_light',
    'WZ_c',
    'WZ_1b',
    'WZ_2b',
    'WW',
    'WW_light',
    'WW_c',
    'WW_1b',
    'WW_2b',
    'ZZ',
    'ZZ_light',
    'ZZ_c',
    'ZZ_1b',
    'ZZ_2b',
    'ZH',
    'VV',

    'QCD100',
    'QCD200',
    'QCD300',
    'QCD400',
    'QCD500',
    'QCD700',
    'QCD1000',
    'QCD1500',
    'QCD2000',

    'ZJets',
    'ZJet100',
    'ZJet200',
    'ZJet400',
    'ZJet600',
    'ZJets_light',
    'ZJet100_light',
    'ZJet200_light',
    'ZJet400_light',
    'ZJet600_light',
    'ZJets_1b',
    'ZJet100_1b',
    'ZJet200_1b',
    'ZJet400_1b',
    'ZJet600_1b',
    'ZJets_c',
    'ZJet100_c',
    'ZJet200_c',
    'ZJet400_c',
    'ZJet600_c',
    'ZJets_2b',
    'ZJet100_2b',
    'ZJet200_2b',
    'ZJet400_2b',
    'ZJet600_2b',
    'WH',
    'WminusHPOWPYT',
    'WplusHPOWPYT',
    'sample_x100'
  ] 
} 