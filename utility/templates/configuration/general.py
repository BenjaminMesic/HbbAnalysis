
# Name of the task which is running
task_name                       = 'test' #'Wen_110_140' #'Wmn_110_140' #'Wen_full' #'Wmn_full' # 

# Just analysis luminosity
luminosity                      = 36400 #12900, # pb-1
# Force all jobs even if the files already exist
force_all                       = False
# Send job either batch or interactively
send_jobs                       = True
# Work on batch
batch                           = True
# Use user created files
user_defined_files              = True
# Merge files after Ls
work_with_Ls_only               = False
# Do final/task selection on merged files if they exist
task_selection_on_merged_files  = True

tag = '13TeV'

# -------- Options for copying files ---------
copy_protocol = {
  'pisa1'     : 'root:/',
  'pisa2'     : 'root:/',
  'pisa3'     : 'root:/',
  'cern'      : 'srm:/',
}

storage_element = {
  'pisa1'     : '/stormgf1.pi.infn.it:1094/', # '/stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms',
  'pisa2'     : '/stormgf1.pi.infn.it:1094/', # '/stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms',
  'pisa3'     : '/stormgf1.pi.infn.it:1094/',
  'cern'      : '/srm-eoscms.cern.ch:8443/srm/v2/server?SFN=/eos', # '/188.184.38.46:1094/eos',
  'fnal'      : '/cmseos.fnal.gov:8443/srm/v2/server?SFN=/eos',
  'psi'       : '/t3se01.psi.ch/pnfs/psi.ch/cms/trivcat'
}

locations = {
  'pisa1'     : 'store/user/arizzi/VHBBHeppyV25b',
  'pisa2'     : 'store/user/tboccali/Ntuples_v25',
  'pisa3'     : 'store/user/arizzi/VHBBHeppyV25b_passall',
  'cern'      : 'cms/store/group/phys_higgs/hbb/ntuples/V25',
}

# Keywords which are going to be searched (or not) for.
search_keywords = {
  'all' : [],
  'any' : [],
  'none': ['.tar.gz','failed', 'log']
}