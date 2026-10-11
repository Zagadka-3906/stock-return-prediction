"""Own-window, fixed-step conjugate-gradient ridge on centered64-column training statistics."""
import numpy as np
from nonflag_SpectralGram64_streamed_v1_20261008 import accumulate,BATCH_ROWS
from nonflag_residual_Ridge_codec_20261007 import export as linear_export,predict_native,predict_decoded as linear_decoded

CONFIGS={f'nonflag_residual_krylovGram64_s{k:02d}':{'maximum_iterations':k,'alpha_per_training_row':.01,
    'batch_rows':BATCH_ROWS,'relative_residual_tolerance':1e-12,'target_not_clipped':True,'intercept_penalized':False,
    'initial_coefficient':'zero','centered_covariance_symmetrized':True} for k in (2,4,8,16)}

class KrylovGram64:
    def __init__(self,cfg,rows):self.cfg=dict(cfg);self.alpha=rows*cfg['alpha_per_training_row'];self.n_features_in_=64
    def get_params(self):return {**self.cfg,'solver':'fixed8192_centered_damped_CG64','alpha':self.alpha}
    def predict(self,x):return np.matmul(x,self.coef_)+self.intercept_

def fit_from_statistics(stats,cfg):
    assert cfg in CONFIGS.values() and cfg['batch_rows']==BATCH_ROWS
    rows=stats['rows'];model=KrylovGram64(cfg,rows)
    matrix=stats['covariance']+np.eye(64,dtype=np.float64)*model.alpha
    rhs=stats['target_covariance'];coef=np.zeros(64,dtype=np.float64);residual=rhs.copy();direction=residual.copy()
    squared=float(residual@residual);initial=squared;iterations=0
    for iteration in range(cfg['maximum_iterations']):
        if squared<=initial*cfg['relative_residual_tolerance']**2:break
        product=matrix@direction;denominator=float(direction@product);assert denominator>0 and np.isfinite(denominator)
        step=squared/denominator;coef+=step*direction;residual-=step*product
        updated=float(residual@residual);direction=residual+(updated/squared)*direction;squared=updated;iterations=iteration+1
    model.coef_=coef;model.intercept_=float(stats['target_mean']-stats['center']@coef);model.actual_iterations_=iterations
    assert np.isfinite(coef).all() and np.isfinite(model.intercept_)
    metadata={'training_solver_recipe':'fixed8192_centered_damped_CG64_v1','actual_rows':rows,'actual_blocks':stats['blocks'],
        'maximum_block_rows':BATCH_ROWS,'maximum_iterations':cfg['maximum_iterations'],'actual_iterations':iterations,'alpha':model.alpha,
        'relative_normal_equation_residual':float(np.sqrt(squared/max(initial,1e-300))),
        'all_statistics_and_stopping_from_own_training_window_only':True,'validation_early_stopping_or_target_clipping':False,
        'no_full_prepared_training_matrix_allocated':True,'new_truncated_solver_recipe_not_full_ridge_identity_claim':True}
    return model,metadata

def fit_streamed(raw,preprocessing,y,cfg):return fit_from_statistics(accumulate(raw,preprocessing,y),cfg)

def export(bundle):
    state=linear_export(bundle);state['kind']='nonflag_residual_KrylovGram64';state['training_configuration']=bundle['model'].get_params();return state

def predict_decoded(state,raw):
    assert state['kind']=='nonflag_residual_KrylovGram64' and state['batch_rows']==BATCH_ROWS
    proxy=dict(state);proxy['kind']='nonflag_residual_Ridge';return linear_decoded(proxy,raw)
