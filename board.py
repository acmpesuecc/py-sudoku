import tabulate


'''------------------------------------------------- custom error classes------------------------------------------------------- '''

class Error(Exception):
    """ Base class for custom exceptions """
    pass

class badFormatError(Error):
    """ raised when user has tried to input anything that is not a number
        into the sudoku board """
    pass


class Board:

    '''
    board class for sudoku
    the functionalities are as follows-
    1) generate the board
    2) check if the board is valid (i.e. no repetitions in each 3x3 grid,
        row or column
    3) print the board
    '''

    def __init__(self):

        # generate 9x9 board for sudoku
        self.board = [['*' for x in range(9)] for y in range(9)]


    def isSegmentValid(segment):

        # accept a list as input and check if any number is repeated in it
        segmap = {i:0 for i in range(1,10)}

        for number in segment:
            if number == '*':
                pass
            elif number.isdigit():
                
