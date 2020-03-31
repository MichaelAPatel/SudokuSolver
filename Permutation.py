import numpy as np
import copy


# Function created a random dictionary mapping the letters A-I to the numbers 1-9.
# Returns
#    dictionary - randomly mapped dictionary
def randDictionary():
    keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    values = np.arange(10)
    np.random.shuffle(values)
    values = values.tolist()
    dictionary = dict(zip(keys, values))
    zero_dictionary = {'-':0}
    dictionary.update(zero_dictionary)
    return dictionary


# Randomly choose one of the seeds and read its content.
puzz = 'Puzzle' + str(np.random.randint(100)) + '.txt'
with open('Seeds/' + puzz, 'r') as f:
    lines = f.readlines()
    puzzleArray = []
    for line in lines:
        row = line.split()
        puzzleArray.append(row)

seed_puzzle = np.array(puzzleArray)
seedPuzzleString = np.array_str(seed_puzzle).replace('[[', '').replace(']', '').replace(' [', '').replace(' ', '')
permutationList = [seedPuzzleString]

# Generate 1,000 puzzles by generating random mappings of seed letters to numbers.
for i in range(1000):
    puzzle = copy.deepcopy(seed_puzzle)
    randDict = randDictionary()
    puzzle = np.vectorize(randDict.get)(puzzle)
    puzzleString = np.array_str(puzzle).replace('[[', '').replace(']', '').replace(' [', '').replace(' ', '')
    permutationList.append(puzzleString.replace('\n', ''))
    with open('Permutations/Puzzle' + str(i) + '.txt', 'w') as f:
        f.write(puzzleString)

# Check to see if any of the randomly generated permutations are repeats.
uniquePuzzles = int(np.unique(np.array(permutationList)).shape[0])
print 'Using ' + puzz + ' as the seed we generated:'
print '\t' + str(uniquePuzzles - 1) + ' unique puzzles'
print '\t' + str(1001 - uniquePuzzles) + ' repeated puzzles'
