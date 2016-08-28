from utility import utility, copy


if __name__ == '__main__':

	utility.print_nice('python_info',  '\nStep 1: copying samples.')

	# Get analysis name, default is 'Wlv'
	analysis_name = utility.analysis_name()

	# Load all configuration files
	configuration = utility.ConfigurationFiles(analysis_name)

	# Force copying on all samples even if they exists, not working
	force_all = False

	# Create instance of CopySamples 
	copy_samples = copy.CopySamples(analysis_name, configuration, force_all)

	# This one takes a lot of time
	# copy_samples.save_logical_file_names_all_samples_from_config_source()

	# All samples from config file
	# copy_samples.save_logical_file_names_all_samples_from_config_destination()
	# copy_samples.copy_files_all_samples_from_config()
	# copy_samples.save_logical_file_names_all_samples_from_config_destination()

	# Single sample
	_sample = 'QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
	copy_samples.save_logical_file_names_from_config_destination(_sample)
	copy_samples.copy_files_single_sample(_sample)
	copy_samples.check_root_files(_sample)
	copy_samples.save_logical_file_names_from_config_destination(_sample)

	# copy_samples.remove_files_single_sample('SingleElectron')