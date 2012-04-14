# tiddlylisp

Tiddlylisp is a toy Lisp interpreter, written in Python, and intended
to accompany the essay
[Lisp as the Maxwell's equations of software](http://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/).

The repository contains the following files:

`tiddlylisp.py`: A simple interpreter for a subset of Lisp.
Tiddlylisp is adapted from and closely based on Peter Norvig's
[lispy interpreter](http://norvig.com/lispy.html).

`tiddlyvau.py`: A modification of the interpreter that uses vau expressions to move all built-in functions and syntactic forms out of the eval function.
[lispy interpreter](http://norvig.com/lispy.html).

`tiddlyparser.py`: A shared module for parsing s-expressions.

`sqrt.tl`: An example tiddlylisp program, for computing square roots.
Adapted from an example in the book
[The Structure and Interpretation of Computer Programs](http://mitpress.mit.edu/sicp/),
by Harold Abelson and Gerald Jay Sussman with Julie Sussmann.

`eval.tl`: A tiddylisp program defining a function `eval` which can
evaluate any Lisp expression, albeit, for an even smaller subset of
Lisp than tiddlylisp.  Based on the
[LISP 1.5 Programmer's Manual](http://www.softwarepreservation.org/projects/LISP/book/LISP%201.5%20Programmers%20Manual.pdf)
and the essay
[The Roots of Lisp](http://lib.store.yahoo.net/lib/paulgraham/jmc.ps)
(postscript) by Paul Graham.

See
[the essay](http://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/)
for more details.
