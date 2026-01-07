"""
The system will use MnSi parameters from [Chalus et al. Phys. Rev. B 111, 064410 (2025)]

    A  = 3.4e-12  J m**-1  (not sure, the paper mentions 3.4e-3)
    Ms = 1.52e5   A m**-1
    D  = 2.1e-3   J m**-2
    lex =   nm
"""

import dolfin as df
import numpy as np
import finmag
from finmag import Simulation as Sim
from finmag.energies import Exchange, DMI, Demag, UniaxialAnisotropy, Zeeman
from finmag.util.consts import mu0
import os


# Material and geometric parameters -------------------------------------------
A  = 3.4e-12
Ms = 1.52e5
D  = 2.1e-3
# Ku = 0.4e6
# Bz = 300e-3  # T

# Simulation name
sim_name = 'half_sphere_sim'

# -----------------------------------------------------------------------------

# We will assume a very thin film (only one element across thickness) The
# center of the stripe will be at (0, 0, 0)
# MESHFILEXDMF = 'nanotube_Py_R4lex_r3lex_L40lex_OC.xdmf'
# mesh = df.Mesh()
# # Do not use MPI here, as in the case o the gmsh folder
# f = df.XDMFFile(MESHFILEXDMF)
# f.read(mesh)

mesh = df.Mesh('mesh/sphere_mesh.xml')

print finmag.util.meshes.mesh_quality(mesh)
print finmag.util.meshes.mesh_info(mesh)

# Generate simulation object
sim = Sim(mesh, Ms, unit_length=1e-9, name=sim_name)

# Add energies
sim.add(Exchange(A))
sim.add(DMI(D, dmi_type='bulk'))
# sim.add(DMI(D, dmi_type='auto'))
# sim.add(UniaxialAnisotropy(Ku, (0, 0, 1), name='Ku'))
sim.add(Demag())

# ZeemanInt = Zeeman((0.0, 0.0, Bz / mu0))
# sim.add(ZeemanInt)

sim.do_precession = False
sim.alpha = 0.9

# sim.set_m(lambda r: helical_n(r, n=-5))
sim.set_m((0., 0.1, 0.9))


# bz = 600.
# bzstep = 10.
# mT = 1e-3 / mu0

DATA_DIR = 'sim_output'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# TODO: Check where log file is saved

# Relax the system at zero field
sim.save_vtk('{}/m_initial.pvd'.format(DATA_DIR), overwrite=False)
sim.relax(stopping_dmdt=1e-1)

# Save the last relaxed state
# sim.save_vtk('{}/m.pvd'.format(DATA_DIR, int(bz)), overwrite=False)
sim.save_vtk('{}/m_final.pvd'.format(DATA_DIR), overwrite=False)
np.save('{}/m_final.npy'.format(DATA_DIR), sim.m)
