from pathlib import Path
# generate_sources.py und generate_xlm.py werden beim start der Main durch den import direkt ausgeführt und die Dateien werden generiert.
from generate_sources import * 
from generate_xlm import *
import matplotlib.pyplot as plt
import acoular as ac

#micgeofile = Path(ac.__file__).parent / 'xml' / 'array_64.xml' # Strandart micgeom file aus Acoular Bibliothek
micgeofile = generate_spiral_geometry()  # Generate the spiral geometry
datafile = Path('three_sources.h5')
assert datafile.exists(), 'Data file not found, run example_three_sources.py first'




mg = ac.MicGeom(file=micgeofile) 
ts = ac.TimeSamples(file=datafile)
ps = ac.PowerSpectra(source=ts, block_size=128, window='Hanning')
rg = ac.RectGrid(x_min=-0.2, x_max=0.2, y_min=-0.2, y_max=0.2, z=-0.3, increment=0.01)
st = ac.SteeringVector(grid=rg, mics=mg)
bb = ac.BeamformerBase(freq_data=ps, steer=st)
pm = bb.synthetic(8000, 3)
Lm = ac.L_p(pm)

plt.figure(1)
plt.imshow(Lm.T, origin='lower', vmin=Lm.max() - 10, extent=rg.extend(), interpolation='bicubic')
plt.colorbar()

plt.figure(2)
plt.plot(mg.pos[0], mg.pos[1], 'o')
plt.axis('equal')
plt.show()