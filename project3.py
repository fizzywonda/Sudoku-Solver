import sys


class Sudoku:
	"""
		Sudoku class, which models a Sudoku game.

		Based on Peter Norvig's Suggested Sudoku setup
	"""

	def __init__(self):
		"""
			Initialize digits, rows, columns, the grid, squares, units, peers, and values.
		"""
		self.digits   = '123456789'
		self.rows     = 'ABCDEFGHI'
		self.cols     = self.digits
		self.grid     = dict()
		self.squares  = self.cross_product(self.rows, self.cols)
		unitlist = ([self.cross_product(self.rows, c) for c in self.cols] + \
					[self.cross_product(r, self.cols) for r in self.rows] + \
					[self.cross_product(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
		self.units = dict((s, [u for u in unitlist if s in u]) for s in self.squares)
		self.peers = dict((s, set(sum(self.units[s], []))-set([s])) for s in self.squares)
		self.values = dict((s, self.digits) for s in self.squares)

	@staticmethod
	def cross_product(A, B):
		"""
			Return the cross product of A and B
		"""
		return [a+b for a in A for b in B]

	def __str__(self):
		"""
			Convert the grid into a human-readable string
		"""
		output = ''
		width = 2 + max(len(self.grid[s]) for s in self.squares)
		line = '+'.join(['-' * (width * 3)] * 3)
		for r in self.rows:
			output += (''.join((self.grid[r+c] if self.grid[r+c] not in '0.' else '').center(width)+('|' if c in '36' else '') for c in self.digits)) + "\n"
			if r in 'CF': output += line + "\n"
		return output

	def load_file(self, filename):
		"""
			Load the file into the grid dictionary. Note that keys
			are in the form '[A-I][1-9]' (e.g., 'E5').
		"""
		with open(filename) as f:
			grid = ''.join(f.readlines())
		grid_values = self.grid_values(grid)
		self.grid = grid_values
		print(self.grid)

	def grid_values(self, grid):
		"""
			Convert grid into a dict of {square: char} with '0' or '.' for empties.
		"""
		chars = [c for c in grid if c in self.digits or c in '0.']
		assert len(chars) == 81
		return dict(zip(self.squares, chars))

	def solve(self):
		"""
			Solve the problem by propagation and backtracking.
		"""
		self.search(self.propagate())

	def propagate(self):
		"""
			TODO: Code the Constraint Propagation Technique Here
		"""
		for square, digit in self.grid.items():
			if digit in self.digits:
				# get the other values in square's domain self.values[square]
				other_values = [val for val in self.values[square] if val != digit]
				for value in other_values:
					self.eliminate(value, square)
		return True

	def eliminate(self, value, square):
		if value in self.values[square]:
			self.values[square] = self.values[square].replace(value, '')
			if len(self.values[square]) == 1:
				self.grid[square] = self.values[square]
				for i in self.peers[square]:
					self.eliminate(self.values[square], i)

		return self.values

	def issolved(self):
		for i in self.grid.values():
			if i not in self.digits:
				return False

		return True

	def iseligible(self, square, val):
		for i in self.peers[square]:
			if val == self.grid[i]:
				return False

		return True

	def search(self, values):
		"""
			TODO: Code the Backtracking Search Technique Here
		"""

		'''
				Recursive version of the backtracking search
			'''
		if self.issolved():
			return True
		else:
			# get all the empty squares sorted in order of smallest possible values
			empty = {sq: val for sq, val in self.values.items() if len(val) > 1}
			empty_sort = sorted(empty, key=lambda x: len(empty[x]))
			lowest = empty_sort[0]
			temp = self.grid[lowest]
			temp_val = self.values[lowest]
			for i in self.values[lowest]:
				if self.iseligible(lowest, i):
					self.grid[lowest] = i
					self.values[lowest] = i
					if self.search(self.grid):
						return True
					self.grid[lowest] = temp
					self.values[lowest] = temp_val

		return False





def main():
	s = Sudoku()
	'''
		The loop reads in as many files as you've passed on the command line.
		Example to read two easy files from the command line:
			python project3.py sudoku_easy1.txt sudoku_easy2.txt
	'''
	for x in range(1,len(sys.argv)):
		s.load_file(sys.argv[x])
		print("\n==============================================")
		print(sys.argv[x].center(46))
		print("==============================================\n")
		print(s)
		print("\n----------------------------------------------\n")
		s.solve()
		print(s)

main()
