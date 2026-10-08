"""Own-window coefficient-constrained ridge using64-dimensional Cholesky-transformed NNLS."""
import numpy as np
from nonflag_SpectralGram64_streamed_v1_20261008 import accumulate,BATCH_ROWS
from nonflag_residual_Ridge_codec_20261007 import export as linear_export,predict_native,predict_decoded as linear_decoded
CONFIGS={f'nonflag_residual_coneRidge64_a{int(alpha*1000):03d}_{name}':{
    'alpha_per_training_row':alpha,'feature_sign':sign,'batch_rows':BATCH_ROWS,'maximum_nnls_iterations':1280,
    'target_not_clipped':True,'intercept_penalized':False,'centered_covariance_symmetrized':True}
    for alpha in (.01,.1) for name,sign in (('positive',1.),('negative',-1.))}

class ConeRidge64:
    def __init__(self,cfg,rows):self.cfg=dict(cfg);self.alpha=rows*cfg['alpha_per_training_row'];self.n_features_in_=64
    def get_params(self):return {**self.cfg,'solver':'fixed8192_centered_signed_ridge_NNLS64_Cholesky_v1','alpha':self.alpha}
    def predict(self,x):return np.matmul(x,self.coef_)+self.intercept_

def fit_from_statistics(stats,cfg):
    from scipy.optimize import nnls
    assert cfg in CONFIGS.values() and cfg['batch_rows']==BATCH_ROWS
    rows=stats['rows'];model=ConeRidge64(cfg,rows);sign=cfg['feature_sign']
    matrix=stats['covariance']+np.eye(64,dtype=np.float64)*model.alpha
    lower=np.linalg.cholesky(matrix);rhs=sign*stats['target_covariance'];transformed=np.linalg.solve(lower,rhs)
    positive,residual_norm=nnls(lower.T,transformed,maxiter=cfg['maximum_nnls_iterations'])
    model.coef_=sign*positive;model.intercept_=float(stats['target_mean']-stats['center']@model.coef_)
    model.nonnegative_parameters_=positive.copy();gradient=matrix@positive-rhs;active=positive>0.
    active_violation=float(np.max(np.abs(gradient[active]))) if active.any() else 0.
    inactive_violation=float(np.max(np.maximum(-gradient[~active],0.))) if (~active).any() else 0.
    violation=max(active_violation,inactive_violation)/max(1.,float(np.max(np.abs(rhs))))
    assert positive.shape==(64,) and np.isfinite(positive).all() and np.all(positive>=0.) and violation<1e-10
    assert np.isfinite(model.intercept_)
    metadata={'training_solver_recipe':'fixed8192_centered_signed_ridge_NNLS64_Cholesky_v1','actual_rows':rows,'actual_blocks':stats['blocks'],
        'maximum_block_rows':BATCH_ROWS,'alpha':model.alpha,'active_coefficients':int(active.sum()),
        'actual_relative_KKT_violation':violation,'actual64dim_transformed_residual_norm':float(residual_norm),
        'all_statistics_and_coefficient_constraints_from_own_training_window_only':True,
        'validation_early_stopping_or_target_clipping':False,'no_full_prepared_training_matrix_allocated':True,
        'new_constrained_solver_recipe_not_unconstrained_ridge_identity_claim':True}
    return model,metadata

def fit_streamed(raw,preprocessing,y,cfg):return fit_from_statistics(accumulate(raw,preprocessing,y),cfg)

def export(bundle):
    state=linear_export(bundle);state['kind']='nonflag_residual_ConeRidge64';state['training_configuration']=bundle['model'].get_params();return state

def predict_decoded(state,raw):
    assert state['kind']=='nonflag_residual_ConeRidge64' and state['batch_rows']==BATCH_ROWS
    proxy=dict(state);proxy['kind']='nonflag_residual_Ridge';return linear_decoded(proxy,raw)
