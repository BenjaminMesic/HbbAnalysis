import os
import hashlib

import ROOT

from utility import MiscTool


class TreeTool(object):
	'''
	-----------
	Description:

	-----------	
	Input files:

	-----------
	Parameters:

	-----------
	Functions:

	-----------
	Useful commands:


	-----------
	To DO:

	'''	
	def __init__(self, arg):
		MiscTool.Print('python_info', '\nCreated instance of TreeTool class')

	@staticmethod	
	def check_if_tree_ok(file_name):
			''' 
			Check if file exists and if it's ok. If yes return True, else False
			'''

			_status = ''

			if os.path.isfile(file_name):

				f = ROOT.TFile.Open(file_name,'read')

				if (not f) or f.GetNkeys() == 0 or f.TestBit(ROOT.TFile.kRecovered) or f.IsZombie():
						
					_status = False

				else:
					_status = True

				f.Close()

			else:
				_status = False

			return _status

	@staticmethod
	def trim_tree(cut, input_file, ID, path_cache, forceReDo=False):
		''' Create and return cached tree'''

		MiscTool.Print('python_info', '\nCalled trim_tree function.')

		# Set location of files
		_path_cache = path_cache
		MiscTool.make_directory(_path_cache)

		# output file name based on md5 of complete cut for this sample
		_unique_name = hashlib.md5(cut).hexdigest()
		_output_file = os.path.join( _path_cache, ID + '_' + _unique_name + '.root' )

		MiscTool.Print('analysis_info', 'Output file:', _output_file)
		MiscTool.Print('analysis_info', 'ID:', ID)
		MiscTool.Print('analysis_info', 'Input_file:', input_file)
		MiscTool.Print('analysis_info', 'Cut:', cut)

		_check_output_file = TreeTool.check_if_tree_ok(_output_file)

		# If file doesn't exists or it is corrupted
		if forceReDo or (not _check_output_file):
			
			# Create cached file (tmp file)
			try:
				if forceReDo:
					_output = ROOT.TFile.Open( _output_file,'recreate')
				else:
					_output = ROOT.TFile.Open( _output_file,'create')
				_output.cd()
			except:
				MiscTool.Print('error', 'Problem with creating _tmp. Delete root file and try again.')

			# Load source file
			_input_file = ROOT.TFile.Open( input_file,'read')
			_tree = _input_file.Get('tree')
			assert type(_tree) is ROOT.TTree

			# ------ Here starts actual skimming -------
			_input_file.cd()
			_obj = ROOT.TObject
			for key in ROOT.gDirectory.GetListOfKeys():
				_input_file.cd()
				_obj = key.ReadObj()
				if _obj.GetName() == 'tree':
					continue
				_output.cd()
				_obj.Write(key.GetName())
			_output.cd()

			# Apparently problem here: not working when empty tree
			_cuttedTree = _tree.CopyTree(cut)
			_cuttedTree.Write()
			_output.Write()
			_input_file.Close()
			del _input_file
			_output.Close()
			del _output
			MiscTool.Print('status', 'File done.')

		else:
			MiscTool.Print('python_info', 'File exists and it is ok.')

		return _output_file
