import tkinter as tk
from tkinter import messagebox
import time
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.cells = {}
        
        # Variables to hold the current puzzle and its solution
        self.current_puzzle = None
        self.current_solution = None

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
                    parent_frame, width=3, font=('Arial', 20), justify='center',
                    relief='solid', bd=1, # UI ENHANCEMENT: Adds the 1x1 grid lines
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

        # Generate and load the first puzzle on startup
        self.new_game()

    def new_game(self):
        """Generates a new puzzle and solution, then loads it."""
        # 1. Create a new empty grid
        new_solution = [[0 for _ in range(9)] for _ in range(9)]
        # 2. Generate a full, valid Sudoku solution
        self._fillGrid(new_solution)
        self.current_solution = new_solution
        # 3. Create a playable puzzle by removing numbers from the solution
        self.current_puzzle = self._create_puzzle(new_solution)
        # 4. Load the puzzle into the UI
        self.load_puzzle()

    def load_puzzle(self):
        """Displays the current puzzle on the grid."""
        for row in range(9):
            for col in range(9):
                value = self.current_puzzle[row][col]
                cell = self.cells[(row, col)]
                # Reset cell style for new game
                cell.config(state='normal', fg='black', bg='white')
                cell.delete(0, 'end')
                if value != 0:
                    cell.insert(0, str(value))
                    cell.config(state='readonly', fg='#3333FF')
        self.start_timer()

    def check_solution(self):
        """Checks the user's input against the stored solution."""
        board = self.get_board_state()
        is_fully_correct = True

        for r in range(9):
            for c in range(9):
                cell = self.cells[(r, c)]
                user_val = board[r][c]
                correct_val = self.current_solution[r][c]

                # UI ENHANCEMENT: Highlight incorrect entries in red
                if cell.cget('state') == 'normal' and user_val != 0:
                    if user_val != correct_val:
                        cell.config(bg='#FFCCCC') 
                        is_fully_correct = False
                    else:
                        cell.config(bg='white') 
        
        if not is_fully_correct:
            messagebox.showerror("Incorrect", "Some numbers are incorrect and have been highlighted.")
        elif any(0 in row for row in board):
            messagebox.showinfo("Correct So Far", "Your entries are correct, but the puzzle isn't finished!")
        else:
            self.timer_running = False
            time_string = self.timer_label.cget("text")
            messagebox.showinfo("Success!", f"Congratulations! You solved the puzzle!\n{time_string}")

    def solve_puzzle(self):
        """Fills the board with the pre-calculated solution."""
        self.timer_running = False
        for r in range(9):
            for c in range(9):
                cell = self.cells[(r, c)]
                if cell.cget('state') == 'normal':
                    cell.delete(0, 'end')
                    cell.insert(0, str(self.current_solution[r][c]))
                    cell.config(fg='green')

    # --- SUDOKU GENERATION LOGIC (Integrated from your other files) ---
    def _create_puzzle(self, solution_grid):
        """Creates a playable puzzle by poking holes in a solved grid."""
        puzzle = [row[:] for row in solution_grid] # Deep copy
        num_to_remove = 45 # Adjust for difficulty
        for _ in range(num_to_remove):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while puzzle[row][col] == 0: # Ensure we don't try to remove an already empty cell
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            puzzle[row][col] = 0
        return puzzle

    def _fillGrid(self, grid):
        values = list(range(1, 10))
        for cellNo in range(81):
            row, col = divmod(cellNo, 9)
            if grid[row][col] == 0:
                random.shuffle(values)
                for testVal in values:
                    if not self._checkRow(testVal, row, grid) and \
                       not self._checkCol(testVal, col, grid) and \
                       not self._checkSquare(testVal, row, col, grid):
                        grid[row][col] = testVal
                        if self._isGridFilled(grid):
                            return True
                        if self._fillGrid(grid):
                            return True
                grid[row][col] = 0
                return False
        return True

    def _checkRow(self, testVal, row, grid):
        return testVal in grid[row]

    def _checkCol(self, testVal, col, grid):
        return testVal in [grid[i][col] for i in range(9)]

    def _checkSquare(self, testVal, row, col, grid):
        square = []
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                square.append(grid[r][c])
        return testVal in square

    def _isGridFilled(self, grid):
        return all(all(cell != 0 for cell in row) for row in grid)

    # --- HELPER & UTILITY FUNCTIONS ---
    def get_board_state(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.cells[(row, col)].get()
                current_row.append(int(value) if value.isdigit() else 0)
            board.append(current_row)
        return board
    
    def start_timer(self):
        self.seconds_elapsed = 0
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.seconds_elapsed += 1
            minutes, seconds = divmod(self.seconds_elapsed, 60)
            time_string = f"Time: {minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string)
            self.root.after(1000, self.update_timer)

    def _validate_input(self, P):
        return P == "" or (P.isdigit() and len(P) == 1 and P != '0')

    def clear_board(self):
        for cell in self.cells.values():
            if cell.cget('state') == 'normal':
                cell.config(bg='white')
                cell.delete(0, 'end')

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()