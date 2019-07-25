import numpy as np
import pymesh as pm

target_mesh = pm.load_mesh("target.obj")
source_mesh = pm.load_mesh("source.obj")
output_mesh = pm.load_mesh("output.obj")

source_vertices = source_mesh.vertices
target_vertices = target_mesh.vertices
output_vertices = output_mesh.vertices


sample_source = source_vertices[50:,:]
sample_output = output_vertices[50:,:]

print(sample_source)
print(sample_output)
print(sample_source-sample_output)
#print(source_vertices-output_vertices)
