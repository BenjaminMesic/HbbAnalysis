{
	# ----------------------------------------
	# List of samples used for particular task 
	# ----------------------------------------

	'task' : {
		'test_cut'				: ['all'],
		'preselection'			: ['all'],
		'control_region_test'	: ['SE', 'SM', 'WH', 'TT', 'WJets_light'],
		'signal_region' 		: ['SE', 'SM', 'WH', 'TT', 'WJet100', 'QCD100', 'QCD200', 'QCD300', 'QCD500', 'QCD700', 'QCD1000', 'QCD1500', 'QCD2000'],
		'datacards' 			: ['SE', 'SM', 'WH', 'ZH', 'WJets', 'TT']
	},


	# ---------------------------------------
	# Complete list of samples and their 
	# ---------------------------------------
	# Conventions
	# ID must be without '_', because '_' is used as separator for subsamples


	'list':{

		'SingleElectron':{
			'ID'	: 'SE',
			'sub'	: ['SE_el'],
			'types' : 'data',
			'xsec'	: 1.0
		},
		'SingleMuon':{
			'ID'	: 'SM',
			'sub'	: ['SM_mu'],
			'types' : 'data',
			'xsec'	: 1.0
		},
		'WH_HToBB_WToLNu_M125_13TeV_amcatnloFXFX_madspin_pythia8':{
			'ID'	: 'WH',
			'types' : 'mc',
			'xsec'	: 0.25942
		},
		'WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8':{
			'ID'	: 'WminusHPOWPYT',
			'types' : 'mc',
			'xsec'	: 0.25942
		},
		'WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8':{
			'ID'	: 'WplusHPOWPYT',
			'types' : 'mc',
			'xsec'	: 0.25942
		},
		'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8':{
			'ID'	: 'ZH',
			'types' : 'mc',
			'xsec'	: 0.0535
		},
		'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJets',
			'sub'	: ['WJets_light', 'WJets_c', 'WJets_1b', 'WJets_2b'],
			'types' : 'mc',
			'xsec'	: 61526.7
		},
		'WBJetsToLNu_Wpt-40toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WBJets',
			'sub'	: ['WBJets_light', 'WBJets_c', 'WBJets_1b', 'WBJets_2b'],
			'types' : 'mc',
			'xsec'	: 34.2
		},
		'WJetsToLNu_BGenFilter_Wpt-40toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJetsBGen',
			'sub'	: ['WJetsBGen_light', 'WJetsBGen_c', 'WJetsBGen_1b', 'WJetsBGen_2b'],
			'types' : 'mc',
			'xsec'	: 201.8
		},
		'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJet100',
			'sub'	: ['WJet100_light', 'WJet100_c', 'WJet100_1b', 'WJet100_2b'],
			'types' : 'mc',
			'xsec'	: 1345
		},
		'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJet200',
			'sub'	: ['WJet200_light', 'WJet200_c', 'WJet200_1b', 'WJet200_2b'],
			'types' : 'mc',
			'xsec'	: 359.7
		},
		'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJet400',
			'sub'	: ['WJet400_light', 'WJet400_c', 'WJet400_1b', 'WJet400_2b'],
			'types' : 'mc',
			'xsec'	: 48.91
		},
		'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJet600',
			'sub'	: ['WJet600_light', 'WJet600_c', 'WJet600_1b', 'WJet600_2b'],
			'types' : 'mc',
			'xsec'	: 12.05
		},
		'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJet800',
			'sub'	: ['WJet800_light', 'WJet800_c', 'WJet800_1b', 'WJet800_2b'],
			'types' : 'mc',
			'xsec'	: 5.501
		},
		'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJet1200',
			'sub'	: ['WJet1200_light', 'WJet1200_c', 'WJet1200_1b', 'WJet1200_2b'],
			'types' : 'mc',
			'xsec'	: 1.329
		},
		'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'WJet2500',
			'sub'	: ['WJet2500_light', 'WJet2500_c', 'WJet2500_1b', 'WJet2500_2b'],
			'types' : 'mc',
			'xsec'	: 0.03216
		},
		'ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1':{
			'ID'	: 'TBarToLeptonst',
			'types' : 'mc',
			'xsec'	: 26.38		
		},
		'ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1':{
			'ID'	: 'TToLeptonst',
			'types' : 'mc',
			'xsec'	: 44.33		
		},
		'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1':{
			'ID'	: 'TToLeptonss',
			'types' : 'mc',
			'xsec'	: 3.36		
		},
		'TT_TuneCUETP8M1_13TeV-powheg-pythia8':{
			'ID'	: 'TT',
			'types' : 'mc',
			'xsec'	: 831.76		
		},
		'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1':{
			'ID'	: 'TtW',
			'types' : 'mc',
			'xsec'	: 35.6		
		},
		'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1':{
			'ID'	: 'TbartW',
			'types' : 'mc',
			'xsec'	: 35.6		
		},
		'WZ_TuneCUETP8M1_13TeV-pythia8':{
			'ID'	: 'WZ',
			'types' : 'mc',
			'xsec'	: 47.13		
		},
		'QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD100',
			'types' : 'mc',
			'xsec'	: 2.785e7
		},
		'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD200',
			'types' : 'mc',
			'xsec'	: 1.717e6
		},
		'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD300',
			'types' : 'mc',
			'xsec'	: 3.513e5
		},
		'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD500',
			'types' : 'mc',
			'xsec'	: 3.163e4
		},
		'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD700',
			'types' : 'mc',
			'xsec'	: 6.802e3
		},
		'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD1000',
			'types' : 'mc',
			'xsec'	: 1.206e3
		},
		'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD1500',
			'types' : 'mc',
			'xsec'	: 120.4
		},
		'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'QCD2000',
			'types' : 'mc',
			'xsec'	: 25.24
		},
		'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'DYmad',
			'types' : 'mc',
			'xsec'	: 6025.2
		},
		'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'DY100',
			'types' : 'mc',
			'xsec'	: 147.40
		},
		'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'DY200',
			'types' : 'mc',
			'xsec'	: 40.99
		},
		'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'DY400',
			'types' : 'mc',
			'xsec'	: 5.678
		},
		'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':{
			'ID'	: 'DY600',
			'types' : 'mc',
			'xsec'	: 2.198
		}
	}
}