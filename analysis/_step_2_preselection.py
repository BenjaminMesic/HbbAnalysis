from utility import utility, preselection


if __name__ == '__main__':

	utility.print_nice('python_info',  '\nStep 2: preselection.')

	# Get analysis name, default is 'Wlv'
	analysis_name = utility.analysis_name()

	# Load all configuration files
	configuration = utility.ConfigurationFiles(analysis_name)

	# Create instance of preselection class
	p = preselection.Preselection(analysis_name, configuration, force_all=False)

	# Preselection
	p.preselection()

	# # Merge files
	# p.merge()