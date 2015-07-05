from distutils.core import setup

setup(name='las_reader',
      version='0.9.0',

      description='LAS reader',
      long_description='LAS reader that was started by https://github.com/kinverarity1',

      # The project's main homepage.
      #url='https://github.com/VelizarVESSELINOV/las-reader',

      # Author details
      #author='Velizar VESSELINOV after fork of https://github.com/kinverarity1',
      #author_email='Velizar.VESSELINOV@gmail.com',
      #install_requires=['numpy>1.8' , 'pandas>0.0', 'namedlist>1.6',],

      # Choose your license
      license='BSD',

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Intended Audience :: Customer Service',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Science/Research',
            'Environment :: Console',
            'Operating System :: OS Independent',
            'Topic :: System :: Filesystems',
            'Topic :: Scientific/Engineering :: Information Analysis',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: BSD License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
      ],
      packages=["las_reader"],
)
