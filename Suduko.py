from pprint import pprint


def find_next_empty(puzzle):
    # finds the next row, col on the puzzle that's not filled yet --> rep with -1
    # return row, col tuple (or (None, None) if there is none)
    for r in range(9):
        for c in range(9): # range(9) is 0, 1, 2, ... 8
            if puzzle[r][c] == -1:
                return r, c

    return None, None  # if no spaces in the puzzle are empty (-1)

def is_valid(puzzle, guess, row, col):
    # let's start with the row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False # if we've repeated, then our guess is not valid!

    # now the column


    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # and then the square
    row_start = (row // 3) * 3 # 10 // 3 = 3, 5 // 3 = 1, 1 // 3 = 0
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True

def solve_sudoku(puzzle):

    
    #choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # if there's nowhere left, then we're done because we only allowed valid inputs
    if row is None:  # this is true if our find_next_empty function returns None, None
        return True 
    
    #if there is a place to put a number, then make a guess between 1 and 9
    for guess in range(1, 10): # range(1, 10) is 1, 2, 3, ... 9
       
        if is_valid(puzzle, guess, row, col):
           
            puzzle[row][col] = guess
            
            if solve_sudoku(puzzle):
                return True
        
        #it is not valid or if nothing gets returned true, then we need to backtrack and try a new number
        puzzle[row][col] = -1

    #if none of the numbers that we try work, then this puzzle is UNSOLVABLE!!
    return False

if __name__ == '__main__':
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    print(solve_sudoku(example_board))
    pprint(example_board)
