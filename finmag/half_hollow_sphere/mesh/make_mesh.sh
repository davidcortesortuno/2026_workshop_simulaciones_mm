#!/bin/bash
FNAME=${1%.geo}
# Save in Version 2 ASCII in order to avoid issues with old dolfin-convert
gmsh -3 ${FNAME}.geo -format msh2
#
# meshio convert ${FNAME}.msh ${FNAME}.xml
# meshio convert ${FNAME}.msh ${FNAME}.xdmf
# XDMF still has problems: (strange floating glyph at the bottom of tube)
# python meshio_msh_to_xdmf.py ${FNAME}.msh

# Better: convert .msh to .xml using dolfin-convert
podman run -it --rm --userns=keep-id -v `pwd`:/home/fenics/shared quay.io/fenicsproject/stable \
    "cd shared && dolfin-convert ${FNAME}.msh ${FNAME}.xml && python3 plot_grain_mesh_stats.py ${FNAME}.xml"
