from abc import ABC, abstractmethod
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
