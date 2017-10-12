import os
import sys

def Print(print_type, *text):
 
  try:

    if print_type == 'python_info': # Bright Yellow
      print '\033[1;33;40m' + ''.join(text) + '\033[0m'

    elif print_type == 'analysis_info': # Bright Cyan
      print '\033[1;36;40m{0:30s}{1}\033[0m'.format(*text)

    elif print_type == 'analysis_info_list': # Bright Cyan
      print '\033[1;36;40m' + text[0] + '\033[0m'
      for _l in text[1]:
        print '\033[1;36;40m{0:30s}{1}\033[0m'.format('' , _l)

    elif print_type == 'error':  # Bright Red
      print '\033[1;31;40m' + ''.join(text) + '\033[0m'

    elif print_type == 'status': # Bright Green
      print '\033[1;32;40m' + ''.join(text) + '\033[0m'   


  except Exception, e:
    print text

def make_directory(directory):

  if not os.path.exists(directory):
    try:
      os.makedirs(directory)
    except OSError:
      if not os.path.isdir(directory):
        raise

  return directory

def get_analysis_name():
  ''' Just function which gets argv and return analysis_name. Need sys library'''
  _analysis_name = ''
  if len(sys.argv) == 1:
    _analysis_name = 'Wlv'
    Print('analysis_info','Missing analysis_name argument, using default: ', _analysis_name)
  else:
    _analysis_name = sys.argv[1]

  return _analysis_name

def get_configuration_files(analysis_name):

  import analysis
  
  exec('from analysis.{0} import configuration'.format(analysis_name))

  return configuration

def ID_sample_dictionary( IDs, samples_configuration):
  'Give list of IDs and return corresponding list of samples'

  _samples = []

  if IDs == ['all']:
    return samples_configuration.samples_list.keys()

  else:

    # Loop over all IDs
    for _id in IDs:
      
      _sample = ''

      # Loop over all samples
      for _s in samples_configuration.samples_list.keys():
        
        # Check if ID match sample
        if _id == samples_configuration.samples_list[_s]['ID']:
          _sample = _s
          break

        # Check if ID match subsample
        elif 'sub' in samples_configuration.samples_list[_s] and _id in samples_configuration.samples_list[_s]['sub']:
          _sample = _s
          break

      if _sample == '':
        Print('error', 'Check your ID {0}'.format(_id))
      else:
        _samples.append(_s)

  # remove duplicates
  return list(set(_samples))
