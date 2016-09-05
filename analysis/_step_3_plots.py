from utility import MiscTool, ConfigurationTool, PlotTool

if __name__ == '__main__':

	MiscTool.print_nice('python_info',  '\nStep 2: preselection.')

	# Get analysis name, default is 'Wlv'
	analysis_name = MiscTool.analysis_name()

	# Load all configuration files
	configuration = ConfigurationTool.ConfigurationLoader(analysis_name)

	# Plot name (plots.ini)
	plot_name = 'signal_region'
	# split samples to subsamples
	sub_samples = True
	# plot event by event or directly from tree
	event_by_event = True

	p = PlotTool.PlotTool(analysis_name, plot_name, configuration, sub_samples, event_by_event)
	p.get_variables()

	p.get_trees()
	p.get_samples_number_of_entries()
	p.get_samples_scale_factors()
	p.set_and_save_histograms()
	p.get_histograms()

	p.plot()

