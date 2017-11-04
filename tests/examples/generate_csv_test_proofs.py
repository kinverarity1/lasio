import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import lasio

las = lasio.read('sample.las')
las.to_csv('sample.las_units-none.csv', units=None)
las.to_csv('sample.las_units-line.csv', units='line')
las.to_csv('sample.las_units-parentheses.csv', units='()')
las.to_csv('sample.las_units-brackets.csv', units='[]')