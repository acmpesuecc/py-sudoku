import random

class Board:
    def __init__(self):
        self.blankIndex = 40
        self.board = [[0 for x in range(9)] for y in range(9)]
        self.solve() # Genertaing a random board
        print(self) # Testing
        self.ReadyToPlay() # Blanking some spots to play
        print(self) # Testing
        
    def __repr__(self):
        rtn = ""
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                rtn += "- - - - - - - - - - -\n"

            for j in range(len(self.board[0])):
                if j % 3 == 0 and j != 0:
                    rtn += "| "

                if j == 8:
                    rtn += str(self.board[i][j]) + "\n" if self.board[i][j] != 0 else "\n"
                else:
                    rtn += str(self.board[i][j]) + " " if self.board[i][j] != 0 else "  "
        return rtn
    
    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find
        
        Set = random.sample([x for x in range(1, 10)], 9)
        for i in Set:
            if self.valid(i, (row, col)):
                self.board[row][col] = i
                # self.blankIndex += 1

                if self.solve():
                    return True

                self.board[row][col] = 0
                # self.blankIndex -= 1

        return False
    
    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)  # row, col

        return None
    
    def valid(self, num, pos):
        # Check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check self.boardx
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if self.board[i][j] == num and (i,j) != pos:
                    return False

        return True
    
    def ReadyToPlay(self):
        while self.blankIndex:
            i = random.randint(0,8)
            j = random.randint(0,8)
            if self.board[i][j] != 0:
                self.board[i][j] = 0
                self.blankIndex -= 1

Board1 = Board()
