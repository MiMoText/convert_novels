'''Generic helper functions.'''


def remove_suffix(string, suffix):
    '''Like `str.removesuffix` for python versions < 3.9.'''
    if suffix and string.endswith(suffix):
        return string[:-len(suffix)]
    else:
        return string


def takewhile_incl(predicate, iterable):
    '''Just like `takewhile` from `itertools`, but includes the
    first item for which the predicate is False.
    '''
    for it in iterable:
        if predicate(it):
            yield it
        else:
            yield it
            break


def dropwhile_excl(predicate, iterable):
    '''Just like `dropwhile` from `itertools`, but it excludes the
    first item for which the predicate is False.
    '''
    already_split = False
    for it in iterable:
        if predicate(it) and not already_split:
            continue
        elif not already_split:
            already_split = True
            continue
        yield it
