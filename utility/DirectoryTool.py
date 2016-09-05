import os

import MiscTool

class DirectoryTool(object):
	"""
	-----------
	Description:
	
	----------- 
	Input files:    samples.ini, paths.ini, general.ini

	-----------
	Parameters:

	-----------
	Functions:

	-----------
	Useful commands:

	-----------
	To DO:

	"""
	def __init__(self, ):
		MiscTool.print_nice('python_info', '\nCreated instance of DirectoryTool class')
		

	@staticmethod
	def make_directory(directory):

		if not os.path.exists(directory):

			try:
				os.makedirs(directory)
			except OSError:
				if not os.path.isdir(directory):
					raise