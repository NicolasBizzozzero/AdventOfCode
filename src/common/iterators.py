from itertools import islice


def batched(iterable, n: int, step: int = None, drop_last_if_shorter: bool = False):
    """
    Batch data into tuples of length n, with a configurable step.
    The last batch may be shorter but can be dropped.

    Parameters:
        iterable: The input iterable.
        n (int): The size of each batch.
        step (int, optional): The step size. Defaults to n.
        drop_last_if_shorter (bool, optional): If True, drop the last batch if it is shorter than n.

    Example usage:
    batched('ABCDEFG', 3) --> ['ABC', 'DEF', 'G']
    batched('ABCDEFG', 3, step=2) --> ['ABC', 'CDE', 'EFG']
    batched('ABCDEFG', 3, step=1, drop_last_if_shorter=True) --> ['ABC', 'BCD', 'CDE', 'DEF']
    """
    if n < 1:
        raise ValueError("n must be at least one")
    if step is None:
        step = n
    if step < 1:
        raise ValueError("step must be at least one")

    iterable = list(iterable)  # Convert to a list for easier slicing
    i = 0
    while i < len(iterable):
        batch = tuple(iterable[i : i + n])
        if drop_last_if_shorter and len(batch) < n:
            break
        yield batch
        i += step


def pair_by_pair(iterable: iter) -> tuple[int, int]:
    """Identical to itertools.pairwise"""
    for idx in range(len(iterable) - 1):
        yield iterable[idx], iterable[idx + 1]


def cycle(iterable: iter):
    while True:
        for element in iterable:
            yield element


def all_elements_except_one(iterable: iter):
    for idx in range(len(iterable)):
        yield iterable[:idx] + iterable[idx + 1 :]
