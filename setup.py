'''Setup script for lasio'''

from setuptools import setup
from os import path

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r","") # Do not forget this line
except:
    print("Pandoc not found. Long_description conversion failure.")

    # pandoc is not installed, fallback to using raw contents
    with open('README.md') as f:
        long_description = f.read()

from lasio import __version__

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

CLASSIFIERS = [
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
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering",
    "Topic :: System :: Filesystems",
    "Topic :: Scientific/Engineering :: Information Analysis",
    ]


setup(name='lasio',
      version=__version__,
      description="Read/write well data from Log ASCII Standard (LAS) files",
      long_description=long_description,
      url="https://github.com/kinverarity1/lasio",
      author="Kent Inverarity",
      author_email="kinverarity@hotmail.com",
      license="MIT",
      classifiers=CLASSIFIERS,
      keywords="science geophysics io",
      packages=["lasio", ],
      install_requires=requirements,
      entry_points={
          'console_scripts': [
              'las2excel = lasio.excel:main',
              'las2excelbulk = lasio.excel:main_bulk',
              'lasio = lasio:version',
          ],
      }
      )
