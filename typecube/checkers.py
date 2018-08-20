
# Type checkers for data given types

def type_check(thetype, data, bindings = None):
    """ Checks that a given bit of data conforms to the type provided 
    if isinstance(thetype, RecordType):
        for child in thetype.children:
            value = data[child.name]
            type_check(child.field_type, value)
    elif isinstance(thetype, TupleType):
        assert isinstance(data, tuple)
        assert len(tuple) == len(thetype.children)
        for value,childtype in zip(data, thetype.children):
            type_check(childtype, value)
    elif isinstance(thetype, UnionType):
        assert isinstance(thetype, dict)
        fields = [for child in thetype.children if child.name in data]
        assert len(fields) == 1, "0 or more than 1 entry in Union"
        type_check(fields[0].field_type, data[fields[0].name])
    elif isinstance(thetype, TypeApp):
        """ Type applications are tricky.  These will "affect" bindings """
        assert False

    # Finally apply any other validators that were nominated 
    # specifically for that particular type
    if thetype.validator:
        thetype.validator(thetype, data)