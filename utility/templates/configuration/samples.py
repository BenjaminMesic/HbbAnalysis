
# ----------------------------------------
# List of samples used for particular task 
# ----------------------------------------

task = {
  'test'        : ['all'], #['WplusHPOWPYT', 'WminusHPOWPYT'], # ['TT'], #
  'Wen_full'    : ['all'],
  'Wmn_full'    : ['all'],
  'Wen_110_140' : ['all'],
  'Wmn_110_140' : ['all'],
}

# ---------------------------------------
# Complete list of samples and their 
# ---------------------------------------
# Conventions
# ID must be without '_', because '_' is used as separator for subsamples

samples_list = {
  # # ------------------------- Data --------------------------------
  # 'SingleElectron':{ # ***
  #   'ID'  : 'SE',
  #   'sub' : ['SE_el'],
  #   'types' : 'data',
  #   'xsec'  : 1.0,
  #   'origin': ['all']
  # },
  # 'SingleMuon':{ # ***
  #   'ID'  : 'SM',
  #   'sub' : ['SM_mu'],
  #   'types' : 'data',
  #   'xsec'  : 1.0,
  #   'origin': ['all']
  # },
  # ------------------------- Signal -------------------------------
  # 'WH_HToBB_WToLNu_M125_13TeV_amcatnloFXFX_madspin_pythia8':{
  #   'ID'  : 'WH',
  #   'types' : 'mc',
  #   'xsec'  : 0.25942,
  #   'origin': ['all']
  # },
  'WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8':{ # ***
    'ID'  : 'WminusHPOWPYT',
    'types' : 'mc',
    'xsec'  : 0.533 * 0.108535 * 0.5824*3.,
    'origin': ['all']
  },
  'WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8':{ # ***
    'ID'  : 'WplusHPOWPYT',
    'types' : 'mc',
    'xsec'  : 0.840 * 0.108535 * 0.5824*3,
    'origin': ['all']
  },
  # # ------------------------- Others -----------------------------
  # 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8':{
  #   'ID'  : 'ZH',
  #   'types' : 'mc',
  #   'xsec'  : 0.0535
  # },
  'WZ_TuneCUETP8M1_13TeV-pythia8':{
    'ID'    : 'WZ',
    'types' : 'mc',
    'xsec'  : 47.13, 
    'origin': ['all']     
  },
  # 'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8':{
  #   'ID'    : 'WZ',
  #   'types' : 'mc',
  #   'xsec'  : 10.71  
  # },
  # 'WW_TuneCUETP8M1_13TeV-pythia8':{
  #   'ID'    : 'WW',
  #   'types' : 'mc',
  #   'xsec'  : 113.898
  # },
  # 'WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8':{
  #   'ID'    : 'WWTo1L1Nu2Q',
  #   'types' : 'mc',
  #   'xsec'  : 49.997  
  # },
  # 'ZZ_TuneCUETP8M1_13TeV-pythia8':{
  #   'ID'    : 'ZZ',
  #   'types' : 'mc',
  #   'xsec'  : 16.523
  # },
  # 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8':{
  #   'ID'    : 'ZZTo2L2Q',
  #   'types' : 'mc',
  #   'xsec'  : 3.22 
  # },
  # ------------------------- WJets ------------------------------- # ***
  # 'WBJetsToLNu_Wpt-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': {
  #   'ID'  : 'WBJets100',
  #   'sub' : ['WBJets100_lightB', 'WBJets100_cB', 'WBJets100_1bB', 'WBJets100_2bB'],
  #   'types' : 'mc',
  #   'xsec'  : 6.004,
  #   'origin': ['all']
  # },
  # 'WBJetsToLNu_Wpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': {
  #   'ID'  : 'WBJets200',
  #   'sub' : ['WBJets200_lightB', 'WBJets200_cB', 'WBJets200_1bB', 'WBJets200_2bB'],
  #   'types' : 'mc',
  #   'xsec'  : 0.8524,
  #   'origin': ['all']
  # },
  # 'WJetsToLNu_BGenFilter_Wpt-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': {
  #   'ID'  : 'WBJetsFilter100',
  #   'sub' : ['WBJetsFilter100_lightB', 'WBJetsFilter100_cB', 'WBJetsFilter100_1bB', 'WBJetsFilter100_2bB'],
  #   'types' : 'mc',
  #   'xsec'  : 26.1,
  #   'origin': ['all']
  # },
  # 'WJetsToLNu_BGenFilter_Wpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': {
  #   'ID'  : 'WBJetsFilter200',
  #   'sub' : ['WBJetsFilter200_lightB', 'WBJetsFilter200_cB', 'WBJetsFilter200_1bB', 'WBJetsFilter200_2bB'],
  #   'types' : 'mc',
  #   'xsec'  : 3.545,
  #   'origin': ['all']
  # },
  # 'WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8': {
  #   'ID'  : 'WJet100',
  #   'sub' : ['WJet100_light', 'WJet100_c', 'WJet100_1b', 'WJet100_2b'],
  #   'types' : 'mc',
  #   'xsec'  : 628.3,
  #   'origin': ['all']
  # },
  # 'WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8': {
  #   'ID'  : 'WJet250',
  #   'sub' : ['WJet250_light', 'WJet250_c', 'WJet250_1b', 'WJet250_2b'],
  #   'types' : 'mc',
  #   'xsec'  : 22.37,
  #   'origin': ['all']
  # },
  # 'WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8': {
  #   'ID'    : 'WJet400',
  #   'sub'   : ['WJet400_light', 'WJet400_c', 'WJet400_1b', 'WJet400_2b'],
  #   'types' : 'mc',
  #   'xsec'  : 2.67,
  #   'origin': ['all']
  # },
  # 'WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8': {
  #   'ID'    : 'WJet600',
  #   'sub'   : ['WJet600_light', 'WJet600_c', 'WJet600_1b', 'WJet600_2b'],
  #   'types' : 'mc',
  #   'xsec'  : 0.408,
  #   'origin': ['all']
  # },
  # 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'WJets',
  #   'sub'   : ['WJets_lightIncl', 'WJets_cIncl', 'WJets_1bIncl', 'WJets_2bIncl'],
  #   'types' : 'mc',
  #   'xsec'  : 61526.7
  # },
  # # Not using this sample because V_pt cut is much higher than this pt bin i.e. < 100
  # 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':{  
  #   'ID'    : 'WJetsNLO',
  #   'sub'   : ['WJetsNLO_lightIncl', 'WJetsNLO_cIncl', 'WJetsNLO_1bIncl', 'WJetsNLO_2bIncl'],
  #   'types' : 'mc',
  #   'xsec'  : 61526.7,
  #   'origin': ['all']
  # },
  # # ---------------------------- TT -------------------------------
  # 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': {
  #   'ID'    : 'TTDiLep',
  #   'types' : 'mc',
  #   'xsec'  : 88.3      
  # },
  # 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': {
  #   'ID'    : 'TTSingleLepFromT',
  #   'types' : 'mc',
  #   'xsec'  : 182.7    
  # },
  # 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': {
  #   'ID'    : 'TTSingleLepFromTbar',
  #   'types' : 'mc',
  #   'xsec'  : 182.7 
  # },
  'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8':{ #TT_TuneCUETP8M1_13TeV-powheg-pythia8 # ***
    'ID'    : 'TT',
    # 'sub'   : ['TT_TTincl'],
    'types' : 'mc',
    'xsec'  : 831.76,
    'origin': ['all']   
  },
  # 'TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8':{ 
  #   'ID'    : 'TTMtt1000',
  #   'types' : 'mc',
  #   'xsec'  : 1.894e+01, # cmsRun ana.py inputFiles="file:/eos/cms/store/mc/RunIISummer16MiniAODv2/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/110000/02AF2136-C2E2-E611-ABAD-02163E00BC94.root" maxEvents=-1
  #   'origin': ['all']   
  # },
  # 'TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8':{ 
  #   'ID'    : 'TTMtt700',
  #   'types' : 'mc',
  #   'xsec'  : 7.065e+01, # cmsRun ana.py inputFiles="file:/eos/cms/store/mc/RunIISummer16MiniAODv2/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0002A8DB-5EE2-E611-9EDB-0CC47AD98D0E.root" maxEvents=-1
  #   'origin': ['all']   
  # },
  # ----------------------- Single top -------------------------------
  # 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1':{
  #   'ID'    : 'TtW',
  #   'types' : 'mc',
  #   'xsec'  : 35.6,
  #   'origin': ['all']
  # },
  # 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1':{
  #   'ID'    : 'TbartW',
  #   'types' : 'mc',
  #   'xsec'  : 35.6,
  #   'origin': ['all']
  # },
  # 'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1':{
  #   'ID'    : 'TbarToLeptonst',
  #   'types' : 'mc',
  #   'xsec'  : 80.95,
  #   'origin': ['all']
  # },
  # 'ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1':{
  #   'ID'    : 'TToLeptonst',
  #   'types' : 'mc',
  #   'xsec'  : 136.02,
  #   'origin': ['all']
  # },
  # 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1':{
  #   'ID'    : 'TToLeptonss',
  #   'types' : 'mc',
  #   'xsec'  : 3.36    
  # },
  # 'ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1':{
  #   'ID'    : 'TToLeptonst',
  #   'types' : 'mc',
  #   'xsec'  : 70.69    
  # },
  # # ----------------------------- QCD ---------------------------------
  # 'QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'QCD100',
  #   'types' : 'mc',
  #   'xsec'  : 2.785e7,
  #   'origin': ['all']
  # },
  # 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'QCD200',
  #   'types' : 'mc',
  #   'xsec'  : 1.717e6,
  #   'origin': ['all']
  # },
  # 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'QCD300',
  #   'types' : 'mc',
  #   'xsec'  : 3.513e5,
  #   'origin': ['all']
  # },
  # 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'QCD500',
  #   'types' : 'mc',
  #   'xsec'  : 3.163e4,
  #   'origin': ['all']
  # },
  # 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'QCD700',
  #   'types' : 'mc',
  #   'xsec'  : 6.802e3,
  #   'origin': ['all']
  # },
  # 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'QCD1000',
  #   'types' : 'mc',
  #   'xsec'  : 1.206e3,
  #   'origin': ['all']
  # },
  # 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'QCD1500',
  #   'types' : 'mc',
  #   'xsec'  : 120.4,
  #   'origin': ['all']
  # },
  # 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'QCD2000',
  #   'types' : 'mc',
  #   'xsec'  : 25.24,
  #   'origin': ['all']
  # },
  # # ----------------------- Drell Yann -------------------------------
  # 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'DYmad',
  #   'types' : 'mc',
  #   'xsec'  : 5765.4 # 6025.2
  # },
  # 'DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'    : 'DY70',
  #   'types' : 'mc',
  #   'xsec'  : 'XXX'
  # },
  # 'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'DY100',
  #   'types' : 'mc',
  #   'xsec'  : 147.40
  # },
  # 'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'DY200',
  #   'types' : 'mc',
  #   'xsec'  : 40.99
  # },
  # 'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'DY400',
  #   'types' : 'mc',
  #   'xsec'  : 5.678
  # },
  # 'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'DY600',
  #   'types' : 'mc',
  #   'xsec'  : 1.367
  # },
  # 'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'DY800',
  #   'types' : 'mc',
  #   'xsec'  : 0.6304
  # },
  # 'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'DY1200',
  #   'types' : 'mc',
  #   'xsec'  : 0.1514
  # },
  # 'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
  #   'ID'  : 'DY2500',
  #   'types' : 'mc',
  #   'xsec'  : 0.003565
  # },
}