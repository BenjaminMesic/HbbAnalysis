{
  'test_plot' :{
    'variables' : {
      'V_pt' : {
        'n_bin' : 10,
        'x_min' : 0,
        'x_max' : 800
      },
      'V_phi' : {
        'n_bin' : 10,
        'x_min' : -3.5,
        'x_max' : 3.5
      }
    }
  },

  'signal_region' :{
    'variables' : {
      'rho' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 40
      },
      'V_pt' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 800
      },
      'met_pt' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 400
      },
    }
  },

  'boost_bkg_estimate':{
    'split_samples'   : True,
    'boosted_trees'   : True,
    'event_by_event'  : False,
    'sample_x100'     : ['WminusHPOWPYT', 'WplusHPOWPYT'],
    'ratio_plot'      : 'Data_MC', #SigBkg
    'ratio_plot_sig'  : ['WplusHPOWPYT', 'WminusHPOWPYT'],
    'ratio_plot_bgk'  : ['TT'],
    'variables' :{
      # 'rho' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 40
      # },
      # 'deltaPhi(V_phi, FatjetAK08ungroomed_phi[0])' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 4
      # },
      'FatjetAK08ungroomed_mass[boost_FatJet_index_max_bb]' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 350
      },
      # 'FatjetAK08ungroomed_mass[1]' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 350
      # },
      # 'FatjetAK08ungroomed_pt[0]' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 800
      # },
      # 'naLeptons' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 3
      # },
      # 'vLeptons_pt[0]' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 500
      # },
      # 'V_pt' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 800
      # },
    } 
  },

  'BooST' :{
    'variables' : {
      # 'rho' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 40
      # },
      # 'FatjetAK08ungroomed_bbtag[0]' : {
      #   'n_bin' : 50,
      #   'x_min' : -1,
      #   'x_max' : 1
      # },
      # 'FatjetAK08ungroomed_mass[0]' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 300
      # },
      # 'FatjetAK08ungroomed_mass[1]' : {
      #   'n_bin' : 50,
      #   'x_min' : 0,
      #   'x_max' : 300
      # },
      'FatjetAK08ungroomed_mass[0]' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 300
      },
      # ----------------- Lepton Plots ----------------
      '( FatjetAK08ungroomed_pt < 200 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])<0.5)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])>0.5)*FatjetAK08ungroomed_mass' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 300
      },
      '( FatjetAK08ungroomed_pt < 200 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])<0.5)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])>0.5)'
      + '*deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 3
      },
      '( FatjetAK08ungroomed_pt < 200 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])<0.5)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])>0.5)'
      + '*Iteration$' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 5
      },
      '( FatjetAK08ungroomed_pt < 200 || FatjetAK08ungroomed_bbtag < 0.4 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])<0.5)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && FatjetAK08ungroomed_bbtag > 0.4 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])>0.5)'
      + '*FatjetAK08ungroomed_mass' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 300
      },
      '( FatjetAK08ungroomed_pt < 200 || FatjetAK08ungroomed_bbtag < 0.4 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])<0.5)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && FatjetAK08ungroomed_bbtag > 0.4 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])>0.5)'
      + '*FatjetAK08ungroomed_pt' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 700
      },
      '( FatjetAK08ungroomed_pt < 200 || FatjetAK08ungroomed_bbtag < 0.4 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])<0.5)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && FatjetAK08ungroomed_bbtag > 0.4 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, vLeptons_eta[0], vLeptons_phi[0])>0.5)'
      + '*V_pt' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 700
      },  
      # ----------------- Higgs Gen Plots ----------------
      '( FatjetAK08ungroomed_pt < 200 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])>0.1)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])<0.1)'
      + '*FatjetAK08ungroomed_mass' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 300
      },      
      '( FatjetAK08ungroomed_pt < 200 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])>0.1)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])<0.1)'
      + '*Iteration$' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 3
      },
      '( FatjetAK08ungroomed_pt < 200 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])>3.0)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])<3.0)'
      + '*deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 3
      },
      '( FatjetAK08ungroomed_pt < 200 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])>0.1)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])<0.1)'
      + '*FatjetAK08ungroomed_bbtag' : {
        'n_bin' : 50,
        'x_min' : -1,
        'x_max' : 1
      },
      '( FatjetAK08ungroomed_pt < 200 || FatjetAK08ungroomed_bbtag < 0.4 || deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])>0.1)*(-999)'  + ' + '
      + '( FatjetAK08ungroomed_pt > 200 && FatjetAK08ungroomed_bbtag > 0.4 && deltaR( FatjetAK08ungroomed_eta, FatjetAK08ungroomed_phi, GenHiggsBoson_eta[0], GenHiggsBoson_phi[0])<0.1)'
      + '*FatjetAK08ungroomed_mass' : {
        'n_bin' : 50,
        'x_min' : 0,
        'x_max' : 300
      },          
    }
  },  

  'definitions':{
    'legend': {
      'SE'    :'Data',
      'SM'      :'Data',
      'SE_el'     :'Data',
      'SM_mu'     :'Data',
      'WZ'      :'VV',
      'WZ_light'  :'VVLF',
      'WZ_c'    :'VVLF',
      'WZ_1b'   :'VVHF',
      'WZ_2b'   :'VVHF',
      'WW'      :'VV',
      'WW_light'  :'VVLF',
      'WW_c'    :'VVLF',
      'WW_1b'   :'VVHF',
      'WW_2b'   :'VVHF',
      'ZZ'      :'VV',
      'ZZ_light'  :'VVLF',
      'ZZ_c'    :'VVLF',
      'ZZ_1b'   :'VVHF',
      'ZZ_2b'   :'VVHF',
      'WH'      :'WH',
      'WminusHPOWPYT':'WH',
      'WplusHPOWPYT'  :'WH',
      'TT'      :'t#bar{t}',
      'QCD100'    :'QCD',
      'QCD200'    :'QCD',
      'QCD300'    :'QCD',
      'QCD400'    :'QCD',
      'QCD500'    :'QCD',
      'QCD700'    :'QCD',
      'QCD1000'   :'QCD',
      'QCD1500'   :'QCD',
      'QCD2000'   :'QCD',
      'WJets'   :'W + jets',
      'WJets_light'   :'W + udscg',
      'WJets_c'   :'W + udscg', # 'W + c#bar{c}'
      'WJets_1b'  :'W + b',
      'WJets_2b'  :'W + b#bar{b}',
      'WJet100'   :'W + jets',
      'WJet100_light':'W + udscg',
      'WJet100_c' :'W + udscg',
      'WJet100_1b'  :'W + b',
      'WJet100_2b'  :'W + b#bar{b}',
      'WJet200'   :'W + jets',
      'WJet200_light':'W + udscg',
      'WJet200_c' :'W + udscg',
      'WJet200_1b'  :'W + b',
      'WJet200_2b'  :'W + b#bar{b}',
      'WJet400'   :'W + jets',
      'WJet400_light':'W + udscg',
      'WJet400_c' :'W + udscg',
      'WJet400_1b'  :'W + b',
      'WJet400_2b'  :'W + b#bar{b}',
      'WJet600'   :'W + jets',
      'WJet600_light':'W + udscg',
      'WJet600_c' :'W + udscg',
      'WJet600_1b'  :'W + b',
      'WJet600_2b'  :'W + b#bar{b}',
      'WJet800'   :'W + jets',
      'WJet800_light':'W + udscg',
      'WJet800_c' :'W + udscg',
      'WJet800_1b'  :'W + b',
      'WJet800_2b'  :'W + b#bar{b}',
      'WJet1200'  :'W + jets',
      'WJet1200_light':'W + udscg',
      'WJet1200_c'  :'W + udscg',
      'WJet1200_1b' :'W + b',
      'WJet1200_2b' :'W + b#bar{b}',
      'WJet2500'  :'W + jets',
      'WJet2500_light':'W + udscg',
      'WJet2500_c'  :'W + udscg',
      'WJet2500_1b' :'W + b',
      'WJet2500_2b' :'W + b#bar{b}',
      'TBarToLeptonst':'Single top',
      'TToLeptonst' :'Single top',
      'TToLeptonss' :'Single top',
      'TtW'   :'Single top',
      'TbartW'    :'Single top',
      'ZJets'   :'Z + jets',
      'ZJets_light'   :'Z + udscg',
      'ZJets_c'   :'Z + udscg',
      'ZJets_1b'  :'Z + b',
      'ZJets_2b'  :'Z + b#bar{b}',
      'ZJet100'   :'Z + jets',
      'ZJet100_light':'Z + udscg',
      'ZJet100_c' :'Z + udscg',
      'ZJet100_1b'  :'Z + b',
      'ZJet100_2b'  :'Z + b#bar{b}',
      'ZJet200'   :'Z + jets',
      'ZJet200_light':'Z + udscg',
      'ZJet200_c' :'Z + udscg',
      'ZJet200_1b'  :'Z + b',
      'ZJet200_2b'  :'Z + b#bar{b}',
      'ZJet400'   :'Z + jets',
      'ZJet400_light':'Z + udscg',
      'ZJet400_c' :'Z + udscg',
      'ZJet400_1b'  :'Z + b',
      'ZJet400_2b'  :'Z + b#bar{b}',
      'ZJet600'   :'Z + jets',
      'ZJet600_light':'Z + udscg',
      'ZJet600_c' :'Z + udscg',
      'ZJet600_1b'  :'Z + b',
      'ZJet600_2b'  :'Z + b#bar{b}',
      'sample_x100'   :'x100'
    },

    'colors': {
      'SE'      :1,
      'SM'      :1,
      'SE_el'     :1,
      'SM_mu'     :1,
      'WZ'      :920,
      'WZ_light'  :920,
      'WZ_c'    :920,
      'WZ_1b'   :921,
      'WZ_2b'   :921,
      'WW'      :920,
      'WW_light'  :920,
      'WW_c'    :920,
      'WW_1b'   :921,
      'WW_2b'   :921,
      'ZZ'      :920,
      'ZZ_light'  :920,
      'ZZ_c'    :920,
      'ZZ_1b'   :921,
      'ZZ_2b'   :921,
      'WH'      :634,
      'WminusHPOWPYT':634,  # 96
      'WplusHPOWPYT'  :634,   # 94    
      'TT'      :596,   # 600
      'QCD100'    :613,
      'QCD200'    :613,
      'QCD300'    :613,
      'QCD400'    :613,
      'QCD500'    :613,
      'QCD700'    :613,
      'QCD1000'   :613,
      'QCD1500'   :613,
      'QCD2000'   :613,
      'WJets'   :814,
      'WJets_light'   :814,
      'WJets_c'   :815,
      'WJets_1b'  :815,
      'WJets_2b'  :820,
      'WJet100'   :814,
      'WJet100_light':814,
      'WJet100_c' :815,
      'WJet100_1b'  :815,
      'WJet100_2b'  :820,
      'WJet200'   :814,
      'WJet200_light':814,
      'WJet200_c' :815,
      'WJet200_1b'  :815,
      'WJet200_2b'  :820,
      'WJet400'   :814,
      'WJet400_light':814,
      'WJet400_c' :815,
      'WJet400_1b'  :815,
      'WJet400_2b'  :820,
      'WJet600'   :814,
      'WJet600_light':814,
      'WJet600_c' :815,
      'WJet600_1b'  :815,
      'WJet600_2b'  :820,
      'WJet800'   :814,
      'WJet800_light':814,
      'WJet800_c' :815,
      'WJet800_1b'  :815,
      'WJet800_2b'  :820,
      'WJet1200'  :814,
      'WJet1200_light':814,
      'WJet1200_c'  :815,
      'WJet1200_1b' :815,
      'WJet1200_2b' :820,
      'WJet2500'  :814,
      'WJet2500_light':814,
      'WJet2500_c'  :815,
      'WJet2500_1b' :815,
      'WJet2500_2b' :820,
      'TBarToLeptonst':840,
      'TToLeptonst' :840,
      'TToLeptonss' :840,
      'TtW'   :840,
      'TbartW'    :840,
      'ZJets'   :402,
      'ZJets_light'   :402,
      'ZJets_c'   :397,
      'ZJets_1b'  :397,
      'ZJets_2b'  :400,
      'ZJet100'   :402,
      'ZJet100_light':402,
      'ZJet100_c' :397,
      'ZJet100_1b'  :397,
      'ZJet100_2b'  :400,
      'ZJet200'   :402,
      'ZJet200_light':402,
      'ZJet200_c' :397,
      'ZJet200_1b'  :397,
      'ZJet200_2b'  :400,
      'ZJet400'   :402,
      'ZJet400_light':402,
      'ZJet400_c' :397,
      'ZJet400_1b'  :397,
      'ZJet400_2b'  :400,
      'ZJet600'   :402,
      'ZJet600_light':402,
      'ZJet600_c' :397,
      'ZJet600_1b'  :397,
      'ZJet600_2b'  :400,
      'sample_x100'   :634
    },

    'plot_order': [
      'SE',
      'SM',
      'SE_el',
      'SM_mu',
      'TT',
      'TBarToLeptonst',
      'TToLeptonst',
      'TToLeptonss',
      'TtW',
      'TbartW',
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
      'WH',
      'WminusHPOWPYT',
      'WplusHPOWPYT',
      'QCD100',
      'QCD200',
      'QCD300',
      'QCD400',
      'QCD500',
      'QCD700',
      'QCD1000',
      'QCD1500',
      'QCD2000',
      'WJets',
      'WJet100',
      'WJet200',
      'WJet400',
      'WJet600',
      'WJet800',
      'WJet1200',
      'WJet2500',
      'WJets_light',
      'WJet100_light',
      'WJet200_light',
      'WJet400_light',
      'WJet600_light',
      'WJet800_light',
      'WJet1200_light',
      'WJet2500_light',
      'WJets_c',
      'WJet100_c',
      'WJet200_c',
      'WJet400_c',
      'WJet600_c',
      'WJet800_c',
      'WJet1200_c',
      'WJet2500_c',
      'WJets_1b',
      'WJet100_1b',
      'WJet200_1b',
      'WJet400_1b',
      'WJet600_1b',
      'WJet800_1b',
      'WJet1200_1b',
      'WJet2500_1b',
      'WJets_2b',
      'WJet100_2b',
      'WJet200_2b',
      'WJet400_2b',
      'WJet600_2b',
      'WJet800_2b',
      'WJet1200_2b',
      'WJet2500_2b',
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
      'sample_x100'
    ] 
  } 
}