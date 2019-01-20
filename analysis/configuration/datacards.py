datacard = {

  'number_of_nuisances' : '*', # If None, len(sys)

  # Channels for which datacards are created
  'channels' : {
    'test'   : {
      'name'     : 'test',
      'variable' : 'Higgs candidate mass'
    },
    # 'Wen_SR'   : {
    #   'name'     : 'WenHighPt',
    #   'variable' : 'Higgs candidate mass'
    # },
    # 'Wmn_SR'   : {
    #   'name'     : 'WmnHighPt',
    #   'variable' : 'Higgs candidate mass'
    # },
    # 'Wen_CR_TT': {
    #   'name'     : 'ttWen',
    #   'variable' : 'Higgs candidate pt'
    # },
    # 'Wmn_CR_TT': {
    #   'name'     : 'ttWmn',
    #   'variable' : 'Higgs candidate pt'
    # },
    # 'Wen_CR_HF': {
    #   'name'     : 'whfWen',
    #   'variable' : 'Higgs candidate pt'
    # },
    # 'Wmn_CR_HF': {
    #   'name'     : 'whfWmn',
    #   'variable' : 'Higgs candidate pt'
    # },
    # 'Wen_CR_LF': {
    #   'name'     : 'wlfWen',
    #   'variable' : 'Higgs candidate pt'
    # },
    # 'Wmn_CR_LF': {
    #   'name'     : 'wlfWmn',
    #   'variable' : 'Higgs candidate pt'
    # }
  },

  # Variables for fit, CR one
  'variables' : {
    'Higgs candidate mass' : {
      'tree variable' : 'FatjetAK08ungroomed_mprunedcorr[boost_HC_index]',
      'bin'           : 16,
      'min'           : 50,
      'max'           : 190
    },
    'Higgs candidate pt'   : {
      'tree variable' : 'FatjetAK08ungroomed_pt[boost_HC_index]',
      'bin'           : 13,
      'min'           : 250,
      'max'           : 900
    }
  },

  # which datacard type to use: counting, shape, ...
  'datacard_type': 'shape', #'counting', # 

  'SF_samples_apply' : True,
  'SF_samples_string' : 
    'SF_TT_Wln    rateParam  <channel> TT    1  [0.1,5]' + '\n' 
    'SF_Wj0b_Wln  rateParam  <channel> Wj0b  1  [0.1,5]' + '\n'
    'SF_Wj1b_Wln  rateParam  <channel> Wj1b  1  [0.1,5]' + '\n'
    'SF_Wj2b_Wln  rateParam  <channel> Wj2b  1  [0.1,5]',
    # 'SF_TT_Wln    rateParam  <channel> TT    1  [0.1,5]' + '\n',

  # Only uncommented process will end up in datacard
  'process' :[
    ['WH'   , '0'],
    ['TT'   , '1'],
    ['Wj0b' , '2'],
    ['Wj1b' , '3'],
    ['Wj2b' , '4'],
    ['s_Top' , '5'],
    # ['QCD'  , '6'], # NOT USED
    ['VV' , '6'],
    # ['VVLF' , '7'], # NOT USED
    # ['Zj0b' , '8'], # NOT USED
    # ['Zj1b' , '9'], # NOT USED
    # ['Zj2b' , '10'] # NOT USED
  ],

  # https://cms-hcomb.gitbooks.io/combine/content/part2/bin-wise-stats.html
  'auto_sys_uncertainty_apply'  : True, # in _export_datacard if condition
  'auto_sys_uncertainty_string' : '* autoMCStats 0',

  'nuisance_parameters': {

    # # --------------------------
    # # lnN
    # # --------------------------

    # 'lumi_13TeV': {
    #   'model': 'lnN',
    #   'description': 'A 2.5% lumi uncertainty',
    #   'process':{
    #     # 'ZH'    : 1.025,
    #     'WH'    : 1.025,
    #     's_Top' : 1.025,
    #     'TT'    : 1.025,
    #     # 'QCD'   : 1.025,
    #     'Wj0b'  : 1.025,
    #     'Wj1b'  : 1.025,
    #     'Wj2b'  : 1.025,
    #     # 'VVHF'  : 1.025,
    #     # 'VVLF'  : 1.025,
    #     # 'Zj0b'  : 1.025,
    #     # 'Zj1b'  : 1.025,
    #     # 'Zj2b'  : 1.025,
    #     'VV'    : 1.025
    #   }
    # },

    # 'CMS_vhbb_boost_EWK_13TeV' : {
    #   'model': 'lnN',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.02
    #   }
    # },

    # 'CMS_vhbb_eff_e_13TeV' : {
    #   'model': 'lnN',
    #   'description': '',
    #   'process':{
    #     'ZH'    : 1.03,
    #     'WH'    : 1.03,
    #     's_Top' : 1.03,
    #     'TT'    : 1.03,
    #     'QCD'   : 1.03,
    #     'Wj0b'  : 1.03,
    #     'Wj1b'  : 1.03,
    #     'Wj2b'  : 1.03,
    #     'VVHF'  : 1.03,
    #     'VVLF'  : 1.03,
    #     'Zj0b'  : 1.03,
    #     'Zj1b'  : 1.03,
    #     'Zj2b'  : 1.03,
    #     'VV'    : 1.03
    #   }
    # },

    # 'pdf_gg' : {
    #   'model': 'lnN',
    #   'description': '',
    #   'process':{
    #     's_Top' : 1.01,
    #   }    
    # },

    # 'pdf_qqbar' : {
    #   'model': 'lnN',
    #   'description': '',
    #   'process':{
    #     'ZH'    : 1.01,
    #     'WH'    : 1.01,
    #     'VV'    : 1.01
    #   }    
    # },

    # # --------------------------
    # # Shapes
    # # --------------------------

    # # ---------------------------------------------------------------------
    # # 'CMS_vhbb_Vpt_TT' : {
    # #   'model': 'shape',
    # #   'description': '',
    # #   'process':{
    # #     'TT'    : 1.0,
    # #   },
    # #   'weight':{
    # #     'main'  : 'scale_factor_Vpt_TT(V_pt, 0)',
    # #     'Up'    : 'scale_factor_Vpt_TT(V_pt, 0.000089)',
    # #     'Down'  : 'scale_factor_Vpt_TT(V_pt, -0.000089)'
    # #   }
    # # },

    # # ---------------------------------------------------------------------
    
    # 'CMS_vhbb_puWeight': {
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     # 'ZH'    : 1.0,
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     # 'VVHF'  : 1.0,
    #     # 'VVLF'  : 1.0,
    #     # 'Zj0b'  : 1.0,
    #     # 'Zj1b'  : 1.0,
    #     # 'Zj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'weight':{
    #     'main'  : 'puWeight',
    #     'Up'    : 'puWeightUp',
    #     'Down'  : 'puWeightDown'
    #   }
    # },

    # 'CMS_vhbb_AK08JEC': {
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'selection':{
    #     'main'  : ['FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'],
    #     'Up'    : ['(FatjetAK08ungroomed_mprunedcorr[boost_HC_index]*boost_sys_HC_AK08JEC_up)'],
    #     'Down'  : ['(FatjetAK08ungroomed_mprunedcorr[boost_HC_index]*boost_sys_HC_AK08JEC_down)']
    #   },
    # },

    # 'CMS_vhbb_AK08JER': {
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'selection':{
    #     'main'  : ['FatjetAK08ungroomed_mprunedcorr[boost_HC_index]'],
    #     'Up'    : ['(FatjetAK08ungroomed_mprunedcorr[boost_HC_index]*boost_sys_HC_AK08JER_up)'],
    #     'Down'  : ['(FatjetAK08ungroomed_mprunedcorr[boost_HC_index]*boost_sys_HC_AK08JER_down)']
    #   }
    # },

    # 'CMS_vhbb_AK08bb_tag':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : 'scale_factor_bb_tag(FatjetAK08ungroomed_pt[boost_HC_index])',
    #     'Up'    : 'boost_sys_HC_bb_up',
    #     'Down'  : 'boost_sys_HC_bb_down'
    #   }    
    # },

    # 'CMS_vhbb_AK08bb_mistag':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'TT'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : 'scale_factor_bb_mistag(FatjetAK08ungroomed_pt[boost_HC_index])',
    #     'Up'    : 'boost_sys_HC_bb_mistag_up',
    #     'Down'  : 'boost_sys_HC_bb_mistag_down'
    #   }    
    # },

    # 'CMS_vhbb_AK08tau21':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0
    #   },
    #   'weight':{
    #     'main'  : 'scale_factor_tau21()',
    #     'Up'    : 'boost_sys_HC_tau21_up',
    #     'Down'  : 'boost_sys_HC_tau21_down'
    #   }    
    # },

    # 'CMS_vhbb_AK08tau21_pt':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0
    #   },
    #   'weight':{
    #     'main'  : 'scale_factor_tau21_pt(FatjetAK08ungroomed_pt[boost_HC_index])',
    #     'Up'    : 'boost_sys_HC_tau21_pt_up',
    #     'Down'  : 'boost_sys_HC_tau21_pt_down'
    #   }    
    # },

    # 'CMS_vhbb_AK04JEC': {
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'selection':{
    #     'main'  : ['boost_n_add_jets < 2', 'boost_btag_veto == 1', 'boost_ctag_veto == 1'],
    #     'Up'    : ['boost_sys_n_add_jets_AK04JEC_up < 2', 'boost_sys_btag_veto_AK04JEC_up == 1', 'boost_sys_ctag_veto_AK04JEC_up == 1'],
    #     'Down'  : ['boost_sys_n_add_jets_AK04JEC_down < 2', 'boost_sys_btag_veto_AK04JEC_down == 1', 'boost_sys_ctag_veto_AK04JEC_down == 1']
    #   }    
    # },

    # 'CMS_vhbb_AK04JER': {
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'selection':{
    #     'main'  : ['boost_n_add_jets < 2', 'boost_btag_veto == 1', 'boost_ctag_veto == 1'],
    #     'Up'    : ['boost_sys_n_add_jets_AK04JER_up < 2', 'boost_sys_btag_veto_AK04JER_up == 1', 'boost_sys_ctag_veto_AK04JER_up == 1'],
    #     'Down'  : ['boost_sys_n_add_jets_AK04JER_down < 2', 'boost_sys_btag_veto_AK04JER_down == 1', 'boost_sys_ctag_veto_AK04JER_down == 1']
    #   }    
    # },

    # 'CMS_vhbb_AK04btag_bc':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'weight':{
    #     'main'  : 'boost_weight_btag_veto',
    #     'Up'    : 'boost_sys_btag_veto_bc_up',
    #     'Down'  : 'boost_sys_btag_veto_bc_down'
    #   }    
    # },

    # 'CMS_vhbb_AK04btag_light':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'weight':{
    #     'main'  : 'boost_weight_btag_veto',
    #     'Up'    : 'boost_sys_btag_veto_light_up',
    #     'Down'  : 'boost_sys_btag_veto_light_down'
    #   }    
    # },

    # 'CMS_vhbb_AK04ctag_bc':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'weight':{
    #     'main'  : 'boost_weight_ctag_veto',
    #     'Up'    : 'boost_sys_ctag_veto_bc_up',
    #     'Down'  : 'boost_sys_ctag_veto_bc_down'
    #   }    
    # },

    # 'CMS_vhbb_AK04ctag_light':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #     's_Top' : 1.0,
    #     'TT'    : 1.0,
    #     'Wj0b'  : 1.0,
    #     'Wj1b'  : 1.0,
    #     'Wj2b'  : 1.0,
    #     'VV'    : 1.0
    #   },
    #   'weight':{
    #     'main'  : 'boost_weight_ctag_veto',
    #     'Up'    : 'boost_sys_ctag_veto_light_up',
    #     'Down'  : 'boost_sys_ctag_veto_light_down'
    #   }    
    # },

    # 'CMS_vhbb_LHE_weights_scale_muF_WH':{
      
    #   # https://twiki.cern.ch/twiki/bin/viewauth/CMS/VHiggsBBCodeUtils#Event_reweighting
      
    #   # LHE_weights_scale_id[0] = 1002  # muR=1,     muF=2
    #   # LHE_weights_scale_id[1] = 1003  # muR=1,     muF=0.5
    #   # LHE_weights_scale_id[2] = 1004  # muR=2,     muF=1
    #   # LHE_weights_scale_id[3] = 1007  # muR=0.5,   muF=1
    #   # LHE_weights_scale_id[4] = 1005  # muR=2,     muF=2
    #   # LHE_weights_scale_id[5] = 1009  # muR=0.5,   muF=0.5'
      
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[0]*',
    #     'Down'  : 'LHE_weights_scale_wgt[1]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_0',
    #     'Down'  : 'CountWeightedLHEWeightScale_1'
    #     }
    # },

    # 'CMS_vhbb_LHE_weights_scale_muF_TT':{

    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'TT'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[0]*',
    #     'Down'  : 'LHE_weights_scale_wgt[1]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_0',
    #     'Down'  : 'CountWeightedLHEWeightScale_1'
    #   }
    # },

    # 'CMS_vhbb_LHE_weights_scale_muF_Wj0b':{
      
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'Wj0b'  : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[0]*',
    #     'Down'  : 'LHE_weights_scale_wgt[1]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_0',
    #     'Down'  : 'CountWeightedLHEWeightScale_1'
    #   }  
    # },

    # 'CMS_vhbb_LHE_weights_scale_muF_Wj1b':{
      
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'Wj1b'  : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[0]*',
    #     'Down'  : 'LHE_weights_scale_wgt[1]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_0',
    #     'Down'  : 'CountWeightedLHEWeightScale_1'
    #   }   
    # },

    # 'CMS_vhbb_LHE_weights_scale_muF_Wj2b':{
      
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'Wj2b'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[0]*',
    #     'Down'  : 'LHE_weights_scale_wgt[1]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_0',
    #     'Down'  : 'CountWeightedLHEWeightScale_1'
    #   }   
    # },

    # 'CMS_vhbb_LHE_weights_scale_muR_WH':{
      
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'WH'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[2]*',
    #     'Down'  : 'LHE_weights_scale_wgt[3]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_2',
    #     'Down'  : 'CountWeightedLHEWeightScale_3'
    #   }
    # },

    # 'CMS_vhbb_LHE_weights_scale_muR_TT':{

    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'TT'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[2]*',
    #     'Down'  : 'LHE_weights_scale_wgt[3]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_2',
    #     'Down'  : 'CountWeightedLHEWeightScale_3'
    #   }
    # },

    # 'CMS_vhbb_LHE_weights_scale_muR_Wj0b':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'Wj0b'  : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[2]*',
    #     'Down'  : 'LHE_weights_scale_wgt[3]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_2',
    #     'Down'  : 'CountWeightedLHEWeightScale_3'
    #   }   
    # },

    # 'CMS_vhbb_LHE_weights_scale_muR_Wj1b':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'Wj1b'  : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[2]*',
    #     'Down'  : 'LHE_weights_scale_wgt[3]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_2',
    #     'Down'  : 'CountWeightedLHEWeightScale_3'
    #   }  
    # },

    # 'CMS_vhbb_LHE_weights_scale_muR_Wj2b':{
    #   'model': 'shape',
    #   'description': '',
    #   'process':{
    #     'Wj2b'    : 1.0,
    #   },
    #   'weight':{
    #     'main'  : '1*',
    #     'Up'    : 'LHE_weights_scale_wgt[2]*',
    #     'Down'  : 'LHE_weights_scale_wgt[3]*'
    #   },
    #   'norm': {
    #     'Up'    : 'CountWeightedLHEWeightScale_2',
    #     'Down'  : 'CountWeightedLHEWeightScale_3'
    #   }  
    # },

    # # # --------------------------
    # # # MC bin uncertainty
    # # # --------------------------
    # # 'CMS_vhbb_stats_Top':{
    # #   'model'           : 'shape',
    # #   'description'     : '',
    # #   'bin_uncertainty' : 'TT', # process and this should be the same
    # #   'process':{
    # #     'TT'   : 1.0,
    # #   }
    # # },

    # # 'CMS_vhbb_stats_Wj2b':{
    # #   'model'           : 'shape',
    # #   'description'     : '',
    # #   'bin_uncertainty' : 'Wj2b', # process and this should be the same
    # #   'process':{
    # #     'Wj2b'   : 1.0,
    # #   }
    # # },

    # # 'CMS_vhbb_stats_Wj1b':{
    # #   'model'           : 'shape',
    # #   'description'     : '',
    # #   'bin_uncertainty' : 'Wj1b', # process and this should be the same
    # #   'process':{
    # #     'Wj1b'   : 1.0,
    # #   }
    # # },
    
    # # 'CMS_vhbb_stats_Wj0b':{
    # #   'model'           : 'shape',
    # #   'description'     : '',
    # #   'bin_uncertainty' : 'Wj0b', # process and this should be the same
    # #   'process':{
    # #     'Wj0b'   : 1.0,
    # #   }
    # # }

  },

  # subsample/sample -> process 
  'definitions'     : {
    'SE_el'         : 'data_obs',
    'SE'            : 'data_obs',
    'SM_mu'         : 'data_obs',
    'SM'            : 'data_obs',
    'QCD100'        : 'QCD',
    'QCD1000'       : 'QCD',
    'QCD1500'       : 'QCD',
    'QCD200'        : 'QCD',
    'QCD2000'       : 'QCD',
    'QCD300'        : 'QCD',
    'QCD500'        : 'QCD',
    'QCD700'        : 'QCD',
    'TT'            : 'TT',
    'TTMtt700'      : 'TT',
    'TTMtt1000'     : 'TT',
    'TbarToLeptonst': 's_Top',
    'TToLeptonst'   : 's_Top',
    'TToLeptonss'   : 's_Top',
    'TtW'           : 's_Top',
    'TbartW'        : 's_Top',
    'WJet100_1b'    : 'Wj1b',    
    'WJet100_2b'    : 'Wj2b',
    'WJet100_c'     : 'Wj0b',
    'WJet100_light' : 'Wj0b',
    'WJet250_1b'    : 'Wj1b',
    'WJet250_2b'    : 'Wj2b',
    'WJet250_c'     : 'Wj0b',
    'WJet250_light' : 'Wj0b',
    'WJet400_1b'    : 'Wj1b',
    'WJet400_2b'    : 'Wj2b',
    'WJet400_c'     : 'Wj0b',
    'WJet400_light' : 'Wj0b',
    'WJet600_1b'    : 'Wj1b',
    'WJet600_2b'    : 'Wj2b',
    'WJet600_c'     : 'Wj0b',
    'WJet600_light' : 'Wj0b',
    'WH'            : 'WH',
    'WminusHPOWPYT' : 'WH',
    'WplusHPOWPYT'  : 'WH',
    'ZH'            : 'VV',
    'WZ'            : 'VV',
    'WW'            : 'VV',
    'ZZ'            : 'VV',
    's_Top'         : 's_Top',
    'TT'            : 'TT',
    'Wj0b'          : 'Wj0b',
    'Wj1b'          : 'Wj1b',
    'Wj2b'          : 'Wj2b',
    'VV'            : 'VV'
  }
}
