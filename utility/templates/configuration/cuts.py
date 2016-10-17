{
	# ----------------------------------
	# Main cuts
	# ----------------------------------

	'preselection_cut': '(Vtype==2 || Vtype==3) && V_pt>100 && HCSV_reg_pt>100 && Jet_btagCSV[hJCidx[1]]>0.4',	
	'blinding_cut': '1',

	# ----------------------------------
	# Cuts which define subsamples
	# ----------------------------------

	'subsamples_cut': {
		'light'			: 'ttCls<41',
		'c'				: 'ttCls>=41 && ttCls<=45',
		'1b'			: 'ttCls>=51 && ttCls<=52',
		'2b'			: 'ttCls>=53 && ttCls<=55',
		'el'			: 'run<=276811 && abs(vLeptons_pdgId[0]) == 11 && Vtype==3 && HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v == 1 && json',
		'mu'			: 'run<=276811 && abs(vLeptons_pdgId[0]) == 13 && Vtype==2 && ( HLT_BIT_HLT_IsoMu22_v == 1 || HLT_BIT_HLT_IsoTkMu22_v == 1 ) && json'
	},

	# ----------------------------------
	# Plot cuts 
	# ----------------------------------

	'test_cut': 	'V_pt<150',
	'signal_region': '((vLeptons_pt[0]>30 && abs(vLeptons_pdgId[0]) == 11) || (vLeptons_pt[0]>25 && abs(vLeptons_pdgId[0]) == 13) ) && Jet_pt_reg[hJCidx[0]] > 25 && Jet_pt_reg[hJCidx[1]] > 25 && HCSV_reg_pt>100 && HCSV_reg_mass > 90 && HCSV_reg_mass < 150 && Jet_btagCSV[hJCidx[0]] > 0.935 && Jet_btagCSV[hJCidx[1]] > 0.46 && Sum$(Jet_pt>25 && abs(Jet_eta)<2.9 && Jet_puId > 0 && Jet_id > 0 && Iteration$ != hJCidx[0] && Iteration$ != hJCidx[1]) < 2 && Sum$(aLeptons_pt>15 && abs(aLeptons_eta)<2.5 && aLeptons_relIso03 < 0.1) == 0 && abs(VHbb::deltaPhi(V_phi, HCSV_reg_phi)) > 2.5 && abs(VHbb::deltaPhi(met_phi, vLeptons_phi[0])) < 2.0 && ( (abs(vLeptons_pdgId[0]) == 11 && vLeptons_relIso03[0] < 0.15) || ((abs(vLeptons_pdgId[0]) == 13 && vLeptons_relIso04[0] < 0.06)) ) ',

	# ----------------------------------
	# Control region cuts 
	# ----------------------------------

	'control_region_test':{
		'cr1': 'V_pt>100 && V_pt<120',
		'cr2': 'V_pt>120 && V_pt<140',
		'cr3': 'V_pt>140 && V_pt<160',
	}

}

