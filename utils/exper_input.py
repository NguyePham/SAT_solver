from generator import *
from copy import deepcopy
import time

size = 25

for _ in range(1, 9):
	puzzle = generatePuzzle(size)
	tmpPuzzle = deepcopy(puzzle)

	start = time.perf_counter()
	product(tmpPuzzle, size)
	end = time.perf_counter()
	solve_time = end - start
	print(solve_time)

	file_name = 'puzzle/{0}x{0}_{1}.txt'.format(size, _)
	with open(file_name, 'w') as raw_puzzle:
		for i in range(size):
			for j in range(size):
				raw_puzzle.write(str(puzzle[i][j]) + ' ')
			raw_puzzle.write('\n')
