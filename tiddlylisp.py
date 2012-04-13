#### tiddlylisp.py
#
# Based on Peter Norvig's lispy (http://norvig.com/lispy.html),
# copyright by Peter Norvig, 2010.
#
# Adaptations by Michael Nielsen.  See
# http://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/

import sys
import traceback
import operator

#### Symbol, Env classes

Symbol = str
isa = isinstance

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

global_env = Env({
    '+':    operator.add,
    '-':    operator.sub,
    '*':    operator.mul,
    '/':    operator.div,
    '>':    operator.gt,
    '<':    operator.lt,
    '>=':   operator.ge,
    '<=':   operator.le,
    '=':    operator.eq,
    'eq?':    lambda x,y:(not isa(x, list)) and (x == y),
    'cons':   lambda x,y:[x]+y,
    'car':    lambda x:x[0],
    'cdr':    lambda x:x[1:],
    'list':   lambda *x:list(x),
    'append':operator.add,
    'len':    len,
    'null?':    lambda x:x==[],
    'symbol?':  lambda x:isa(x,Symbol),
    'list?':    lambda x:isa(x,list),
    'atom?':    lambda x:not isa(x, list),
    'exit': exit,
    'True': True,
    'False': False
})

#### eval

def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isa(x, Symbol):              # variable reference
        return env.find(x)[x]
    elif not isa(x, list):          # constant literal
        return x
    elif x[0] == 'quote' or x[0] == 'q': # (quote exp), or (q exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':              # (if test conseq alt)
        (_, test, conseq, alt) = x
        return eval((conseq if eval(test, env) else alt), env)
    elif x[0] == 'cond':            # (cond (p1 e1) ... (pn en))
        for (p, e) in x[1:]:
            if eval(p, env):
                return eval(e, env)
        raise ValueError("No Branch Evaluates to True")
    elif x[0] == 'set!':            # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'define':          # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'lambda':          # (lambda (var*) exp)
        (_, vars, exp) = x
        return lambda *args: eval(exp, Env(zip(vars, args), env))
    elif x[0] == 'begin':           # (begin exp*)
        for exp in x[1:]:
            val = eval(exp, env)
        return val
    else:                           # (proc exp*)
        exps = [eval(exp, env) for exp in x]
        proc = exps.pop(0)
        if hasattr(proc, '__call__'): return proc(*exps)
        else: raise ValueError("%s is not a procedure" % (to_string(x[0]),))

#### parsing

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace("(", " ( ").replace(")", " ) ").split()

def parse(tokens):
    "Parse a Lisp expression from a string."
    return read_from(tokens)

def read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    if not isa(exp, list):
        return str(exp)
    else:
        return '('+' '.join(map(to_string, exp))+')'

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
                    if val is not None: print to_string(val)
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