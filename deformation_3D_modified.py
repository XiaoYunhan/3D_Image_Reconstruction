import numpy as np
import pymesh as pm
from scipy import linalg
from scipy.special import xlogy
from scipy.spatial.distance import cdist, pdist, squareform

class Rbf(object):

	def thin_plate(self, r):
        
		return xlogy(r**2, r)

	def __init__(self, input_x, input_y, input_z, displacement):
        
		self.x = input_x
		self.y = input_y
		self.z = input_z
		self.d = displacement
		self.flatten = np.asarray([np.asarray(self.x).flatten(),
							       np.asarray(self.y).flatten(),
                                   np.asarray(self.z).flatten()]) # shape (2, num_of_input)
		self.num_of_input = self.flatten.shape[-1]
		# print(self.flatten.shape)
		self.last = np.asarray(self.d).flatten() # shape (num_of_input,)
		# print(self.last.shape)

		self.A = self.thin_plate(squareform(pdist(self.flatten.T, 'euclidean')))
		
		self.B = linalg.solve(self.A, self.last) # least squares

	def __call__(self, input_x, input_y, input_z):
		
		sp = input_x.shape
		xa = np.asarray([input_x.flatten(), input_y.flatten(), input_z.flatten()])
		# print(xa.shape)
		r = cdist(xa.T, self.flatten.T, 'euclidean')
		return np.dot(self.thin_plate(r), self.B).reshape(sp)

target_mesh = pm.load_mesh("target.obj")
source_mesh = pm.load_mesh("source.obj")

source_vertices = source_mesh.vertices
target_vertices = target_mesh.vertices
#source_face = source_mesh.faces
target_face = target_mesh.faces

source_vertices_x = source_vertices[:,0]
source_vertices_y = source_vertices[:,1]
source_vertices_z = source_vertices[:,2]

target_vertices_x = target_vertices[:,0]
target_vertices_y = target_vertices[:,1]
target_vertices_z = target_vertices[:,2]

control_num = 50
#control_index = np.arange(control_num)

generate_x = np.array([])
generate_y = np.array([])
generate_z = np.array([])

source_control_x = source_vertices_x[0:control_num]
source_control_y = source_vertices_y[0:control_num]
source_control_z = source_vertices_z[0:control_num]
target_control_x = target_vertices_x[0:control_num]
target_control_y = target_vertices_y[0:control_num]
target_control_z = target_vertices_z[0:control_num]

result_x = source_control_x
result_y = source_control_y
result_z = source_control_z

vertex_num = source_vertices_x.size
for i in range(control_num, vertex_num):
    source_di_x = np.array([])
    source_di_y = np.array([])
    source_di_z = np.array([])
    for j in range(0, control_num):
        di_x = source_vertices_x.item(i) - source_vertices_x.item(j)
        di_y = source_vertices_y.item(i) - source_vertices_y.item(j)
        di_z = source_vertices_z.item(i) - source_vertices_z.item(j)
        source_di_x = np.append(source_di_x, di_x)
        source_di_y = np.append(source_di_y, di_y)
        source_di_z = np.append(source_di_z, di_z)
    #print(source_di_x.shape)
    #print(source_di_y.shape)
    #print(source_di_z.shape)
    #print(source_control_x.shape)
    fitting_x = Rbf(source_control_x, source_control_y, source_control_z, source_di_x)
    fitting_y = Rbf(source_control_x, source_control_y, source_control_z, source_di_y)
    fitting_z = Rbf(source_control_x, source_control_y, source_control_z, source_di_z)
    generate_x = np.add(fitting_x(target_control_x, target_control_y, target_control_z),target_control_x)
    generate_y = np.add(fitting_y(target_control_x, target_control_y, target_control_z),target_control_y)
    generate_z = np.add(fitting_z(target_control_x, target_control_y, target_control_z),target_control_z)
    result_x = np.append(result_x, np.mean(generate_x))
    result_y = np.append(result_y, np.mean(generate_y))
    result_z = np.append(result_z, np.mean(generate_z))

result_vertices = np.vstack([result_x, result_y, result_z]).T
pm.save_mesh_raw("output.obj", result_vertices, target_face, voxels = None)
print("deformation finished")

check_a = result_vertices.flatten()
check_b = source_vertices.flatten()

percentage = 0
for i in range(0,check_a.size):
    percentage = percentage + (abs(check_a.item(i)-check_b.item(i))/check_b.item(i))
print(percentage)    
percentage = percentage/check_a.size
print(percentage)



