import sys
import time
import os
import subprocess as sp

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

def analysis_name():
	''' Just function which gets argv and return analysis_name. Need sys library'''
	_analysis_name = ''
	if len(sys.argv) == 1:
		_analysis_name = 'Wlv'
		Print('analysis_info','Missing analysis_name argument, using default: ', _analysis_name)
	else:
		_analysis_name = sys.argv[1]

	return _analysis_name

def get_configuration_files(analysis_name):
	
	_configuration_files_path = os.path.join( os.environ['Hbb_WORKING_DIRECTORY'], 'configuration', analysis_name)

	Print('analysis_info', 'Configuration files from ', analysis_name)	

	_files = sp.check_output(['ls', _configuration_files_path]).split()

	_configuration_files = {}

	for _c in _files:

		if '~' in _c:
			continue

		Print('analysis_info', '', _c)

		try:
			_configuration_files[_c.split('.')[0]] = eval(open(os.path.join( _configuration_files_path, _c)).read())
		except Exception, e:
			Print('error', 'Problem with loading: ' + _c)
			raise

	return _configuration_files

def make_directory(directory):

	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
		except OSError:
			if not os.path.isdir(directory):
				raise

def progress_bar(progress):
	barLength = 100 # Modify this to change the length of the progress bar
	status = ""
	if isinstance(progress, int):
		progress = float(progress)
	if not isinstance(progress, float):
		progress = 0
		status = "error: progress var must be float\r\n"
	if progress < 0:
		progress = 0
		status = "Halt...\r\n"
	if progress >= 1:
		progress = 1
		status = "Done...\r\n"
	block = int(round(barLength*progress))
	text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
	sys.stdout.write(text)
	sys.stdout.flush()