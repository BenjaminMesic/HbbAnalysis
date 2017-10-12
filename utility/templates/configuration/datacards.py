datacard = {
  # TBD: Add Data, right now set to some default values

  'datacard_name': 'test.txt', # 'vhbb_Wmn_13TeV.txt', #
  'template_name': 'test.root', #'vhbb_Wmn_13TeV.root', #

  'channels'                      : ['Wmn'], #[ 'Wmn', 'Wen'],
  'number_of_channels'            : 1,
  'input_files': {
    'Wmn' : '/users/bmesic/WorkingDirectory/2017/17_10_Hbb_v25/CMSSW_9_4_0_pre1/src/HbbAnalysis/analysis/Wlv/results/plots/test.root'
    # 'Wmn' : '/users/bmesic/WorkingDirectory/17_04_Hbb_v25/CMSSW_7_4_16/src/HbbAnalysis/plots/Wlv/Wmn.root',
    # 'Wen' : '/users/bmesic/WorkingDirectory/17_04_Hbb_v25/CMSSW_7_4_16/src/HbbAnalysis/plots/Wlv/Wen.root',
    # 'Wmn' : '/users/bmesic/WorkingDirectory/2017/17_07_Hbb_v24/CMSSW_7_4_16/src/HbbAnalysis/analysis/Wlv/results/plots/Wmn_110_140.root',
    # 'Wen' : '/users/bmesic/WorkingDirectory/2017/17_07_Hbb_v24/CMSSW_7_4_16/src/HbbAnalysis/analysis/Wlv/results/plots/Wen_110_140.root',
    # 'Wmn' : '/users/bmesic/WorkingDirectory/2017/17_07_Hbb_v24/CMSSW_7_4_16/src/HbbAnalysis/analysis/Wlv/results/plots/Wmn_full.root',
    # 'Wen' : '/users/bmesic/WorkingDirectory/2017/17_07_Hbb_v24/CMSSW_7_4_16/src/HbbAnalysis/analysis/Wlv/results/plots/Wen_full.root',
  },

  # Name of the variable used for doing fit
  'variable' : 'Higgs candidate mass',

  'number_of_backgrounds'         : 1,
  'number_of_nuisance_parameters' : 0,
 
  # which datacard type to use: counting, shape, ...
  'datacard_type': 'shape', #'counting', # 

  # Only uncommented process will end up in datacard
  'process' :[
    ['WH'   , '0'],
    ['TT'   , '1'],
    # ['Wj0b' , '2'],
    # ['Wj1b' , '3'],
    # ['Wj2b' , '4'],
    # ['s_Top' , '5'],
    # ['QCD'  , '6'],
    # ['VVHF' , '6'],
    # ['VVLF' , '7'],
    # ['Zj0b' , '8'],
    # ['Zj1b' , '9'],
    # ['Zj2b' , '10']
  ],

  'nuisance_parameters': {
    # 'lumi_13TeV': {
    #   'model': 'lnN',
    #   'description': 'A 6.2% lumi uncertainty',
    #   'process':{
    #     'ZH'    : 1.062,
    #     'WH'    : 1.062,
    #     's_Top' : 1.062,
    #     'TT'    : 1.062,
    #     'QCD'   : 1.062,
    #     'Wj0b'  : 1.062,
    #     'Wj1b'  : 1.062,
    #     'Wj2b'  : 1.062,
    #     'VVHF'  : 1.062,
    #     'VVLF'  : 1.062,
    #     'Zj0b'  : 1.062,
    #     'Zj1b'  : 1.062,
    #     'Zj2b'  : 1.062
    #   }
    # },
  #   'CMS_vhbb_puWeight': {
  #     'model': 'shape',
  #     'process':{
  #       'ZH'  : 1.0,
  #       'WH'  : 1.0,
  #       's_Top' : 1.0,
  #       'TT'  : 1.0,
  #       'Wj0b'  : 1.0,
  #       'Wj1b'  : 1.0,
  #       'Wj2b'  : 1.0,
  #       'VVHF'  : 1.0,
  #       'VVLF'  : 1.0,
  #       'Zj0b'  : 1.0,
  #       'Zj1b'  : 1.0,
  #       'Zj2b'  : 1.0
  #     }
  #   }, 
  },

  # subsample/sample -> process 
  'definitions'     : {
    'SE_el'         : 'data',
    'SE'            : 'data',
    'SM_mu'         : 'data',
    'SM'            : 'data',
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
    'WminusHPOWPYT' : 'WH',
    'WplusHPOWPYT'  : 'WH'
  }
}