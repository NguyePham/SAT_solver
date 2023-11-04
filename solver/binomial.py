from pysat.solvers import Glucose42
from math import sqrt
from pysat.formula import CNF


def binomial(puzzle, size):

	sqrtSize = int(sqrt(size))
	cubedSize = size ** 3
	nofAuxVars = sqrtSize + sqrtSize

	print('Binomial:')
	for _ in range(size):
		print(puzzle[_])
	print('solved')


	###############################################################
	# The encoding API for Binomial Encoding
	def cellLitId(i, j, k):
		return (i * size + j) * size + k


	def getSquareId(i, j):
		return (i // sqrtSize) * sqrtSize + j // sqrtSize
	###############################################################


	###############################################################
	def encodeData(lits):
		""" Encode value of the cells """
		for i in range(size):
			for j in range(size):

				k = puzzle[i][j]
				if k > 0:
					litId = cellLitId(i, j, k)
					lits[litId] *= -1
	###############################################################


	###############################################################
	def generateLits(size):
		lits = [-i for i in range(size ** 3 + 1)]
		encodeData(lits)
		return lits
	###############################################################


	lits = generateLits(size)


	###############################################################
	def cellConstraint(i, j):
		clauses = []

		###################################
		atLeastOne = []
		# ALO clauses
		for k in range(1, size + 1):
			litId = cellLitId(i, j, k)
			atLeastOne.append(litId)

		clauses.append(atLeastOne)
		###################################

		###################################
		# AMO clauses
		for x in range(1, size):
			for y in range(x + 1, size + 1):
				clauses.append([-cellLitId(i, j, x), -cellLitId(i, j, y)])
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
		for k in range(1, size + 1):
			for x in range(size - 1):
				for y in range(x + 1, size):
					clauses.append([-cellLitId(i, x, k), -cellLitId(i, y, k)])
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
		for k in range(1, size + 1):
			for x in range(size - 1):
				for y in range(x + 1, size):
					clauses.append([-cellLitId(x, j, k), -cellLitId(y, j, k)])
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
		for k in range(1, size + 1):
			thisSquare = []
			
			for i in range(size):
				for j in range(size):

					if getSquareId(i, j) == squareId:
						litId = cellLitId(i, j, k)
						thisSquare.append(litId)

					if getSquareId(i, j) > squareId:
						break

			for x in range(size - 1):
				for y in range(x + 1, size):
					clauses.append([-thisSquare[x], -thisSquare[y]])
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
