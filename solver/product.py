from pysat.solvers import Glucose42
from math import sqrt
from pysat.formula import CNF


def product(puzzle, size):

	sqrtSize = int(sqrt(size))
	cubedSize = size ** 3
	nofAuxVars = sqrtSize + sqrtSize

	print('Product:')
	for _ in range(size):
		print(puzzle[_])
	print('solved')


	###############################################################
	# The encoding API for Product Encoding
	def cellLitId(i, j, k):
		return (i * size + j) * size + k


	def getSquareId(i, j):
		return (i // sqrtSize) * sqrtSize + j // sqrtSize

	# k := {1, size}

	def cellAuxRowLitId(i, j, k):
		return cubedSize + (i * size + j) * nofAuxVars + k


	def cellAuxColLitId(i, j, k):
		return cellAuxRowLitId(i, j, k) + sqrtSize


	def rowAuxRowLitId(i, j, k):
		return cellAuxColLitId(size - 1, size - 1, sqrtSize) + (i * size + j) * nofAuxVars + k


	def rowAuxColLitId(i, j, k):
		return rowAuxRowLitId(i, j, k) + sqrtSize


	def colAuxRowLitId(i, j, k):
		return rowAuxColLitId(size - 1, size - 1, sqrtSize) + (i * size + j) * nofAuxVars + k


	def colAuxColLitId(i, j, k):
		return colAuxRowLitId(i, j, k) + sqrtSize


	def squareAuxRowLitId(i, j, k):
		return colAuxColLitId(size - 1, size - 1, sqrtSize) + (i * size + j) * nofAuxVars + k


	def squareAuxColLitId(i, j, k):
		return squareAuxRowLitId(i, j, k) + sqrtSize
	###############################################################


	###############################################################
	# The encoding API for Product Encoding
	def createSquareList():
		squares = [[] for _ in range(size)]

		for i in range(size):
			for j in range(size):

				squareId = getSquareId(i, j)
				squares[squareId].append(puzzle[i][j])

		return squares
	###############################################################


	squares = createSquareList()


	###############################################################
	def encodeCellData(lits):
		""" Encode value of the cells """
		for i in range(size):
			for j in range(size):

				k = puzzle[i][j]
				if k > 0:
					litId = cellLitId(i, j, k)
					lits[litId] *= -1
	###############################################################


	###############################################################
	def encodeData(lits):
		"""
		Encode data of the initial puzzle to literals
		Method: Product encoding
		"""
		encodeCellData(lits)
		
		###################################
		# Encode value of the auxiliary variables of each cell
		# Each cell contains precisely ONE number
		for i in range(size):
			for j in range(size):

				k = puzzle[i][j]
				if (k == 0): continue
						
				rowId = (k - 1) // sqrtSize + 1
				colId = (k - 1) % sqrtSize + 1

				lits[cellAuxRowLitId(i, j, rowId)] *= -1
				lits[cellAuxColLitId(i, j, colId)] *= -1
		###################################

		###################################
		# Encode value of the auxiliary variables of each row
		# Each number appears precisely ONCE in each row
		for i in range(size):
			for k in range(size):
				for j in range(size):
					
					if puzzle[i][j] == k + 1:

						rowId = j // sqrtSize + 1
						colId = j % sqrtSize + 1

						lits[rowAuxRowLitId(i, k, rowId)] *= -1
						lits[rowAuxColLitId(i, k, colId)] *= -1

						break
		###################################

		###################################
		# Encode value of the auxiliary variables of each column
		# Each number appears precisely ONCE in each column
		for j in range(size):
			for k in range(size):
				for i in range(size):
					
					if puzzle[i][j] == k + 1:

						rowId = i // sqrtSize + 1
						colId = i % sqrtSize + 1

						lits[colAuxRowLitId(j, k, rowId)] *= -1
						lits[colAuxColLitId(j, k, colId)] *= -1

						break
		###################################
		
		###################################
		# Encode value of the auxiliary variables of each square
		# Each number appears precisely ONCE in each square
		for squareId in range(size):
			for k in range(size):
				for _ in range(size):

					if squares[squareId][_] == k + 1:

						rowId = _ // sqrtSize + 1
						colId = _ % sqrtSize + 1

						lits[squareAuxRowLitId(squareId, k, rowId)] *= -1
						lits[squareAuxColLitId(squareId, k, colId)] *= -1

						break
		###################################
	###############################################################


	###############################################################
	def generateLits(size):
		lits = [-i for i in range(int(cubedSize + 4 * size * size * nofAuxVars) + 1)]
		encodeData(lits)
		return lits
	###############################################################


	lits = generateLits(size)


	###############################################################
	def cellConstraint(i, j):
		clauses = []

		###################################
		atLeastOne = []
		# ALO clause
		for k in range(1, size + 1):
			litId = cellLitId(i, j, k)
			atLeastOne.append(litId)

		clauses.append(atLeastOne)
		###################################

		###################################
		# AMO clause
		for x in range(1, sqrtSize):
			for y in range(x + 1, sqrtSize + 1): 
				clauses.append([-cellAuxRowLitId(i, j, x), -cellAuxRowLitId(i, j, y)])

		for x in range(1, sqrtSize):
			for y in range(x + 1, sqrtSize + 1): 
				clauses.append([-cellAuxColLitId(i, j, x), -cellAuxColLitId(i, j, y)])

		for k in range(1, size + 1):

			rowId = (k - 1) // sqrtSize + 1
			colId = (k - 1) % sqrtSize + 1

			clauses.append([-cellLitId(i, j, k), cellAuxRowLitId(i, j, rowId)])
			clauses.append([-cellLitId(i, j, k), cellAuxColLitId(i, j, colId)])
		###################################
		
		return clauses


	def cellsConstraint():
		clauses = []

		for i in range(size):
			for j in range(size):
				clauses += cellConstraint(i, j)

		return clauses


	def rowConstraint(i):
		clauses = []

		###################################
		# ALO clauses
		for k in range(1, size + 1):
			atLeastOne = []
			
			for j in range(size):
				litId = cellLitId(i, j, k)
				atLeastOne.append(litId)

			clauses.append(atLeastOne)
		###################################

		###################################
		# AMO clauses
		for k in range(size):

			for x in range(1, sqrtSize):
				for y in range(x + 1, sqrtSize + 1):
					clauses.append([-rowAuxRowLitId(i, k, x), -rowAuxRowLitId(i, k, y)])

			for x in range(1, sqrtSize):
				for y in range(x + 1, sqrtSize + 1):
					clauses.append([-rowAuxColLitId(i, k, x), -rowAuxColLitId(i, k, y)])

		for k in range(size):
			for j in range(size):

				rowId = j // sqrtSize + 1
				colId = j % sqrtSize + 1

				clauses.append([-cellLitId(i, j, k + 1), rowAuxRowLitId(i, k, rowId)])
				clauses.append([-cellLitId(i, j, k + 1), rowAuxColLitId(i, k, colId)])
		###################################
		
		return clauses


	def rowsConstraint():
		clauses = []

		for i in range(size):
			clauses += rowConstraint(i)

		return clauses


	def colConstraint(j):
		clauses = []

		###################################
		# ALO clauses
		for k in range(1, size + 1):
			atLeastOne = []
			
			for i in range(size):
				litId = cellLitId(i, j, k)
				atLeastOne.append(litId)

			clauses.append(atLeastOne)
		###################################

		###################################
		# AMO clauses
		for k in range(size):

			for x in range(1, sqrtSize):
				for y in range(x + 1, sqrtSize + 1):
					clauses.append([-colAuxRowLitId(j, k, x), -colAuxRowLitId(j, k, y)])

			for x in range(1, sqrtSize):
				for y in range(x + 1, sqrtSize + 1):
					clauses.append([-colAuxColLitId(j, k, x), -colAuxColLitId(j, k, y)])

		for k in range(size):
			for i in range(size):

				rowId = i // sqrtSize + 1
				colId = i % sqrtSize + 1

				clauses.append([-cellLitId(i, j, k + 1), colAuxRowLitId(j, k, rowId)])
				clauses.append([-cellLitId(i, j, k + 1), colAuxColLitId(j, k, colId)])
		###################################
		
		return clauses


	def colsConstraint():
		clauses = []

		for j in range(size):
			clauses += colConstraint(j)

		return clauses


	def squareConstraint(squareId):
		clauses = []

		###################################
		# ALO clauses
		for k in range(1, size + 1):
			atLeastOne = []
			
			for i in range(size):
				for j in range(size):

					if getSquareId(i, j) == squareId:
						litId = cellLitId(i, j, k)
						atLeastOne.append(litId)

					if getSquareId(i, j) > squareId:
						break

			clauses.append(atLeastOne)
		###################################

		###################################
		# AMO clauses
		for k in range(size):

			for x in range(1, sqrtSize):
				for y in range(x + 1, sqrtSize + 1): 
					clauses.append([-squareAuxRowLitId(squareId, k, x), -squareAuxRowLitId(squareId, k, y)])

			for x in range(1, sqrtSize):
				for y in range(x + 1, sqrtSize + 1): 
					clauses.append([-squareAuxColLitId(squareId, k, x), -squareAuxColLitId(squareId, k, y)])

		for k in range(size):
			_ = -1

			for i in range(size):
				for j in range(size):

					if squareId == getSquareId(i, j):

						_ += 1
						rowId = _ // sqrtSize + 1
						colId = _ % sqrtSize + 1

						clauses.append([-cellLitId(i, j, k + 1), squareAuxRowLitId(squareId, k , rowId)])
						clauses.append([-cellLitId(i, j, k + 1), squareAuxColLitId(squareId, k, colId)])

					if (squareId < getSquareId(i, j)):
						break
		###################################
		
		return clauses


	def squaresConstraint():
		clauses = []

		for _ in range(size):
			clauses += squareConstraint(_)

		return clauses
	###############################################################


	cellClauses = cellsConstraint()
	rowClauses = rowsConstraint()
	colClauses = colsConstraint()
	squareClauses = squaresConstraint()


	###############################################################
	def solvePuzzle():
		clauses = cellClauses + rowClauses + colClauses + squareClauses

		inputClause = CNF()
		for clause in clauses:
			inputClause.append(clause=clause)

		print('Number of variables: ' + str(inputClause.nv))
		print('Number of clauses: '  + str(len(inputClause.clauses)))

		for clause in clauses:
			inputClause.append(clause)

		with Glucose42(bootstrap_with=inputClause) as s:

			assumptions = []

			for lit in lits:
				if lit > 0: assumptions.append(lit)

			s.solve(assumptions=assumptions)
			model = s.get_model()

		solution = []

		for _ in model:
			
			if _ > cubedSize:
				break

			if _ > 0:
				solution.append(_)

		return solution, inputClause.nv, len(inputClause.clauses)
	###############################################################


	solution, nofVariables, nofClauses = solvePuzzle()


	###############################################################
	def loadSolution(solution):
		_ = 0
		for i in range(size):
			for j in range(size):
				for k in range(1, size + 1):
					if cellLitId(i, j, k) == solution[_]:

						puzzle[i][j] = k
						_ += 1

						if _ == len(solution):
							break
	###############################################################


	loadSolution(solution=solution)
	for _ in range(size):
		print(puzzle[_])

	return nofVariables, nofClauses
