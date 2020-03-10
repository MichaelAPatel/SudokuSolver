import numpy as np
import copy
import os
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

puzzle = np.empty((9, 9))


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
def isSolved():
    return not np.isin(0, puzzle)


# Function to recursively solve the puzzle. First the function checks if the puzzle has already been solved, and if
# so returns true. If the puzzle has not been solved then the function proceeds to find the first empty cell. Once
# once the first empty cell is identified then it determines all the possible values that that individual cell could
# have. The function then loops through those values recursively calling itself. If the recursion gets stuck then the
# function resets the puzzle to its previous states and attempts the next guess.
def recursiveSolve():
    # The puzzle must be defined globally here so that this function can both access it AND make changes to it as
    # by default python functions can access variables outside their scope but they are immutable.
    global puzzle
    if isSolved():
        return True

    emptyCells = np.where(puzzle == 0)
    firstCell = list(zip(emptyCells[0], emptyCells[1]))[0]
    i, j = firstCell
    idxrow = i / 3 * 3
    idxcol = j / 3 * 3

    guesses = list(reduce(np.intersect1d, (findValues(puzzle[i, :]), findValues(puzzle[:, j]), findValues(puzzle[idxrow:idxrow + 3, idxcol:idxcol + 3]))))

    if len(guesses) == 0:
        return False

    for guess in guesses:
        prePuzzle = copy.deepcopy(puzzle)
        puzzle[i][j] = guess
        result = recursiveSolve()
        if result:
            return True
        else:
            puzzle = copy.deepcopy(prePuzzle)
    return False


solutionTimes = []
puzzleFiles = os.listdir('Puzzles/')

# Solve each puzzle in the Puzzle directory.
for puzzleFile in puzzleFiles:
    with open('Puzzles/' + puzzleFile, 'r') as f:
        lines = f.readlines()
        puzzleArray = []
        for line in lines:
            row = [int(val) for val in str(line).strip()]
            puzzleArray.append(row)

    puzzle = np.array(puzzleArray)
    start = time.time()
    recursiveSolve()
    processtime = time.time() - start
    solutionTimes.append(processtime)
    with open('Solutions/' + puzzleFile.replace('.txt', '_SOLUTION.txt'), 'w') as f:
        if not isSolved():
            f.write('No Solution Found')
        else:
            puzzleString = np.array_str(puzzle).replace('[[', '').replace(']', '').replace(' [', '')
            f.write(puzzleString)
        f.write('\nDuration: ' + str(processtime))

# Print some basic statistics and plot the results as a histogram.
print 'Puzzle ' + str(solutionTimes.index(max(solutionTimes)) + 1) + ' took the longest to solve, ' + str(max(solutionTimes)) + ' seconds.'
print 'Puzzle ' + str(solutionTimes.index(min(solutionTimes)) + 1) + ' took the shortest to solve, ' + str(min(solutionTimes)) + ' seconds.'

solutionTimes = np.array([round(i) for i in solutionTimes])
plt.hist(solutionTimes)
plt.show()
