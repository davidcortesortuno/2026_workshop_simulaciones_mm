from pathlib import Path
import sys
import dolfin as df
import dolfin_mesh_tools as dmt

# Path to .mesh file
FILE = sys.argv[1]


MESHFILE = Path(FILE)
MESHFILEXDMF = MESHFILE.with_suffix('.xdmf')
MESHFILEXML = MESHFILE.with_suffix('.xml')
# if not MESHFILEXML.exists():
#     subprocess.call(f'dolfin-convert {str(MESHFILE)} {str(MESHFILEXML)}',
#                     shell=True)

if MESHFILE.suffix == '.xdmf':
    mesh = df.Mesh()
    f = df.XDMFFile(df.MPI.comm_world, str(MESHFILEXDMF))
    f.read(mesh)
elif MESHFILE.suffix == '.xml':
    mesh = df.Mesh(str(MESHFILEXML))
else:
    raise Exception('Use xdmf or xml file')

mesh_i = dmt.mesh_info(mesh, 
                       edge_lengths_output=MESHFILE.stem + '_ELs.npy')
mesh_q = dmt.mesh_quality(mesh,
                          ratios_output=MESHFILE.stem + '_ratios.npy')

print(mesh_i)
print(MESHFILE.stem + '_stats.txt')
with open(MESHFILE.stem + '_stats.txt', 'w') as f:
    f.write(mesh_i)
    f.write(mesh_q)
