#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from distutils.core import setup

import os

def files_in(dir):
    files = []

    if os.path.isdir(dir):
        # Remove dot-files.
        files = filter(lambda x: not x.startswith('.'), os.listdir(dir))
        # Make it dir/file and not just file.
        files = map(lambda x: '%s/%s' % (dir, x), files)

    return files

setup(name         = 'pymei',
      version      = '0.1',
      description  = 'PyMei - A Python Media Interface',
      url          = 'http://pymei.org',
      author       = 'Jørgen Pedersen Tjernø',
      author_email = 'contact@pymei.org',
      scripts      = ['pymei'],
      packages     = ['mei',
                      'mei.plugins',
                      'mei.gui',
                      'mei.gui.widgets'
                     ],
      data_files   = [
                      ('/etc', ['pymei.config']),
                      ('/usr/share/pymei/data', files_in('data')),
                      ('/usr/share/pymei/themes', files_in('themes'))
                     ]
     )
