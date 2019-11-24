# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 08:13:32 2017

Formulates sudoku as a CSP, solving the riddle from
https://www.sudoku.ws/hard-1.htm as an example.

@author: stdm
@modif: tugg
"""

import sys

sys.path.append("./python-constraint-1.2")
import constraint as csp

# ------------------------------------------------------------------------------
# sudoku to solve (add "0" where no number is given)
# ------------------------------------------------------------------------------
riddle = [[0, 0, 0, 2, 0, 0, 0, 6, 3],
          [3, 0, 0, 0, 0, 5, 4, 0, 1],
          [0, 0, 1, 0, 0, 3, 9, 8, 0],
          [0, 0, 0, 0, 0, 0, 0, 9, 0],
          [0, 0, 0, 5, 3, 8, 0, 0, 0],
          [0, 3, 0, 0, 0, 0, 0, 0, 0],
          [0, 2, 6, 3, 0, 0, 5, 0, 0],
          [5, 0, 3, 7, 0, 0, 0, 0, 8],
          [4, 7, 0, 0, 0, 1, 0, 0, 0]]


# ------------------------------------------------------------------------------
# create helpful lists of variable names
# ------------------------------------------------------------------------------
rownames = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
colnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

rows = []
for i in rownames:
    row = []
    for j in colnames:
        row.append(i + j)
    rows.append(row)

cols = []
for j in colnames:
    col = []
    for i in rownames:
        col.append(i + j)
    cols.append(col)

boxes = []
for x in range(3):  # over rows of boxes
    for y in range(3):  # over columns of boxes
        box = []
        for i in range(3):  # over variables in rows (in a box)
            for j in range(3):  # over variables in cols (in a box)
                box.append(rownames[x * 3 + i] + colnames[y * 3 + j])
        boxes.append(box)

# ------------------------------------------------------------------------------
# formulate sudoku as CSP
# ------------------------------------------------------------------------------
sudoku = csp.Problem()

row_counter = 0
col_counter = 0

for r in rows:
    for c in cols:
        # if there is a value for the field in the riddle, set the domain with the specific value
        if riddle[row_counter][col_counter] != 0:
            sudoku.addVariable(rows[row_counter][col_counter], [riddle[row_counter][col_counter]])
        # else set the domain from 1 to 9
        else:
            sudoku.addVariable(rows[row_counter][col_counter], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        col_counter += 1
    row_counter += 1
    col_counter = 0

# erster Lösungsansatz
# # add constraint for rows
# for i in range(9):
#     for j in range (8):
#         for k in range(j+1, 9, 1):
#             sudoku.addConstraint(lambda a, b: a != b, (rows[i][j], rows[i][k]))
#
# # add constraint for cols
# for i in range(9):
#     for j in range (8):
#         for k in range(j+1, 9, 1):
#             sudoku.addConstraint(lambda a, b: a != b, (cols[i][j], cols[i][k]))
#
# # add constraint for boxes
# for i in range(9):
#     for j in range (8):
#         for k in range(j+1, 9, 1):
#             sudoku.addConstraint(lambda a, b: a != b, (boxes[i][j], boxes[i][k]))

# Optimierte Lösung
for row in rows:
    sudoku.addConstraint(csp.AllDifferentConstraint(), row)

for col in cols:
    sudoku.addConstraint(csp.AllDifferentConstraint(), col)

for box in boxes:
    sudoku.addConstraint(csp.AllDifferentConstraint(), box)

# ------------------------------------------------------------------------------
# solve CSP
# ------------------------------------------------------------------------------
solutions = sudoku.getSolutions()


# ------------------------------------------------------------------------------
# Print Sudoku
# ------------------------------------------------------------------------------
#print(solutions)


print_col_counter = 0
print_row_counter = 0
print("  ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗")
for solution in solutions:
    for row in rows:
        print("  ║", end='')
        for col in row:
            print(" ",str(solution[col]), end='')
            if print_col_counter % 3 == 2:
                print("║", end='')
            else:
                print("|", end='')
            print_col_counter += 1
        print("\r")
        if (print_row_counter % 3 == 2) and (print_row_counter < 8):
            print('  ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣')
        elif (print_row_counter % 3 != 2) and (print_row_counter < 8):
            print('  ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢')
        print_row_counter += 1
        print_col_counter = 0
print("  ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝")
