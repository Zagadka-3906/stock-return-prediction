"""New model recipe: bounded columnwise training-only location and scale statistics."""
import numpy as np
from memory_bounded_numeric_preparation_20261007 import prepare
def fit_preprocessing(x):
    assert x.ndim==2 and x.shape[1]==64 and len(x)>0
    median=[];mean=[];scale=[]
    for j in range(x.shape[1]):
        column=np.asarray(x[:,j],dtype=np.float64);finite=np.isfinite(column)
        med=float(np.median(column[finite])) if finite.any() else 0.
        clean=np.where(finite,column,med)
        avg=float(clean.mean());std=float(clean.std());std=std if std>1e-8 else 1.
        median.append(med);mean.append(avg);scale.append(std)
    return {'median':median,'mean':mean,'scale':scale,'clip':10.}
