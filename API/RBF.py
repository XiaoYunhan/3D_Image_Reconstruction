import numpy as np 
from scipy import linalg
from scipy.special import xlogy
from scipy.spatial.distance import cdist, pdist, squareform

__all__ = ['RBF']

class RBF(object):

	def thin_plate(self, r):
        
		return xlogy(r**2, r)

	def cubic(self, r):
        
		return r**3
    
	def linear(self, r):
        
		return r
    
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

#print(callable(RBF))

