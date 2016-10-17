from utility import MiscTool, SampleTool, ControlRegionTool

if __name__ == '__main__':

	MiscTool.Print('python_info',  '\nStep 4: control regions.')

	# Get analysis name, default is 'Wlv'
	analysis_name = MiscTool.analysis_name()

	# Load all configuration files
	configuration = MiscTool.get_configuration_files(analysis_name)

	# Task tells which config options to choose
	task = 'control_region_test'

	# ----------- Initialize samples ----------------
	# Decide if you want to split samples on subsamples
	split_samples = True
	# Get samples using SampleTool
	sample_tool = SampleTool.SampleTool( task, configuration, split_samples)

	# ----------- Here starts task ----------------
	c = ControlRegionTool.ControlRegionTool( task, analysis_name, configuration, sample_tool)
