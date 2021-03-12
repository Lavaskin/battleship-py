# Prints player boards to the console
def drawBoardsConsole(board1, board2, size):
	for i in range(0, size):
		for j in range(0, size):
			print(board1[i][j], end=" ")
		print(" |  ", end="")
		for k in range(0, size):
			print(board2[i][k], end=" ")
		print("") # make an endl
#END drawBoardsConsole()