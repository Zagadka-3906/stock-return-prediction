"""Reverse valid neural forecasts, preserve invalid sentinels, then mix complete-parent daily ranks."""
import numpy as np
import BF16_complete_parent_rank_CDF_v1_20261008 as original
ROLES=original.ROLES
selected=original.selected
apply_prepared=original.apply_prepared


def reversed_signal(neural,valid):
    value=np.asarray(neural)
    mask=np.asarray(valid,dtype=bool)
    assert value.dtype==np.float64 and value.ndim==mask.ndim==1 and value.shape==mask.shape
    assert np.isfinite(value).all()
    result=value.copy();result[mask]=-value[mask]
    assert np.array_equal(result[~mask].view('u8'),value[~mask].view('u8'))
    return result


def prepare(parent,neural,dates,flags,valid):
    return original.prepare(parent,reversed_signal(neural,valid),dates,flags,valid)


def transform(parent,neural,dates,flags,valid,role,weight):
    return apply_prepared(parent,flags,valid,role,weight,prepare(parent,neural,dates,flags,valid))


def pandas_oracle(parent,neural,dates,flags,valid,role,weight):
    # Independently construct the signed vector; never turn the invalid -1e6 sentinel into +1e6.
    mask=np.asarray(valid,dtype=bool);signal=np.asarray(neural,dtype=np.float64).copy()
    signal[mask]=np.negative(np.asarray(neural)[mask])
    return original.pandas_oracle(parent,signal,dates,flags,valid,role,weight)
