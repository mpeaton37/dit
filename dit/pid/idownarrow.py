"""
The I_downarrow unique measure, proposed by Griffith et al, and shown to be inconsistent.

The idea is to measure unique information as the intrinsic mutual information between
and input and the output, given the other inputs. It turns out that these unique values
are inconsistent, in that they produce differing redundancy values.
"""

from __future__ import division

from .pid import BaseUniquePID

from ..multivariate import (intrinsic_total_correlation,
                            reduced_intrinsic_total_correlation,
                            minimal_intrinsic_total_correlation,
                           )
from ..utils import flatten


def i_downarrow(d, inputs, output):
    """
    This computes unique information as I(input : output \downarrow other_inputs).

    Parameters
    ----------
    d : Distribution
        The distribution to compute i_downarrow for.
    inputs : iterable of iterables
        The input variables.
    output : iterable
        The output variable.

    Returns
    -------
    ida : dict
        The value of I_downarrow for each individual input.
    """
    uniques = {}
    for input_ in inputs:
        others = list(inputs)
        others.remove(input_)
        others = list(flatten(others))
        uniques[input_] = intrinsic_total_correlation(d, [input_, output], others, nhops=25)
    return uniques


class PID_downarrow(BaseUniquePID):
    """
    The intrinsic mutual information partial information decomposition.

    Notes
    -----
    This decomposition is known to be invalid; that is, the redundancy values
    computed using either unique value are not consistent.
    """
    _name = "I_da"
    _measure = staticmethod(i_downarrow)


def i_double_downarrow(d, inputs, output):
    """
    This computes unique information as I(input : output \Downarrow other_inputs).

    Parameters
    ----------
    d : Distribution
        The distribution to compute i_double_downarrow for.
    inputs : iterable of iterables
        The input variables.
    output : iterable
        The output variable.

    Returns
    -------
    idda : dict
        The value of I_double_downarrow for each individual input.
    """
    uniques = {}
    for input_ in inputs:
        others = list(inputs)
        others.remove(input_)
        others = list(flatten(others))
        uniques[input_] = reduced_intrinsic_total_correlation(d, [input_, output], others, nhops=5)
    return uniques


class PID_double_downarrow(BaseUniquePID):
    """
    The reduced intrinsic mutual information partial information decomposition.
    """
    _name = "I_dda"
    _measure = staticmethod(i_double_downarrow)


def i_triple_downarrow(d, inputs, output):
    """
    This computes unique information as I(input : output \downarrow\downarrow\downarrow other_inputs).

    Parameters
    ----------
    d : Distribution
        The distribution to compute i_triple_downarrow for.
    inputs : iterable of iterables
        The input variables.
    output : iterable
        The output variable.

    Returns
    -------
    itda : dict
        The value of I_triple_downarrow for each individual input.
    """
    uniques = {}
    for input_ in inputs:
        others = list(inputs)
        others.remove(input_)
        others = list(flatten(others))
        uniques[input_] = minimal_intrinsic_total_correlation(d, [input_, output], others, nhops=5)
    return uniques


class PID_triple_downarrow(BaseUniquePID):
    """
    The minimal intrinsic mutual information partial information decomposition.
    """
    _name = "I_tda"
    _measure = staticmethod(i_triple_downarrow)
