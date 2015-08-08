"""Setup script for lasio

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


with open(path.join(path.dirname(__file__), "requirements.txt"), "r") as f:
    requirements = f.read().splitlines()


setup(name='lasio',

      version="0.7",

      description="Read/write well data from Log ASCII Standard (LAS) files",
      long_description=(
          "This is a Python package to read and write Log ASCII Standard (LAS)"
          " files, used for borehole/well data (e.g. geophysical/geological/ "
          "petrophysical logs). It is compatible with versions 1.2 and 2.0 of "
          "the LAS file specification, published by the Canadian Well Logging "
          "Society. In principle it is designed to read as many types of LAS "
          "files as possible, including ones containing common errors or "
          "non-compliant formatting. \n\nIt is written entirely in Python and "
          "works on any platform."),

      url="https://github.com/kinverarity1/lasio",

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
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Topic :: Scientific/Engineering",
          "Topic :: System :: Filesystems",
          "Topic :: Scientific/Engineering :: Information Analysis",
      ],

      keywords="science geophysics io",

      packages=["lasio", ],

      install_requires=requirements,

      entry_points={
          'console_scripts': [
              'las2excel = lasio.las2excel:main'
          ],
      }
      )
