import numpy as np
import pymesh as pm
from RBF import RBF

__all__ = ['RBF_Deformation']

class RBF_Deformation(object):
    
    def __init__(self, targetMesh, sourceMesh, num_control):
        
        self.target_mesh = pm.load_mesh(targetMesh+".obj")
        self.source_mesh = pm.load_mesh(sourceMesh+".obj")
        
        self.source_vertices = self.source_mesh.vertices
        self.target_vertices = self.target_mesh.vertices
        #self.source_face = self.source_mesh.faces
        self.target_face = self.target_mesh.faces
        
        self.source_vertices_x = self.source_vertices[:,0]
        self.source_vertices_y = self.source_vertices[:,1]
        self.source_vertices_z = self.source_vertices[:,2]
        
        self.target_vertices_x = self.target_vertices[:,0]
        self.target_vertices_y = self.target_vertices[:,1]
        self.target_vertices_z = self.target_vertices[:,2]
        
        self.control_num = num_control
        #control_index = np.arange(control_num)
        print("Initialization finished")
        
    def __call__(self, outputMesh):
        
        generate_x = np.array([])
        generate_y = np.array([])
        generate_z = np.array([])
        
        source_control_x = self.source_vertices_x[0:self.control_num]
        source_control_y = self.source_vertices_y[0:self.control_num]
        source_control_z = self.source_vertices_z[0:self.control_num]
        target_control_x = self.target_vertices_x[0:self.control_num]
        target_control_y = self.target_vertices_y[0:self.control_num]
        target_control_z = self.target_vertices_z[0:self.control_num]
        
        result_x = source_control_x
        result_y = source_control_y
        result_z = source_control_z
        
        vertex_num = self.source_vertices_x.size
        for i in range(self.control_num, vertex_num):
            source_di_x = np.array([])
            source_di_y = np.array([])
            source_di_z = np.array([])
            for j in range(0, self.control_num):
                di_x = self.source_vertices_x.item(i) - self.source_vertices_x.item(j)
                di_y = self.source_vertices_y.item(i) - self.source_vertices_y.item(j)
                di_z = self.source_vertices_z.item(i) - self.source_vertices_z.item(j)
                source_di_x = np.append(source_di_x, di_x)
                source_di_y = np.append(source_di_y, di_y)
                source_di_z = np.append(source_di_z, di_z)
                #print(source_di_x.shape)
                #print(source_di_y.shape)
                #print(source_di_z.shape)
                #print(source_control_x.shape)
            fitting_x = RBF(source_control_x, source_control_y, source_control_z, source_di_x)
            fitting_y = RBF(source_control_x, source_control_y, source_control_z, source_di_y)
            fitting_z = RBF(source_control_x, source_control_y, source_control_z, source_di_z)
            generate_x = np.add(fitting_x(target_control_x, target_control_y, target_control_z),target_control_x)
            generate_y = np.add(fitting_y(target_control_x, target_control_y, target_control_z),target_control_y)
            generate_z = np.add(fitting_z(target_control_x, target_control_y, target_control_z),target_control_z)
            result_x = np.append(result_x, np.mean(generate_x))
            result_y = np.append(result_y, np.mean(generate_y))
            result_z = np.append(result_z, np.mean(generate_z))
                
        result_vertices = np.vstack([result_x, result_y, result_z]).T
        pm.save_mesh_raw(outputMesh+".obj", result_vertices, self.target_face, voxels = None)
        print("Deformation finished")
        
        check_a = result_vertices.flatten()
        check_b = self.source_vertices.flatten()
        
        percentage = 0
        for i in range(0,check_a.size):
            percentage = percentage + (abs(check_a.item(i)-check_b.item(i))/check_b.item(i))
        #print(percentage)    
        percentage = percentage/check_a.size
        print("Average error (in percentage):", percentage*100)



