"""Apply unchanged numeric preprocessing in bounded row blocks."""
import numpy as np
from cpu_conditional_residual_mlp_codec_20261007 import prepare as original_prepare

BATCH_ROWS=8192

def prepare(x,preprocessing):
    x=np.asarray(x)
    if x.ndim!=2:
        return original_prepare(x,preprocessing)
    original_prepare(x[:0],preprocessing)
    values=np.empty(x.shape,dtype=np.float64,order='C')
    for left in range(0,len(x),BATCH_ROWS):
        right=min(len(x),left+BATCH_ROWS)
        values[left:right]=original_prepare(x[left:right],preprocessing)
    return values
