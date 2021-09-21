import numpy as np

board = [[0] * 25 for _ in range(25)]
for i in range(25):
    board[i][i] = 'Q'

for r in board:
    print(r)
print('----------------------')
board = np.array(board)
for r in board:
    print(r)
