import pygame
from pygame.locals import *
from classes.board import *
from classes.square import *

BOARD_SIZE = 8
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


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
p1 = Board(BOARD_SIZE)
p1.board = b1
p2 = Board(BOARD_SIZE)
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