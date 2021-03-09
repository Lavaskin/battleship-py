from classes.square import *

# Info about a given board
class Board:
	board = []
	ships = 5
	size = 0

	# Fill board with water
	def __init__(self, size):
		self.size = size

		for i in range(0, size):
			self.board.append([])
			for j in range(0, size):
				self.board[i].append(Square.water)
	#END __init__()

	# Determines if coords are on the board
	def inBounds(self, x, y):
		return True if x > -1 and x < self.size and y > -1 and y < self.size else False
	#END inBounds()

	# Detects if a ship at given coords is sunk
	# Returns true if sunk, false otherwise
	def detectSink(self, x, y):
		dirs = [1, 1, 1, 1] # if we shuld traverse that direction (top right bottom left)
		ship = [(x, y)] # list of coord tuples
		iter = 1
		searching = True

		# Fill array with hits
		while searching:
			if iter == 10: return False
			# Run up
			if dirs[0] == 1 and (self.inBounds(x, y+iter)):
				# Found a piece of the ship
				if self.board[x][y+iter] == Square.hit:
					ship.append((x, y+iter))
				# Found unhit ship
				elif self.board[x][y+iter] == Square.ship:
					return False
				# Found miss
				elif self.board[x][y+iter] == Square.miss or self.board[x][y+iter] == Square.water:
					dirs[0] = 0
			elif self.inBounds(x, y+iter) == False:
				dirs[0] = 0

			# Run right
			if dirs[1] == 1 and (self.inBounds(x+iter, y)):
				# Found a piece of the ship
				if self.board[x+iter][y] == Square.hit:
					ship.append((x+iter, y))
				# Found unhit ship
				elif self.board[x+iter][y] == Square.ship:
					return False
				# Found miss
				elif self.board[x+iter][y] == Square.miss or self.board[x+iter][y] == Square.water:
					dirs[1] = 0
			elif self.inBounds(x+iter, y) == False:
				dirs[1] = 0

			# Run down
			if dirs[2] == 1 and (self.inBounds(x, y-iter)):
				# Found a piece of the ship
				if self.board[x][y-iter] == Square.hit:
					ship.append((x, y-iter))
				# Found unhit ship
				elif self.board[x][y-iter] == Square.ship:
					return False
				# Found miss
				elif self.board[x][y-iter] == Square.miss or self.board[x][y-iter] == Square.water:
					dirs[2] = 0
			elif self.inBounds(x, y-iter) == False:
				dirs[2] = 0

			# Run left
			if dirs[3] == 1 and (self.inBounds(x-iter, y)):
				# Found a piece of the ship
				if self.board[x-iter][y] == Square.hit:
					ship.append((x-iter, y))
				# Found unhit ship
				elif self.board[x-iter][y] == Square.ship:
					return False
				# Found miss
				elif self.board[x-iter][y] == Square.miss or self.board[x-iter][y] == Square.water:
					dirs[3] = 0
			elif self.inBounds(x-iter, y) == False:
				dirs[3] = 0

			# Test if dirs is all 0
			if dirs[0] == 0 and dirs[1] == 0 and dirs[2] == 0 and dirs[3] == 0:
				searching = False
			else:
				iter += 1
		#END while

		# change all hit pieces to sunk
		for i in range(0, len(ship)):
			self.board[ship[i][0]][ship[i][1]] = Square.sunk
		return True
	#END detectSink()

	# Detects what do do given other players input
	# Returns -1 for a duplicate
	# Returns  0 for a miss
	# Returns  1 for a game over (all ships down)
	# Returns  2 for a hit
	def placeMove(self, x, y):
		# Miss
		if self.board[x][y] == Square.water:
			self.board[x][y] = Square.miss
			return 0

		# Hit
		elif self.board[x][y] == Square.ship:
			self.board[x][y] = Square.hit
			if self.detectSink(x, y):
				self.ships -= 1
				return 2 if self.ships > 0 else 1

			# All ships sunk
			return 0 if self.ships > 0 else 1

		# Duplicate pick
		else: return -1
	#END placeMove()
#END class_Board