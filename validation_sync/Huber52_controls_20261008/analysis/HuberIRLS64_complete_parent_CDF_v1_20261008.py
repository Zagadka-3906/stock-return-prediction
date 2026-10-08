"""Signed fixed-Huber residuals followed by the existing causal complete-parent CDF recipe."""
import numpy as np
from CrossFamily_complete_parent_CDF_v1_20261008 import prepare,apply_prepared,transform,pandas_oracle
HEADS=('huber_d010','huber_d025')
MODES=((HEADS[:1],1.),(HEADS[1:],1.),(HEADS,1.),(HEADS[:1],-1.),(HEADS[1:],-1.),(HEADS,-1.))


def required_heads(group):return list(MODES[group][0])


def mixture(raw,group):
    names,sign=MODES[group]
    value=np.asarray(raw[names[0]],dtype=np.float64)
    if len(names)==2:value=(value+np.asarray(raw[names[1]],dtype=np.float64))/2.
    return sign*value


def independent_mixture(raw,group):
    names,sign=MODES[group]
    first=np.array(raw[names[0]],dtype=np.float64,copy=True)
    if len(names)==2:
        np.add(first,raw[names[1]],out=first);np.divide(first,2.,out=first)
    np.multiply(first,sign,out=first)
    return first
