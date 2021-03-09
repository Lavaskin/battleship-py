import pygame
from pygame.locals import *


BOARD_SIZE = 8
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


# Enum for board piece
class Square:
	# water = 0
	# miss  = 1
	# ship  = 2
	# hit   = 3
	# sunk  = 4
	water = '~'
	miss  = '.'
	ship  = 'S'
	hit   = 'H'
	sunk  = 'x'
#END class_Square

b1 = [[Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water],
	  [Square.ship, Square.water,Square.ship, Square.ship, Square.ship, Square.ship, Square.ship, Square.water],
	  [Square.ship, Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water],
	  [Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water],
	  [Square.ship, Square.water,Square.water,Square.ship, Square.water,Square.water,Square.ship, Square.water],
	  [Square.ship, Square.water,Square.water,Square.ship, Square.water,Square.water,Square.ship, Square.water],
	  [Square.ship, Square.water,Square.water,Square.ship, Square.water,Square.water,Square.ship, Square.water],
	  [Square.water,Square.water,Square.water,Square.ship, Square.water,Square.water,Square.water,Square.water]]

b2 = [[Square.water, Square.ship,Square.water, Square.water, Square.water, Square.water, Square.water, Square.water],
	  [Square.water, Square.hit,Square.water, Square.water, Square.water, Square.water, Square.ship,Square.water],
	  [Square.water, Square.hit,Square.water, Square.water, Square.water, Square.water, Square.ship,Square.water],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water],
	  [Square.ship,Square.ship,Square.ship,Square.ship,Square.water, Square.water, Square.water, Square.water],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.ship],
	  [Square.ship,Square.ship,Square.ship,Square.ship,Square.ship,Square.water, Square.water, Square.ship],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.ship]]


# Info about a given board
class Board:
	board = []
	ships = 5

	# Fill board with water
	def __init__(self):
		for i in range(0, BOARD_SIZE):
			self.board.append([])
			for j in range(0, BOARD_SIZE):
				self.board[i].append(Square.water)
	#END __init__()

	# Determines if coords are on the board
	def inBounds(self, x, y):
		return True if x > -1 and x < BOARD_SIZE and y > -1 and y < BOARD_SIZE else False
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
		print("SUNK SHIP: ", ship)
		return True
	#END detectSink()

	# Detects what do do given other players input
	# Returns -1 for a duplicate
	# Returns 1 for a game over (all ships down)
	# Returns 0 otherwise
	def placeMove(self, x, y):
		# Miss
		if self.board[x][y] == Square.water:
			self.board[x][y] = Square.miss
			return 0

		# Hit
		elif self.board[x][y] == Square.ship:
			print("HIT")
			self.board[x][y] = Square.hit
			if self.detectSink(x, y):
				self.ships -= 1

			# All ships sunk
			return 0 if self.ships > 0 else 1

		# Duplicate pick
		else: return -1
	#END placeMove()
#END class_Board


# Prints player boards to the console
def drawBoardsConsole(board1, board2):
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			print(board1.board[i][j], end=" ")
		print(" |  ", end="")
		for k in range(0, BOARD_SIZE):
			print(board2.board[i][k], end=" ")
		print("") # make an endl
#END drawBoardsConsole()

# Does a player move using opponents board
# Returns true if the game is over
def doMove(player):
	while True:
		x = int(input("Enter x: "))
		y = int(input("Enter y: "))
		if x > -1 and x < BOARD_SIZE and y > -1 and y < BOARD_SIZE:
			ret = player.placeMove(x, y)

			if ret == 1: return True    # end of game
			elif ret == 0: return False # Valid move
#END doMove()


ongoing = True
p1 = Board()
p1.board = b1
p2 = Board()
p2.board = b2

# main loop
while ongoing:
	print("P1's Turn ==========")
	drawBoardsConsole(p1, p2)
	if doMove(p2) == True:
		ongoing = False
		print("Player 1 wins!")

	else:
		print("\nP2's Turn ==========")
		drawBoardsConsole(p1, p2)
		if doMove(p1) == True:
			ongoing = False
			print("Player 1 wins!")
#END while