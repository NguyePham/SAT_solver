import sys
sys.path.append('/home/nguye/fm/sudoku/solver')

from load_puzzle import *
from binomial import *
from product import *

from time import perf_counter

size_options = [9, 16, 25, 36]

for size in size_options:
	aggregation = open('/home/nguye/fm/start/solution/{0}x{0}_aggregation.txt'.format(size), 'w')

	aggregation.write('{0}x{0} puzzles:\n'.format(size))
	aggregation.write('==================================\n\n')

	for puzzle_id in range(1, 9):
		
		file_name = 'puzzle/{0}x{0}_{1}.txt'.format(size, puzzle_id)

		with open(file_name, 'r') as file:
			raw_puzzle = file.read()
			puzzle = extract_puzzle(raw_puzzle)

		int_puzzle = convert_to_ints(puzzle=puzzle)
		start_time = perf_counter()
		binomial_nof_variables, binomial_nof_clauses = binomial(int_puzzle, size)
		end_time = perf_counter()
		binomial_time = end_time - start_time

		
		int_puzzle = convert_to_ints(puzzle=puzzle)
		start_time = perf_counter()
		product_nof_variables, product_nof_clauses = product(int_puzzle, size)
		end_time = perf_counter()
		product_time = end_time - start_time

		puzzle = convert_to_strs(int_puzzle)

		file_name = '/home/nguye/fm/start/solution/{0}x{0}_{1}_out.txt'.format(size, puzzle_id)
		with open(file_name, 'w') as file:
			for i in range(size - 1):
				for j in range(size - 1):
					file.write(puzzle[i][j] + ' ')
				file.write('\n')
			
			file.write('\n')

			file.write('Binomial encoding:\n')
			file.write('Solving time: ' + str(binomial_time) + '\n')
			file.write('Number of variables: ' + str(binomial_nof_variables) + '\n')
			file.write('Number of clauses: ' + str(binomial_nof_clauses) + '\n')

			file.write('\n')

			file.write('Product encoding:\n')
			file.write('Solving time: ' + str(product_time) + '\n')
			file.write('Number of variables: ' + str(product_nof_variables) + '\n')
			file.write('Number of clauses: ' + str(product_nof_clauses) + '\n')

		
		aggregation.write('Puzzle {0}:\n-------------------\n'.format(puzzle_id))

		aggregation.write('Binomial encoding:\n')	
		aggregation.write('Solving time: ' + str(binomial_time) + '\n')
		aggregation.write('Number of variables: ' + str(binomial_nof_variables) + '\n')
		aggregation.write('Number of clauses: ' + str(binomial_nof_clauses) + '\n')

		aggregation.write('\n')

		aggregation.write('Product encoding:\n')
		aggregation.write('Solving time: ' + str(product_time) + '\n')
		aggregation.write('Number of variables: ' + str(product_nof_variables) + '\n')
		aggregation.write('Number of clauses: ' + str(product_nof_clauses) + '\n')

		aggregation.write('-------------------\n\n')

	aggregation.write('==================================\n')
	aggregation.close()

