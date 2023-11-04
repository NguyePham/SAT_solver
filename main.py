import sys
sys.path.append('/home/nguye/fm/sudoku/solver')
sys.path.append('/home/nguye/fm/sudoku/utils')
from binomial import *
from product import *
from load_puzzle import *

import tkinter as tk
import tkinter.ttk as ttk
import time
import copy


board_size = 9
nofHint = 30
binomial_time = None
product_time = None
binomial_nVars = None
binomial_nClauses = None
product_nVars = None
product_nClauses = None
puzzle = None
int_puzzle = None
input_id = 0


def draw_board():
	global puzzle
	global board_size

	sudokuBoard.delete("all")

	for i in range(board_size + 1):
		color = "black" if i % int(sqrt(board_size)) == 0 else "grey"
		width = 2 if i % int(sqrt(board_size)) == 0 else 1
		x0 = i * WIDTH // board_size
		y0 = 0
		x1 = i * WIDTH // board_size
		y1 = WIDTH
		sudokuBoard.create_line(x0+1, y0+1, x1+1, y1+1,
								fill=color, width=width)
		sudokuBoard.create_line(y0+1, x0+1, y1+1, x1+1,
								fill=color, width=width)

	for i in range(board_size):
		for j in range(board_size):
			x0 = j * WIDTH // board_size
			y0 = i * WIDTH // board_size
			x1 = (j + 1) * WIDTH // board_size
			y1 = (i + 1) * WIDTH // board_size
			display = puzzle[i][j] if puzzle[i][j] != 0 else ""
			sudokuBoard.create_text(x0 + WIDTH // board_size // 2, y0 + WIDTH // board_size // 2,
									text=display, fill="black", font=("Arial", int(WIDTH // board_size // 2)))


def display_metrics():
	global binomial_time
	global product_time
	global binomial_nVars
	global binomial_nClauses
	global product_nVars
	global product_nClauses

	if binomial_time is not None:
		binomialLabel.config(
			text="Binomial time: {:.4f}s".format(binomial_time))
		binomialLabel.pack()
	else:
		binomialLabel.pack_forget()

	if product_time is not None:
		productLabel.config(text="Product time: {:.4f}s".format(product_time))
		productLabel.pack()
	else:
		productLabel.pack_forget()


def set_size(size_string):
	global board_size

	if size_string == '9x9':
		board_size = 9
	elif size_string == '16x16':
		board_size = 16
	elif size_string == '25x25':
		board_size = 25
	else:
		board_size = 36


def new_puzzle():
	global board_size
	global puzzle
	global input_id
	global binomial_time
	global product_time
	
	
	puzzle, input_id = load_puzzle(size=board_size, cur_id=input_id)
	print(input_id)
	binomial_time = None
	product_time = None

	display_metrics()
	draw_board()


def solve():
	global puzzle
	global int_puzzle
	global board_size
	global binomial_time
	global product_time
	global binomial_nVars
	global binomial_nClauses
	global product_nVars
	global product_nClauses

	int_puzzle = convert_to_ints(puzzle)
	tmp = copy.deepcopy(int_puzzle)

	bi_start = time.perf_counter()
	binomial_nVars, binomial_nClauses = binomial(int_puzzle, board_size)
	bi_end = time.perf_counter()
	binomial_time = bi_end - bi_start

	pr_start = time.perf_counter()
	product_nVars, product_nClauses = product(tmp, board_size)
	pr_end = time.perf_counter()
	product_time = pr_end - pr_start
	display_metrics()

	puzzle = convert_to_strs(int_puzzle)
	draw_board()


root = tk.Tk()
root.title("Sudoku Solver")

try:
	from ctypes import windll
	windll.shcore.SetProcessDpiAwareness(1)
except:
	pass


WIDTH = 750

root.geometry("1000x800")
root.resizable(False, False)
root.attributes("-topmost", True)

sudokuFrame = tk.Frame(root, width=800, height=800, background="#cccccc")
sudokuFrame.grid(row=0, column=0)
sudokuBoard = tk.Canvas(sudokuFrame, width=WIDTH,
						height=WIDTH, background="white")
sudokuBoard.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

sidebar = tk.Frame(root, background="grey")
sidebar.grid(row=0, column=1)

binomialLabel = tk.Label(sidebar, text="Binomial: ", background="#dddddd")
productLabel = tk.Label(sidebar, text="Product: ", background="#dddddd")


sizeOptions = ["9x9", "16x16", "25x25", "36x36"]
sizeVar = tk.StringVar(root, "9x9")
new_puzzle()

sizeVar.trace_add('write', lambda *args: set_size(sizeVar.get()))
size_dropdown = ttk.OptionMenu(sidebar, sizeVar, "9x9", *sizeOptions)
size_dropdown.pack()


new_puzzle_button = tk.Button(sidebar, text="New Puzzle",
						command=new_puzzle, background="#dddddd")
new_puzzle_button.pack()


solve_button = tk.Button(sidebar, text="Solve",
						command=solve, background="#dddddd")
solve_button.pack()


root.mainloop()