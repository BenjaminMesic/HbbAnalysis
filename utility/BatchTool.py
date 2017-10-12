import os
import subprocess as sp
import stat

from utility import MiscTool

class BatchTool(object):

  def __init__(self, arguments, batch=True, send_job=True):

    self.arguments    = arguments
    self.template_txt = [
      'executable  =  <script_name>.sh',
      'universe    =  vanilla',
      'log         =  <script_name>.log',
      'initialdir  =  <initial_directory>',
      'error       =  <script_name>.error',
      'getenv      =  True',
      'queue'
    ]

    self.template_sh  = [
      '#!/bin/bash',
      'cd <initial_directory>',
      'python <script_name>.py'
    ]

    self.batch        = batch
    self.send         = send_job

    # make batch directory
    MiscTool.make_directory(self.arguments['<initial_directory>'])

  def make_scripts(self):

    # make scripts

    _scripts = {
      '.sh' : '\n'.join(self.template_sh),
      '.txt': '\n'.join(self.template_txt)
    }

    with open(self.arguments['python_template']) as f:
      _scripts['.py'] = f.read()
    del self.arguments['python_template']

    # make loop through all arguments and change all scripts
    for _arg, value in self.arguments.iteritems():

      for _script in _scripts:

        _scripts[_script] = _scripts[_script].replace(_arg, value)

    # Save files
    for _script in _scripts:

      _f = open( os.path.join(self.arguments['<initial_directory>'], self.arguments['<script_name>'] + _script),'w')
      _f.write(_scripts[_script])
      _f.close()

  def send_job(self):

    # if _i > 5:
    #   continue
    # if i%100 == 0 and i!=0:
    #   time.sleep(40)
    if self.send:

      # Change permission so that it can be executed 
      _sh = os.path.join(self.arguments['<initial_directory>'], self.arguments['<script_name>'] + '.sh')
      os.chmod(_sh, os.stat(_sh).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
      
      MiscTool.Print('python_info', _sh)

      _working_dir = os.getcwd()
      os.chdir( self.arguments['<initial_directory>'] )
      # print sp.check_output('pwd', shell=True)
      if self.batch:
        sp.call('condor_submit ' + self.arguments['<script_name>'] + '.txt', shell=True)      
      else:
        sp.call('./{0}.sh'.format(self.arguments['<script_name>']), shell=True)
      os.chdir(_working_dir)

