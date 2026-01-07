import meshio
import sys
from pathlib import Path


FNAME = Path(sys.argv[1])

stl_mesh = meshio.read(FNAME)

# For a simple 3D mesh, the physical volumes can be
# read from the gmsh_mesh.cell_sets dictionary
# The tag numbers in gmsh:physical will be saved to the SD data
# in the .tec file, since MERRILL expects SingleDomain tags
mesh = meshio.Mesh(stl_mesh.points, stl_mesh.cells)

# Notice that MERRILL 1.3.2 expects different headers so we must manually
# change: DATAPACKING -> F , ZONETYPE -> ET , BLOCK -> FEBLOCK
#         FETETRAHEDRON -> TETRAHEDRON
# Also replace cell data into ints: 1.00000 -> 1

meshio.write(
    FNAME.parents[0] / Path(FNAME.stem + "_stl_NOMAG.tec"),
    mesh,
    ncol=10,
    data_formats=dict(X=".5f", Y=".5f", Z=".5f", SD=".0f"),
)
# meshio.write(FNAME.parents[0] / Path(FNAME.stem + '_gmsh.xml'), mesh)
