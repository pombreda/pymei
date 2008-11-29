#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
from distutils.core import setup
from mei.version import APP_VERSION

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
      version      = APP_VERSION,
      description  = 'PyMei - A Python Media Interface',
      url          = 'http://pymei.org',
      author       = 'Jørgen Pedersen Tjernø',
      author_email = 'contact@pymei.org',
      license      = 'New BSD (3-clause BSD)',
      scripts      = ['pymei'],
      packages     = ['mei',
                      'mei.plugins',
                      'mei.gui',
                      'mei.gui.widgets'
                     ],
      data_files   = [
                      ('/etc', ['example_configuration/pymei.config']),
                      ('share/pymei/data', files_in('data')),
                      ('share/pymei/themes', files_in('themes'))
                     ]
     )
