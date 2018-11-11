import numpy as np
from typing import List
from classifier import Classifier

class DecisionTree(Classifier):
	def __init__(self):
		self.clf_name = "DecisionTree"
		self.root_node = None

	def train(self, features: List[List[float]], labels: List[int]):
		# init.
		assert(len(features) > 0)
		self.feautre_dim = len(features[0])
		num_cls = np.max(labels)+1

		# build the tree
		self.root_node = TreeNode(features, labels, num_cls)
		if self.root_node.splittable:
			self.root_node.split()

		return
		
	def predict(self, features: List[List[float]]) -> List[int]:
		y_pred = []
		for feature in features:
			y_pred.append(self.root_node.predict(feature))
		return y_pred

	def print_tree(self, node=None, name='node 0', indent=''):
		if node is None:
			node = self.root_node
		print(name + '{')
		
		string = ''
		for idx_cls in range(node.num_cls):
			string += str(node.labels.count(idx_cls)) + ' '
		print(indent + ' num of sample / cls: ' + string)

		if node.splittable:
			print(indent + '  split by dim {:d}'.format(node.dim_split))
			for idx_child, child in enumerate(node.children):
				self.print_tree(node=child, name= '  '+name+'/'+str(idx_child), indent=indent+'  ')
		else:
			print(indent + '  cls', node.cls_max)
		print(indent+'}')


class TreeNode(object):
	def __init__(self, features: List[List[float]], labels: List[int], num_cls: int):
		self.features = features
		self.labels = labels
		self.children = []
		self.num_cls = num_cls

		count_max = 0
		for label in np.unique(labels):
			if self.labels.count(label) > count_max:
				count_max = labels.count(label)
				self.cls_max = label # majority of current node

		if len(np.unique(labels)) < 2:
			self.splittable = False
		else:
			self.splittable = True

		self.dim_split = None # the index of the feature to be split

		self.feature_uniq_split = None # the possible unique values of the feature to be split


	def split(self):
		def conditional_entropy(branches: List[List[int]]) -> float:
			'''
			branches: C x B array, 
					  C is the number of classes,
					  B is the number of branches
					  it stores the number of 
					  corresponding training samples 
					  e.g.
					              ○ ○ ○ ○
					              ● ● ● ●
					            ┏━━━━┻━━━━┓
				               ○ ○       ○ ○
				               ● ● ● ●
				               
				      branches = [[2,2], [4,0]]
			'''
			########################################################
			# TODO: compute the conditional entropy
			########################################################

			tot = np.sum(branches, axis = 0)
			# print(tot)
			means = tot / np.sum(tot)
			branch_tot = branches / tot
			entropy_each = []
			for x in branch_tot:
				tmp = []
				for y in x:
					if y:
						temp = np.log(y) * y * -1
					else:
						temp = 0
					tmp.append(temp)

				entropy_each.append(tmp)

			# print()
			# print(entropy_each)
			# print()
			# entropy =
			entropy = np.sum(np.sum(entropy_each, axis=0) * means)
			return entropy
			
		
		for idx_dim in range(len(self.features[0])):
		############################################################
		# TODO: compare each split using conditional entropy
		#       find the best split
		############################################################

			entropy_min = 9999999999999
			# print(idx_dim, self.features)
			# print()
			x_i = 'placeholder'
			x_i = []
			for x in self.features:
				x_i.append(x[idx_dim])
			# print(idx_dim, x_i)
			# print()
			# print(idx_dim, self.features)

			if None in x_i:
				continue

			x_i_uniq = np.unique(x_i)
			branches = [[0 for _ in range(len(x_i_uniq))] for __ in range(self.num_cls)]
			# print(self.num_cls, len(x_i_uniq), branches)
			i = -1
			for item in x_i_uniq:
				i += 1
				y = np.array(self.labels)[np.where(x_i == item)]
				for y_item in y:
					branches[y_item][i] += 1
			entropy = conditional_entropy(branches)
			if entropy_min > entropy:
				entropy_min = min(entropy, entropy_min)
				self.dim_split = idx_dim
				self.feature_uniq_split = list(x_i_uniq)




		############################################################
		# TODO: split the node, add child nodes
		############################################################

		xi = []
		for x in self.features:
			xi.append(x[self.dim_split])
		x = np.array(self.features, dtype=object)
		x[:, self.dim_split] = None
		y = []
		y.extend(self.features)
		# for _ in y:
		# 	_[self.dim_split] = None
		# print()
		# print(y)
		# print()
		# print(x)
		# x = np.delete(self.features, self.dim_split, axis=1)
		for val in self.feature_uniq_split:
			# print(xi,)
			# print(val)
			# print(len(xi), xi.count(val))
			indexes = np.where(xi == val)
			# print([len(x) for x in indexes])
			# print(indexes2)
			x2 = list(x[indexes])
			y_temp = np.array(self.labels)[indexes]
			y2 = list(y_temp)
			child = TreeNode(x2, y2, self.num_cls)
			if np.array(x2).size == 0:
				child.splittable = False
			if all(i == None for i in x2[0]):
				child.splittable = False

			self.children.append(child)




		# split the child nodes
		for child in self.children:
			if child.splittable:
				child.split()

		return

	def predict(self, feature: List[int]) -> int:
		if self.splittable:
			# print(feature)
			idx_child = self.feature_uniq_split.index(feature[self.dim_split])
			return self.children[idx_child].predict(feature)
		else:
			return self.cls_max



