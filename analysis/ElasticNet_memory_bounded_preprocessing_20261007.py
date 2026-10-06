"""Own-fold raw63 median/mean/std with column-sized temporary arrays."""
import numpy as np

def fit_preprocessing(x):
    x=np.asarray(x,dtype=np.float64);assert x.ndim==2
    medians=[];means=[];scales=[]
    for c in x.T:
        finite=np.isfinite(c);median=float(np.median(c[finite])) if finite.any() else 0.
        clean=np.where(finite,c,median);mean=float(clean.mean());scale=float(clean.std())
        medians.append(median);means.append(mean);scales.append(scale if scale>1e-8 else 1.)
    return {'median':medians,'mean':means,'scale':scales,'clip':10.}

def prepare_training_fortran(x,preprocessing):
    x=np.asarray(x,dtype=np.float64);result=np.empty(x.shape,dtype=np.float64,order='F')
    for j,(med,mean,scale) in enumerate(zip(preprocessing['median'],preprocessing['mean'],preprocessing['scale'])):
        column=np.where(np.isfinite(x[:,j]),x[:,j],med)
        result[:,j]=np.clip((column-mean)/scale,-preprocessing['clip'],preprocessing['clip'])
    assert np.isfinite(result).all() and result.flags.f_contiguous
    return result
