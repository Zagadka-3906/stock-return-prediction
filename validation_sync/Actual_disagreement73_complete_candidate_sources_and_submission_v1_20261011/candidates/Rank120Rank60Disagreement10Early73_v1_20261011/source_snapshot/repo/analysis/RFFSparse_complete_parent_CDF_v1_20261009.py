"""Signed RFF and sparse residual mixtures on the complete parent's daily CDF."""
import numpy as np
from RFFCrossFamily_complete_parent_CDF_v1_20261008 import prepare, selected, apply_prepared, transform, pandas_oracle

HEADS=('rff_g00625','rff_g0125','sparse_l1','sparse_elastic')
GROUPS=tuple(((('rff_g00625','rff_g0125'),1.),(names,sign))
             for names in (('sparse_l1',),('sparse_elastic',),('sparse_l1','sparse_elastic'))
             for sign in (1.,-1.))


def mixture(raw,group,share):
    assert group in range(len(GROUPS)) and share in (.25,.5,.75)
    parts=[]
    for names,sign in GROUPS[group]:
        part=np.asarray(raw[names[0]],dtype=np.float64).copy()
        if len(names)==2:
            part+=np.asarray(raw[names[1]],dtype=np.float64)
            part/=2.
        part*=sign
        parts.append(part)
    parts[0]*=float(share)
    parts[1]*=1.-float(share)
    parts[0]+=parts[1]
    assert np.isfinite(parts[0]).all()
    return parts[0]


def independent_mixture(raw,group,share):
    (names0,sign0),(names1,sign1)=GROUPS[group]
    a=np.array(raw[names0[0]],dtype=np.float64,copy=True)
    b=np.array(raw[names1[0]],dtype=np.float64,copy=True)
    if len(names0)==2:
        a=np.divide(np.add(a,raw[names0[1]]),2.)
    if len(names1)==2:
        b=np.divide(np.add(b,raw[names1[1]]),2.)
    a=np.multiply(np.multiply(a,sign0),float(share))
    b=np.multiply(np.multiply(b,sign1),1.-float(share))
    return np.add(a,b)
