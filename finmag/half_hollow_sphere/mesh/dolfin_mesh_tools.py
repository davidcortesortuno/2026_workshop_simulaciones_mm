import dolfin as df
import numpy as np
import textwrap


def mesh_info(mesh, edge_lengths_output=None):
    """
    Return a string containing some basic information about the mesh
    (such as the number of cells/vertices/interior and surface triangles)
    as well as the distribution of edge lengths.
    """
    # Note: It might be useful for this function to return the 'raw' data
    #       (number of cells, vertices, triangles, edge length distribution,
    #       etc.) instead of a string; this could then be used by another
    #       function generate such an info string (or to print the data
    #       directly). However, until such a need arises we leave it as it is.

    # Remark: the number of surface triangles is computed below as follows:
    #
    #     F_s = 4*C - F_i,
    #
    # where we use the abbreviation:
    #
    #    C = number of cells/tetrahedra
    #    F_i = number of interior facets
    #    F_s = number of surface facets
    #
    # Proof: Suppose that each tetrahedron was separated from its neighbours by
    # a small distance. Then the number of surface facets F_s would be exactly
    # 4*C (since each tetrahedron has four surface triangles).  To get the
    # number of surface facets in the "true" mesh (without space between
    # neighbouring cells), all the facets at which two tetrahedra are "glued
    # together" (i.e., precisely the interior facets) need to be subtracted
    # from this because otherwise they would be counted twice.

    edges = [e for e in df.edges(mesh)]
    facets = [f for f in df.facets(mesh)]
    C = mesh.num_cells()
    F = len(facets)
    F_i = 4 * C - F
    F_s = F - F_i
    E = len(edges)
    V = mesh.num_vertices()

    lens = [e.length() for e in df.edges(mesh)]
    if edge_lengths_output is not None:
        np.save(edge_lengths_output, np.array(lens))

    vals, bins = np.histogram(lens, bins=20)
    # to ensure that 'vals' and 'bins' have the same number of elements
    vals = np.insert(vals, 0, 0)
    vals_normalised = 70.0 / max(vals) * vals

    info_string = textwrap.dedent("""\
        ===== Mesh info: ==============================
        {:6d} cells (= volume elements)
        {:6d} facets
        {:6d} surface facets
        {:6d} interior facets
        {:6d} edges
        {:6d} vertices
        ===== Distribution of edge lengths: ===========
        """.format(C, F, F_s, F_i, E, V))

    for (b, v) in zip(bins, vals_normalised):
        info_string += "{:.3f} {}\n".format(b, int(round(v)) * '*')

    return info_string


def mesh_quality(mesh, ratios_output=None):
    """
    Returns a histogram string about the quality of the cells a mesh.
    The cell quality is measured by
        cell_dimension * inradius / circumradius
    which can take values between 0 and 1, where 1 is the best quality
    (e.g. a triangular/tetrahedral cell would be equilateral/regular).
    """

    ratios = df.MeshQuality.radius_ratios(mesh).array()
    if ratios_output is not None:
        np.save(ratios_output, ratios)

    vals, bins = np.histogram(ratios, bins=20)
    # to ensure that 'vals' and 'bins' have the same number of elements
    vals = np.insert(vals, 0, 0)
    vals_normalised = 70.0 / max(vals) * vals

    info_string = "======== Mesh quality info: ========\n"

    for (b, v) in zip(bins, vals_normalised):
        info_string += "{:.3f} {}\n".format(b, int(round(v)) * '*')

    return info_string
