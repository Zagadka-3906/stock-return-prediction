"""New bounded ElasticNet objective on each own past-only centered Gram64."""
import numpy as np
from nonflag_residual_Ridge_codec_20261007 import BATCH_ROWS,predict_native
from nonflag_residual_HGB_preprocessing_20261007 import prepare
from nonflag_RFF128_streamed_gram_fitter_20261007 import prepared_sha

class SparseGram64:
    def __init__(self,cfg,training_rows):
        self.cfg=dict(cfg);self.n_features_in_=64;self.training_rows_=training_rows
    def get_params(self):return {**self.cfg,'solver':'own_centered_Gram64_cyclic_coordinate_descent','alpha':self.alpha_}
    def predict(self,x):
        assert x.ndim==2 and x.shape[1]==64
        return np.matmul(x,self.coef_)+self.intercept_

def fit_streamed(raw,preprocessing,y,cfg):
    assert raw.shape==(len(y),64) and len(y)>64 and np.isfinite(y).all()
    assert 0.<cfg['l1_ratio']<=1. and 0.<cfg['alpha_max_fraction']<1.
    count=len(y);sum_x=np.zeros(64);gram=np.zeros((64,64));rhs=np.zeros(64);sum_y=float(np.sum(y,dtype=np.float64));blocks=0
    for left in range(0,count,BATCH_ROWS):
        x=prepare(raw[left:left+BATCH_ROWS],preprocessing);target=np.asarray(y[left:left+len(x)],dtype=np.float64)
        sum_x+=x.sum(axis=0,dtype=np.float64);gram+=x.T@x;rhs+=x.T@target;blocks+=1
    mean_x=sum_x/count;mean_y=sum_y/count
    centered=(gram-np.outer(sum_x,sum_x)/count)/count;centered=(centered+centered.T)*.5
    values,vectors=np.linalg.eigh(centered);G=(vectors*np.maximum(values,0.))@vectors.T
    b=(rhs-sum_x*mean_y)/count
    alpha_max=float(np.max(np.abs(b))/cfg['l1_ratio']);alpha=max(alpha_max*cfg['alpha_max_fraction'],1e-15)
    l1=alpha*cfg['l1_ratio'];l2=alpha*(1.-cfg['l1_ratio']);coef=np.zeros(64);history=[]
    for iteration in range(cfg['max_iter']):
        before=coef.copy()
        for j in range(64):
            z=b[j]-G[j]@coef+G[j,j]*coef[j];denom=G[j,j]+l2
            coef[j]=np.sign(z)*max(abs(z)-l1,0.)/denom if denom>1e-15 else 0.
        delta=float(np.max(np.abs(coef-before)));gradient=G@coef-b+l2*coef
        violation=np.where(coef!=0.,np.abs(gradient+l1*np.sign(coef)),np.maximum(np.abs(gradient)-l1,0.))
        kkt=float(violation.max())
        if iteration%100==0 or (delta<=cfg['tol'] and kkt<=cfg['kkt_tol']):
            history.append({'iteration':iteration+1,'coefficient_delta':delta,'maximum_KKT_violation':kkt,'nonzero_coefficients':int(np.count_nonzero(coef))})
        if delta<=cfg['tol'] and kkt<=cfg['kkt_tol']:break
    assert np.isfinite(coef).all() and kkt<=cfg['kkt_tol'],('not_converged',iteration+1,kkt)
    model=SparseGram64(cfg,count);model.coef_=coef;model.intercept_=float(mean_y-mean_x@coef);model.alpha_=alpha;model.n_iter_=iteration+1
    return model,{'training_solver_recipe':'fixed8192_centered_Gram64_cyclic_ElasticNet_objective_v1',
      'objective':'squared_error/(2*N)+alpha*l1_ratio*abs(coef).sum()+alpha*(1-l1_ratio)*coef@coef/2',
      'actual_rows':count,'actual_blocks':blocks,'maximum_actual_block_rows':min(count,BATCH_ROWS),
      'alpha_max_own_training_only':alpha_max,'actual_alpha':alpha,'actual_iterations':iteration+1,
      'nonzero_coefficients':int(np.count_nonzero(coef)),'maximum_KKT_violation':kkt,'history':history,
      'centered_covariance_negative_eigenvalues_clipped_to_zero':True,'no_full_training_feature_matrix_allocated':True,
      'penalty_selected_from_own_mature_training_covariance_only':True}

def export(bundle):
    from nonflag_residual_Ridge_codec_20261007 import export as linear_export
    state=linear_export(bundle);state['kind']='nonflag_residual_SparseGram64';return state

def predict_decoded(state,raw):
    from nonflag_residual_Ridge_codec_20261007 import predict_decoded as linear_predict
    assert state['kind']=='nonflag_residual_SparseGram64'
    converted=dict(state);converted['kind']='nonflag_residual_Ridge'
    return linear_predict(converted,raw)
