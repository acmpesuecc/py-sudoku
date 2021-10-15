#Advaitha S,1st year CSE,PESU-EC
import random
from tabulate import tabulate

#========================================================
# Function checks if the number is in the row
#========================================================

def checkRow(testVal, row, grid):
    return bool(testVal in grid[row])

#========================================================
# Function checks if the number is in the column
#========================================================

def checkCol(testVal, col, grid):
    colList = []
    for i in range(9):
        colList.append(grid[i][col])
    return bool(testVal in colList)

#========================================================
# Function checks if the number is in the square (3*3)
#========================================================

def checkSquare(testVal, row, col, grid):
    square = []

    #To identify which (3*3) square the cell belongs to
    #square (list) is the list of all values in the (3*3) square
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

    return bool(testVal in square[0]+square[1]+square[2])

#========================================================
# Function to check if the grid is filled
#========================================================

def isGridFilled(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c]==0:
                return False
    else:
        return True

#========================================================
# Function to generate a full sudoku
#========================================================

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

                    r1 = checkRow(testVal, row, grid)
                    r2 = checkCol(testVal, col, grid)
                    r3 = checkSquare(testVal, row, col, grid)

                    if r1 == False and r2 == False and r3 == False:
                        #If testVal is unique in its row, column and (3*3) square
                        grid[row][col] = testVal

                        if isGridFilled(grid):
                            return True
                        else:
                            if fillGrid(grid, cellNo):
                               return True

                break 
    grid[row][col] = 0



#========================================================
#Main 
#========================================================

grid = []
for i in range(9):
    #create empty grid
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

fillGrid(grid, 1)

#========================================================
#Display generated grid
#========================================================

print(tabulate(grid,tablefmt="grid"))


