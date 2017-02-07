from utility import MiscTool, CopyTool

if __name__ == '__main__':
  
  MiscTool.Print('python_info',  '\nStep 1: copying samples.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # Force copying on all samples even if they exists, not tested yet
  force_all = False

  # Create instance of CopySamples 
  copy_samples = CopyTool.CopyTool(analysis_name, configuration, force_all)

  # Get the list of all the samples from sources
  copy_samples.get_list_of_samples_from_sources()

  # print copy_samples.wrapper_gfal_ls_r('/stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms/store/user/arizzi/VHBBHeppyV24/ggZH_HToBB_ZToNuNu_M125_13TeV_amcatnlo_pythia8/VHBB_HEPPY_V24_ggZH_HToBB_ZToNuNu_M125_13TeV_amcatnlo_Py8__spr16MAv2-puspr16_HLT_80r2as_v14-v1')

  # # ----------------------------------------
  # # Get LFNs
  # # ----------------------------------------
  # # It executes ls command for each directory from pisa/psi..
  # copy_samples.save_logical_file_names_all_samples_from_config_source()

  # # ----------------------------------------
  # # Copy part
  # # ----------------------------------------

  # # All samples from config file
  # copy_samples.save_logical_file_names_all_samples_from_config_destination()
  # copy_samples.copy_files_all_samples_from_config()
  # copy_samples.save_logical_file_names_all_samples_from_config_destination()

  # # All samples from config file using batch
  # copy_samples.copy_files_all_samples_from_config_batch()
  # copy_samples.save_logical_file_names_all_samples_from_config_destination()

  # # Single sample
  # _sample = 'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
  # # Copy part
  # copy_samples.save_logical_file_names_from_config_destination(_sample)
  # copy_samples.copy_files_single_sample(_sample)
  # copy_samples.save_logical_file_names_from_config_destination(_sample)


  # ----------------------------------------
  # Check files part
  # ----------------------------------------

  # # Check if all root files have ok structure
  # copy_samples.check_root_files(_sample)
  # copy_samples.check_root_files_all_samples_from_config()

  # # Check if some of files are not existing in Pisa/...
  # copy_samples.check_root_files_non_existing('SingleMuon.txt')
  # copy_samples.check_root_files_non_existing_all_samples_from_config()

  # # Remove files which have error
  # copy_samples.remove_files_single_sample(_sample)

  # # Events file matching
  # copy_samples.events_files_matching('SingleMuon_local.txt')
  # copy_samples.event_list_file_matching('SingleElectron_local.txt')