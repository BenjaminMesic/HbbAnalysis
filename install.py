import os
import subprocess as sp

if __name__ == '__main__':
	
	print '\n','-'*50, '\nWelcome to Hbb code! Setup started! \n', '-'*50

	# ------------ Change only this part -----------------
	# This will be stored in configuration files after they are created
	working_directory 	= os.environ['Hbb_WORKING_DIRECTORY']
	samples_directory 	= '/STORE/Hbb/2016_10_VHBBHeppyV24'
	analysis_name 		= 'Wlv'
	samples_directory_preselection = '_'.join([samples_directory,'preselection'])
	# ----------------------------------------------------

	print '{0:35s}{1}'.format('Analysis name:', analysis_name)
	print '\n{0:35s}{1}'.format('Working directory:', working_directory)
	print '{0:35s}{1}'.format('Samples directory:', samples_directory)
	print '{0:35s}{1}'.format('Samples directory preselection:', samples_directory_preselection)


	# Check if setup started for the first time, i.e. if directory structure exists
	# If not create it
	if not os.path.exists( os.path.join( working_directory, 'configuration', analysis_name)):
		print '\nSetup.py started for the first time. Creating directory structure.'

		# Create directory structure
		try:
			os.makedirs(samples_directory)
		except Exception, e:
			print '\nSample directory already exists.' 
			pass	

		os.makedirs(os.path.join( working_directory, 'configuration', analysis_name))
		open(os.path.join( working_directory, 'configuration', '__init__.py'), 'wa').close()
		os.makedirs(os.path.join( working_directory, 'plots', analysis_name))
		os.makedirs(os.path.join( working_directory, 'results', analysis_name))
		os.makedirs(os.path.join( working_directory, 'extra', analysis_name))

		# Copy configuration template files
		config_templates_path = os.path.join( working_directory, 'utility/templates/configuration/*')
		_command = 'cp -r ' + config_templates_path + ' ' + os.path.join( working_directory, 'configuration', analysis_name)
		sp.call(_command, shell=True)

		# Modify configuration paths.py
		config_files = sp.check_output('ls ' + config_templates_path, shell=True).split()

		paths = os.path.join( working_directory, 'configuration', analysis_name ,'paths.py')
		with open(paths) as f:
			newText=f.read().\
					replace('<samples_directory>', samples_directory).\
					replace('<samples_directory_preselection>', samples_directory_preselection)

		with open(paths, "w") as f:
			f.write(newText)

	else:
		print '\nDirectory structure exists: configuration directory!'

	print '\n','-'*50, '\nSetup done!\n', '-'*50