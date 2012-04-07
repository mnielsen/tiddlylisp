# tiddlylisp

Tiddlylisp is a toy Lisp interpreter, written in Python, and intended
to accompany the essay
[Lisp as the Maxwell's equations of software](http://michaelnielsen.org/lisp-as-the-maxwells-equations-of-software/).

The repository contains the following files:

`tiddlylisp.py`: A simple interpreter for a subset of Lisp.
Tiddlylisp is adapted from and closely based on Peter Norvig's
[lispy interpreter](http://norvig.com/lispy.html).

`sqrt.tl`: An example tiddlylisp program, for computing square roots.
Adapted from an example in the book
[The Structure and Interpretation of Computer Programs](http://mitpress.mit.edu/sicp/),
by Harold Abelson and Gerald Jay Sussman with Julie Sussmann.

`eval.tl`: A tiddylisp program defining a function `eval` which can
evaluate any Lisp expression, albeit, for an even smaller subset of
Lisp than tiddlylisp.

See
[the essay](http://michaelnielsen.org/lisp-as-the-maxwells-equations-of-software/)
for more details.