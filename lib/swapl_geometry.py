# -----------------------------------------------------------------------------
# swapl_geometry.py
# -----------------------------------------------------------------------------

import math

def normalize_angle_degrees(d):
    if d > 180:
        d = d - 360
    if d < -180:
        d = d + 360
    return d

def normalize_angle_radians(d):
    if d > math.pi:
        d = d - 2*math.pi
    if d < -math.pi:
        d = d + 2*math.pi
    return d
