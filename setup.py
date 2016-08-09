import os
import subprocess as sp


if __name__ == '__main__':
	
	print '\n','-'*50, '\nWelcome to Hbb code! Setup started! \n', '-'*50

	# This will be stored in config files after they are created
	working_directory 	= os.getcwd()
	samples_directory 	= '/STORE/Hbb/2016_08_VHBBHeppyV21'
	analysis_name 		= 'Wlv'


	print '\n{0:30s}{1}'.format('Working directory:', working_directory)
	print '{0:30s}{1}'.format('Samples directory:', samples_directory)
	print '{0:30s}{1}'.format('Analysis_name:', analysis_name)

	# Check if setup started for the first time, i.e. if directory structure exists
	# If not create it
	if not os.path.exists( os.path.join( *[working_directory, 'config', analysis_name]) ):
		print '\nSetup.py started for the first time. Creating directory structure.'

		# Create directory structure
		os.makedirs(samples_directory)
		os.makedirs(os.path.join(*[working_directory, 'config', analysis_name]))
		os.makedirs(os.path.join(*[working_directory, 'plots', analysis_name]))
		os.makedirs(os.path.join(*[working_directory, 'results', analysis_name]))
		os.makedirs(os.path.join(*[working_directory, 'extra', analysis_name]))

		# Copy config template files
		config_templates_path = os.path.join(working_directory, 'utility/templates/config')
		config_files = sp.check_output('ls ' + config_templates_path, shell=True).split()

		for _config in config_files:
			_command = 'cp ' + os.path.join(config_templates_path, _config) + \
						' ' + os.path.join(*[working_directory, 'config', analysis_name])
			sp.call(_command, shell=True)

		# Modify config paths.ini
		paths = os.path.join(*[working_directory,'config', analysis_name ,'paths.ini'])

		with open(paths) as f:
			newText=f.read().\
					replace('string_working_directory', working_directory).\
					replace('string_samples_directory', samples_directory)

		with open(paths, "w") as f:
			f.write(newText)

	else:
		print '\nDirectory structure exists.'

	print '\n','-'*50, '\nSetup done!\n', '-'*50