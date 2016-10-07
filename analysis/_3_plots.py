from utility import MiscTool, PlotTool

if __name__ == '__main__':

	MiscTool.Print('python_info',  '\nStep 2: preselection.')

	# Get analysis name, default is 'Wlv'
	analysis_name = MiscTool.analysis_name()

	# Load all configuration files
	configuration = MiscTool.get_configuration_files(analysis_name)

	# Plot name (plots.ini)
	plot_name = 'signal_region'
	# split samples to subsamples
	sub_samples = True
	# plot event by event or directly from tree
	event_by_event = False

	p = PlotTool.PlotTool(analysis_name, plot_name, configuration, sub_samples, event_by_event)

	# Get variables for plot
	p.get_variables()

	# Get trees using trim_trees() from TreeTool
	p.get_trees()

	p.get_samples_number_of_entries()
	p.get_samples_scale_factors()
	p.set_and_save_histograms()
	p.get_histograms()

	p.plot()

