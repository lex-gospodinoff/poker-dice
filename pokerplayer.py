from die import *;from pokertable import *
import pokerplayer
from operator import itemgetter;from collections import *
from copy import *;from math import pow,ceil
sFile = "Hand_Dictionary.hand"

HUMAN =0;PRUNING =1;BEST_AVERAGE=2;DUMMY =3

class PokerPlayer:
	"""
	The poker player class
	that plays poker dice
	"""
	def __init__(self, funds, bettor = False, player =1, AI = HUMAN, rasie_by =0):
		"""
		The player has a set of funds to bet (ints only)
		a dice and a set of unique hands
		"""
		self.player = player; self.AI =AI
		self.funds =funds; self.hand = []
		self.to_roll = [];self.bettor = bettor
		self.ptable = PokerTable(sFile); self.it =0
		if self.ptable.hand_dict == {}:
			self.ptable.enum_hands(); self.ptable.save(sFile)
		self.table =self.ptable.hand_dict

		for i in range(5): d = PokerDie(i); d.roll(); self.hand.append(d)

		self.hand =self.hand_sort(self.hand)

	def __str__(self):
		return str(self.funds)+ " "+str(self.bettor)+" "+ str(self.player) + " "+ str(self.AI)

	def __repr__(self):
		return self.player

	def reveal_hand(self):
		"""
		Finally showing your hand
		"""
		return self.hand

	def bet(self, diff_bet):
		"""
		Making a bet, call, folding, etc.
		"""
		want_bet = -1
		if self.AI != 0:
			want_bet = self.choose_bet(self.hand, diff_bet)
		if diff_bet > self.funds:
			want_bet = self.funds
		elif diff_bet + want_bet >  self.funds:
			want_bet = self.funds - diff_bet
		return want_bet  

	def roll(self, indexes):
		"""
		The roll or reroll depending on the round
		"""
		if indexes != []:
			self.select_to_roll(indexes)
			for die in self.to_roll:
				die.roll()
				self.hand.append(die)
			self.hand_sort(self.hand); self.to_roll =[]
			

	def hand_sort(self, hand): 
		"""
		Sorts a hand from largest values to shortest values
		"""
		hand = sorted(hand, key=lambda pokerdie: pokerdie.faces[pokerdie.face_up], reverse =True)
		return hand

	def select_to_hold(self):
		"""
		Method to choose which dice will be rerolled
		"""
		for die in self.to_roll: self.hand.remove(die)

	def select_to_roll(self, list_of_indexes):
		"""
		chosing the dice to be rolled based on the indexes of the dice
		"""
		for index in list_of_indexes: self.to_roll.append(self.hand[index])
		self.select_to_hold()


	def search(self, hand, ply=0):
		"""
		The search function based on a given hand returning a set of dice to be rerolled
		based on which configuation of dice would yeild the highest average score above what
		we have as a current best score. This is multiplied by the chance to get one of 
		these scores and doesn't even consider scores less than what we already have
		"""
		current_score = pokerplayer.score(hand)
		current_best = (current_score,[]) 								#the best possibility in a tuple format
		for score in self.table:
			if self.AI ==1:												#SMART
				if score > current_score:
					r =[0,1,2,3,4];x=[]
					for i in range(4,-1,-1):
						if hand[i] not in self.table[score]:
							r.remove(i)
					self.enum_rolls(r,hand,0,x); better_list = []
					for each in x:
						if each >= current_score:
							better_list.append(each)
					t =Counter(better_list); some_sum =0
					for each in t:
						some_sum += t[each]
					if better_list != []:
						s = (sum(better_list)/len(better_list)) * (some_sum /pow(6,len(r))) 
					else: s =0
					if s > current_best[0]: current_best = (s,r)
			elif self.AI ==2:														#EVERYTHING
				r =[0,1,2,3,4];x=[]
				for i in range(4,-1,-1):
					if hand[i] not in self.table[score]:
						r.remove(i)
				self.enum_rolls(r,hand,0,x); better_list = []
				for each in x:
					if each >= current_score:
						better_list.append(each)
				t =Counter(better_list); some_sum =0
				for each in t:
					some_sum += t[each]
				if better_list != []:
					s = (sum(better_list)/len(better_list)) * (some_sum /pow(6,len(r))) 
				else: s =0
				if s > current_best[0]: current_best = (s,r)
			elif self.AI == 3:														#IDOT
				r =[0,1,2,3,4];x=[]
				for i in range(4,-1,-1):
					if hand[i] not in self.table[score]: r.remove(i)
				self.enum_rolls(r,hand,0,x); better_list = []
				for each in x:
					if each >= current_score: better_list.append(each)
				s = max(better_list)
				if s > current_best[0]: current_best = (s,r)
		return current_best[1]						#could also return the score if we wanted to go deeper

	def enum_rolls(self,roll, hand, num, l): #return the probablility
		'''
		for each die in the index of dice roll all of the 
		dice and count the number of hands resulting in a higherscore and 
		return that over 6*len(list_to_be_roll)
		'''
		if num >= len(roll):
			l.append(score(hand));self.it +=1; return
		else:
			n =roll[num]
			h_1 = deepcopy(hand); h_2 = deepcopy(hand);h_3 = deepcopy(hand)
			h_4 = deepcopy(hand); h_5 = deepcopy(hand); h_6 = deepcopy(hand)
			h_1[n].face_up = 'Ace';h_2[n].face_up = 'King';h_3[n].face_up = 'Queen'
			h_4[n].face_up = 'Jack';h_5[n].face_up = 'Ten';h_6[n].face_up = 'Nine'
			self.enum_rolls(roll,h_1,num+1,l);self.enum_rolls(roll,h_2,num+1,l)
			self.enum_rolls(roll,h_3,num+1,l);self.enum_rolls(roll,h_4,num+1,l)
			self.enum_rolls(roll,h_5,num+1,l);self.enum_rolls(roll,h_6,num+1,l)

	def choose_bet(self,hand, diff_bet, raise_by = 0):
		"""
		choose the best bet given a hand an a round
		"""
		hand_combos =dict(Bust =480, Pair=3600,Two_Pair=1800,Three_of_a_Kind=1200,Straight=240,Full_House=300,Four_of_a_Kind=150,Five_of_a_Kind=6)
		s = score(hand); t = self.threshold(hand);hand_probs ={}
		if self.AI < 4 and self.AI != 0:
			for each in self.table:
				if self.update_probs(each, hand_probs, 65, 'Bust', s): break
				if self.update_probs(each, hand_probs, 274, 'Pair', s): break
				if self.update_probs(each, hand_probs, 811,'Two_Pair', s): break
				if self.update_probs(each, hand_probs, 1429, 'Three_of_a_Kind', s):break
				if self.update_probs(each, hand_probs, 1675, 'Straight', s): break
				if self.update_probs(each, hand_probs, 2539, 'Full_House', s): break
				if self.update_probs(each, hand_probs, 4095, 'Four_of_a_Kind', s): break
				if self.update_probs(each, hand_probs, 6678, 'Five_of_a_Kind', s): break
			num_above= 0;num_below =0
			for hand_sets in hand_probs:
				above =  hand_probs[hand_sets][0]; below =  hand_probs[hand_sets][1]
				if above != 0: num_above += (hand_combos[hand_sets] / above)
				if below != 0: num_below += (hand_combos[hand_sets] / below)
			percent_above = ceil((num_above / 7776.0) *100)/100; percent_below = ceil((num_below / 7776.0) *100)/100
			if diff_bet < t/1.5:
				if (percent_above/3.0) < percent_below:bet = diff_bet + t/6
				elif percent_above < percent_below: bet = diff_bet + t/10
				elif percent_below < .07: bet = -1 										#fold
				else: bet = diff_bet
			else:
				if (percent_above/6.0) < percent_below: bet = diff_bet + t/8
				elif percent_above < percent_below: bet = diff_bet
				else: bet = -1
		print bet
		return int(bet)

	def update_probs(self, score, hand_probs,max_score, hand_type, current_score):
		'''
		helper funtion to update the probablility dictionary
		'''
		if score < max_score:
			hand_probs[hand_type] = hand_probs.get(hand_type, [0,0])
			if score > current_score:
				hand_probs[hand_type][1] += 1
			else:
				hand_probs[hand_type][0] += 1
			return True
		else: return False

	def threshold(self, hand):
		'''
		getting the threshold that the AI is comfortable with
		'''
		s = score(hand); return ceil(s/10)

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
