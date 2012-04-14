Symbol = str
isa = isinstance

def tokenize(s):
	"Convert a string into a list of tokens."
	return s.replace("(", " ( ").replace(")", " ) ").replace("'"," ' ").split()

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
	elif "'" == token:
		return ['q',read_from(tokens)]
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