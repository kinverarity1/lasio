import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    
setup(name='las_reader',
      entry_points={'console_scripts': ['las2excel = las_reader.las2excel:main']})

