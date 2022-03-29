import math
from collections import namedtuple
from colorama import Fore, Back
import random

BLANK = 0
BLUE = 1
RED = 2
BLACK = 3


def main():
	card_list = [card.strip() for card in open("cards.txt", 'r')]
	word_list = [word.strip() for word in open("words", 'r')]

	board = Board(card_list)
	board.print_words()

	red_spy = Spymaster(RED, board, word_list)
	num_guesses, spaces, clue = red_spy.random_clue()
	print(num_guesses, spaces, clue)

	red_field_op = FieldOperative(RED, board)
	guesses = red_field_op.random_guess(clue, num_guesses)
	print(guesses)


Space = namedtuple("Space", ['color', 'word'])


class Board:
	def __init__(self, all_words):
		BOARD_SIZE = 25

		# Determine start color and randomly select board colors
		start_color = random.randint(BLUE, RED)

		# Randomly select 25 words for the board
		self.words = random.sample(all_words, BOARD_SIZE)

		# Assign words to space colors
		self.NUM_REDS = 9 if start_color is RED else 8
		self.reds = [Space(RED, self.words.pop()) for _ in range(self.NUM_REDS)]
		self.NUM_BLUES = 9 if start_color is BLUE else 8
		self.blues = [Space(BLUE, self.words.pop()) for _ in range(self.NUM_BLUES)]
		self.NUM_BLANKS = 7
		self.blanks = [Space(BLANK, self.words.pop()) for _ in range(self.NUM_BLANKS)]
		self.black = Space(BLACK, self.words.pop())

		# Shuffle board
		self.spaces = self.reds + self.blues + self.blanks + [self.black]
		random.shuffle(self.spaces)

		self.words = [space.word for space in self.spaces]
		self.key = [space.color for space in self.spaces]

	def __getitem__(self, index):
		return self.spaces

	def get_color_spaces(self, color):
		if color is RED:
			return self.reds
		elif color is BLUE:
			return self.blues
		elif color is BLANK:
			return self.blanks
		elif color is BLACK:
			return self.black
		else:
			return None

	def print_words(self):
		styled_words = []
		max_word_len = max([len(word) for word in self.words])
		for space in self.spaces:
			if space.color is RED:
				styled_words += [Back.RED + Fore.RESET + f"{space.word:{max_word_len}}"]
			elif space.color is BLUE:
				styled_words += [Back.BLUE + Fore.RESET + f"{space.word:{max_word_len}}"]
			elif space.color is BLACK:
				styled_words += [Back.RESET + Fore.RESET + f"{space.word:{max_word_len}}"]
			else:
				styled_words += [Back.WHITE + Fore.BLACK + f"{space.word:{max_word_len}}"]

		for i in range(5):
			print(' '.join(styled_words[i*5: i*5+5]) + (Back.RESET + Fore.RESET + ''))


class Spymaster:
	def __init__(self, color, board, clues_dict):
		self.color = color
		self.board = board
		self.clues_dict = clues_dict

	def random_clue(self):
		num_guesses = round(random.gauss(2, 1))
		num_guesses = 1 if num_guesses < 1 else num_guesses
		try_spaces = self.board.get_color_spaces(self.color)
		guesses = random.sample(try_spaces, num_guesses)
		return num_guesses, guesses, random.choice(self.clues_dict)


class FieldOperative:
	def __init__(self, color, board):
		self.color = color
		self.board = board

	def random_guess(self, clue, num_guesses):
		guesses = random.sample(self.board.spaces, num_guesses)
		guess_confidence = {}
		for guess in guesses:
			guess_confidence[guess] = 1 / (1 + math.exp(-random.gauss(.5, 1)))
		good_guesses = [(guess, guess_confidence[guess]) for guess in guesses if guess_confidence[guess] > 0.5]
		good_guesses.sort(key=lambda x: x[1], reverse=True)
		return good_guesses


if __name__ == '__main__':
	main()
