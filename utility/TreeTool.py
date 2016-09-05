import os
import hashlib

import ROOT

import MiscTool
import DirectoryTool


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
		MiscTool.print_nice('python_info', '\nCreated instance of TreeTool class')
	
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
	def trim_trees(cut, subsamples_cut, samples_list, location_of_samples, forceReDo = False):
		''' Creates cached trees with cut and returns their dictionary'''

		MiscTool.print_nice('python_info', '\nCalled trim_trees function.')

		_samples_dict = {} 

		for _id in samples_list:

			_unique_name = hashlib.md5(cut).hexdigest()
			_source = os.path.join(location_of_samples, samples_list[_id] + '.root')
			_tmp_name = _id + '_' + _unique_name + '.root'
			_tmp_directory = os.path.join(location_of_samples, 'cache')
			_tmp = os.path.join(_tmp_directory, _tmp_name)

			DirectoryTool.DirectoryTool.make_directory(_tmp_directory)

			MiscTool.print_nice('status', '\nSample: ' + samples_list[_id])
			MiscTool.print_nice('analysis_info', 'Cut:', cut)
			MiscTool.print_nice('analysis_info', 'Source:', _source)
			MiscTool.print_nice('analysis_info', 'Tmp_file:', _tmp_name)

			_tmp_status_ok = TreeTool.check_if_tree_ok(_tmp)

			# If file doesn't exists or it is corrupted
			if (not _tmp_status_ok) or forceReDo:
				# Creating cached file (tmp file)
				try:
					if forceReDo:
						_output = ROOT.TFile.Open(_tmp,'recreate')
					else:
						_output = ROOT.TFile.Open(_tmp,'create')
					_output.cd()
				except:
					MiscTool.print_nice('error', 'Problem with creating _tmp. Delete root file and try again.')

				# Load source file
				_input = ROOT.TFile.Open( _source,'read')
				_tree = _input.Get('tree')
				assert type(_tree) is ROOT.TTree

				# ------ Here starts actual skimming -------
				_input.cd()
				_obj = ROOT.TObject
				for key in ROOT.gDirectory.GetListOfKeys():
					_input.cd()
					_obj = key.ReadObj()
					if _obj.GetName() == 'tree':
						continue
					_output.cd()
					_obj.Write(key.GetName())
				_output.cd()

				# ------ Sub samples cut -------
				if any(x in subsamples_cut for x in _id.split('_')):
					_subsample_cut = '&&' + subsamples_cut[_id.split('_')[1]]
				else:
					_subsample_cut = ''

				_cut = ''.join([cut, _subsample_cut])

				#Problem here: not working when empty tree
				_cuttedTree = _tree.CopyTree(_cut)
				_cuttedTree.Write()
				_output.Write()
				_input.Close()
				del _input
				_output.Close()
				del _output
				MiscTool.print_nice('status', 'File done.')

			else:
				MiscTool.print_nice('python_info', 'File exists and it is ok.')

			_samples_dict[_id] = _tmp

		return _samples_dict