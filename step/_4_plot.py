from utility import MiscTool, SampleTool, PlotTool 

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 4: plots.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.get_analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # Get samples using SampleTool
  sample_tool = SampleTool.SampleTool(configuration)

  # Initalize plots
  p = PlotTool.PlotTool( configuration, sample_tool)
  
  p.plot()
