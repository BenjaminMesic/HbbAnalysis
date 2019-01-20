from utility import MiscTool, PlotTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 7: Postfit plot.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.get_analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # ----------- Here starts task ----------------
  p = PlotTool.PlotPostfitTool(configuration)

  p.plot()