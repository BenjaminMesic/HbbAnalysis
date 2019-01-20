from utility import MiscTool, WeightTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 5: setup weights.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.get_analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  weight = WeightTool.WeightTool(configuration)

  # -------------- Setup C++ functions -------------------------
  # weight.pile_up_handler() # Not used for some time now. There is a variable in ntuple

  # weight.scale_factor_muon_ID_handler()
  # weight.scale_factor_muon_iso_handler()
  # weight.scale_factor_muon_trk_handler()
  # weight.scale_factor_muon_trigger_handler()

  # weight.scale_factor_electron_ID_handler()
  # weight.scale_factor_electron_trk_handler()
  # weight.scale_factor_electron_trigger_handler()

  # weight.scale_factor_bbtag_handler()
  # weight.scale_factor_bbmistag_handler()

  # weight.scale_factor_tau21_handler()
  # weight.scale_factor_tau21_pt_handler()

  # # # ----------- Get dictionary with total weighted number of events -------------
  # # weight.get_total_number_of_events()

  # # --------------------------- Tests -------------------
  # # print WeightTool.WeightTool.weight_handler(configuration.weights.weights)
  # weight._load_C_code()
