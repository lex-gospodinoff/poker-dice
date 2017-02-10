from die import *;from math import *; import os, pickle
from operator import itemgetter
from copy import *;from collections import *

class PokerTable:
	"""
	The Class that will compute
	and hold the dictionary of 
	hands (hashed by score)
	each of them the unique hands
	"""
	def __init__(self,sFile = ""):
		d = PokerDie(1);self.hand_dict={}
		if sFile != "":
			try:
				self.load(sFile)
			except Exception, e:
				pass
	def enum_hands(self):
		"""
		function to enumerate all hands and there
		scores for reference
		"""
		h =[]
		for i in range(5): h.append(PokerDie(i));h[i].face_up = 'Nine'
		self.get_enum(h)

	def get_enum(self,hand,num =0,):
		'''
		getting all of the enumerations
		not elegant but doing so by checking each permutation
		explictly
		'''
		if num >= len(hand): return
		else:
			h_1 = deepcopy(hand); h_2 = deepcopy(hand);h_3 = deepcopy(hand)
			h_4 = deepcopy(hand); h_5 = deepcopy(hand); h_6 = deepcopy(hand)
			h_1[num].face_up = 'Ace';h_2[num].face_up = 'King';h_3[num].face_up = 'Queen'
			h_4[num].face_up = 'Jack';h_5[num].face_up = 'Ten';h_6[num].face_up = 'Nine'
			s_1 =score(h_1); s_2 =score(h_2); s_3 =score(h_3)
			s_4 =score(h_4);s_5 =score(h_5); s_6 =score(h_6)
			l_h = [h_1,h_2,h_3,h_4,h_5,h_6]; l_s = [s_1,s_2,s_3,s_4,s_5,s_6]

			for i in range(6):
				h = l_h[i]; h= self.hand_sort(h); self.hand_dict[l_s[i]] = h

			self.get_enum(h_1,num+1);self.get_enum(h_2,num+1);self.get_enum(h_3,num+1)
			self.get_enum(h_4,num+1);self.get_enum(h_5,num+1);self.get_enum(h_6,num+1)

	def hand_sort(self, hand):
		'''
		sorts the hand to make it more presentable
		and to help eliminate duplicates
		'''
		h = sorted(hand, key=lambda pokerdie: pokerdie.faces[pokerdie.face_up]);h.reverse(); return h


	def save(self,sFile):
		'''
		saving the dictionary
		'''
		f = open(sFile, "w");p = pickle.Pickler(f)
		p.dump(self.hand_dict); f.close()			 # use dump to dump your variables

	def load(self, lFlie):
		'''
		loading the dictionary
		'''
		l =open(lFlie,"r"); p = pickle.Pickler(l)
		self.hand_dict = l.load(); l.close()

def score(hand):
	"""
	Evaluate a given hand
	"""
	f= []; d =PokerDie('dummy')# the die is only a reference to be used for retrieving the scores
	for each in hand: f.append(each.face_up)
	count_hand = Counter(f)
	face = sorted(count_hand.items(), key=lambda face: (face[1], d.faces[face[0]]), reverse =True)
	length = len(count_hand); score = 0
	if length == 5:
		s = 0
		for each in face:
			s += d.faces[each[0]]
			if s == 60 or s == 55:
				score = pow(s,1.5) *2.4#straight
			else:#bust
				score = d.faces[face[0][0]]+ d.faces[face[1][0]]*.8+ d.faces[face[2][0]] *.5+ d.faces[face[3][0]] *.3 +d.faces[face[4][0]]
	elif length == 4:#Pair
		score = 2*(((d.faces[face[0][0]])*(count_hand[face[0][0]]) *2.5 ) + d.faces[face[1][0]]+ d.faces[face[2][0]] *.45+ d.faces[face[3][0]] *.25)
	elif length == 3:
		if count_hand[face[0][0]] == 2:#two-pair
			score = 2*(((d.faces[face[0][0]])*(count_hand[face[0][0]])*3.01) + ((d.faces[face[1][0]])*(count_hand[face[1][0]]) *.4) *16.71 + d.faces[face[2][0]])
		else:#three of a kind
			score = ((d.faces[face[0][0]]*count_hand[face[0][0]] *4.5) + d.faces[face[1][0]]+ d.faces[face[2][0]] *.75) *4.51 	
	elif length ==2:
		if count_hand[face[0][0]] == 4:#Four of a kind
			score =(d.faces[face[0][0]]*count_hand[face[0][0]]*4 + d.faces[face[1][0]] )*11.51 
		else:# Full house
			score = (d.faces[face[0][0]]*count_hand[face[0][0]]*3 + d.faces[face[1][0]]*count_hand[face[1][0]]*2 ) * 9.5
	else: #five of a kind
		score =(d.faces[face[0][0]]*count_hand[face[0][0]] * 5) *12.71 
	return ceil((score*10000)*1.501)/10000
