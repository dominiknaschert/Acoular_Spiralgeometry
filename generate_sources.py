from pathlib import Path
import matplotlib.pyplot as plt

import acoular as ac

"""Basic Beamforming -- Generate a map of three sources.
=====================================================

Loads the simulated signals from the `three_sources.h5` file, analyzes them with Conventional
Beamforming and generates a map of the three sources.

.. note:: The `three_sources.h5` file must be generated first by running the
:doc:`example_three_sources` example.
"""

"""
Three sources -- Generate synthetic microphone array data.
==========================================================

Generates a test data set for three sources.

The simulation generates the sound pressure at 64 microphones that are
arrangend in the 'array64' geometry which is part of the package. The sound
pressure signals are sampled at 51200 Hz for a duration of 1 second.
The simulated signals are stored in a HDF5 file named 'three_sources.h5'.

Source location (relative to array center) and levels:

====== =============== ======
Source Location        Level
====== =============== ======
1      (-0.1,-0.1,0.3) 1 Pa
2      (0.15,0,0.3)    0.7 Pa
3      (0,0.1,0.3)     0.5 Pa
====== =============== ======


"""

def generate_xlm():
    sfreq = 51200
    duration = 1
    num_samples = duration * sfreq
    h5savefile = Path('three_sources.h5')

    m = ac.MicGeom(file='spiral_geom.xml')
    n1 = ac.WNoiseGenerator(sample_freq=sfreq, num_samples=num_samples, seed=1, rms=1.0)
    n2 = ac.WNoiseGenerator(sample_freq=sfreq, num_samples=num_samples, seed=2, rms=0.7)
    n3 = ac.WNoiseGenerator(sample_freq=sfreq, num_samples=num_samples, seed=3, rms=0.5)
    n4 = ac.WNoiseGenerator(sample_freq=sfreq, num_samples=num_samples, seed=4, rms=1.0)
    p1 = ac.PointSource(signal=n1, mics=m, loc=(-0.1, -0.1, -0.3))
    p2 = ac.PointSource(signal=n2, mics=m, loc=(0.15, 0, -0.3))
    p3 = ac.PointSource(signal=n3, mics=m, loc=(0, 0.1, -0.3))
    p4 = ac.PointSource(signal=n4, mics=m, loc=(0.1, 0.05, -0.4))
    p = ac.Mixer(source=p1, sources=[p2, p3, p4])
    wh5 = ac.WriteH5(source=p, file=h5savefile)
    wh5.save()
    path = path('three_sources.h5')

    return path


