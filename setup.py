from distutils.core import setup
    
setup(name='las_reader',
      # packages=["las_reader",],
      entry_points={'console_scripts': ['las2excel = las_reader.las2excel:main']})

