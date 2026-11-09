"""magnet.py - decide north / south pole of the package.

Depends on the sensor you have: digital Hall (two pins?) or analogue (ADC).
If analogue: record the no-magnet reading at startup, then the SIGN of (reading - rest)
gives N or S. Print raw values with real blocks before writing the thresholds.
"""


def read_polarity():
    """TODO: return "N", "S" or None (no clear field). Average a few samples."""
