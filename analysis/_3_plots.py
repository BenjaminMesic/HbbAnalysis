from utility import MiscTool, PlotTool, SampleTool

if __name__ == '__main__':

	MiscTool.Print('python_info',  '\nStep 3: plots.')

	# Get analysis name, default is 'Wlv'
	analysis_name = MiscTool.analysis_name()

	# Load all configuration files
	configuration = MiscTool.get_configuration_files(analysis_name)

	# Task tells which config options to choose
	task = 'signal_region'
	event_by_event = False

	# ----------- Initialize samples ----------------
	# Decide if you want to split samples on subsamples
	split_samples = True
	# Get samples using SampleTool
	sample_tool = SampleTool.SampleTool( task, configuration, split_samples)


	p = PlotTool.PlotTool(task, analysis_name, configuration, sample_tool, event_by_event)

	# Just creating histograms
	p.set_variables()
	p.set_and_save_histograms()
	p.get_and_prepare_histograms()

	# Create canvas, make stack histograms and do plot
	p.plot()

