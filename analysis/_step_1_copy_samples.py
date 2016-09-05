from utility import MiscTool, ConfigurationTool, CopyTool


if __name__ == '__main__':

	MiscTool.print_nice('python_info',  '\nStep 1: copying samples.')

	# Get analysis name, default is 'Wlv'
	analysis_name = MiscTool.analysis_name()

	# Load all configuration files
	configuration = ConfigurationTool.ConfigurationLoader(analysis_name)

	# Force copying on all samples even if they exists, not tested yet
	force_all = False

	# Create instance of CopySamples 
	copy_samples = CopyTool.CopyTool(analysis_name, configuration, force_all)

	# # This one takes a lot of time because it executes ls command for each directory from pisa/psi..
	# copy_samples.save_logical_file_names_all_samples_from_config_source()

	# # All samples from config file
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