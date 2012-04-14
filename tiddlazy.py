#### tiddlyvau.py
#
# Simple Lisp interpreter that uses vau expressions
# to remove all built-in functions and syntactic forms from eval
#
# Adapted from tiddlylisp by Michael Nielsen.  See
# http://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/

import sys
import traceback
from tiddlyparser import *

class Env(dict):
	"An environment: a dict of {'var':val} pairs, with an outer Env."
	def __init__(self, bindings={}, outer=None):
		self.update(bindings)
		self.outer = outer

	def __getitem__(self, var):
		loc = self.find(var)
		val = super(Env,loc).__getitem__(var)
		if isa(val, Deferral):
			val = eval(val.expr, val.env)
			loc[var] = val
		return val

	def find(self, var):
		"Find the innermost Env where var appears."
		if var in self:
			return self
		elif not self.outer is None:
			return self.outer.find(var)
		else: raise ValueError("%s is not defined"%(var,))

class Deferral():
	def __init__(self, expr, env):
		self.expr = expr
		self.env = env

def define(var,exp):
	val = eval(exp)
	if not isa(var.expr, Symbol):
		raise Exception("Invalid Symbol %s" % (var.expr,))
	exp.env[var.expr] = val
	return val
	
def setvar(var, exp):
	val = eval(exp)
	env.find(var)[var] = val
	return val

def quote(exp): return exp.expr

def cond(*x):
	for clause in x:
		(p, e) = clause.expr
		if eval(p,clause.env):
			return eval(e,clause.env)
	raise ValueError("No Branch Evaluates to True")

def begin(*x):
	val = 0
	for exp in x:
		val = eval(exp)
	return val
	
def vprint(x):
	val = eval(x)
	print to_string(val)
	return val
	
global_env = Env({
	'+':	lambda x,y:eval(x)+eval(y),
	'-':	lambda x,y:eval(x)-eval(y),
	'*':	lambda x,y:eval(x)*eval(y),
	'/':	lambda x,y:eval(x)/eval(y),
	'>':	lambda x,y:eval(x)>eval(y),
	'<':	lambda x,y:eval(x)<eval(y),
	'>=':	lambda x,y:eval(x)>=eval(y),
	'<=':	lambda x,y:eval(x)<=eval(y),
	'=':	lambda x,y:eval(x)==eval(y),
	'eq?':	lambda x,y:
				(lambda vx,vy: (not isa(vx, list)) and (vx == vy))(eval(x),eval(y)),
	'cons':	lambda x,y:[eval(x)]+eval(y),
	'car':	lambda x:eval(x)[0],
	'cdr':	lambda x:eval(x)[1:],
	'list':	lambda *x:[eval(exp) for exp in x],
	'append':	lambda x,y:eval(x)+eval(y),
	'len':	lambda x:len(eval(x)),
	'null?':	lambda x:eval(x)==[],
	'symbol?':	lambda x:isa(eval(x),Symbol),
	'list?':	lambda x:isa(eval(x),list),
	'atom?':	lambda x:not isa(eval(x), list),
	'exit':		lambda:exit(),
	'True':		True,
	'False':	False,
	'if':		lambda test,conseq,alt: eval((conseq if eval(test) else alt)),
	'cond':		cond,
	'define':	define,
	'set!':		setvar,
	'lambda':	lambda vars, body:
					(lambda *args: eval(body.expr, Env(zip(vars.expr, args), body.env))),
	'q': quote,
	'quote': quote,
	'begin': begin,
	'print': vprint,
	'eval': lambda x,e: eval(x,e)
})

#### eval

def eval(x, env=global_env):
	"Evaluate an expression in an environment."
	if isa(x, Symbol):			  # variable reference
		return env.find(x)[x]
	if isa(x, Deferral):
		return eval(x.expr, x.env)
	if isa(x, list):		  # (proc exp*)
		proc = eval(x[0], env)
		args = [Deferral(expr,env) for expr in x[1:]]
		if hasattr(proc, '__call__'): return proc(*args)
		else: raise ValueError("%s = %s is not a procedure" % (to_string(x[0]),to_string(proc)))
	return x

#### Load from a file and run

def load(filename):
	"""
	Load the tiddlylisp program in filename, execute it, and start the
	repl.  If an error occurs, execution stops, and we are left in the
	repl.  Note that load copes with multi-line tiddlylisp code by
	merging lines until the number of opening and closing parentheses
	match.
	"""
	print "Loading and executing %s" % filename
	rps = 0
	full_line = ""
	for line in open(filename, "r"):
		line = line.strip()
		full_line += line
		rps += line.count("(")-line.count(")")
		if rps == 0 and full_line.strip() != "":
			try:
				tokens = tokenize(full_line)
				while len(tokens) > 0:
					val = eval(parse(tokens))
			except SystemExit:
				exit()
			except:
				handle_error()
				print "\nThe line in which the error occurred:\n%s" % full_line
				break
			full_line = ""

#### repl

def repl(prompt='tiddlylisp> '):
	"""
	A prompt-read-eval-print loop.
	"""
	try:
		while True:
			full_line = raw_input(prompt)
			rps = full_line.count("(")-full_line.count(")")
			while rps != 0 or full_line == "":
				line = raw_input(">\t")
				full_line += line
				rps += line.count("(")-line.count(")")
			try:
				tokens = tokenize(full_line)
				while len(tokens) > 0:
					val = eval(parse(tokens))
					if val is not None: print to_string(val)
			except (KeyboardInterrupt, SystemExit) as e:
				raise e
			except ValueError as e:
				print e.message
			except:
				handle_error()
	except (KeyboardInterrupt, SystemExit):
		print "\nExiting tiddlylisp\n"
	except:
		print "\nFatal Error\n"
		traceback.print_exc()
	exit()

#### error handling

def handle_error():
	"""
	Simple error handling for both the repl and load.
	"""
	print "An error occurred.  Here's the Python stack trace:\n"
	traceback.print_exc()
		
#### on startup from the command line

if __name__ == "__main__":
	if len(sys.argv) > 1:
		load(sys.argv[1])
	repl()

#### on startup from the command line

if __name__ == "__main__":
	if len(sys.argv) > 1:
		load(sys.argv[1])
	repl()
