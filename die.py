from random import *
from operator import itemgetter

class Die:
	"""
	The class for a basic arbitrary die
	"""
	def __init__(self, name, n_sides, faces=[]):
		"""
		Creating the die
		"""
		try:
			self.name = name
			self.n_sides = n_sides
			self.faces = faces
			self.face_up = "to be rolled"
		except n_sides < 2 or not isinstance(n_sides, int):
			print "Error, please give a number larger than one for the number of sides"

	def __repr__(self):
		return self.face_up

	def result(self):
		""" 
		The result of a roll
		"""
		return self.face_up

	def roll(self):
		"""
		Rolling a given die
		"""
		if self.faces:
			self.face_up = self.faces[randint(0,self.n_sides-1)]
			return self.result()
		else:
			self.face_up = randint(1,self.n_sides)
			return self.result()

class PokerDie(Die):
	"""
	Class for the poker dice
	"""

	def __init__(self, name):
		"""
		Making a poker die
		"""
		self.name = name; self.n_sides = 6
		self.faces = {'Ace':14,'King':13,'Queen':12,'Jack':11,'Ten':10,'Nine':9}
		self.face_up = "N/A"

	def __eq__(self,other):
		"""
		checking equality
		"""
		return self.face_up == other.face_up

	def __ne__(self,other):
		"""
		checking inequality1
		"""
		return self.face_up != other.face_up

	def roll(self):
		sides = self.faces.keys(); self.face_up = sides[randint(0,self.n_sides-1)]

	def list_faces(self):
		"""
		gives a list of the faces
		"""
		face = sorted(self.faces.items(), key=itemgetter(1), reverse =True);f =[]
		for each in face: f.append(each[0])
		return f