from utility import utility, preselection


if __name__ == '__main__':

	print '\n','-'*50, '\nStep 2: preselection.\n', '-'*50

	# Get analysis name, default is 'Wlv'
	analysis_name = utility.analysis_name()

	# Load all configuration files
	configuration = utility.ConfigurationFiles(analysis_name)

	# Create instance of preselection class
	p = preselection.Preselection(analysis_name, configuration, force_all=False)

	# Preselection
	p.preselection()

	# Merge files
	p.merge()