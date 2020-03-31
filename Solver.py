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
exitFlag = False


# Thread that runs the systematic recursive solver. Accesses the global exitFlag to know when to terminate.
class RS(threading.Thread):

    def run(self):
        global exitFlag
        exitFlag = recursiveSolve()


# Thread that runs the human like solver. Accesses the global exitFlag to know when to terminate.
class RSH(threading.Thread):

    def run(self):
        global exitFlag
        exitFlag = recursiveSolveHuman()


# Function determines the values not specified in the given slice of data by preforming an symmetrical difference
# on the slice of data with a list containing the values 1-9.
# Arguments
#   slice - The slice of data (e.g. row, column, or 3x3 box)
# Returns
#   List containing possible values not in the slice
def findValues(slice):
    return [element for element in range(1, 10) if element not in slice]


# Function checks whether or not the puzzle is solved by checking if any empty (0) cells remain.
# Arguments
#   puzz - Puzzle to be checked.
# Returns
#   True - If the puzzle is solved.
#   False - If the puzzle is unsolved.
def isSolved(puzz):
    return not np.isin(0, puzz)


# Function to recursively solve the puzzle. First the function checks if the puzzle has already been solved, and if
# so returns true or exits the thread. If the puzzle has not been solved then the function proceeds to find the first
# empty cell. Once the first empty cell is identified then it determines all the possible values that that individual
# cell could have. The function then loops through those values recursively calling itself. If the recursion gets stuck
# then the function resets the puzzle to its previous states and attempts the next guess.
def recursiveSolve():
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


# Function to recursively solve the puzzle. First the function checks if the puzzle has already been solved, and if
# so returns true or exits the thread. If the puzzle has not been solved, then the function proceeds to loop through
# the puzzle to determine how many valid guesses there are for each cell. It then picks the cell with the minimum
# number of guesses. The function then loops through those guess recursively calling itself. If the recursion gets stuck
# then the function resets the puzzle to its previous states and attempts the next guess.
def recursiveSolveHuman():
    global puzzle2
    global exitFlag

    if exitFlag:
        sys.exit()

    if isSolved(puzzle2):
        return True

    guessesPerCell = []
    for i in range(0, 9):
        for j in range(0, 9):
            idxrow = i / 3 * 3
            idxcol = j / 3 * 3
            if puzzle2[i][j] == 0:
                guessesPerCell.append(len(list(reduce(np.intersect1d, (findValues(puzzle2[i, :]), findValues(puzzle2[:, j]), findValues(puzzle2[idxrow:idxrow + 3, idxcol:idxcol + 3]))))))
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


solutionTimes = []
puzzleFiles = os.listdir('Permutations/')
solvers = [0, 0]

# Solve each puzzle in the Puzzle directory.
for puzzleFile in puzzleFiles:
    with open('Permutations/' + puzzleFile, 'r') as f:
        lines = f.readlines()
        puzzleArray = []
        for line in lines:
            row = [int(val) for val in str(line).strip()]
            puzzleArray.append(row)

    puzzle = np.array(puzzleArray)
    # Make copies of the puzzles so that the threads do not try to edit the same puzzle.
    puzzle1 = copy.deepcopy(puzzle)
    puzzle2 = copy.deepcopy(puzzle)
    threadRS = RS()
    threadRSH = RSH()
    exitFlag = False
    start = time.time()
    # Start the race.
    threadRSH.start()
    threadRS.start()
    # Wait until both threads exit. Presumably one with the solution and the other with an exception since the puzzle
    # was solved by the other thread.
    while threading.active_count() > 1:
        continue
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
    with open('Solutions/' + puzzleFile.replace('.txt', '_SOLUTION.txt'), 'w') as f:
        if not isSolved(puzzle):
            f.write('No Solution Found')
        else:
            puzzleString = np.array_str(puzzle).replace('[[', '').replace(']', '').replace(' [', '')
            f.write(puzzleString)
        f.write('\nDuration: ' + str(processtime))
        f.write(solver)

# Print some basic statistics and plot the results as bar graphs.
print 'Puzzle ' + str(solutionTimes.index(max(solutionTimes)) + 1) + ' took the longest to solve, ' + str(max(solutionTimes)) + ' seconds.'
print 'Puzzle ' + str(solutionTimes.index(min(solutionTimes)) + 1) + ' took the shortest to solve, ' + str(min(solutionTimes)) + ' seconds.'
print list(solvers)

solutionTimes = np.array([round(i) for i in solutionTimes])
fig, ax = plt.subplots(1, 2, sharey=True, constrained_layout=True)
fig.suptitle('Solver Statistics')
labels, counts = np.unique(solutionTimes, return_counts=True)
ax[0].bar(labels, counts, align='center', color='plum')
ax[1].set_xticks(labels)
ax[0].set_xlabel('Binned Computation Time (seconds)')
ax[0].set_ylabel('Number of Puzzles')
ax[1].yaxis.set_tick_params(which='both', labelleft=True)


objects = ('Recursive Solve', 'Human Recursive\n Solve')
y_pos = np.arange(len(objects))

ax[1].bar(y_pos, solvers, align='center', color='plum')
ax[1].set_xticks((0, 1))
ax[1].set_xticklabels(objects)
plt.show()
