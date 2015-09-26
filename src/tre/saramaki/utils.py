# -*- coding: UTF-8 -*-

import math

# from http://stackoverflow.com/a/312464/735926
def __chunks(l, n):
    """yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def mk_chunk_indexes(l, n):
    """
    Return a dict which maps an element of l to a chunk index, as if l was
    splitted into n chunks, assuming that l contains unique elements only.
    For example, with

        l=[3, 2, 5, 7, 1, 2]
        n=3

    l would be splitted into [[3, 2], [5, 7], [1, 2]], and thus the dict would
    be:
        { 3: 0, 2: 0,
          5: 1, 7: 1,
          1: 2, 2: 2  }

    Less chunks can be created than asked, for example with

        l=[1,2,3,4,5]
        n=3

    Only 3 chunks will be created instead of 4.
    """
    indexes = {}
    length = len(l)

    if length == 0:
        return indexes

    chunks = __chunks(l, int(math.ceil(length/float(n))))

    for i, chunk in enumerate(chunks):
        for el in chunk:
            indexes[el] = i

    return indexes

