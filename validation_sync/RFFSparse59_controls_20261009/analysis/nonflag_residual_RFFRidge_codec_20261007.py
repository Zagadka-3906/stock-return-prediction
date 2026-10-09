"""Native RBF random Fourier projection and independent JSON state, fixed padded rows."""
import numpy as np
from nonflag_residual_HGB_preprocessing_20261007 import prepare
BATCH_ROWS=8192

def make_model(cfg,training_rows):
    from sklearn.pipeline import Pipeline
    from sklearn.kernel_approximation import RBFSampler
    from sklearn.linear_model import Ridge
    return Pipeline([('rbf',RBFSampler(gamma=cfg['gamma'],n_components=cfg['n_components'],random_state=cfg['random_state'])),
        ('ridge',Ridge(alpha=training_rows*cfg['alpha_per_training_row'],solver='cholesky',fit_intercept=True,copy_X=True))])

def export(bundle):
    projection=bundle['model'].named_steps['rbf'];linear=bundle['model'].named_steps['ridge']
    assert projection.random_weights_.shape==(64,projection.n_components)
    assert linear.coef_.shape==(projection.n_components,)
    assert np.isfinite(projection.random_weights_).all() and np.isfinite(linear.coef_).all()
    return {'kind':'nonflag_residual_RFFRidge','batch_rows':BATCH_ROWS,
        'random_weights':projection.random_weights_.tolist(),'random_offset':projection.random_offset_.tolist(),
        'n_components':projection.n_components,'gamma':projection.gamma,'random_state':projection.random_state,
        'coefficients':linear.coef_.tolist(),'intercept':float(linear.intercept_),
        'preprocessing':bundle['preprocessing'],'features':bundle['features']}

def predict_native(bundle,raw):
    result=np.empty(len(raw),dtype=np.float64)
    for left in range(0,len(raw),BATCH_ROWS):
        n=min(BATCH_ROWS,len(raw)-left);block=np.zeros((BATCH_ROWS,64),dtype=np.float64)
        block[:n]=prepare(raw[left:left+n],bundle['preprocessing'])
        result[left:left+n]=bundle['model'].predict(block)[:n]
    return result

def predict_decoded(state,raw):
    assert state['kind']=='nonflag_residual_RFFRidge' and state['batch_rows']==BATCH_ROWS
    weights=np.asarray(state['random_weights'],dtype=np.float64);offset=np.asarray(state['random_offset'],dtype=np.float64)
    coef=np.asarray(state['coefficients'],dtype=np.float64);result=np.empty(len(raw),dtype=np.float64)
    assert weights.shape==(64,state['n_components']) and offset.shape==coef.shape==(state['n_components'],)
    for left in range(0,len(raw),BATCH_ROWS):
        n=min(BATCH_ROWS,len(raw)-left);block=np.zeros((BATCH_ROWS,64),dtype=np.float64)
        block[:n]=prepare(raw[left:left+n],state['preprocessing'])
        mapped=np.matmul(block,weights);mapped+=offset;np.cos(mapped,mapped)
        mapped*=(2.0/state['n_components'])**0.5
        result[left:left+n]=(np.matmul(mapped,coef)+state['intercept'])[:n]
    return result
