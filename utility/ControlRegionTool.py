import os

from utility import MiscTool

class ControlRegionTool(object):
	'''

	'''	
	
	def __init__(self, task, analysis_name, configuration, sample_tool):

		MiscTool.Print('python_info', '\nCreated instance of ControlRegionTool class')

		# ------ Paths -------
		self.path_working_directory = os.environ['Hbb_WORKING_DIRECTORY']
		self.path_results 			= os.path.join( self.path_working_directory, 'results', analysis_name)

		# ------ Samples -------
		self.sample_tool 	= sample_tool




