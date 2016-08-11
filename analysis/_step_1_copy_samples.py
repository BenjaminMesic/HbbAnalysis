from utility import utility, copy


if __name__ == '__main__':

	utility.print_nice('python_info',  '\nStep 1: copying samples.')

	# Get analysis name, default is 'Wlv'
	analysis_name = utility.analysis_name()

	# Load all configuration files
	configuration = utility.ConfigurationFiles(analysis_name)

	# Force preselection on all samples even if they exists
	force_all = False

	# Create instance of CopySamples 
	copy_samples = copy.CopySamples(analysis_name, configuration, force_all)

	# Save list of logical file names
	copy_samples.get_list_of_logical_file_names()

	# Copy files
	copy_samples.copy_files()