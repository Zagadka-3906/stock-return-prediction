"""Fixed-batch native and exported dense ElasticNet forecasts in target units."""
import numpy as np
from cpu_conditional_residual_mlp_codec_20261007 import fit_preprocessing,prepare
BATCH=8192

def target_scale(y):
    y=np.asarray(y,dtype=np.float64);center=float(y.mean());scale=float(y.std())
    assert np.isfinite(center) and np.isfinite(scale)
    return {'center':center,'scale':scale if scale>1e-12 else 1.}

def export(bundle):
    m=bundle['model'];assert m.coef_.ndim==1 and np.isfinite(m.coef_).all() and np.isfinite(m.intercept_)
    return {'kind':'sklearn_ElasticNet_dense_export','coef':m.coef_.tolist(),'intercept':float(m.intercept_),'preprocessing':bundle['preprocessing'],'target_scaling':bundle['target_scaling'],'features':bundle['features'],'native_parameters':m.get_params(),'native_iterations':int(m.n_iter_),'native_dual_gap':float(m.dual_gap_),'fixed_padded_inference_batch':BATCH,'dtype':'float64'}

def predict(bundle,raw,decoded=False):
    x=prepare(raw,bundle['preprocessing']);assert x.shape[1]==len(bundle['features'])
    if decoded:
        assert bundle['kind']=='sklearn_ElasticNet_dense_export' and bundle['fixed_padded_inference_batch']==BATCH
        coef=np.asarray(bundle['coef'],dtype=np.float64);intercept=float(bundle['intercept'])
    output=np.empty(len(x),dtype=np.float64);scaling=bundle['target_scaling']
    for left in range(0,len(x),BATCH):
        n=min(BATCH,len(x)-left);padded=np.zeros((BATCH,x.shape[1]),dtype=np.float64);padded[:n]=x[left:left+n]
        z=(padded@coef+intercept) if decoded else bundle['model'].predict(padded)
        output[left:left+n]=z[:n]*float(scaling['scale'])+float(scaling['center'])
    assert np.isfinite(output).all();return output

def predict_native(bundle,raw):return predict(bundle,raw,decoded=False)
def predict_decoded(state,raw):return predict(state,raw,decoded=True)
