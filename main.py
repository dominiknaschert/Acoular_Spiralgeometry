import numpy as np
import matplotlib.pyplot as plt
import acoular as ac
from acoular import MicGeom, WNoiseGenerator, PointSource, Mixer, WriteH5
from pathlib import Path

# Spiral-Array-Generierung nach Sarradj (Paper) 

def generate_spiral_geometry(num_mics=64, R=1.0, V=1.5, filename='spiralgeometrie.xml'):
    """
    Generiert eine Spiral-Mikrofonanordnung nach Sarradj mit V-Parameter aus dem Paper.
    Speichert das Array als XML-Datei im Acoular-Format.
    """
    print(f"Generating spiral geometry with V={V}, M={num_mics}, R={R}...")

    m = np.arange(1, num_mics + 1)  # Mikrofon-Index: 1 bis M

    # Formel aus dem Paper
    r = R * np.sqrt(m / num_mics)
    phi = 2 * np.pi * m * ((1 + np.sqrt(V))/2)

    x = r * np.cos(phi)
    y = r * np.sin(phi)
    z = np.zeros_like(x)

    positions = np.vstack([x, y, z])  # shape (3, num_mics)

    mg = MicGeom(pos_total=positions)
    mg.export_mpos(filename)

    print(f"Spiral geometry exported to {filename}")
    return Path(filename)


# H5-Datei mit synthetischen Quellen erzeugen 
def generate_synthetic_sources(h5_filename='three_sources.h5', xml_file='spiralgeometrie.xml', sfreq=51200, duration=1.0):
    num_samples = int(sfreq * duration)
    mics = MicGeom(file=xml_file)

    n1 = WNoiseGenerator(sample_freq=sfreq, num_samples=num_samples, seed=1, rms=1.0)
    n2 = WNoiseGenerator(sample_freq=sfreq, num_samples=num_samples, seed=2, rms=0.7)
    n3 = WNoiseGenerator(sample_freq=sfreq, num_samples=num_samples, seed=3, rms=0.5)

    p1 = PointSource(signal=n1, mics=mics, loc=(-0.1, -0.1, -0.3))
    p2 = PointSource(signal=n2, mics=mics, loc=(0.15, 0, -0.3))
    p3 = PointSource(signal=n3, mics=mics, loc=(0, 0.1, -0.3))

    p = Mixer(source=p1, sources=[p2, p3])
    writer = WriteH5(source=p, file=h5_filename)
    writer.save()
    print(f"h5-file generiert: {h5_filename}")
    return h5_filename

# Hauptprogramm

def main():
    print("Generiere Geometrie")

    xml_file = generate_spiral_geometry()
    h5_file = generate_synthetic_sources(xml_file=xml_file)

    micgeofile = Path(xml_file)
    datafile = Path(h5_file)
    assert datafile.exists(), 'H5-Datenfile nicht gefunden.'

    # Beamforming berechnen 
    mg = ac.MicGeom(file=micgeofile)
    ts = ac.TimeSamples(file=datafile)
    ps = ac.PowerSpectra(source=ts, block_size=128, window='Hanning')
    rg = ac.RectGrid(x_min=-0.2, x_max=0.2, y_min=-0.2, y_max=0.2, z=-0.3, increment=0.01)
    st = ac.SteeringVector(grid=rg, mics=mg)
    bb = ac.BeamformerBase(freq_data=ps, steer=st)

    # Frequenzanalyse bei 8000 Hz
    f = 4000
    pm = bb.synthetic(f, 3)
    Lm = ac.L_p(pm)

    # Plot: Beamforming-Map 
    plt.figure(1)
    plt.title(f"Beamforming Map @ {f} Hz")
    plt.imshow(Lm.T, origin='lower', vmin=Lm.max() - 10, extent=rg.extend(), interpolation='bicubic')
    plt.colorbar(label="dB")

    # Plot: Mikrofonpositionen
    plt.figure(2)
    plt.title("Mikrofonanordnung (Spiral)")
    plt.plot(mg.mpos[0], mg.mpos[1], 'o')
    plt.axis('equal')
    plt.grid()

    plt.show()
    print("Beamforming abgeschlossen und visualisiert.")

if __name__ == "__main__":
    main()
