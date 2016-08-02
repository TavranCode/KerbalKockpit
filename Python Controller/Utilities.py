from math import sqrt


# UTILITY Functions
# determines if bit n is set in val x


def is_set(val, pos):
    return val & 2 ** pos != 0


# takes a flight control input 0-255 and returns a value -1 to 1.
# it also applies a linear dead band, adds a trim value and allows scaling


def map_flt_ctl(ctl_raw, db, trim, fine):
    ctl = ctl_raw / 255 * 2 - 1
    if abs(ctl) < db:
        return trim * fine
    else:
        return ((ctl - abs(ctl) / ctl * db) / (1 - db) + trim) * fine


# returns the length of a position vector


def norm(v):
    return sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
