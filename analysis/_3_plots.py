from utility import MiscTool, PlotTool, SampleTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 3: plots.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # Task tells which config options to choose
  task = 'boost_bkg_estimate'

  # Get samples using SampleTool
  sample_tool = SampleTool.SampleTool( analysis_name, task, configuration, configuration['plots'][task]['split_samples'])

  # Initalize plots
  p = PlotTool.PlotTool( task, analysis_name, configuration, sample_tool)
  
  p.plot()

