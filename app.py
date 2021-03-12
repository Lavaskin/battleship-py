import pygame
import sys
from pygame.locals import *
from classes.board import *
from classes.square import *

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
	  [Square.water, Square.hit,Square.water, Square.water, Square.water, Square.water, Square.ship,Square.water],
	  [Square.water, Square.hit,Square.water, Square.water, Square.water, Square.water, Square.ship,Square.water],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water],
	  [Square.ship,Square.ship,Square.ship,Square.ship,Square.water, Square.water, Square.water, Square.water],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.ship],
	  [Square.ship,Square.ship,Square.ship,Square.ship,Square.ship,Square.water, Square.water, Square.ship],
	  [Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.water, Square.ship]]


# Lets the users pick where to place their ships
def placeShips(board):
	pass
#END placeShips()

# Draws a colored square given coords
def drawSquare(x, y, width, height, square):
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
	
	rect = pygame.Rect(x, y, width, height)
	pygame.draw.rect(screen, color, rect)
#END drawSquare()

# Draws both boards on the screen
def drawBoards(board1, board2):
	padding = ((screen.get_width() + screen.get_height()) / 2) * 0.03
	squareWidth  = int(((screen.get_width()  - (padding * 3)) / BOARD_SIZE) / 2)
	squareHeight = int(((screen.get_height() - (padding * 2)) / BOARD_SIZE))
	xOff = (BOARD_SIZE * squareWidth) + padding
	x, y = padding, padding

	# Draw boards
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			drawSquare(x, y, squareWidth, squareHeight, board1[i][j])
			drawSquare(x + xOff, y, squareWidth, squareHeight, board2[i][j])
			x += squareWidth
		y += squareHeight
		x = padding
	#END for
#END drawBoards()

# Prints player boards to the console
def drawBoardsConsole(board1, board2):
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			print(board1[i][j], end=" ")
		print(" |  ", end="")
		for k in range(0, BOARD_SIZE):
			print(board2[i][k], end=" ")
		print("") # make an endl
#END drawBoardsConsole()

# Does a player move using opponents board
# Returns true if the game is over
def doMove(player):
	drawBoardsConsole(p1, p2)
	while True:
		x = int(input("Enter x: "))
		y = int(input("Enter y: "))
		if x > -1 and x < BOARD_SIZE and y > -1 and y < BOARD_SIZE:
			ret = player.placeMove(x, y)

			if ret == 2: doMove(player)
			elif ret == 1: return True    # end of game
			elif ret == 0: return False # Valid move
#END doMove()


# Setup
ongoing = True
state = 2 # 0 = Place pieces p1, 1 = Place pieces p2, 2 = Main game loop
turn = 0

p1 = Board(BOARD_SIZE)
p1.board = b1
p2 = Board(BOARD_SIZE)
p2.board = b2

pygame.init()
pygame.display.set_caption("Pygame Battleship")
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

# main loop
while ongoing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.fill((10, 10, 10))
	drawBoards(p1.board, p2.board)

	# run through game states
	if state == 0:
		pass
	elif state == 1:
		pass
	else:
		
		turn = (turn + 1) % 2

	pygame.display.update()
#END while