"""Fixed-block own-window spectral truncation of centered64-column ridge normal equations."""
import numpy as np
from nonflag_residual_HGB_preprocessing_20261007 import prepare
from nonflag_residual_Ridge_codec_20261007 import export as linear_export,predict_native,predict_decoded as linear_decoded
BATCH_ROWS=8192
CONFIGS={f'nonflag_residual_spectralGram64_k{k:02d}':{'n_components':k,'alpha_per_training_row':.01,
    'batch_rows':BATCH_ROWS,'target_not_clipped':True,'intercept_penalized':False,'eigenvalues_order':'descending',
    'centered_covariance_symmetrized':True} for k in (8,16,32,48)}


class SpectralGram64:
    def __init__(self,cfg,rows):self.cfg=dict(cfg);self.alpha=rows*cfg['alpha_per_training_row'];self.n_features_in_=64
    def get_params(self):return {**self.cfg,'solver':'fixed8192_centered_top_eigen_Gram64','alpha':self.alpha}
    def predict(self,x):return np.matmul(x,self.coef_)+self.intercept_


def accumulate(raw,preprocessing,y):
    assert raw.shape==(len(y),64) and len(y)>64 and np.isfinite(y).all()
    gram=np.zeros((64,64),dtype=np.float64);rhs=np.zeros(64,dtype=np.float64);total=np.zeros(64,dtype=np.float64);blocks=0
    for left in range(0,len(y),BATCH_ROWS):
        x=prepare(raw[left:left+BATCH_ROWS],preprocessing);target=np.asarray(y[left:left+len(x)],dtype=np.float64)
        total+=x.sum(axis=0,dtype=np.float64);gram+=x.T@x;rhs+=x.T@target;blocks+=1
    rows=len(y);center=total/rows;target_mean=float(np.mean(y,dtype=np.float64))
    covariance=gram-np.outer(total,total)/rows;covariance=(covariance+covariance.T)*.5
    target_covariance=rhs-total*target_mean
    eigenvalues,eigenvectors=np.linalg.eigh(covariance)
    assert np.isfinite(eigenvalues).all() and np.isfinite(eigenvectors).all()
    assert eigenvalues.min()>=-1e-10*max(1.,float(eigenvalues.max()))
    order=np.arange(63,-1,-1);eigenvalues=eigenvalues[order].copy();eigenvectors=eigenvectors[:,order].copy()
    return {'rows':rows,'center':center,'target_mean':target_mean,'covariance':covariance,'target_covariance':target_covariance,
        'eigenvalues':eigenvalues,'eigenvectors':eigenvectors,'blocks':blocks}


def fit_from_statistics(stats,cfg):
    assert cfg in CONFIGS.values() and cfg['batch_rows']==BATCH_ROWS
    k=cfg['n_components'];rows=stats['rows'];basis=stats['eigenvectors'][:,:k]
    values=np.maximum(stats['eigenvalues'][:k],0.);alpha=rows*cfg['alpha_per_training_row']
    model=SpectralGram64(cfg,rows);model.coef_=basis@((basis.T@stats['target_covariance'])/(values+alpha))
    model.intercept_=float(stats['target_mean']-stats['center']@model.coef_)
    assert np.isfinite(model.coef_).all() and np.isfinite(model.intercept_)
    model.retained_eigenvalues_=values.copy();model.training_basis_=basis.copy()
    metadata={'training_solver_recipe':'fixed8192_centered_top_eigen_Gram64_v1','actual_rows':rows,'actual_blocks':stats['blocks'],
        'maximum_block_rows':BATCH_ROWS,'retained_components':k,'alpha':alpha,
        'retained_training_variance_fraction':float(values.sum()/max(1e-30,float(np.maximum(stats['eigenvalues'],0.).sum()))),
        'training_eigenvalue_cutoff':float(values[-1]),'training_eigenvalue_gap':float(stats['eigenvalues'][k-1]-stats['eigenvalues'][k]),
        'all_statistics_and_basis_from_own_training_window_only':True,'validation_early_stopping_or_target_clipping':False,
        'no_full_prepared_training_matrix_allocated':True,'new_floating_point_recipe_not_dense_fit_identity_claim':True}
    return model,metadata


def fit_streamed(raw,preprocessing,y,cfg):return fit_from_statistics(accumulate(raw,preprocessing,y),cfg)


def export(bundle):
    state=linear_export(bundle);state['kind']='nonflag_residual_SpectralGram64'
    state['training_configuration']=bundle['model'].get_params();return state


def predict_decoded(state,raw):
    assert state['kind']=='nonflag_residual_SpectralGram64' and state['batch_rows']==BATCH_ROWS
    proxy=dict(state);proxy['kind']='nonflag_residual_Ridge';return linear_decoded(proxy,raw)
