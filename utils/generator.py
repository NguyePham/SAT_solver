import random
from math import sqrt
import sys
sys.path.append('/home/nguye/fm/sudoku/solver')
from product import *


###############################################################
def digHoles(puzzle):
	size = len(puzzle)
	nofHint = (size * size) // 81 * 42
	sqrtSize = int(sqrt(size))

	def canBeA(puzzle, i, j, litId):
		v = puzzle[litId // size][litId % size]
		if puzzle[i][j] == v:
			return True
		if puzzle[i][j] in range(1, size + 1):
			return False

		for k in range(size):
			if not (k == litId // size and j == litId % size) and puzzle[k][j] == v:
				return False
			if not (i == litId // size and k == litId % size) and puzzle[i][k] == v:
				return False
			if not (((litId // size) // sqrtSize) * sqrtSize + k // sqrtSize == litId // size
					and ((litId // size) % sqrtSize) * sqrtSize + k % sqrtSize == litId % size):
				if puzzle[int(((litId // size) // sqrtSize) * sqrtSize + k // sqrtSize)][int(((litId // size) % sqrtSize) * sqrtSize + k % sqrtSize)] == v:
					return False

		return True

	cells = set(range(size * size))
	unCheckeds = cells.copy()

	while len(cells) > nofHint and len(unCheckeds):
		cell = random.choice(list(unCheckeds))
		unCheckeds.discard(cell)

		row = col = square = False

		for k in range(size):
			if k != cell // size:
				if canBeA(puzzle, k, cell % size, cell):
					row = True
			if k != cell % size:
				if (canBeA(puzzle, cell // size, k, cell)):
					col = True
			if not (((cell // size) // sqrtSize) * sqrtSize + k // sqrtSize == cell // size and ((cell // size) % sqrtSize) * sqrtSize + k % sqrtSize == cell % size):
				if canBeA(puzzle, int(((cell // size) // sqrtSize) * sqrtSize + k // sqrtSize), int(((cell // size) % sqrtSize) * sqrtSize + k % sqrtSize), cell):
					square = True

		if row and col and square:
			continue
		else:
			puzzle[cell // size][cell % size] = 0
			cells.discard(cell)

	return puzzle
###############################################################


###############################################################
def generatePuzzle(size):
	puzzle = [[0] * size for i in range(size)]
	samples = set(range(1, size + 1))
	###################################
	sample = random.choice(list(samples))
	puzzle[0][0] = sample
	samples.discard(sample)
	###################################
	sample = random.choice(list(samples))
	puzzle[0][size - 1] = sample
	samples.discard(sample)
	###################################
	sample = random.choice(list(samples))
	puzzle[size - 1][0] = sample
	samples.discard(sample)
	###################################
	sample = random.choice(list(samples))
	puzzle[size - 1][size - 1] = sample
	samples.discard(sample)
	###################################
	sample = random.choice(list(samples))
	puzzle[0][size // 2] = sample
	samples.discard(sample)
	###################################
	sample = random.choice(list(samples))
	puzzle[size - 1][size // 2] = sample
	samples.discard(sample)
	###################################
	sample = random.choice(list(samples))
	puzzle[size // 2][0] = sample
	samples.discard(sample)
	###################################
	sample = random.choice(list(samples))
	puzzle[size // 2][size - 1] = sample
	samples.discard(sample)
	###################################
	product(puzzle, size)
	puzzle = digHoles(puzzle)
	return puzzle
###############################################################