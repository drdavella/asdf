#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
import builtins

from setuptools import setup

from setup_helpers import (get_package_info, generate_version_file,
                           read_metadata, read_readme)

from astropy_helpers.setup_helpers import register_commands
from astropy_helpers.git_helpers import get_git_devstr

metadata = read_metadata('setup.cfg')
PACKAGE_NAME = metadata.get('package_name', 'asdf')
DESCRIPTION = metadata.get('description', 'package description')
AUTHOR = metadata.get('author', '')
AUTHOR_EMAIL = metadata.get('author_email', '')
LICENSE = metadata.get('license', 'unknown')
URL = metadata.get('url', '')

# Store the package name in a built-in variable so it's easy
# to get from other parts of the setup infrastructure
builtins._PACKAGE_NAME_ = PACKAGE_NAME

# VERSION should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)
VERSION = '1.3.2.dev'

# Indicates if this version is a release version
RELEASE = 'dev' not in VERSION

if not RELEASE:
    VERSION += get_git_devstr(False)

# Populate the dict of setup command overrides; this should be done before
# invoking any other functionality from distutils since it can potentially
# modify distutils' behavior.
cmdclassd = register_commands(PACKAGE_NAME, VERSION, RELEASE)

# Dynamically generate version.py file distributed with package
generate_version_file(os.path.curdir, PACKAGE_NAME, VERSION, RELEASE)

package_info = get_package_info()

#Define entry points for command-line scripts
entry_points = {}
entry_points['console_scripts'] = [
    'asdftool = asdf.commands.main:main',
]
entry_points['asdf_extensions'] = [
    'builtin = asdf.extension:BuiltinExtension'
]

# Add the dependencies which are not strictly needed but enable otherwise skipped tests
extras_require = []
if os.getenv('CI'):
    extras_require.extend(['lz4>=0.10'])


setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      python_requires='>=3.3',
      install_requires=[
          'semantic_version>=2.3.1',
          'pyyaml>=3.10',
          'jsonschema>=2.3.0',
          'six>=1.9.0',
          'numpy>=1.8',
          'astropy>=1.3',
      ] + extras_require,
      tests_require=['pytest-astropy'],
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL,
      long_description=read_readme('README.md'),
      cmdclass=cmdclassd,
      zip_safe=False,
      use_2to3=True,
      entry_points=entry_points,
      **package_info
)
