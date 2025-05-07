import numpy as np
from acoular import MicGeom
from pathlib import Path

# Parameter
def generate_spiral_geometry():
    """
    Generates a spiral microphone array geometry and saves it to an XML file.
    """

    print("Generating spiral geometry...")
    num_mics = 64
    a = 0.01  # Startabstand
    b = 0.05  # Abstandszuwachs pro Winkel (Spiralenbreite)
    angles = np.linspace(0, 4 * np.pi, num_mics)  # Spiralwinkel

    # Positionen berechnen (x = r*cos, y = r*sin, z = 0)
    radii = a + b * angles
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    z = np.zeros_like(x)  # Spiral liegt in XY-Ebene

    # Als (3, n)-Array wie von MicGeom erwartet
    positions = np.vstack([x, y, z])

    mg = MicGeom(pos_total=positions)

    mg.export_mpos('spiral_geom.xml')

    xmlfile = Path('spiral_geom.xml')

    return xmlfile 


