// NOTE: Base geometry generated using Gemini
//
// Use the OpenCASCADE kernel for robust boolean operations
SetFactory("OpenCASCADE");

Mesh.CharacteristicLengthMin = 2;
Mesh.CharacteristicLengthMax = 3;

// Define parameters for radii and mesh size
outer_radius = 60.0;
inner_radius = 50.0;

// Create the outer sphere
Sphere(1) = {0, 0, 0, outer_radius};

// Create the inner sphere
Sphere(2) = {0, 0, 0, inner_radius};

// Perform a boolean difference to create the hollow shell
// Syntax: BooleanDifference(result_tag) = {object_to_subtract_from} {tool_to_subtract};
BooleanDifference(3) = { Volume{1}; Delete; } { Volume{2}; Delete; };

// Create a box that will cut the sphere in half (e.g., in the negative Z direction)
// Dimensions for a large enough box to cover half the sphere
box_size = outer_radius * 2;
Box(4) = {-box_size/2, -box_size/2, box_size, box_size, box_size, -box_size};

// Perform a boolean intersection to keep only the upper half (Z > 0)
// Syntax: BooleanIntersection(result_tag) = {object_1} {object_2};
// This operation creates a new volume which is the intersection of the two, effectively cutting the sphere in half.
BooleanIntersection(5) = { Volume{3}; Delete; } { Volume{4}; Delete; };

// Optional: Define physical groups for boundary conditions and meshing
// Get surfaces of the final volume (tag 5)
// Surface Loop(100) = { Duplicates{ Volume{5}; } };
// Physical Volume("FluidDomain") = {5};

// To identify the surfaces, you might need to run the script once, visualize
// the surface IDs in the GUI, and add physical surfaces specifically for the
// outer surface, inner surface, and cut plane faces.

// Needs MMG:
RefineMesh;
Mesh.OptimizeNetgen = 1;

// Generate the 3D mesh
Mesh 3;

