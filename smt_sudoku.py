from pysmt.shortcuts import Symbol, And, Plus, Equals, GE, LT, Int, AllDifferent, get_model
from pysmt.shortcuts import Solver
from pysmt.typing import INT
import sys

# This program works with an array of 81 values
# whose indices are arranged like this:
#
#  0  1  2    3  4  5    6  7  8
#  9 10 11   12 13 14   15 16 17
# 18 19 20   21 22 23   24 25 26
#
# 27 28 29   30 31 32   33 34 35
# 36 37 38   39 40 41   42 43 44
# 45 46 47   48 49 50   51 52 53
#
# 54 55 56   57 58 59   60 61 62
# 63 64 65   66 67 68   69 70 71
# 72 73 74   75 76 77   78 79 80
#

def block_at(n):
    """Return the 9 indices of the block that starts with n"""
# The numbers being added here are the indices of the upper-left
# box in the above diagram
    return [n, n+1, n+2, n+9, n+10, n+11, n+18, n+19, n+20]

def row_at(n):
    """Return the 9 indices of the row that starts with n"""
    return [i for i in range(n, n+9)]

def col_at(n):
    """Return the 9 indices of the column that starts with n"""
#   Each index in a column is 9 higher than the previous one
#   So column 4 is 4,13,22,31,40 ...
    return [i+n for i in range(0, 81, 9)]

def digit_check(sud, i, sud_str):
    """If the i-th char in sud_str is ., return a range check for 1-9, otherwise return a test for a specific digit"""
    if sud_str[i] == '.':
        return And(GE(sud[i],Int(1)),LT(sud[i],Int(10)))
    else:
        return Equals(sud[i],Int(ord(sud_str[i])-ord('0')))

def solve_sudoku(sud_str):
    # create 81 symbols named s0..s80
    # these represent the digits that the SMT solver is trying to solve
    sud = [Symbol("s"+str(i), INT) for i in range(0, 81)]

    # For each block, create an AllDifferent call for each member of
    # the block and And them all together
    # the values here for block_num are the upper-left indices of
    # each 3x3 box (according to the diagram at the top of this file)
    blocks = And([AllDifferent([sud[i] for i in block_at(block_num)])
        for block_num in [0, 3, 6, 27, 30, 33, 54, 57, 60]])

    # For each row, create an AllDifferent call for each item in the
    # row and And them all together
    # The first index of each row is 9 higher than the first index
    # of the previous row 0..9..18..27..
    rows = And([AllDifferent([sud[i] for i in row_at(row_num)])
        for row_num in range(0, 81, 9)])

    # For each column, create an AllDifferent call for each item in the
    # column and And them all together
    # The first index of each column is just 0,1,2,3,4.. and then
    cols = And([AllDifferent([sud[i] for i in col_at(col_num)])
        for col_num in range(0, 9)])

    # Create the initial digit specifications from the puzzle string where
    # a . in the string means the digit can be anything from 1-9, or it
    # will have a specific digit
    digits = And([digit_check(sud, i, sud_str) for i in range(0, 81)])

    # create the formula from the digit specification and the row, col,
    # and block restrictions
    formula = And(digits, And([blocks, rows, cols]))

    with Solver() as solver:
        solver.add_assertion(formula)
        if solver.solve():
            for row in range(0, 81, 9):
                for col in row_at(row):
                    print(solver.get_value(sud[col]), end='')
            print()
        else:
            print("No solution found")

# Load the puzzle set (http://norvig.com/top95.txt)
filename = "top95.txt"
if len(sys.argv) > 1:
    filename = sys.argv[1]
for line in open(filename, "r"):
    solve_sudoku(line.rstrip())
