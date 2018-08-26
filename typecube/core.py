
class Namespace(object):
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.types = {}

class Type(object):
    def __init__(self, name, args = None):
        self.name = name
        self.args = args or []
        self.validator = None

    def set_name(self, name):
        self.name = name
        return self

    def __repr__(self):
        out = "<%s(0x%x)" % (self.__class__.__name__, id(self))
        if self.name:
            out += ": " + self.name
        if self.args:
            out += " [%s]" % ", ".join(self.args)
        out += ">"
        return out

    def set_validator(self, validator):
        self.validator = validator
        return self

    def __getitem__(self, type_vals):
        if type(type_vals) is tuple:
            type_vals = list(iter(type_vals))
        elif type(type_vals) is not list:
            type_vals = [type_vals]
        param_values = dict(zip(self.args, type_vals))
        return self.apply(**param_values)

    def apply(self, **param_values):
        return TypeApp(self, **param_values)

class TypeVar(Type):
    """ A type variable.  """
    def __init__(self, name, args = None):
        assert name is not None and name.strip(), "Type vars MUST have names"
        Type.__init__(self, name, args)

class TypeApp(Type):
    """ Type applications allow generics to be concretized. """
    def __init__(self, target_type, **param_values):
        Type.__init__(self, target_type.name)
        self.param_values = param_values
        self.root_type = target_type
        if isinstance(target_type, TypeApp):
            self.root_type = target_type.root_type
            self.param_values.update(target_type.param_values)
            # now only update *new* values that have not been duplicated
            for k,v in param_values.iteritems():
                if k in target_type.args:
                    self.param_values[k] = v

class NativeType(Type):
    """ A native type whose details are not known but cannot be 
    inspected further - like a leaf type. 

    eg Array<T>, Map<K,V> etc
    """
    def __init__(self, name, args = None):
        Type.__init__(self, name, args)
        self.mapper_functor = None

class ContainerType(Type):
    """ Non leaf types.  These include:

        Product types (Records, Tuples, Named tuples etc) and 
        Sum types (Eg Unions, Enums (Tagged Unions), Algebraic Data Types.
    """
    def __init__(self, name, args = None):
        Type.__init__(self, name, args)
        self.child_types = []
        self.child_names = []

    def add(self, child_type, child_name = None):
        if child_name and child_name in self.child_names:
            assert False, "Child type with name '%s' already exists" % child_name
        self.child_types.append(child_type)
        self.child_names.append(child_name)
        return self

class RecordType(ContainerType): pass

class TupleType(ContainerType): pass

class UnionType(ContainerType): pass

class FunctionType(Type):
    input_types = None
    return_type = None

