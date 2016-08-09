from utility import utility, plots

if __name__ == '__main__':

	print '\n','-'*50, '\nStep 3: plots.\n', '-'*50

	# Get analysis name, default is 'Wlv'
	analysis_name = utility.analysis_name()

	# Load all configuration files
	configuration = utility.ConfigurationFiles(analysis_name)

	# Plot name (plots.ini)
	plot_name = 'test_plot'
	# split samples to subsamples
	sub_samples = True

	p = plots.Plot(analysis_name, plot_name, configuration, sub_samples)
	p.get_variables()

	p.get_samples_for_plot()
	p.get_trees()
	p.set_and_save_histograms()
	p.get_histograms()

	p.plot()
