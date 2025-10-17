import tkinter as tk
from tkinter import messagebox
import time
import copy
import random
import board

CELL_SIZE = 48
GRID_SIZE = 9
BOLD_LINE_WIDTH = 4
NORMAL_LINE_WIDTH = 1
PREFILL_COLOR = '#dbeafe'
USER_COLOR = '#fff'
SELECT_COLOR = '#facc15'
FONT = ("Arial", 18)

class SudokuGUI:
	def __init__(self, root):
		self.root = root
		self.root.title("Sudoku")
		self.frame = tk.Frame(root)
		self.frame.pack()
		self.canvas = tk.Canvas(self.frame, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE)
		self.canvas.grid(row=0, column=0, columnspan=4)
		self.timer_label = tk.Label(self.frame, text="Time: 00:00", font=("Arial", 14))
		self.timer_label.grid(row=1, column=0, sticky="w", pady=8)
		self.new_btn = tk.Button(self.frame, text="New", width=8, command=self.new_puzzle)
		self.new_btn.grid(row=1, column=1)
		self.check_btn = tk.Button(self.frame, text="Check", width=8, command=self.check)
		self.check_btn.grid(row=1, column=2)
		self.solve_btn = tk.Button(self.frame, text="Solve", width=8, command=self.solve)
		self.solve_btn.grid(row=1, column=3)
		self.clear_btn = tk.Button(self.frame, text="Clear", width=8, command=self.clear)
		self.clear_btn.grid(row=2, column=1, columnspan=2)
		self.selected = None
		self.timer_running = False
		self.start_time = None
		self.puzzle = None
		self.solution = None
		self.user_grid = None
		self.prefilled = None
		self.draw_grid()
		self.new_puzzle()
		self.canvas.bind("<Button-1>", self.cell_click)
		self.root.bind("<Key>", self.key_press)

	def draw_grid(self):
		self.canvas.delete("grid")
		for i in range(GRID_SIZE+1):
			width = BOLD_LINE_WIDTH if i % 3 == 0 else NORMAL_LINE_WIDTH
			color = '#e11d48' if width == BOLD_LINE_WIDTH else '#f59e42'
			self.canvas.create_line(0, i*CELL_SIZE, CELL_SIZE*GRID_SIZE, i*CELL_SIZE, width=width, fill=color, tags="grid")
			self.canvas.create_line(i*CELL_SIZE, 0, i*CELL_SIZE, CELL_SIZE*GRID_SIZE, width=width, fill=color, tags="grid")

	def draw_numbers(self):
		self.canvas.delete("numbers")
		for r in range(GRID_SIZE):
			for c in range(GRID_SIZE):
				x = c*CELL_SIZE + CELL_SIZE//2
				y = r*CELL_SIZE + CELL_SIZE//2
				val = self.user_grid[r][c]
				if val != 0:
					color = "#222"
					bg = PREFILL_COLOR if self.prefilled[r][c] else USER_COLOR
					self.canvas.create_rectangle(c*CELL_SIZE+2, r*CELL_SIZE+2, (c+1)*CELL_SIZE-2, (r+1)*CELL_SIZE-2, fill=bg, outline="", tags="numbers")
					self.canvas.create_text(x, y, text=str(val), font=FONT, fill=color, tags="numbers")
				elif self.prefilled[r][c]:
					self.canvas.create_rectangle(c*CELL_SIZE+2, r*CELL_SIZE+2, (c+1)*CELL_SIZE-2, (r+1)*CELL_SIZE-2, fill=PREFILL_COLOR, outline="", tags="numbers")
		if self.selected:
			r, c = self.selected
			self.canvas.create_rectangle(c*CELL_SIZE+2, r*CELL_SIZE+2, (c+1)*CELL_SIZE-2, (r+1)*CELL_SIZE-2, outline=SELECT_COLOR, width=3, tags="numbers")

	def new_puzzle(self):
		self.puzzle, self.solution = self.generate_puzzle()
		self.user_grid = copy.deepcopy(self.puzzle)
		self.prefilled = [[self.puzzle[r][c] != 0 for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
		self.selected = None
		self.start_timer()
		self.draw_grid()
		self.draw_numbers()

	def generate_puzzle(self):
		grid = [[0]*9 for _ in range(9)]
		board.fillGrid(grid)
		solution = copy.deepcopy(grid)
		puzzle = copy.deepcopy(grid)
		cells_to_remove = 40
		while cells_to_remove > 0:
			r = random.randint(0,8)
			c = random.randint(0,8)
			if puzzle[r][c] != 0:
				puzzle[r][c] = 0
				cells_to_remove -= 1
		return puzzle, solution

	def cell_click(self, event):
		col = event.x // CELL_SIZE
		row = event.y // CELL_SIZE
		if 0 <= row < 9 and 0 <= col < 9:
			if not self.prefilled[row][col]:
				self.selected = (row, col)
				self.draw_numbers()

	def key_press(self, event):
		if not self.selected:
			return
		r, c = self.selected
		if self.prefilled[r][c]:
			return
		if event.char in '123456789':
			self.user_grid[r][c] = int(event.char)
		elif event.keysym in ('BackSpace', 'Delete', '0'):
			self.user_grid[r][c] = 0
		self.draw_numbers()

	def check(self):
		for r in range(9):
			for c in range(9):
				val = self.user_grid[r][c]
				if val == 0 or val != self.solution[r][c]:
					messagebox.showinfo("Sudoku", "Incorrect or incomplete solution.")
					return
		elapsed = int(time.time() - self.start_time)
		mins, secs = divmod(elapsed, 60)
		messagebox.showinfo("Sudoku", f"Congratulations! You solved it in {mins:02d}:{secs:02d}.")
		self.stop_timer()

	def solve(self):
		self.user_grid = copy.deepcopy(self.solution)
		self.draw_numbers()
		self.stop_timer()

	def clear(self):
		for r in range(9):
			for c in range(9):
				if not self.prefilled[r][c]:
					self.user_grid[r][c] = 0
		self.draw_numbers()

	def start_timer(self):
		self.start_time = time.time()
		self.timer_running = True
		self.update_timer()

	def stop_timer(self):
		self.timer_running = False

	def update_timer(self):
		if not self.timer_running:
			return
		elapsed = int(time.time() - self.start_time)
		mins, secs = divmod(elapsed, 60)
		self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
		self.root.after(1000, self.update_timer)

if __name__ == "__main__":
	root = tk.Tk()
	app = SudokuGUI(root)
	root.mainloop()
import tkinter as tk