## Gene.py
##
##

"""
1. What is the dimensionality for each gene type?

INPUT - [ m * n * k] ???

2. Constraints on kernel_size, stripe or num_kernels when generating random Genes?

3. Can we sample on a Gaussion distribution to get the number of conv and pooling?
	Also number of fully connected?

"""


# Enumerate the different gene types
INPUT = "INPUT"
CONV1D = "CONV1D"
CONV2D = "CONV2D"
POOL1D = "POOL1D"
POOL2D = "POOL2D"
FULLY_CONNECTED = "FULLYCONNECTED"

import random
from models.parts import *

"""
def createCNNgenotype(N=2):
	"""
	# Create an N layer (conv-pool) CNN encoding
	"""

	MIN_CNN_WIDTH = 2
	MAX_CNN_WIDTH = 75
	MIN_CNN_KERNELS = 5
	MAX_CNN_KERNELS = 30
	MIN_CNN_STRIDE = 1
	MAX_CNN_STRIDE = 5
	MIN_POOL_SIZE = 2
	MAX_POOL_SIZE = 5
	MIN_POOL_STRIDE = 1
	MAX_POOL_STRIDE = 5
	MIN_FULL_CONNECTION = 5
	MAX_FULL_CONNECTION = 200

	# Genotype is [CNN_width, num_CNN_kernels, CNN_stride, pool_size, pool_stride] * N
	# followed by number of full connections.  In total, an integer string of length 
	# 5*N+1.

	genotype = [0]*(5*N+1)

	# Fill in the CNN and pooling layer encodings
	for i in range(N):
		genotype[5*i+0] = np.random.randint(MIN_CNN_WIDTH, MAX_CNN_WIDTH+1)
		genotype[5*i+1] = np.random.randint(MIN_CNN_KERNELS, MAX_CNN_KERNELS+1)
		genotype[5*i+2] = np.random.randint(MIN_CNN_STRIDE, MAX_CNN_STRIDE+1)
		genotype[5*i+3] = np.random.randint(MIN_POOL_SIZE, MAX_POOL_SIZE+1)
		genotype[5*i+4] = np.random.randint(MIN_POOL_STRIDE, MAX_POOL_STRIDE+1)

	# Fill in the fully connected layer bit
	genotype[5*N] = np.random.randint(MIN_FULL_CONNECTION, MAX_FULL_CONNECTION+1)

	return genotype
"""


class Gene:
	"""
	An abstract gene.
	"""

	def __init__(self):
		"""
		Create a new gene.  This shouldn't do anything for this abstract class
		"""


		# What type of gene is this?  Since this is abstract, it isn't anything
		self.type = None


 
	def canFollow(self, prevGene):
		"""
		Can this gene follow the previous gene?  I.e., are all constraints satisfied?
		"""

		pass


	def outputDimension(self, prevGene):
		"""
		What is the dimensionality of the output of this gene?
		"""

		return None


	def mutate(self, prevGene, nextGene):
		"""
		Alter this gene, ensuring that the constraints from the previous and next gene are satisfied
		"""

		pass


	def generateLayer(self, name_suffix):
		"""
		Create the CNN part(s) (tuple of objects) used to construct this particular layer in the CNN
		"""

		pass



class InputGene(Gene):
	"""
	"""

	def __init__(self, dimensionality):
		"""
		Placeholder gene for the input dimensionality of the problem set
		"""

		self.dimensionality = dimensionality
		self.type = INPUT


	def canFollow(self, prevGene):
		"""
		This never follows a gene, it's the input
		"""

		return False


	def outputDimension(self, prevGene):
		"""
		"""

		return self.dimensionality


	def mutate(self, prevGene, nextGene):
		"""
		"""
		assert prevGene is None, "The input should not have previous gene!"
		print "You are mutating an input, not allowed!"


class Conv1DGene(Gene):
	"""
	"""

	def __init__(self, kernel_size, stride, num_filters, activation_function):
		"""
		"""

		self.kernel_size = kernel_size
		self.stride = stride
		self.num_filters = num_filters
		self.activation = activation_function

		self.type = CONV1D


	def canFollow(self, prevGene):
		"""
		A Conv1Dgene can follow an 'InputGene' or an 'Pool1DGene'
		The constraints are kernel_size should not larger than prevGene.output_size
		"""
		if prevGene.type == INPUT or prevGene.type == Pool1DGene:
			## next step is to see if 
			output_size = outputDimension(prevGene)		## calculate output dimension
			if self.kernel_size > output_size:
				return False
			else:
				return True
		else:
			return False


	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		input_size = prevGene.dimensionality
		output_size = (input_size-self.kernel_size)/stride + 1

		self.dimensionality = output_size
		return self.dimensionality


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_filters should be mutated based on the constraints from prevGene and nextGene
		"""

		pass



class Conv2DGene(Gene):
	"""
	"""

	def __init__(self, kernel_size, stride, num_filters, activation_function):
		"""
		"""

		self.kernel_size = kernel_size
		self.stride = stride
		self.num_filters = num_filters
		self.activation = activation_function

		self.type = CONV2D


	def canFollow(self, prevGene):
		"""
		A Conv2Dgene can follow an 'InputGene' or an 'Pool2DGene'
		The constraints are kernel_size should not larger than prevGene.output_size
		"""
		if prevGene.type == INPUT or prevGene.type == Pool2DGene:
			## next step is to see if 
			output_size = outputDimension(prevGene)		## calculate output dimension
			if self.kernel_size > output_size:
				return False
			else: 
				return True
		else:
			return False


	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		input_size = prevGene.dimensionality
		output_size = (input_size-self.kernel_size)/stride + 1

		self.dimensionality = output_size
		return self.dimensionality


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_filters should be mutated based on the constraints from prevGene and nextGene
		"""

		pass


