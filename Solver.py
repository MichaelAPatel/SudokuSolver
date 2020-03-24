import numpy as np
import copy
import os
import sys
import time
import matplotlib
import threading
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

puzzle = np.empty((9, 9))
puzzle1 = np.empty((9, 9))
puzzle2 = np.empty((9, 9))
puzzle3 = np.empty((9, 9))
puzzle4 = np.empty((9, 9))
exitFlag = False


class RS(threading.Thread):

    def run(self):
        global exitFlag
        exitFlag = recursiveSolve()


class RSB(threading.Thread):

    def run(self):
        global exitFlag
        exitFlag = recursiveSolveBackward()


class RSH(threading.Thread):

    def run(self):
        global exitFlag
        exitFlag = recursiveSolveHuman()


class RSHB(threading.Thread):

    def run(self):
        global exitFlag
        exitFlag = recursiveSolveHumanBackward()


# Function determines the values not specified in the given slice of data by preforming an symmetrical difference
# on the slice of data with a list containing the values 1-9.
# Arguments
#   slice - The slice of data (e.g. row, column, or 3x3 box)
# Returns
#   List containing possible values not in the slice
def findValues(slice):
    return [element for element in range(1, 10) if element not in slice]


# Function checks whether or not the puzzle is solved by checking if any empty (0) cells remain.
# Returns
#   True - If the puzzle is solved.
#   False - If the puzzle is unsolved.
def isSolved(puzz):
    return not np.isin(0, puzz)


def writeSolution(puzz):
    global puzzle
    puzzle = copy.deepcopy(puzz)

# Function to recursively solve the puzzle. First the function checks if the puzzle has already been solved, and if
# so returns true. If the puzzle has not been solved then the function proceeds to find the first empty cell. Once
# once the first empty cell is identified then it determines all the possible values that that individual cell could
# have. The function then loops through those values recursively calling itself. If the recursion gets stuck then the
# function resets the puzzle to its previous states and attempts the next guess.
def recursiveSolve(order='forward'):
    # The puzzle must be defined globally here so that this function can both access it AND make changes to it as
    # by default python functions can access variables outside their scope but they are immutable.
    global puzzle1
    global exitFlag

    if exitFlag:
        sys.exit()

    if isSolved(puzzle1):
        return True

    emptyCells = np.where(puzzle1 == 0)
    firstCell = list(zip(emptyCells[0], emptyCells[1]))[0]
    i, j = firstCell
    idxrow = i / 3 * 3
    idxcol = j / 3 * 3

    guesses = list(reduce(np.intersect1d, (findValues(puzzle1[i, :]), findValues(puzzle1[:, j]), findValues(puzzle1[idxrow:idxrow + 3, idxcol:idxcol + 3]))))
    if len(guesses) == 0:
        return False

    for guess in guesses:
        prePuzzle = copy.deepcopy(puzzle1)
        puzzle1[i][j] = guess
        result = recursiveSolve()
        if result:
            return True
        else:
            puzzle1 = copy.deepcopy(prePuzzle)
    return False

def recursiveSolveBackward():
    # The puzzle must be defined globally here so that this function can both access it AND make changes to it as
    # by default python functions can access variables outside their scope but they are immutable.
    global puzzle3
    global exitFlag

    if exitFlag:
        sys.exit()

    if isSolved(puzzle3):
        return True

    emptyCells = np.where(puzzle3 == 0)
    firstCell = list(zip(emptyCells[0], emptyCells[1]))[0]
    i, j = firstCell
    idxrow = i / 3 * 3
    idxcol = j / 3 * 3

    guesses = list(reduce(np.intersect1d, (findValues(puzzle3[i, :]), findValues(puzzle3[:, j]), findValues(puzzle3[idxrow:idxrow + 3, idxcol:idxcol + 3]))))
    guesses.reverse()
    if len(guesses) == 0:
        return False

    for guess in guesses:
        prePuzzle = copy.deepcopy(puzzle3)
        puzzle3[i][j] = guess
        result = recursiveSolveBackward()
        if result:
            return True
        else:
            puzzle3 = copy.deepcopy(prePuzzle)
    return False


def recursiveSolveHuman():
    # The puzzle must be defined globally here so that this function can both access it AND make changes to it as
    # by default python functions can access variables outside their scope but they are immutable.
    global puzzle2
    global exitFlag

    if isSolved(puzzle2):
        return True

    guessesPerCell = []
    for i in range(0,9):
        for j in range(0,9):
            idxrow = i / 3 * 3
            idxcol = j / 3 * 3
            if puzzle2[i][j] == 0:
                guessesPerCell.append(len(list(reduce(np.intersect1d, (findValues(puzzle2[i, :]), findValues(puzzle2[:, j]),findValues(puzzle2[idxrow:idxrow + 3, idxcol:idxcol + 3]))))))
            else:
                guessesPerCell.append(100)

    i = guessesPerCell.index(min(guessesPerCell)) / 9
    j = guessesPerCell.index(min(guessesPerCell)) % 9
    idxrow = i / 3 * 3
    idxcol = j / 3 * 3
    guesses = list(reduce(np.intersect1d, (findValues(puzzle2[i, :]), findValues(puzzle2[:, j]), findValues(puzzle2[idxrow:idxrow + 3, idxcol:idxcol + 3]))))
    if len(guesses) == 0:
        return False

    for guess in guesses:
        prePuzzle = copy.deepcopy(puzzle2)
        puzzle2[i][j] = guess
        result = recursiveSolveHuman()
        if result:
            return True
        else:
            puzzle2 = copy.deepcopy(prePuzzle)
    return False


