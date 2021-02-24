# smt_sudoku
Solve Sudoku puzzles with pysmt

I just wanted to see how to use PySMT, so I threw together a simple
Sudoku solver.

For input, I use Peter Norvig's list of puzzles from here:
http://norvig.com/top95.txt

To run it, make sure you have python3, and then install pysmt
with pip:

    pip3 install pysmt

You will probably need to install a solver for pysmt as well:

    pysmt-install --check

    pysmt-install --z3
    pysmt-install --msat

I don't know if you need both z3 and msat for this, I think at least
msat.

Finally, run it with:
    python smt_sudoku.py

Assuming you have downloaded the top95.txt file, it will start
printing out solutions one-per-line.
