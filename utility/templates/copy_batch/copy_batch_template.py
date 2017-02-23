import subprocess as sp

from utility import MiscTool

def copy(destination, source):
	"""
	Just copy file.
	"""

	MiscTool.make_directory(destination)

	_command = ['gfal-copy', '--force']
	_command.append('srm:/' + source)
	_command.append('file:///' + destination)

	sp.call(_command)

if __name__ == '__main__':
	
	destination = '<destination>'
	source 		= '<source>'

	copy( destination, source)