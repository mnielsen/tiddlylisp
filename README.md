# tiddlylisp

Tiddlylisp is a toy Lisp interpreter, written in Python, and intended
to accompany the essay
[Lisp as the Maxwell's equations of software](http://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/).

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
Lisp than tiddlylisp.  Based on the
[LISP 1.5 Programmer's Manual](http://www.softwarepreservation.org/projects/LISP/book/LISP%201.5%20Programmers%20Manual.pdf)
and the essay
[The Roots of Lisp](http://lib.store.yahoo.net/lib/paulgraham/jmc.ps)
(postscript) by Paul Graham.

See
[the essay](http://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/)
for more details.

Notifications of bugs (and bug fixes) are welcome, but I am not adding
new features to tiddlylisp, as its main purpose is as a complement to
the essay.