def recursiveSolveHumanBackward():
    # The puzzle must be defined globally here so that this function can both access it AND make changes to it as
    # by default python functions can access variables outside their scope but they are immutable.
    global puzzle4
    global exitFlag

    if isSolved(puzzle4):
        return True

    guessesPerCell = []
    for i in range(0, 9):
        for j in range(0, 9):
            idxrow = i / 3 * 3
            idxcol = j / 3 * 3
            if puzzle4[i][j] == 0:
                guessesPerCell.append(len(list(reduce(np.intersect1d, (
                findValues(puzzle4[i, :]), findValues(puzzle4[:, j]),
                findValues(puzzle4[idxrow:idxrow + 3, idxcol:idxcol + 3]))))))
            else:
                guessesPerCell.append(100)

    i = guessesPerCell.index(min(guessesPerCell)) / 9
    j = guessesPerCell.index(min(guessesPerCell)) % 9
    idxrow = i / 3 * 3
    idxcol = j / 3 * 3
    guesses = list(reduce(np.intersect1d, (findValues(puzzle4[i, :]), findValues(puzzle4[:, j]), findValues(puzzle4[idxrow:idxrow + 3, idxcol:idxcol + 3]))))
    guesses.reverse()
    if len(guesses) == 0:
        return False

    for guess in guesses:
        prePuzzle = copy.deepcopy(puzzle4)
        puzzle4[i][j] = guess
        result = recursiveSolveHumanBackward()
        if result:
            return True
        else:
            puzzle4 = copy.deepcopy(prePuzzle)
    return False

solutionTimes = []
puzzleFiles = os.listdir('Puzzles/')
solvers = [0, 0, 0, 0]

# Solve each puzzle in the Puzzle directory.
for puzzleFile in puzzleFiles:
    with open('Puzzles/' + puzzleFile, 'r') as f:
        lines = f.readlines()
        puzzleArray = []
        for line in lines:
            row = [int(val) for val in str(line).strip()]
            puzzleArray.append(row)

    puzzle = np.array(puzzleArray)
    puzzle1 = copy.deepcopy(puzzle)
    puzzle2 = copy.deepcopy(puzzle)
    puzzle3 = copy.deepcopy(puzzle)
    puzzle4 = copy.deepcopy(puzzle)
    threadRS = RS()
    threadRSH = RSH()
    threadRSB = RSB()
    threadRSHB = RSHB()
    exitFlag = False
    start = time.time()
    threadRS.start()
    threadRSH.start()
    threadRSB.start()
    threadRSHB.start()
    threadRS.join()
    threadRSH.join()
    threadRSB.join()
    threadRSHB.join()
    processtime = time.time() - start
    solutionTimes.append(processtime)
    solver = ''
    if isSolved(puzzle1):
        puzzle = copy.deepcopy(puzzle1)
        solver = '\nPure Recursive'
        solvers[0] += 1
    elif isSolved(puzzle2):
        puzzle = copy.deepcopy(puzzle2)
        solver = '\nHuman Recursive'
        solvers[1] += 1
    elif isSolved(puzzle3):
        puzzle = copy.deepcopy(puzzle3)
        solver = '\nPure Recursive Backward'
        solvers[3] += 1
    elif isSolved(puzzle4):
        puzzle = copy.deepcopy(puzzle4)
        solver = '\nHuman Recursive Backward'
        solvers[4] += 1

    with open('Solutions/' + puzzleFile.replace('.txt', '_SOLUTION.txt'), 'w') as f:
        if not isSolved(puzzle):
            f.write('No Solution Found')
        else:
            puzzleString = np.array_str(puzzle).replace('[[', '').replace(']', '').replace(' [', '')
            f.write(puzzleString)
        f.write('\nDuration: ' + str(processtime))
        f.write(solver)

# Print some basic statistics and plot the results as a histogram.
print 'Puzzle ' + str(solutionTimes.index(max(solutionTimes)) + 1) + ' took the longest to solve, ' + str(max(solutionTimes)) + ' seconds.'
print 'Puzzle ' + str(solutionTimes.index(min(solutionTimes)) + 1) + ' took the shortest to solve, ' + str(min(solutionTimes)) + ' seconds.'
print list(solvers)

solutionTimes = np.array([round(i) for i in solutionTimes])
plt.hist(solutionTimes)
plt.show()
