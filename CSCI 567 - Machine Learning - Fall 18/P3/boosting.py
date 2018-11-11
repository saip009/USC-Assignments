import numpy as np
from typing import List, Set

from classifier import Classifier
from decision_stump import DecisionStump
from abc import abstractmethod

class Boosting(Classifier):
  # Boosting from pre-defined classifiers
	def __init__(self, clfs: Set[Classifier], T=0):
		self.clfs = clfs      # set of weak classifiers to be considered
		self.num_clf = len(clfs)
		if T < 1:
			self.T = self.num_clf
		else:
			self.T = T
	
		self.clfs_picked = [] # list of classifiers h_t for t=0,...,T-1
		self.betas = []       # list of weights beta_t for t=0,...,T-1
		return

	@abstractmethod
	def train(self, features: List[List[float]], labels: List[int]):
		return

	def predict(self, features: List[List[float]]) -> List[int]:
		'''
		Inputs:
		- features: the features of all test examples
   
		Returns:
		- the prediction (-1 or +1) for each example (in a list)
		'''
		########################################################
		# TODO: implement "predict"
		########################################################


		h = np.zeros(len(features))
		for i in range(len(self.clfs_picked)):
			clf = self.clfs_picked[i]
			beta = self.betas[i]
			h += self.betas[i] * np.array(self.clfs_picked[i].predict(features))
		h = [-1 if x <= 0 else 1 for x in h]
		return h
		

class AdaBoost(Boosting):
	def __init__(self, clfs: Set[Classifier], T=0):
		Boosting.__init__(self, clfs, T)
		self.clf_name = "AdaBoost"
		return
		
	def train(self, features: List[List[float]], labels: List[int]):
		'''
		Inputs:
		- features: the features of all examples
		- labels: the label of all examples
   
		Require:
		- store what you learn in self.clfs_picked and self.betas
		'''
		############################################################
		# TODO: implement "train"
		############################################################

		d = np.array([1/len(labels)]*len(labels))
		# print(len(labels), len(d))
		# print(d)

		for t in range(self.T):
			epsilon_min = float("inf")
			for clf in self.clfs:
				hx = clf.predict(features)
				# weighted error
				epsilon = 0
				for i in range(len(hx)):
					if labels[i] == hx[i]:
						pass
					else:
						epsilon += d[i]*1
				if epsilon < epsilon_min:
					ht = clf
					epsilon_min = epsilon
					htx = hx
			self.clfs_picked.append(ht)

			beta = 1/(2*np.log((1 - epsilon_min)/epsilon_min))
			self.betas.append(beta)

			for i in range(len(labels)):
				if labels[i] == htx[i]:
					d[i] = d[i]*np.exp(-beta)
				else:
					d[i] = d[i]*np.exp(beta)

			d = d/sum(d)
		
		
	def predict(self, features: List[List[float]]) -> List[int]:
		return Boosting.predict(self, features)



	