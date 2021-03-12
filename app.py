import pygame
import sys
from pygame.locals import *
from classes.board import *
from classes.square import *
from functions.console import *

BOARD_SIZE = 8
b1 = [[Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water],
	  [Square.ship, Square.water,Square.ship, Square.ship, Square.ship, Square.ship, Square.ship, Square.water],
	  [Square.ship, Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water],
	  [Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water,Square.water],
	  [Square.ship, Square.water,Square.water,Square.ship, Square.water,Square.water,Square.ship, Square.water],
	  [Square.ship, Square.water,Square.water,Square.ship, Square.water,Square.water,Square.ship, Square.water],
	  [Square.ship, Square.water,Square.water,Square.ship, Square.water,Square.water,Square.ship, Square.water],
	  [Square.water,Square.water,Square.water,Square.ship, Square.water,Square.water,Square.water,Square.water]]
b2 = [[Square.water, Square.ship,Square.water, Square.water, Square.water, Square.water, Square.water, Square.water],
	  [Square.water, Square.ship,Square.water, Square.water, Square.water, Square.water, Square.ship,Square.water],
	  [Square.water, Square.ship,Square.water, Square.water, Square.water, Square.water, Square.ship,Square.water],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water],
	  [Square.ship,Square.ship,Square.ship,Square.ship,Square.water, Square.water, Square.water, Square.water],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.ship],
	  [Square.ship,Square.ship,Square.ship,Square.ship,Square.ship,Square.water, Square.water, Square.ship],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.ship]]


#####################
# Drawing Functions #
#####################

# Returns the margin of screenspace to not be used for game objects
def getPadding():
	return ((screen.get_width() + screen.get_height()) / 2) * 0.03
#END getPadding()

# Returns the current width/height of squares given screen dimensions and board size
def getSquareDimensions():
	squareWidth  = int(((screen.get_width()  - (getPadding() * 3)) / BOARD_SIZE) / 2)
	squareHeight = int(((screen.get_height() - (getPadding() * 2)) / BOARD_SIZE))
	return squareWidth, squareHeight
#END getSquareDimensions()

# Draws an arrow over the current players board
def drawPlayerIndicator(turn):
	# Figure out coords for drawing and size
	halfBoard = (BOARD_SIZE * getSquareDimensions()[0]) / 2
	x = getPadding() + halfBoard
	y = getPadding() * 0.5
	if turn == 1: x += BOARD_SIZE * getSquareDimensions()[0] + getPadding()

	pygame.draw.circle(screen, (100, 0, 0), (x, y), int((getPadding() / 2)) * 0.5)
#END drawPlayerIndicator()

# Draws a colored square given coords
def drawSquare(screen, x, y, width, height, square):
	color = (255, 255, 255)
	# Set color based on square type
	if square == Square.water:
		color = (0, 30, 255)
	elif square == Square.ship:
		color = (100, 100, 100)
	elif square == Square.hit:
		color = (255, 80, 0)
	elif square == Square.sunk:
		color = (100, 0, 0)
	elif square == Square.miss:
		color = (0, 30, 100)
	
	rect = pygame.Rect(x, y, width, height)
	pygame.draw.rect(screen, color, rect)
#END drawSquare()

# Draws both boards on the screen
def drawBoards(board1, board2):
	padding = ((screen.get_width() + screen.get_height()) / 2) * 0.03
	squareWidth, squareHeight = getSquareDimensions()

	xOff = (BOARD_SIZE * squareWidth) + padding
	x, y = padding, padding

	# Draw boards
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			drawSquare(screen, x, y, squareWidth, squareHeight, board1[i][j])
			drawSquare(screen, x + xOff, y, squareWidth, squareHeight, board2[i][j])
			x += squareWidth
		y += squareHeight
		x = padding
	#END for
#END drawBoards()


##################
# Game Functions #
##################

# Lets the users pick where to place their ships
def placeShips(board):
	pass
#END placeShips()

# Returns a tuple of indexes representing which square was clicked
def coordToSquare(x, y, turn):
	padding = getPadding()

	# Determine indexes by rounding divided coords
	i = 0
	if turn == 0:
		i = int(((x - ((padding * 2) + (getSquareDimensions()[0]) * BOARD_SIZE)) / ((screen.get_width() / 2) - (padding * 1.5))) * BOARD_SIZE)
	else:
		i = int(((x - padding) / ((screen.get_width() / 2) - (padding * 1.5))) * BOARD_SIZE)
	
	j = int(((y - padding) / (screen.get_height() - (padding * 2))) * BOARD_SIZE)

	return j, i
#END coordToSquare()

# Lets the player select a square to shoot
# Returns -1 for a duplicate
# Returns  0 for a miss
# Returns  1 for a game over (all ships down)
# Returns  2 for a hit
def doMove(player, turn):
	squareWidth, squareHeight = getSquareDimensions()
	padding = getPadding()

	if pygame.mouse.get_pressed()[0] == True:
		x, y = pygame.mouse.get_pos()

		# Player 2's turn works by clicking on player 1's board
		if turn == 1:
			if x > padding and x < (squareWidth * BOARD_SIZE) + padding and y > padding and y < screen.get_height() - padding:
				i, j = coordToSquare(x, y, turn)
				return player.placeMove(i, j)
			else:
				return -1

		# Player 1's turn works by clicking on player 2's board
		else:
			if x > (padding * 2) + (BOARD_SIZE * squareWidth) and x < screen.get_width() - padding and y > padding and y < screen.get_height() - padding:
				i, j = coordToSquare(x, y, turn)
				return player.placeMove(i, j)
			else:
				return -1
	#END if
#END doMove()

# main game loop, iterates through each players turns until one player beats the other
def runGame():
	ongoing = True
	state = 2 # 0 = Place pieces p1, 1 = Place pieces p2, 2 = Main game loop
	turn = 0

	while ongoing:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.fill((20, 20, 20))
		drawBoards(p1.board, p2.board)
		drawPlayerIndicator(turn)

		# run through game states
		if state == 0:
			pass
		elif state == 1:
			pass
		else:
			# Do a move and verify if the turn increments given the result
			ret = -1
			if turn == 0:
				ret = doMove(p2, turn)
			elif turn == 1:
				ret = doMove(p1, turn)
			
			# Returns -1 for a duplicate
			# Returns  0 for a miss
			# Returns  1 for a game over (all ships down)
			# Returns  2 for a hit

			# Process the result
			if ret == 0: # Miss
				turn = (turn + 1) % 2
			elif ret == 1: # Game over
				print("Player " + str(turn + 1) + " wins!")
				pygame.quit()
				sys.exit()

		pygame.display.update()
	#END while
#END runGame()


p1 = Board(BOARD_SIZE)
p1.board = b1
p2 = Board(BOARD_SIZE)
p2.board = b2

pygame.init()
pygame.display.set_caption("Pygame Battleship")
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

runGame()