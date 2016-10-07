from utility import MiscTool, PreselectionTool

if __name__ == '__main__':

	MiscTool.Print('python_info',  '\nStep 2: preselection.')

	# Get analysis name, default is 'Wlv'
	analysis_name = MiscTool.analysis_name()

	# Load all configuration files
	configuration = MiscTool.get_configuration_files(analysis_name)

	force_all = False

	# Create instance of preselection class
	p = PreselectionTool.PreselectionTool(analysis_name, configuration, force_all)

	# ---------------------------------
	# Choose what you want to do
	# ---------------------------------

	# # Preselection
	# p.preselection()

	# # Check root files
	# for _s in configuration['samples']:
	# 	try:
	# 		p.check_root_preselected_files( _s + '_local.txt')
	# 		print _s

	# 	except Exception, e:
	# 		print 'Problem with {0}.'.format(_s)

	# Check single root file
	# p.check_root_preselected_files('SingleElectron_local.txt')

	# # Merge files
	# p.merge()
