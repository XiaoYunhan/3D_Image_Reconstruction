import numpy as np
import pymesh as pm
from scipy import linalg
from scipy.special import xlogy
from scipy.spatial.distance import cdist, pdist, squareform
#import rbf

class Rbf(object):

	def multiquadric(self, r):
        
		return np.sqrt((1.0/self.epsilon*r)**2 + 1)

	def thin_plate(self, r):
        
		return xlogy(r**2, r)

	def __init__(self, input_x, input_y, input_z):
        
		self.x = input_x
		self.y = input_y
		self.z = input_z
		self.flatten = np.asarray([np.asarray(self.x).flatten(),
							       np.asarray(self.y).flatten()]) # shape (2, num_of_input)
		self.num_of_input = self.flatten.shape[-1]
		# print(self.flatten.shape)
		self.last = np.asarray(self.z).flatten() # shape (num_of_input,)
		# print(self.last.shape)

		self.A = self.thin_plate(squareform(pdist(self.flatten.T, 'euclidean')))
		
		self.B = linalg.solve(self.A, self.last) # least squares

	def __call__(self, input_x, input_y):
		
		sp = input_x.shape
		xa = np.asarray([input_x.flatten(), input_y.flatten()])
		# print(xa.shape)
		r = cdist(xa.T, self.flatten.T, 'euclidean')
		return np.dot(self.thin_plate(r), self.B).reshape(sp)

target_mesh = pm.load_mesh("target.obj")
source_mesh = pm.load_mesh("source.obj")

source_vertices = source_mesh.vertices
#print(source_vertices.shape)
# source_faces = source_mesh.faces

target_vertices = target_mesh.vertices
# faces index of target_mesh are unchanged
# target_faces = target_mesh.faces

# print(source_vertices)
# print(source_faces)

source_vertices_x = source_vertices[:,0]
source_vertices_y = source_vertices[:,1]
source_vertices_z = source_vertices[:,2]

target_vertices_x = target_vertices[:,0]
target_vertices_y = target_vertices[:,1]
target_vertices_z = target_vertices[:,2]

#print(target_vertices_x.shape)
#print(source_vertices_y.shape)
#print(source_vertices_z.shape)

sample_vertices_x = np.array([])
sample_vertices_y = np.array([])
sample_vertices_z = np.array([])

vertex_num = source_vertices_x.size
for i in range(0,vertex_num):
    if i%5==0:
        sample_vertices_x = np.append(sample_vertices_x, source_vertices_x[i])
        sample_vertices_y = np.append(sample_vertices_y, source_vertices_y[i])
        sample_vertices_z = np.append(sample_vertices_z, source_vertices_z[i])

fitting_func = Rbf(sample_vertices_x, sample_vertices_y, sample_vertices_z)
generate_z = fitting_func(target_vertices_x, target_vertices_y)

result_vertices = np.vstack([target_vertices_x, target_vertices_y, generate_z]).T

#percentage = 0.0

#for i in range(0,20574):
#    percentage = percentage + (generate_z[i]-target_vertices_z[i])/target_vertices_z[i]

# print(percentage)
pm.save_mesh_raw("output.obj", result_vertices, target_mesh.faces, voxels=None)
#result_mesh = pm.meshio.form_mesh(result_vertices, target_mesh.faces, voxels=None)
#pm.save_mesh("output.obj", result_mesh)
print(target_vertices_x)
print(target_vertices_y)
print(generate_z)
#print(target_vertices_x.shape)
#print(target_vertices_y.shape)
#print(generate_z.shape)
#print(result_vertices.shape)