class Pool1DGene(Gene):
	"""
	"""

	def __init__(self, kernel_size, stride, activation_function):
		"""
		"""

		self.kernel_size = kernel_size
		self.stride = stride
		self.activation = activation_function

		self.type = POOL1D


	def canFollow(self, prevGene):
		"""
		A Pool1DGene can only follow an 'Conv1DGene'
		"""
		if prevGene.type == Conv1DGene:
			## next step is to see if 
			output_size = outputDimension(prevGene)		## calculate output dimension
			if self.kernel_size > output_size:
				return False
			else: 
				return True
		else:
			return False


	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		input_size = prevGene.dimensionality
		output_size = (input_size-self.kernel_size)/stride + 1

		self.dimensionality = output_size
		return self.dimensionality


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_filters should be mutated based on the constraints from prevGene and nextGene		
		"""

		pass


class Pool2DGene(Gene):
	"""
	"""

	def __init__(self, kernel_size, stride, activation_function):
		"""
		"""

		self.kernel_size = kernel_size
		self.stride = stride
		self.activation = activation_function

		self.type = POOL2D


	def canFollow(self, prevGene):
		"""
		A Pool2DGene can only follow an 'Conv2DGene'
		"""
		if prevGene.type == Conv2DGene:
			## next step is to see if 
			output_size = outputDimension(prevGene)		## calculate output dimension
			if self.kernel_size > output_size:
				return False
			else return True
		else
			return False


	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		input_size = prevGene.dimensionality
		output_size = (input_size-self.kernel_size)/stride + 1

		self.dimensionality = output_size
		return self.dimensionality


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_filters should be mutated based on the constraints from prevGene and nextGene		
		"""

		pass


class FullyConnectedGene(Gene):
	"""
	"""

	def __init__(self, size, activation_function):
		"""
		"""

		self.size = size
		self.activation = activation_function

		self.type = FULLY_CONNECTED


	def canFollow(self, prevGene):
		"""
		A FullyConnectedGene can follow an 'Pool1DGene', an 'Pool2DGene' or another 'FullyConnectedGene'
		"""
		if prevGene.type == Conv1DGene or prevGene.type == Conv2DGene:
			return True
		else if prevGene.type == FullyConnectedGene:
			## Should the num of nodes of the following fully-connected layer be smaller???
			if prevGene.dimensionality < self.dimensionality:
				return False
			else:
				return True
		else:
			return False


	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		input_size = prevGene.dimensionality
		output_size = (input_size-self.kernel_size)/stride + 1

		self.dimensionality = output_size
		return self.dimensionality


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_filters should be mutated based on the constraints from prevGene and nextGene		
		"""

		pass


def generateGenotypeProb(inputGene, ConvProb=0.5, PoolProb=1.0, FullConnectProb = 0.5, is2D=False):
	"""
	Create a list of genes that describes a random, valid CNN
	"""

	# Pick out the appropriate Gene types
	if is2D:
		ConvGene = Conv2DGene
		PoolGene = Pool2DGene
	else:
		ConvGene = Conv1DGene
		PoolGene = Pool1DGene

	genotype = [InputGene(None)]

	# Add convolution layers (and possibly pooling layers) until a random check fails
	while random.random() < ConvProb:
		# Add the Convolution layer, with random arguments...
		genotype.append(ConvGene(None))

		# Should a pooling layer be added?
		if random.random() < PoolProb:
			genotype.append(PoolGene(None))

	# Added all the Convolution layers, now add FC layers
	while random.random() < FullConnectProb:
		# Add a fully connected layer
		genotype.append(FullyConnectedGene(None))

	return genotype


def generateGenotypeNum(inputGene, numConv, numFullConnected, is2D=False):
	"""
	Create a list of genes that describes a random, valid CNN
	"""

	# Pick out the appropriate Gene types
	if is2D:
		ConvGene = Conv2DGene
		PoolGene = Pool2DGene
	else:
		ConvGene = Conv1DGene
		PoolGene = Pool1DGene

	genotype = [InputGene(None)]

	# Add convolution layers (and possibly pooling layers) until a random check fails
	for i in range(numConv):
		genotype.append(ConvGene(None))
		genotype.append(PoolGene(None))

	# Added all the Convolution layers, now add FC layers
	for i in range(numFullConnected):
		genotype.append(FullyConnectedGene(None))

	return genotype


