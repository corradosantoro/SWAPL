# -----------------------------------------------------------------
# swapl_lib_control.py
# -----------------------------------------------------------------

import time
import math

from swapl_types import *

# -----------------------------------------------------------------
class saturate(PythonFunction):
    def evaluate(self, val, _min, _max):
        if val > _max:
            val = _max
        if val < _min:
            val = _min
        return val
