import numpy as np
import random
# find the f score when we queen on col 'nc' to (nr, nc)
def calculateFval(board, nr, nc):
    # find the location of queen
    for r in range(len(board)):
        if board[r][nc] == 'Q':
            # original location
            (qr, qc) = (r, nc)
    # move queen to (nr, nc)
    board[nr][nc] = 'Q'
    board[qr][qc] = 0

    total = 0
    i = 0
    for c in range(len(board[0])):
        for r in range(len(board)):
            if board[r][c] == 'Q':
                total += calculateConflicts(board, r, c)
                i += 1
                continue

    board[nr][nc] = 0
    board[qr][nc] = 'Q'
    return total // 2

# calculate the number of conflicts with block (row, col)
def calculateConflicts(board, row, col):
    cnt = 0
    # check rows
    for c in range(len(board[0])):
        if (row, c) != (row, col) and board[row][c] == 'Q':
            cnt += 1

    # check left diagonal (/)
    sum = row + col
    for i in range(sum + 1):
        r = i
        c = sum - i
        if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]):
            continue
        if (r, c) != (row, col) and board[r][c] == 'Q':
            cnt += 1

    # check right diagonal (\)
    (r, c) = (row - min(row, col), col - min(row, col))
    while 0 <= r < len(board) and 0 <= c < len(board[0]):
        if (row, col) != (r, c) and board[r][c] == 'Q':
            cnt += 1
        r += 1
        c += 1
    return cnt


# check this function works correctly using textbook 8 Queens example
def calculateScore(s):
    # board contains fval of each coordinate
    sBoard = [[0,0,0,0,0,0,0,0] for _ in range(8)]
    for r in range(len(sBoard)):
        for c in range(len(sBoard[0])):
            if s[r][c] == 'Q':
                sBoard[r][c] = float('inf')
            else:
                sBoard[r][c] = calculateFval(s, r, c)
    return sBoard


myBoard = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 'Q', 0, 0, 0, 0],
    ['Q', 0, 0, 0, 'Q', 0, 0, 0],
    [0, 'Q', 0, 0, 0, 'Q', 0, 'Q'],
    [0, 0, 'Q', 0, 0, 0, 'Q', 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
scoreBoard = calculateScore(myBoard)

for line in scoreBoard:
    print(line)
scoreBoard = np.array(scoreBoard)
minimum = min([min(r) for r in scoreBoard])

coordX, coordY = np.where(scoreBoard == minimum)

r = random.randrange(len(coordX))
# pick a successor
(rx, ry) = (coordX[r], coordY[r])

print(coordX[r], coordY[r])

print([[0]*8 for _ in range(8)])


