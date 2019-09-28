import tabulate


class Error(Exception):
    """ Base class for custom exceptions """
    pass

class badFormatError(Error):
    """ raised when user has tried to input anything that is not a number
        into the sudoku board """
    pass

class badBoardError(Error):
    """ raised when the user has tried to input a number into a wrong
        position (i.e. repeated number in block, row or column """
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
        '''
        init function for board class, generate board
        '''

        self.board = [['*' for x in range(9)] for y in range(9)]


    def isSegmentValid(self, segment):
        '''
        accept a list and see if it is valid - return True/False
        '''

        allowed = {x for x in range(1, 10)}
        allowed.add('*')

        if set(segment).issubset(allowed):
            pass
        else:
            raise badFormatError

        segmap = {i:0 for i in range(1,10)}

        for number in segment:
            if number == '*':
                pass
            else:
                segmap[number] += 1

        if set(segmap.values()).issubset({0,1}):
            return True
        else:
            return False
