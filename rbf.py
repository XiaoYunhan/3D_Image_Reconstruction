import numpy as np
from scipy import linalg
from scipy.special import xlogy
from scipy.spatial.distance import cdist, pdist, squareform

__all__ = ['rbf']

class rbf(object):

	def multiquadric(self, r):

		result = np.sqrt((1.0/self.epsilon*r)**2 + 1)
		return result

	def thin_plate(self, r):

		result = xlogy(r**2, r)
		return result

	def cubic(self, r):

		result = r**3
		return result

	def linear(self, r):

		return r

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

