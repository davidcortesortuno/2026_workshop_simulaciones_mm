import numpy as np

from finmag import Simulation as Sim
from finmag.energies import Exchange, Demag, DMI, Zeeman
from finmag.util.consts import mu0

import os, shutil
import dolfin as df

# Info
# from finmag.util.helpers import set_logging_level
# set_logging_level("INFO")
# set_logging_level("DEBUG")

# Geometries
from finmag.util.mesh_templates import Nanodisk


# MESH ------------------------------------------------------------------------

mesh_file = "mesh/nanocylinder.xml.gz"
if os.path.exists(mesh_file):
    mesh = df.Mesh(mesh_file)
else:
    mesh = Nanodisk(
        d=80, h=101, center=(0, 0, 0), valign="bottom", name="nanocylinder"
    ).create_mesh(
        maxh=2,
        save_result=True,
        filename="nanocylinder",
        directory="mesh",
    )


# Simulation and energies -----------------------------------------------------

# Bulk
A = 3.4e-12
Ms = 1.52e5
D = 2.1e-3
B = 0.4
initial_sk_diam = 20

sim = Sim(mesh, Ms=Ms, unit_length=1e-9, name="MnSi_cylinder")


# A linear model for the skyrmion profile
def m_init(pos):
    x, y = pos[0], pos[1]
    if (x**2 + y**2) ** 0.5 < initial_sk_diam:
        r = (x**2 + y**2) ** 0.5
        phi = np.arctan2(y, x) + 0.5 * np.pi
        k = np.pi / initial_sk_diam
        return (
            np.sin(k * r) * np.cos(phi),
            np.sin(k * r) * np.sin(phi),
            -np.cos(k * r),
        )
    else:
        return (0, 0, 1)


sim.set_m(m_init)

# -----------------------------------------------------------------------------

# Exchange Energy
sim.add(Exchange(A))
# DMI
sim.add(DMI(D, dmi_type="bulk"))
# Add the corresponding Zeeman field
sim.add(Zeeman((0, 0, B / mu0)))

# -----------------------------------------------------------------------------

sim.do_precession = False
sim.alpha = 0.9

if os.path.exists("vtks"):
    shutil.rmtree("vtks")
os.mkdir("vtks")

sim.save_vtk(filename="vtks/m.pvd".format(0))
sim.relax()
sim.save_vtk(filename="vtks/m.pvd".format(1))
sim.save_field("m", "m_relaxed.npy", overwrite=True)
