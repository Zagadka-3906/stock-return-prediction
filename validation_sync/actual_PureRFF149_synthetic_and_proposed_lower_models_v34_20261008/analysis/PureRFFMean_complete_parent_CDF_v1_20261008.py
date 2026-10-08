"""Pure mean of two saved RFF heads; all CDF arithmetic retains the original current-day complete universe."""
import numpy as np
from CrossFamilyFine_complete_parent_CDF_v1_20261008 import prepare,selected,apply_prepared,transform,pandas_oracle
HEADS=('rff_g00625','rff_g0125')
GROUPS=((),(),(),(),((HEADS,1.),))
def mixture(raw,group,share):
 assert group==4 and share==0.
 value=np.array(raw[HEADS[0]],dtype=np.float64,copy=True)
 value+=np.asarray(raw[HEADS[1]],dtype=np.float64);value/=2.
 assert np.isfinite(value).all();return value
def independent_mixture(raw,group,share):
 assert group==4 and share==0.
 return np.divide(np.add(np.asarray(raw[HEADS[0]],dtype=np.float64),np.asarray(raw[HEADS[1]],dtype=np.float64)),2.)
