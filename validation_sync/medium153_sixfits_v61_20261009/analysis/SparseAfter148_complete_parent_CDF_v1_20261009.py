"""Signed sparse residuals applied after the entire frozen148 parent forecast."""
import numpy as np
from HuberCrossFamily_complete_parent_CDF_v1_20261008 import prepare,selected,apply_prepared,transform,pandas_oracle
HEADS=('sparse_l1','sparse_elastic')
GROUPS=tuple(((names,sign),) for names in (('sparse_l1',),('sparse_elastic',),HEADS) for sign in (1.,-1.))
def mixture(raw,group,share):
 assert group in range(6) and share==.5
 (names,sign),=GROUPS[group]
 value=np.asarray(raw[names[0]],dtype=np.float64).copy()
 if len(names)==2:value+=np.asarray(raw[names[1]],dtype=np.float64);value/=2.
 value*=sign
 assert np.isfinite(value).all()
 return value
def independent_mixture(raw,group,share):
 assert group in range(6) and share==.5
 (names,sign),=GROUPS[group]
 value=np.array(raw[names[0]],dtype=np.float64,copy=True)
 if len(names)==2:value=np.divide(np.add(value,raw[names[1]]),2.)
 return np.multiply(value,sign)
