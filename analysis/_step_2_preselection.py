from utility import MiscTool, ConfigurationTool, PreselectionTool

if __name__ == '__main__':

	MiscTool.print_nice('python_info',  '\nStep 2: preselection.')

	# Get analysis name, default is 'Wlv'
	analysis_name = MiscTool.analysis_name()

	# Load all configuration files
	configuration = ConfigurationTool.ConfigurationLoader(analysis_name)

	force_all = False

	# Create instance of preselection class
	p = PreselectionTool.PreselectionTool(analysis_name, configuration, force_all)

	# # Preselection
	# p.preselection()

	# p.check_root_files('SingleMuon_local.txt')

	# Merge files
	p.merge()