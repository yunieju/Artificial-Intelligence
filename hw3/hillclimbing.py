import random
import numpy as np
import copy

'''
N Queen puzzle solver using Hill Climbing Search Algorithm

1. Pick initial state s
2. Pick t in neighbors(s) with lowest f(t)
3. IF f(t) >= f(s) THEN STOP, return s
4. s = t. GOTO 2
'''
class State:
    def __init__(self, state, fval):
        self.state = state
        self.fval = fval

class HCSolver:
    def __init__(self):
        # self.minFval = float('inf')
        # self.minState = []

        # a path of State, just to visualize the searching process
        self.moves = []

    def solvePuzzle(self):
        initial = self.initialize()
        curr = initial
        while True:
            self.moves.append(curr)
            sBoard = self.calculateScore(curr.state)
            sBoard = np.array(sBoard)

            # find the lowest score value
            minimum = min([min(r) for r in sBoard])
            (coordX, coordY) = np.where(sBoard == minimum)

            # if there are multiple lowest values, randomly pick one
            r = random.randrange(len(coordX))
            # pick a successor
            (sx, sy) = (coordX[r], coordY[r])

            # curr is the local optima
            if sBoard[sx][sy] >= curr.fval:
                return curr

            state = curr.state
            for i in range(len(curr.state)):
                if state[i][sy] == 'Q':
                    (nr, ny) = (i, sy)
                    break

            # move a queen
            state[sx][sy], state[nr][ny] = state[nr][ny], state[sx][sy]
            # curr = neighbor
            curr = State(state, sBoard[sx][sy])

    # randomly distribute queens on a 25*25 board
    # place a queen each column
    def initialize(self):
        board = [[0] * 25 for _ in range(25)]
        for col in range(25):
            r = random.randint(0, 24)
            # put a queen
            board[r][col] = 'Q'

        total = 0
        for c in range(len(board[0])):
            for r in range(len(board)):
                if board[r][c] == 'Q':
                    total += self.calculateConflicts(board, r, c)
                    continue

        return State(board, total // 2)

    # calculate the number of pairs of queens that are attacking each other if move a queen to (nr, nc)
    # check how many queens on the same row
    # check how many queens on the diagonal
    def calculateFval(self, board, nr, nc):
        # find the location of queen
        for r in range(len(board)):
            if board[r][nc] == 'Q':
                # original location
                (qr, qc) = (r, nc)
        # move queen to (nr, nc)
        board[nr][nc], board[qr][qc] = board[qr][qc], board[nr][nc]

        total = 0
        for c in range(len(board[0])):
            for r in range(len(board)):
                if board[r][c] == 'Q':
                    total += self.calculateConflicts(board, r, c)
                    continue

        board[nr][nc], board[qr][qc] = board[qr][qc], board[nr][nc]
        return total // 2

    # calculate the number of conflicts with block (row, col)
    def calculateConflicts(self, board, row, col):
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

    def calculateScore(self, s):
        # board contains fval of each coordinate
        sBoard = [[0]*25 for _ in range(25)]

        for r in range(len(sBoard)):
            for c in range(len(sBoard[0])):
                if s[r][c] == 'Q':
                    sBoard[r][c] = float('inf')
                else:
                    sBoard[r][c] = self.calculateFval(s, r, c)
        return sBoard

    # print a path of solution
    def processSolution(self):
        for m in self.moves:
            print('Fval', m.fval)
            for row in m.state:
                print(row)
            print('------------------------------------------------------------------------')


solver = HCSolver()
solver.solvePuzzle()
solver.processSolution()

        
    
        

