"""Signed medium-neural rank mixing after the entire148 parent, including2020."""
import numpy as np
import BF16_complete_parent_rank_CDF_v1_20261008 as original
ROLES=original.ROLES
selected=original.selected
apply_prepared=original.apply_prepared

def signal(raw,valid,sign):
    assert sign in (-1.,1.)
    raw=np.asarray(raw);valid=np.asarray(valid,dtype=bool)
    assert raw.dtype==np.float64 and raw.ndim==valid.ndim==1 and raw.shape==valid.shape
    assert np.isfinite(raw).all()
    out=raw.copy();out[valid]*=float(sign)
    assert np.array_equal(out[~valid].view('u8'),raw[~valid].view('u8'))
    return out

def prepare(parent,raw,dates,flags,valid,sign):
    return original.prepare(parent,signal(raw,valid,sign),dates,flags,valid)

def transform(parent,raw,dates,flags,valid,role,weight,sign):
    return apply_prepared(parent,flags,valid,role,weight,prepare(parent,raw,dates,flags,valid,sign))

def pandas_oracle(parent,raw,dates,flags,valid,role,weight,sign):
    mask=np.asarray(valid,dtype=bool);independent=np.asarray(raw,dtype=np.float64).copy()
    if sign==-1.:independent[mask]=np.negative(np.asarray(raw)[mask])
    else:assert sign==1.
    return original.pandas_oracle(parent,independent,dates,flags,valid,role,weight)
