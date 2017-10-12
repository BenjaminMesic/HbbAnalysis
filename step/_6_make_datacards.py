from utility import MiscTool, DataCardTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 6: Make datacards.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.get_analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # ----------- Here starts task ----------------
  d = DataCardTool.DataCardTool( configuration)
  d.get_yields_and_templates()
  d.make()