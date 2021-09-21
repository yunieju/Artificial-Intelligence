import numpy as np
import random

class State:
    def __init__(self, state, fval, path):
        self.state = state
        self.fval = fval
        self.path = path

class RandomStartSolver():
    def __init__(self, k):
        # number of random restarts
        self.k = k
        self.minState = State(None, float('inf'), [])
        # self.minFval = float('inf')
        # self.minState = []
        self.movecnt= []

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

        return State(board, total // 2, [])

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

    def solvePuzzle(self):
        for i in range(self.k):
            initial = self.initialize()
            curr = initial
            while True:
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
                    self.movecnt.append(len(curr.path)+ 1)
                    if self.minState.fval > curr.fval:
                        # self.minState = curr.state
                        self.minState = State(curr.state, curr.fval, curr.path + [curr])
                    # else - just don't update the minState
                    break

                state = curr.state
                for i in range(len(curr.state)):
                    if state[i][sy] == 'Q':
                        (nr, ny) = (i, sy)
                        break

                # move a queen
                state[sx][sy], state[nr][ny] = state[nr][ny], state[sx][sy]
                # curr = neighbor
                curr = State(state, sBoard[sx][sy], curr.path + [curr])

        return self.minState

    # print a path of solution
    def processSol(self, sol):
        for m in sol.path:
            print('Fval', m.fval)
            for row in m.state:
                print(row)
            print('------------------------------------------------------------------------')
        print(self.movecnt)
        print("Average the number of moves took - ", sum(self.movecnt) / len(self.movecnt))
        print("Process completed, the number of states visited - ", len(sol.path))


randomSolver = RandomStartSolver(10)
solution = randomSolver.solvePuzzle()
randomSolver.processSol(solution)