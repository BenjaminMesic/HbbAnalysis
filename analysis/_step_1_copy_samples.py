from utility import utility, copy


if __name__ == '__main__':

	print '\n','-'*50, '\n Step 1: copying samples.\n', '-'*50

	# Get analysis name, default is 'Wlv'
	analysis_name = utility.analysis_name()

	# Load all configuration files
	configuration = utility.ConfigurationFiles(analysis_name)

	# Create instance of CopySamples 
	copy_samples = copy.CopySamples(analysis_name, configuration, force_all=False)

	# # Save list of logical file names
	# copy_samples.get_list_of_logical_file_names()

	# Copy files
	copy_samples.copy_files()