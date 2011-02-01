from string import uppercase
symbols = ('~', '(', ')', '&', '|', '>>', '<<')

class Wff():
    def value(self, assignment):
        raise 'Abstract class error'
    def __invert__(self):
        return Negation(self)
    def __and__(self, other):
        return Conjunction(self, other)
    def __or__(self, other):
        return Disjunction(self, other)
    def __rshift__(self, other):
        return Implication(self, other)
    def __lshift__(self, other) :
        return Equality(self, other)

class Variable(Wff):
    def __init__(self, name):
        self.name = name
        self._value = None
    def value(self):
        return self._value
    def __repr__(self):
        return self.name

class Negation(Wff):
    def __init__(self, var):
        self.var = var
    def value(self):
        return not self.var.value()
    def __repr__(self):
        return '~%s' % self.var

class BoolOperator(Wff):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def value(self):
        raise 'Abstract class error'
    
class Conjunction(BoolOperator):
    def value(self):
        return self.left.value() & self.right.value()
    def __repr__(self):
        return '(%s&%s)' % (self.left, self.right)

class Disjunction(BoolOperator):
    def value(self):
        return self.left.value() | self.right.value()
    def __repr__(self):
        return '(%sv%s)' % (self.left, self.right)

class Implication(BoolOperator):
    def value(self):
        if self.left.value() == True:
            return self.right.value()
        else:
            return True
    def __repr__(self):
        return '(%s->%s)' % (self.left, self.right)
        
class Equality(BoolOperator):
    def value(self):
        return self.left.value() == self.right.value()
    def __repr__(self):
        return '(%s<->%s)' % (self.left, self.right)

def truth_table(f):
    lines = []
    
    # Replace input notation with python operators and remove whitespace
    f = f.replace('v', '|') # Disjunction
    f = f.replace('<->', '<<') # Equality
    f = f.replace('->', '>>') # Implication
    f = f.replace(' ', '')
    
    # Create a copy of f and test if it contains invalid symbols
    mod_f = f
    for s in symbols:
        mod_f = mod_f.replace(s, '')
    for c in mod_f:
        if c not in uppercase:
            return ['Input is not a wff, it contains invalid symbols']

    # Create instances of Variable for each letter present in mod_f
    # eg. if mod_f = 'AC': A = Variable('A'), C = Variable('C')
    vars = {}
    for c in mod_f:
        vars[c] = Variable(c)

    # One last horrible string hack. Replace all instances of uppercase letters
    # with vars['LETTER']
    for l in uppercase:
        f = f.replace(l, 'vars[\'%s\']' % l)
    
    # Try to evaluate the string f using python's native syntax evaluation.
    # This is a really cheap hack and doesn't perfectly conform to prop-calc's
    # lack of operator precedence.
    # eg. A&B->C is evaluated as the wff A&(B->C) due to python evaluating >>
    # before &.
    try:
        f = eval(f)
    except SyntaxError:
        return ['Input is not a wff']
    
    # Nicely format top row of table
    s = ''
    for v in vars:
        s += '%s&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp ' % v
    s += str(f)
    lines.append(s)
    
    # Make divider
    divider = ''
    for _ in vars:
        divider += '-----'
    for _ in str(f):
        divider += '--'
    lines.append(divider)

    # Test each possible truth value for each Variable and print a nicely
    # formatted truth table
    for n in xrange(0, 2**(len(vars))):
        s = ''
        for i, id in enumerate(vars):
            if i == 0: # Avoid division by 0
                vars[id]._value = bool(n%2)
            else:
                vars[id]._value = bool((n/(2*i))%2)
            s += '%s&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp '  % str(vars[id]._value)[0]
        s += '%s' % str(f.value())[0]
        lines.append(s)
        lines.append(divider)
    
    return lines