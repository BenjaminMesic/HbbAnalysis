from utility import MiscTool, WeightTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 5: Weights Tool.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  weight = WeightTool.WeightTool( analysis_name, configuration)

  # -------------- Setup C++ functions -------------------------
  weight.pile_up_handler()

  # weight.scale_factor_muon_ID_handler()
  # weight.scale_factor_muon_iso_handler()
  # weight.scale_factor_muon_trk_handler()
  # weight.trigger_muon_handler()

  # #weight.scale_factor_electron_handler() Not used
  # weight.scale_factor_electron_ID_handler()
  # weight.scale_factor_electron_trk_handler()
  # weight.trigger_electron_handler()

  # # ----------- Get dictionary with total weighted number of events -------------
  # weight.get_total_number_of_events()

  # --------------------------- Tests -------------------
  # print WeightTool.WeightTool.weight_handler(configuration['weights'])
  # weight._load_C_code()
