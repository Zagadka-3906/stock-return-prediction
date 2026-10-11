"""Reverse only the predeclared residual; retain the original exact CDF recipe."""
import numpy as np
from nonflag_residual_HGB_CDF_transform_20261007 import prepare,apply_prepared as original_apply
def apply_prepared(parent,reference,flags,residual,weight,prepared):
    return original_apply(parent,reference,flags,-np.asarray(residual),weight,prepared)
def transform(parent,reference,dates,flags,valid,residual,weight,universe):
    return apply_prepared(parent,reference,flags,residual,weight,prepare(reference,dates,flags,valid,universe))
