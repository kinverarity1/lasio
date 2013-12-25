import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
import versioneer

versioneer.versionfile_source = os.path.join('las_reader', '_version.py')
versioneer.versionfile_build = os.path.join('las_reader', '_version.py')
versioneer.tag_prefix = '' # tags are like 1.2.0
versioneer.parentdir_prefix = 'las-reader-' # dirname like 'myproject-1.2.0'    

setup(name='las_reader',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      )
