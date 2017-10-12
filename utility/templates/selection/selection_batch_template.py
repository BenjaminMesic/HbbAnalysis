import os
import ROOT

from utility import MiscTool

ROOT.gROOT.SetBatch(True)

def preselection(i_file, o_file, cut):
	"""
	Apply preselection(cut) on input_file, as a result you get output_file
	Objects other than the TTree 'tree' are copied directly.
	"""

	input_file = ROOT.TFile.Open( i_file, 'read')
	output_file = ROOT.TFile( o_file, 'recreate')

	for key in input_file.GetListOfKeys():
		if key.GetName() == 'tree':
			continue
		obj = key.ReadObj()
		obj.Write()

	input_tree = input_file.Get('tree')
	n_total = input_tree.GetEntriesFast()
	output_tree = input_tree.CopyTree(cut)
	n_selected = output_tree.GetEntriesFast()
	output_tree.Write()

	return n_selected, n_total

if __name__ == '__main__':
	
	input_file = '<input_file>'
	output_file = '<output_file>'

	cut = '<cut>'

	output_directory = output_file.split('tree')[0]
	MiscTool.make_directory(output_directory)

	preselection(input_file, output_file, cut)