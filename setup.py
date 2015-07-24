"""Setup script for las_reader

Based on:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from distutils.core import setup


setup(name='las_reader',

      version="0.3",
      
      description="Read borehole data from Log ASCII Standard (LAS) files",
      long_description=("A library for reading borehole data from log "
                        "standard ASCII (LAS) files (only specifications "
                        "1.2 and 2.0 are supported for now)."),
      
      url="https://github.com/kinverarity1/las_reader",
      
      author="Kent Inverarity",
      author_email="kinverarity1@gmail.com",
      
      license="MIT",
      
      classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Customer Service",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Other Audience",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering",
            "Topic :: System :: Filesystems",
            "Topic :: Scientific/Engineering :: Information Analysis",
            ],

      keywords="science geophysics io",
      
      packages=["las_reader", ],
      
      install_requires=["numpy", "namedlist", ],
      
      entry_points={
            'console_scripts': [
                  'las2excel = las_reader.las2excel:main'
            ],
      }
)
