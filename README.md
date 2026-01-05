# 2026_workshop_simulaciones_mm

# Finite elements

## MERRILL

The focus of this micromagnetic FE code is to simulate magnetic rocks such as magnetite, at different temperatures, by scaling the magnetic parameters. Hysteresis, states of minimum energy, and energy paths can be computed. The code does not include dynamics via the LLG equation.

### Installation

Instruction can be found in the official repository: ![MERRILL](https://bitbucket.org/wynwilliams/merrill/src/master/)
The code uses `Cmake` to compile the Fortran code

    git clone https://bitbucket.org/wynwilliams/merrill
    cd merrill
    mkdir build
    cd build
    cmake .. 
    make

## Finmag

Full FE micromagnetic code, that currently works only via a virtual machine, such as Docker or Podman.

### Meshes

FE meshes can be generated directly from the code, using Netgen. Or using an external mesh tool such as ![Gmsh](https://gmsh.info/), which requires to convert the mesh into Dolfin's  `xml` format.

### Installation

The easiest way is to pull the Docker image from the cloud, as specified in the ![Finmag](https://github.com/fangohr/finmag) repository:

    docker pull finmag/finmag:latest
