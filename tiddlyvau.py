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

	def find(self, var):
		"Find the innermost Env where var appears."
		if var in self:
			return self
		elif not self.outer is None:
			return self.outer.find(var)
		else: raise ValueError("%s is not defined"%(var,))

class Closure():
	def __init__(self, body, vars, env):
		self.body = body
		self.vars = vars
		self.env = env

	def __call__(self, *args, **kwargs):
		exps = [eval(exp, kwargs['v']) for exp in args]
		return eval(self.body, Env(zip(self.vars, exps), self.env))

class Vau():
	def __init__(self, body, vars, call_env_sym, clos_env):
		self.body = body
		self.vars = vars
		self.vars.append(call_env_sym)
		self.env = clos_env

	def __call__(self, *args, **kwargs):
		args.append(kwargs['v'])
		return eval(self.body, Env(zip(self.vars, args), self.env))
		
def define(var,exp,v=Env()):
	val = eval(exp, v)
	v[var] = val
	return val
	
def set(var, exp, v=Env()):
	val = eval(exp, v)
	env.find(var)[var] = val
	return val

def quote(exp,v=Env()): return exp

def cond(*x,**k):
	env = k['v']
	for (p, e) in x:
		if eval(p, env):
			return eval(e, env)
	raise ValueError("No Branch Evaluates to True")

def begin(*x,**k):
	env = k['v']
	val = 0
	for exp in x:
		val = eval(exp, env)
	return val
	
def vprint(x,v=Env()):
	val = eval(x, v)
	print to_string(val)
	return val
	
global_env = Env({
	'+':	lambda x,y,v=Env():eval(x,v)+eval(y,v),
	'-':	lambda x,y,v=Env():eval(x,v)-eval(y,v),
	'*':	lambda x,y,v=Env():eval(x,v)*eval(y,v),
	'/':	lambda x,y,v=Env():eval(x,v)/eval(y,v),
	'>':	lambda x,y,v=Env():eval(x,v)>eval(y,v),
	'<':	lambda x,y,v=Env():eval(x,v)<eval(y,v),
	'>=':	lambda x,y,v=Env():eval(x,v)>=eval(y,v),
	'<=':	lambda x,y,v=Env():eval(x,v)<=eval(y,v),
	'=':	lambda x,y,v=Env():eval(x,v)==eval(y,v),
	'eq?':	lambda x,y,v=Env():
				(lambda vx,vy: (not isa(vx, list)) and (vx == vy))(eval(x,v),eval(y,v)),
	'cons':	lambda x,y,v=Env():[eval(x,v)]+eval(y,v),
	'car':	lambda x,v=Env():eval(x,v)[0],
	'cdr':	lambda x,v=Env():eval(x,v)[1:],
	'list':	lambda *x,**k:[eval(expr, k['v']) for exp in x],
	'append':	lambda x,y,v=Env():eval(x,v)+eval(y,v),
	'len':	lambda x,v=Env():len(eval(x,v)),
	'null?':	lambda x,v=Env():eval(x,v)==[],
	'symbol?':	lambda x,v=Env():isa(eval(x,v),Symbol),
	'list?':	lambda x,v=Env():isa(eval(x,v),list),
	'atom?':	lambda x,v=Env():not isa(eval(x,v), list),
	'exit':		lambda v=Env:exit(),
	'True':		True,
	'False':	False,
	'if':		lambda test,conseq,alt,v=Env(): eval((conseq if eval(test,v) else alt), v),
	'cond':		cond,
	'define':	define,
	'set!':		set,
	'lambda':	lambda vars, body, v=Env(): Closure(body, vars, v),
	'vau':		lambda vars, env, body, v=Env(): Vau(body, vars, env, v),
	'q': quote,
	'quote': quote,
	'begin': begin,
	'print': vprint,
	'eval': lambda x,e,v=Env(): eval(x,e)
})

#### eval

def eval(x, env=global_env):
	"Evaluate an expression in an environment."
	val = x
	if isa(x, Symbol):			  # variable reference
		val = env.find(x)[x]
	elif isa(x, list):		  # (proc exp*)
		proc = eval(x[0], env)
		if hasattr(proc, '__call__'): val = proc(*x[1:],v=env)
		else: raise ValueError("%s = %s is not a procedure" % (to_string(x[0]),to_string(proc)))
	return val

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