import os
import subprocess as sp

if __name__ == '__main__':
	
	print '\n','-'*50, '\nWelcome to Hbb code! Setup started! \n', '-'*50

	# ----------------------------------------------------
	# ------------ Change only this part -----------------
	# ----------------------------------------------------
	
	# This will be stored in configuration files after they are created, you can modify config files at any time
	analysis_name 	= 'Wlv'
	path_samples 	= '/STORE/Hbb/2016_10_VHBBHeppyV24'
	path_working_directory = os.environ['Hbb_WORKING_DIRECTORY']

	paths = {
		'path_samples'					: path_samples,
		'path_samples_preselection' 	: '_'.join([path_samples, analysis_name, 'preselection']),
		'path_samples_modified' 		: '_'.join([path_samples, analysis_name, 'modified']),
		'path_cache' 					: '_'.join([path_samples, analysis_name, 'cache']),
		'path_configuration'			: os.path.join( path_working_directory, 'configuration', analysis_name),
		'path_plots'					: os.path.join( path_working_directory, 'plots', analysis_name),
		'path_results'					: os.path.join( path_working_directory, 'results', analysis_name),
		'path_extra'					: os.path.join( path_working_directory, 'extra', analysis_name)
	}

	# ----------------------------------------------------
	# ----------------------------------------------------

	print '\n{0:35s}{1}'.format('Analysis name:', analysis_name)
	print '{0:35s}{1}'.format('path_working_directory:', path_working_directory)
	print '{0:35s}{1}'.format('path_samples:', path_samples)
	print '{0:35s}{1}'.format('path_samples_preselection:', paths['path_samples_preselection'])
	print '{0:35s}{1}'.format('path_samples_modified:', paths['path_samples_modified'])
	print '{0:35s}{1}'.format('path_cache:', paths['path_cache'])

	# ------------ Setup location of samples, code structure, etc.... -----------------

	print '\nChecking directory structure.'

	for _p in paths:

		if os.path.isdir(paths[_p]):
			print '{0} directory already exists.'.format(paths[_p]) 
		else:
			# Create directory if it doesn't exist
			try:
				os.makedirs(paths[_p])
				print '{0} directory created.'.format(paths[_p]) 				
			except Exception as e:
				print '\nERROR: Problem creating {0}. Check permissions.'.format(samples_directory)
				raise	


	# ------------ Setup analysis code structure -----------------

	print '\nSetup configuration files.'

	# Copy configuration template files
	config_templates_path = os.path.join( path_working_directory, 'utility/templates/configuration/*')
	_command = 'cp -r ' + config_templates_path + ' ' + os.path.join( path_working_directory, 'configuration', analysis_name)
	sp.call(_command, shell=True)

	# Modify configuration paths.py
	config_files = sp.check_output('ls ' + config_templates_path, shell=True).split()

	paths_config = os.path.join( path_working_directory, 'configuration', analysis_name ,'paths.py')
	with open(paths_config) as f:
		newText=f.read().\
				replace('<path_samples>', path_samples).\
				replace('<path_samples_preselection>', paths['path_samples_preselection']).\
				replace('<path_samples_modified>', paths['path_samples_modified']).\
				replace('<path_cache>', paths['path_cache'])


	with open(paths_config, "w") as f:
		f.write(newText)

	print '\n','-'*50, '\nSetup done!\n', '-'*50