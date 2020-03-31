import numpy as np
import os

# Dictionary containing how the characters are mapped.
dictionary = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 0: '-'}

# Read each puzzle file and apply the mapping to it. Print out the result seed puzzles.
for file in os.listdir('Puzzles/'):
    with open('Puzzles/' + file, 'r') as f:
        lines = f.readlines()
        puzzleArray = []
        for line in lines:
            row = [int(val) for val in str(line).strip()]
            puzzleArray.append(row)

    puzzle = np.array(puzzleArray)
    puzzle = np.vectorize(dictionary.get)(puzzle)
    puzzleString = np.array_str(puzzle).replace('[[', '').replace(']', '').replace(' [', '').replace("'", '')

    with open('Seeds/' + file, 'w') as f:
        f.write(puzzleString)
