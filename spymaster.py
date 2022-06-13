import itertools
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import random


class Spymaster(ABC):
	def __init__(self, color, board, clues_dict):
		self.color = color
		self.board = board
		self.clues_dict = clues_dict

	@abstractmethod
	def clue(self):
		pass


class SpymasterRandom(Spymaster):
	def clue(self):
		num_guesses = round(random.gauss(2, 1))
		num_guesses = 1 if num_guesses < 1 else num_guesses
		try_spaces = self.board.get_color_spaces(self.color)
		guesses = random.sample(try_spaces, num_guesses)
		return num_guesses, guesses, random.choice(self.clues_dict)


class SpymasterAI(Spymaster):
	def __init__(self, color, board, clues_dict):
		super().__init__(color, board, clues_dict)

		# Load word embeddings
		self.embeddings = {}
		with open("glove.6B/glove.6B.300d.txt", 'r') as glove:
			for line in glove:
				values = line.split()
				word = values[0]
				vector = np.asarray(values[1:], 'float32')
				self.embeddings[word] = vector

	def clue(self):
		target_words = self.board.get_color_spaces(self.color)
		bad_words = self.board.get_opposite_color_spaces(self.color) + self.board.blanks + self.board.black
		candidate_clues = []
		for k in range(1, len(target_words) + 1):
			for clue_targets in itertools.combintions(target_words, k):
				best = sorted(self.embeddings.keys(), key=lambda w: self.goodness())
