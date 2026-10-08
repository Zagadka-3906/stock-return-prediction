"""New fixed-delta Huber residual recipe: streamed65-column IRLS with own-window L2 regularization."""
import numpy as np
from nonflag_residual_HGB_preprocessing_20261007 import prepare
from nonflag_residual_Ridge_codec_20261007 import export as linear_export,predict_native,predict_decoded as linear_decoded

BATCH_ROWS=8192
CONFIGS={f'nonflag_residual_huberIRLS64_d{suffix}':{'delta':delta,'alpha_per_training_row':.01,'max_iter':8,'tol':1e-6,
    'batch_rows':BATCH_ROWS,'target_not_clipped':True,'intercept_penalized':False,'initialization':'own_mature_L2_normal_equations'}
    for suffix,delta in (('010',.1),('025',.25))}


class HuberIRLS64:
    def __init__(self,cfg,rows):self.cfg=dict(cfg);self.alpha=rows*cfg['alpha_per_training_row'];self.n_features_in_=64
    def get_params(self):return {**self.cfg,'solver':'fixed8192_Huber_IRLS65_normal_equations','alpha':self.alpha}
    def predict(self,x):return np.matmul(x,self.coef_)+self.intercept_


def objective(raw,preprocessing,y,beta,cfg):
    total=0.;delta=cfg['delta']
    for left in range(0,len(y),BATCH_ROWS):
        x=prepare(raw[left:left+BATCH_ROWS],preprocessing);r=np.asarray(y[left:left+len(x)],dtype=np.float64)-(x@beta[:64]+beta[64]);a=np.abs(r)
        total+=float(np.sum(np.where(a<=delta,.5*r*r,delta*(a-.5*delta)),dtype=np.float64))
    return total+.5*(len(y)*cfg['alpha_per_training_row'])*float(beta[:64]@beta[:64])


def normal_equations(raw,preprocessing,y,beta,cfg):
    gram=np.zeros((65,65),dtype=np.float64);rhs=np.zeros(65,dtype=np.float64);blocks=0
    for left in range(0,len(y),BATCH_ROWS):
        x=prepare(raw[left:left+BATCH_ROWS],preprocessing);target=np.asarray(y[left:left+len(x)],dtype=np.float64)
        augmented=np.empty((len(x),65),dtype=np.float64);augmented[:,:64]=x;augmented[:,64]=1.
        weights=np.ones(len(x),dtype=np.float64) if beta is None else np.minimum(1.,cfg['delta']/np.maximum(np.abs(target-(x@beta[:64]+beta[64])),1e-12))
        gram+=augmented.T@(weights[:,None]*augmented);rhs+=augmented.T@(weights*target);blocks+=1
    gram[np.arange(64),np.arange(64)]+=len(y)*cfg['alpha_per_training_row']
    return gram,rhs,blocks


def fit_streamed(raw,preprocessing,y,cfg):
    from scipy.linalg import cho_factor,cho_solve
    assert raw.shape==(len(y),64) and len(y)>65 and np.isfinite(y).all()
    assert cfg['delta']>0. and cfg['alpha_per_training_row']>0. and cfg['batch_rows']==BATCH_ROWS
    gram,rhs,blocks=normal_equations(raw,preprocessing,y,None,cfg)
    beta=cho_solve(cho_factor(gram,lower=True,check_finite=True),rhs,check_finite=True)
    previous=objective(raw,preprocessing,y,beta,cfg);history=[]
    for iteration in range(cfg['max_iter']):
        gram,rhs,iteration_blocks=normal_equations(raw,preprocessing,y,beta,cfg)
        updated=cho_solve(cho_factor(gram,lower=True,check_finite=True),rhs,check_finite=True)
        value=objective(raw,preprocessing,y,updated,cfg);change=float(np.max(np.abs(updated-beta)))
        assert np.isfinite(updated).all() and value<=previous+1e-9*max(1.,abs(previous))
        history.append({'iteration':iteration+1,'training_objective':value,'coefficient_delta':change,'blocks':iteration_blocks})
        beta=updated;previous=value
        if change<cfg['tol']:break
    model=HuberIRLS64(cfg,len(y));model.coef_=beta[:64].copy();model.intercept_=float(beta[64]);model.n_iter_=len(history)
    return model,{'training_solver_recipe':'fixed8192_Huber_IRLS65_v1','actual_rows':len(y),'initial_blocks':blocks,
        'actual_iterations':len(history),'history':history,'converged_by_own_training_coefficient_tolerance':history[-1]['coefficient_delta']<cfg['tol'],
        'fixed_maximum_iterations_recipe_not_global_optimum_claim':True,'validation_early_stopping_or_target_clipping':False,
        'maximum_block_rows':BATCH_ROWS,'no_full_prepared_training_matrix_allocated':True}


def export(bundle):
    state=linear_export(bundle);state['kind']='nonflag_residual_HuberIRLS64';state['training_configuration']=bundle['model'].get_params();return state


def predict_decoded(state,raw):
    assert state['kind']=='nonflag_residual_HuberIRLS64' and state['batch_rows']==BATCH_ROWS
    proxy=dict(state);proxy['kind']='nonflag_residual_Ridge'
    return linear_decoded(proxy,raw)
