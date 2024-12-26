def identity(*args):
    """Always returns the same value that was used as its argument.
    Example:
    >>> identity(1)
    1
    >>> identity(1, 2)
    (1, 2)
    """
    if len(args) == 1:
        return args[0]
    return args
