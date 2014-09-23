#!/bin/env python

import datetime

from datetime import datetime as dtm

print datetime.__version__

dtstr = '00:01:29.123'

dt = dtm.strptime(dtstr, '%X.%f')

print dt


