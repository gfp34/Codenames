from collections import namedtuple
from colorama import Fore, Back
import random

from spymaster import Spymaster, SpymasterRandom
from field_operative import FieldOperative, FieldOperativeRandom

BLANK = "BLANK"
BLUE = "BLUE"
RED = "RED"
BLACK = "BLACK"


def main():
	card_list = [card.strip() for card in open("cards.txt", 'r')]
	word_list = [word.strip() for word in open("words", 'r')]

	board = Board(card_list)
	board.print_words()

	red_spy = SpymasterRandom(RED, board, word_list)
	num_guesses, spaces, clue = red_spy.clue()
	print(num_guesses, spaces, clue)

	red_field_op = FieldOperativeRandom(RED, board)
	guesses = red_field_op.guess(clue, num_guesses)
	print(guesses)


Space = namedtuple("Space", ['color', 'word'])


class Board:
	def __init__(self, all_words):
		BOARD_SIZE = 25

		# Determine start color and randomly select board colors
		start_color = random.choice([RED, BLUE])

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


if __name__ == '__main__':
	main()
