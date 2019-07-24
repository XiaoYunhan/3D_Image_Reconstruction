import numpy as np 
import pymesh as pm
from scipy import linalg
from scipy.special import xlogy
from scipy.spatial.distance import cdist, pdist, squareform

class Rbf(object):

	def thin_plate(self, r):
        
		return xlogy(r**2, r)

	def __init__(self, input_x, input_y):
        
		self.x = input_x
		self.y = input_y
		self.flatten = np.asarray(self.x).flatten()
		self.num_of_input = self.flatten.shape[-1]
		self.last = np.asarray(self.y).flatten()

		self.A = self.thin_plate(squareform(pdist(self.flatten.T, 'euclidean')))
		self.B = linalg.solve(self.A, self.last)

	def __call__(self, input_x):
		
		sp = input_x.shape
		xa = np.asarray(input_x.flatten())
		r = cdist(xa.T, self.flatten.T, 'euclidean')
		return np.dot(self.thin_plate(r), self.B).reshape(sp)
    
target_mesh = pm.load_mesh("target.obj")
source_mesh = pm.load_mesh("source.obj")

source_vertices = source_mesh.vertices
#source_faces = source_mesh.faces
target_vertices = target_mesh.vertices
target_faces = target_mesh.faces

control_num = 50

control_index = np.arange(control_num)

source_vertices_x = source_vertices[:,0]
source_vertices_y = source_vertices[:,1]
source_vertices_z = source_vertices[:,2]

target_vertices_x = target_vertices[:,0]
target_vertices_y = target_vertices[:,1]
target_vertices_z = target_vertices[:,2]

source_distance_x = np.array([])
source_distance_y = np.array([])
source_distance_z = np.array([])
generate_x = np.array([])
generate_y = np.array([])
generate_z = np.array([])

source_control_x = source_vertices_x[0:control_num]
source_control_y = source_vertices_y[0:control_num]
source_control_z = source_vertices_z[0:control_num]
target_control_x = target_vertices_x[0:control_num]
target_control_y = target_vertices_y[0:control_num]
target_control_z = target_vertices_z[0:control_num]

result_x = target_control_x
result_y = target_control_y
result_z = target_control_z

vertex_num = source_vertices_x.size
for i in range(control_num, vertex_num):
    for j in range(0, control_num):
        distance_x = source_vertices_x.item(i) - source_vertices_x.item(j)
        distance_y = source_vertices_y.item(i) - source_vertices_y.item(j)
        distance_z = source_vertices_z.item(i) - source_vertices_z.item(j)
        source_distance_x = np.append(source_distance_x, distance_x)
        source_distance_y = np.append(source_distance_y, distance_y)
        source_distance_z = np.append(source_distance_z, distance_z)
    fitting_func_x = Rbf(source_control_x, source_distance_x)
    fitting_func_y = Rbf(source_control_y, source_distance_y)
    fitting_func_z = Rbf(source_control_z, source_distance_z)
    generate_x = np.add(Rbf(source_control_x)+target_control_x)
    generate_y = np.add(Rbf(source_control_y)+target_control_y)
    generate_z = np.add(Rbf(source_control_z)+target_control_z)
    result_x = np.append(result_x, np.mean(generate_x))
    result_y = np.append(result_y, np.mean(generate_y))
    result_z = np.append(result_z, np.mean(generate_z))
    
result_vertices = np.vstack([result_x, result_y, result_z]).T
pm.save_mesh_raw("output.obj", result_vertices, target_faces, voxels = None)
    





















