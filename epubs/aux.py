'''Generic helper functions.'''


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
