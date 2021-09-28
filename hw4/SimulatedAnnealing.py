"""
1. Pick an intial state s
2. Randomly pick t in neighbors(s)
3. If f(t) is better THEN accept s <- t
4. ELSE
5. Accept s <- with a small probability
6. GOTO 2 and REPEAT

Use Boltzmann Distribution for the probability
exp(-|f(s)-f(t)|^2 / temp)

Temp goes down, every iteration
"""
import math
import numpy as np
import random
import copy


class State:
    def __init__(self, state, fval, path):
        self.state = state
        self.fval = fval
        self.path = path

class SASolver:
    def __init__(self, T):
        self.T = T

    def solvePuzzle(self):
        initial = self.initialize()
        curr = initial

        # TODO - termination condition? T < 1
        while self.T > 1:
            sBoard = self.calculateScore(curr.state)

            # randomly pick a successor
            sx = random.randrange(len(sBoard))
            sy = random.randrange(len(sBoard[0]))

            # if f(neighbor) is better than f(curr) THEN ACCEPT
            if sBoard[sx][sy] < curr.fval:
                # swap the queens and update the curr value
                state = copy.deepcopy(curr.state)
                for i in range(len(curr.state)):
                    if state[i][sy] == 'Q':
                        (nr, ny) = (i, sy)
                        break
                print('Move queen ', (sx, sy), 'to', (nr, ny))
                state[sx][sy], state[nr][ny] = state[nr][ny], state[sx][sy]
                curr = State(state, sBoard[sx][sy], curr.path + [curr])

            # neighbor is worse than current than accept with probability
            else:
                p = random.randrange(0, 100) / 100
                if p < self.getProbability(curr.fval, sBoard[sx][sy], self.T):
                    # swap the queens and update the curr value
                    state = copy.deepcopy(curr.state)
                    for i in range(len(curr.state)):
                        if state[i][sy] == 'Q':
                            (nr, ny) = (i, sy)
                            break
                    print('Move queen ', (sx, sy), 'to', (nr, ny))
                    state[sx][sy], state[nr][ny] = state[nr][ny], state[sx][sy]
                    curr = State(state, sBoard[sx][sy], curr.path + [curr])

            # cool down the temperature by 10%
            self.cooldown()
        return curr

    def getProbability(self, fs, ft, temp):
        return math.exp((pow(abs(fs - ft), 2) / temp) * -1)
    
    def cooldown(self):
        self.T *= 0.9

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

        # move queen back
        board[nr][nc], board[qr][qc] = board[qr][qc], board[nr][nc]
        return total // 2

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

    def initialize(self):
        board = [[0] * 25 for _ in range(25)]
        # put queens
        for i in range(25):
            board[i][i] = 'Q'
        total = 0
        for c in range(len(board[0])):
            for r in range(len(board)):
                if board[r][c] == 'Q':
                    total += self.calculateConflicts(board, r, c)
                    continue
        return State(board, total // 2, [])

    def processSolution(self, sol):
        print(sol)
        for m in sol.path:
            print('Fval', m.fval)
            for row in m.state:
                print(row)
            print('------------------------------------------------------------------------')
        print("Process completed, the number of states visited - ", len(sol.path))

solver = SASolver(10000000)
solution = solver.solvePuzzle()
print(solution)
solver.processSolution(solution)
