import random
from tabulate import tabulate 

def Row(x, row, grid):
    if x in grid[row]:
        return True
    else:
        return False

def Col(x, col, grid):
    colList = []
    for i in range(9):
        colList.append(grid[i][col])
    if x in colList:
        return True
    else:
        return False

def Square(x, row, col, grid):
    square = []

    if row < 3:
        if col < 3:
            square = [grid[i][0:3] for i in range(0, 3)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(0, 3)]
        else:
            square = [grid[i][6:9] for i in range(0, 3)]
    elif row < 6:
        if col < 3:
            square = [grid[i][0:3] for i in range(3, 6)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(3, 6)]
        else:
            square = [grid[i][6:9] for i in range(3, 6)]
    else:
        if col < 3:
            square = [grid[i][0:3] for i in range(6, 9)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(6, 9)]
        else:
            square = [grid[i][6:9] for i in range(6, 9)]

    return bool(x in square[0]+square[1]+square[2])

def isGridFilled(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c]==0:
                return False
    else:
        return True


def fillGrid(grid, tracker):

    values= [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for cellNo in range(81):
            row = cellNo // 9
            col = cellNo % 9

            random.shuffle(values)
            if grid[row][col] == 0:

                for testVal in values:
                    # 1. in the row
                    # 2. in the col
                    # 3. in the square

                    a = Row(testVal, row, grid)
                    b = Col(testVal, col, grid)
                    c = Square(testVal, row, col, grid)

                    if a == False and b == False and b == False:
                        #If testVal is unique in its row, column and (3*3) square
                        grid[row][col] = testVal

                        if isGridFilled(grid):
                            return True
                        else:
                            if fillGrid(grid, cellNo):
                               return True

                break 
    grid[row][col] = 0

grid = []
for i in range(9):
    #create empty grid
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

fillGrid(grid, 1)

#prints sudoku in the table
def Printgrid(Grid):
        print(tabulate(grid,tablefmt="fancy_grid"))

Printgrid(grid)