"""
    Functions for generating sigma algebras.

    http://users.ices.utexas.edu/~chetan/talks/tech_report_sigma_algebra.pdf

"""

from collections import defaultdict

import numpy as np

__all__ = ['is_sigma_algebra', 'sigma_algebra']

def sets2matrix(C, X=None):
    """Returns the sets in C as binary strings representing elements in X.

    Paramters
    ---------
    C : set of frozensets
        The set of subsets of X.
    X : frozenset, None
        The underlying set. If None, then X is taken to be the union of the
        sets in C.

    Returns
    -------
    Cmatrix : NumPy array, shape ( len(C), len(X) )
        The 0-1 matrix whose rows represent sets in C. The columns tell us
        if the corresponding element in X is present in the subset of C.
    X : frozenset
        The underlying set that was used to construct Cmatrix.

    """
    # make sure C consists of frozensets and that X is frozen
    C = set([frozenset(c) for c in C])
    if X is None:
        X = set([])
        for cet in C:
            X.update(cet)
    X = frozenset(X)

    # Each element of C will be represented as a binary string of 0s and 1s.
    # Note, X is frozen, so its iterating order is constant.
    Cmatrix = [[ 1 if x in cet else 0 for x in X ] for cet in C]
    Cmatrix = np.array(Cmatrix, dtype=int)

    return Cmatrix, X

def unique_columns(Cmatrix):
    """Returns a dictionary mapping columns to identical column indexes.

    Parameters
    ----------
    Cmatrix : NumPy array
        A 0-1 matrix whose rows represent subsets of an underlying set. The
        columns express membership of the underlying set's elements in the
        subset.

    Returns
    -------
    unique_cols : defaultdict(set)
        A dictionary mapping columns in Cmatrix to sets of column indexes.
        All indexes in the same set represent identical columns.

    """
    unique_cols = defaultdict(set)
    for idx, col in enumerate(Cmatrix.transpose()):
        unique_cols[tuple(col)].add(idx)
    return unique_cols

def sigma_algebra(C, X=None):
    """Returns the sigma algebra generated by the subsets in C.

    Let X be a set and C be a collection of subsets of X.  The sigma algebra
    generated by the subsets in C is the smallest sigma-algebra which contains
    every subset in C.

    Parameters
    ----------
    C : set of frozensets
        The set of subsets of X.
    X : frozenset, None
        The underlying set. If None, then X is taken to be the union of the
        sets in C.

    Returns
    -------
    sC : frozenset of frozensets
        The sigma-algebra generated by C.

    Notes
    -----
    The algorithm run time is generally exponential in |X|, the size of X.

    """
    from cmpy.util import words_iter

    Cmatrix, X = sets2matrix(C, X)
    unique_cols = unique_columns(Cmatrix)

    # Create a lookup from column IDs representing identical columns to the
    # index of a unique representative.  This will be used to repopulate the
    # larger binary string representation.
    lookups = {}
    reps = []
    for indexes in unique_cols.itervalues():
        representative = min(indexes)
        reps.append(representative)
        for index in indexes:
            lookups[index] = representative
    reps.sort()

    # The total number of elements is given by the powerset on all unique
    # indexes. That is, we just generate all binary strings. Then, for each
    # binary string, we construct the subset in the sigma algebra.
    indexes = range(len(X))
    sC = set([])
    for word in words_iter(alphabet=[0,1], L=len(unique_cols)):
        subset = [ x for i,x in enumerate(X) if word[lookups[i]] == 1]
        sC.add( frozenset(subset) )
    sC = frozenset(sC)

    return sC

def is_sigma_algebra(F, X=None):
    """Returns True if F is a sigma algebra on X.

    Parameters
    ----------
    F : set of frozensets
        The candidate sigma algebra.
    X : frozenset, None
        The universal set. If None, then X is taken to be the union of the
        sets in F.

    Returns
    -------
    issa : bool
        True if F is a sigma algebra and False if not.

    Notes
    -----
    The time complexity of this algorithm is O ( len(F) * len(X) ).

    """
    # Unsure if this algorithm is "if and only if". The idea is to construct
    # the matrix representing F. Then count the number of redundant columns.
    # Denote this number by q. If F is a sigma algebra, then we must have:
    #    len(F) == 2**(len(X) - q)).
    # However, it isn't clear if one could have a non-sigma algebra whose
    # matrix also has this property.

    Fmatrix, X = sets2matrix(F, X)
    unique_cols = unique_columns(Fmatrix)

    if len(F) == 2**len(unique_cols):
        return True
    else:
        return False

def is_sigma_algebra__brute(F, X=None):
    """Returns True if F is a sigma algebra on X.

    Parameters
    ----------
    F : set of frozensets
        The candidate sigma algebra.
    X : frozenset, None
        The universal set. If None, then X is taken to be the union of the
        sets in F.

    Returns
    -------
    issa : bool
        True if F is a sigma algebra and False if not.

    Notes
    -----
    This is a brute force check against the definition of a sigma algebra.
    Its time complexity is O( len(F)**2 ).

    """
    if X is None:
        X = set([])
        for cet in F:
            X.update(cet)
    X = frozenset(X)

    for subset1 in F:
        if X.difference(subset1) not in F:
            return False
        for subset2 in F:
            if subset1.union(subset2) not in F:
                return False
    else:
        return True
