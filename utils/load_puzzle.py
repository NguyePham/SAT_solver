import random
from copy import deepcopy

def extract_puzzle(raw: str):
	puzzle = []
	rows = raw.split('\n')
	for row in rows:
		puzzle.append(row.split(' '))
	return puzzle


def load_puzzle(size, cur_id=0):
	choices = set(range(1, 9))
	choices.discard(cur_id)
	file_id = random.choice(list(choices))
	file_name = 'puzzle/{0}x{0}_{1}.txt'.format(size, file_id)

	with open(file_name, 'r') as file:
		raw_puzzle = file.read()
		puzzle = extract_puzzle(raw_puzzle)
	return puzzle, file_id


def convert_to_ints(puzzle):
	puzz = deepcopy(puzzle)
	size = len(puzz) - 1

	for i in range(size):
		for j in range(size):
			puzz[i][j] = int(puzz[i][j])
	return puzz


def convert_to_strs(puzzle):
	size = len(puzzle) - 1

	for i in range(size):
		for j in range(size):
			puzzle[i][j] = str(puzzle[i][j])
	return puzzle