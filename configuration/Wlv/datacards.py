{

	# Channels for which we are making datacards
	'channels'	: ['Wmn', 'Wen'],

	# Signal/Control regions definition(cuts) defined in cuts.py 
	'bins'		: ['sr','cr1', 'cr2', 'cr3'],

	# Samples(IDs) used, defined in samples.py (task, datacards)
	'process' :[
		['ZH'	, '-1'],
		['WH'	, '0'],
		['s_Top', '1'],
		['TT'	, '2'],
		['Wj0b'	, '3'],
		['Wj1b'	, '4'],
		['Wj2b'	, '5'],
		['VVHF'	, '6'],
		['VVLF'	, '7'],
		['Zj0b'	, '8'],
		['Zj1b'	, '9'],
		['Zj2b'	, '10']
	],

	'nuisance_parameters': {
		'lumi_13TeV': {
			'model': 'lnN',
			'process':{
				'ZH'	: 1.062,
				'WH'	: 1.062,
				's_Top'	: 1.062,
				'TT'	: 1.062,
				'Wj0b'	: 1.062,
				'Wj1b'	: 1.062,
				'Wj2b'	: 1.062,
				'VVHF'	: 1.062,
				'VVLF'	: 1.062,
				'Zj0b'	: 1.062,
				'Zj1b'	: 1.062,
				'Zj2b'	: 1.062
			}
		},
		'CMS_vhbb_puWeight': {
			'model': 'shape',
			'process':{
				'ZH'	: 1.0,
				'WH'	: 1.0,
				's_Top'	: 1.0,
				'TT'	: 1.0,
				'Wj0b'	: 1.0,
				'Wj1b'	: 1.0,
				'Wj2b'	: 1.0,
				'VVHF'	: 1.0,
				'VVLF'	: 1.0,
				'Zj0b'	: 1.0,
				'Zj1b'	: 1.0,
				'Zj2b'	: 1.0
			}
		}, 
	},

	# Here comes part with subsample datacard definitions, etc...
	'definitions'			: {
		'SE_el'	: 'Wen',
		'SE'	: 'Wen',
		'SM_mu'	: 'Wmn',
		'SM'	: 'Wmn',	
		'WH'	: 'WH',
		'ZH'	: 'ZH', 
		'WJets_light': 'Wj0b',
		'WJets_c': 'Wj0b',
		'WJets_1b':  'Wj1b',
		'WJets_2b': 'Wj2b',		
		'TT'	: 'TT'
	}

}