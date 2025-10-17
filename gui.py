import tkinter as tk
from tkinter import messagebox
import time

class SudokuGUI:
    sample_puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    # Solution for the sample puzzle, for quick checking
    # We will generate this with our solver
    solved_puzzle = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8], [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5], [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.cells = {}
        self.timer_label = tk.Label(root, text="Time: 00:00", font=('Arial', 14))
        self.timer_label.pack(pady=10)
        self.timer_running = False
        self.seconds_elapsed = 0
        vcmd = (self.root.register(self._validate_input), '%P')
        master_frame = tk.Frame(root, bd=3, relief='ridge', bg='black')
        master_frame.pack(pady=10, padx=20)
        sub_frames = {}
        for r in range(3):
            for c in range(3):
                frame = tk.Frame(master_frame, bd=1, relief='ridge')
                frame.grid(row=r, column=c)
                sub_frames[(r, c)] = frame
        for row in range(9):
            for col in range(9):
                frame_row, frame_col = row // 3, col // 3
                cell_row, cell_col = row % 3, col % 3
                parent_frame = sub_frames[(frame_row, frame_col)]
                cell = tk.Entry(
                    parent_frame, width=3, font=('Arial', 20), justify='center', relief='flat',
                    validate='key', validatecommand=vcmd
                )
                cell.grid(row=cell_row, column=cell_col, ipady=5)
                self.cells[(row, col)] = cell
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        new_button = tk.Button(button_frame, text="New", command=self.new_game)
        check_button = tk.Button(button_frame, text="Check", command=self.check_solution)
        solve_button = tk.Button(button_frame, text="Solve", command=self.solve_puzzle)
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_board)
        new_button.grid(row=0, column=0, padx=5)
        check_button.grid(row=0, column=1, padx=5)
        solve_button.grid(row=0, column=2, padx=5)
        clear_button.grid(row=0, column=3, padx=5)
        self.load_puzzle(self.sample_puzzle)

    def update_timer(self):
        if self.timer_running:
            self.seconds_elapsed += 1
            minutes, seconds = divmod(self.seconds_elapsed, 60)
            time_string = f"Time: {minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string)
            self.root.after(1000, self.update_timer)

    def _validate_input(self, P):
        return P == "" or (P.isdigit() and len(P) == 1 and P != '0')

    def load_puzzle(self, puzzle_board):
        for row in range(9):
            for col in range(9):
                value = puzzle_board[row][col]
                cell = self.cells[(row, col)]
                cell.config(state='normal', fg='black')
                cell.delete(0, 'end')
                if value != 0:
                    cell.insert(0, str(value))
                    cell.config(state='readonly', fg='#3333FF')
        self.start_timer()

    def start_timer(self):
        self.seconds_elapsed = 0
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def new_game(self):
        self.load_puzzle(self.sample_puzzle)

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                cell = self.cells[(row, col)]
                if cell.cget('state') == 'normal':
                    cell.delete(0, 'end')
    
    def get_board_state(self):
        board = [[0]*9 for _ in range(9)]
        for row in range(9):
            for col in range(9):
                value = self.cells[(row, col)].get()
                if value.isdigit():
                    board[row][col] = int(value)
        return board

    def is_valid_solution(self, board):
        def is_valid_unit(unit):
            unit = [i for i in unit if i != 0]
            return len(unit) == len(set(unit))
        for i in range(9):
            if not is_valid_unit(board[i]) or not is_valid_unit([board[j][i] for j in range(9)]):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not is_valid_unit([board[x][y] for x in range(i, i+3) for y in range(j, j+3)]):
                    return False
        return True

    def check_solution(self):
        board = self.get_board_state()
        if any(0 in row for row in board):
            messagebox.showwarning("Incomplete", "The puzzle is not completely filled!")
            return
        if self.is_valid_solution(board):
            self.timer_running = False
            time_string = self.timer_label.cget("text")
            messagebox.showinfo("Success!", f"Congratulations! You solved the puzzle!\n{time_string}")
        else:
            messagebox.showerror("Incorrect", "The solution is incorrect. Keep trying!")

    # --- NEW SOLVER CODE ---
    def _find_empty(self, board):
        """Finds the next empty cell (represented by 0)."""
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def _is_valid_move(self, board, num, pos):
        """Checks if a number is a valid move for a given position."""
        row, col = pos
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        # Check 3x3 box
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num:
                    return False
        return True

    def _solve_backtracking(self, board):
        """Solves the Sudoku puzzle using backtracking (recursive)."""
        find = self._find_empty(board)
        if not find:
            return True  # Puzzle is solved
        else:
            row, col = find

        for num in range(1, 10):
            if self._is_valid_move(board, num, (row, col)):
                board[row][col] = num

                if self._solve_backtracking(board):
                    return True

                board[row][col] = 0 # Backtrack
        return False

    def solve_puzzle(self):
        self.timer_running = False
        board = self.get_board_state() # Get the initial state with user's numbers
        
        # We solve a copy of the original puzzle to display the absolute solution
        solve_board = [row[:] for row in self.sample_puzzle]

        if self._solve_backtracking(solve_board):
            for r in range(9):
                for c in range(9):
                    cell = self.cells[(r, c)]
                    if cell.cget('state') == 'normal': # Only fill empty cells
                        cell.delete(0, 'end')
                        cell.insert(0, str(solve_board[r][c]))
                        cell.config(fg='green') # Show solved numbers in green
        else:
            messagebox.showerror("Unsolvable", "The puzzle could not be solved from the initial state.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()