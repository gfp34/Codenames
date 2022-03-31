from abc import ABC, abstractmethod
import math
import random


class FieldOperative(ABC):
	def __init__(self, color, board):
		self.color = color
		self.board = board

	@abstractmethod
	def guess(self, clue, num_guesses):
		pass


class FieldOperativeRandom(FieldOperative):
	def guess(self, clue, num_guesses):
		guesses = random.sample(self.board.spaces, num_guesses)
		guess_confidence = {}
		for guess in guesses:
			guess_confidence[guess] = 1 / (1 + math.exp(-random.gauss(.5, 1)))
		good_guesses = [(guess, guess_confidence[guess]) for guess in guesses if guess_confidence[guess] > 0.5]
		good_guesses.sort(key=lambda x: x[1], reverse=True)
		return good_guesses
