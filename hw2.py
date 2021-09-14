import copy

'''
empty block -> 0
blackhole -> -1
h(s) - Manhattan distance (i.e. sum of the distances of the tiles from their goal states(1~20))
'''
class State:
    def __init__(self, state, fval, gval, prev):
        self.state = state
        self.fval = fval
        self.gval = gval
        # previous state, where it came from
        self.prev = prev

    # compare state based on fval
    def __lt__(self, other):
        return self.fval <= other.fval

class Puzzle:
    def __init__(self, goal):
        self.goal = goal
        # a list of states we explored(seen)
        self.seen = []
        # a priority queue sorted by state.fval
        self.open = []
        self.closed = []

    def findAllNext(self, curr):
        # we can move an empty block to Up, Down, Left, Right
        # We can not swap an empty block with blackhole
        successors = []
        state = curr.state
        hval = self.findDistance(state)
        # empty block is represented as 0
        x, y = self.findNumber(state, 0)
        delta = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for dx, dy in delta:
            nx = x + dx
            ny = y + dy
            # out of the boundary case or blackhole
            if nx < 0 or ny < 0 or nx >= 5 or ny >= 5 or state[nx][ny] == -1:
                continue
            succs = copy.deepcopy(state)
            succs[x][y], succs[nx][ny] = succs[nx][ny], succs[x][y]
            # Append it as State instance
            successors.append(State(succs, hval + curr.gval + 1, curr.gval + 1, curr))

            if succs not in self.seen:
                self.seen.append(succs)
        return successors

    def checkOpen(self, currentState):
        for s in self.open:
            if s.state == currentState.state:
                return s
        return None

    def checkClose(self, currentState):
        for s in self.closed:
            if s.state == currentState.state:
                return s
        return None

    def findDistance(self, curr):
        total = 0
        for num in range(1, 21):
            currR, currC = self.findNumber(curr, num)
            goalR, goalC = self.findNumber(self.goal, num)
            dist = abs(goalR - currR) + abs(goalC - currC)
            total += dist
        return total

    def findNumber(self, grid, n):
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == n:
                    return (row, col)

    # TODO - Fix this part and we are done!
    def findPath(self, goal):
        print("Total steps to find a solution is ", goal.gval)
        print("The number of states we saw", len(self.closed))
        print("We saw total states", len(self.seen) + len(self.open))
        path = [goal.state]
        curr = goal
        prev = curr.prev
        while curr and prev:
            if not curr.prev:
                break
            prev = self.checkClose(curr.prev)
            path.append(prev.state)
            curr = prev
        i = 0
        for p in reversed(path):
            print('State ', i)
            i += 1
            for line in p:
                print(line)
            print('----------------------------------')

    # Take an initial state and find the solution for the given state
    def process(self, initial):
        initialH = self.findDistance(initial)
        self.open = [State(initial, initialH, 0, None)]
        self.seen.append(initial)
        while self.open:
            # pop the state with the least f value
            curr = self.open.pop(0)
            # append curr to closed
            self.closed.append(curr)
            if curr.state not in self.seen:
                self.seen.append(curr.state)

            if curr.state == self.goal:
                return self.findPath(curr)

            # find all the next available states
            successors = self.findAllNext(curr)
            for succs in successors:
                seen = self.checkOpen(succs) or self.checkClose(succs)
                if not seen:
                    self.open.append(succs)
                else:
                    if curr.gval < seen.gval:
                        # update gval in OPEN -> fval will be updated
                        if self.checkOpen(succs):
                            seen.gval = curr.gval
                        else:
                            # remove the succs from close and place it to open with a new g value
                            self.closed.remove(seen)
                            self.open.append(succs)
            self.open.sort(key= lambda x: x.fval)
        print("Search ended with no solution found!")

initialState = [
    [2,3,7,4,5],
    [1,-1,11,-1,8],
    [6,10,0,12,15],
    [9,-1,14,-1,20],
    [13,16,17,18,19]
]

goalState = [
    [1, 2, 3, 4, 5],
    [6, -1, 7, -1, 8],
    [9, 10, 0, 11, 12],
    [13, -1, 14, -1, 15],
    [16, 17, 18, 19, 20]
]

p = Puzzle(goalState)
p.process(initialState)
