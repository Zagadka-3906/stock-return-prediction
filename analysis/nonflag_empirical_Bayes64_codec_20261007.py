"""New past-only empirical Bayes linear residuals with scalar or diagonal learned priors."""
import numpy as np
from nonflag_residual_Ridge_codec_20261007 import export,predict_native,predict_decoded,BATCH_ROWS
from nonflag_residual_HGB_preprocessing_20261007 import prepare
from nonflag_RFF128_streamed_gram_fitter_20261007 import prepared_sha

class EmpiricalBayes64:
    def __init__(self,cfg,training_rows):
        self.cfg=dict(cfg);self.alpha=training_rows*cfg['alpha_per_training_row'];self.n_features_in_=64
    def get_params(self):return {**self.cfg,'solver':'empirical_bayes_centered_Gram64','alpha':self.alpha}
    def predict(self,x):
        assert x.ndim==2 and x.shape[1]==64
        return np.matmul(x,self.coef_)+self.intercept_

def fit_streamed(raw,preprocessing,y,cfg):
    from scipy.linalg import cho_factor,cho_solve
    assert raw.shape==(len(y),64) and len(y)>64 and cfg['mode'] in ('scalar','diagonal')
    assert np.isfinite(y).all()
    count=len(y);sum_x=np.zeros(64);gram=np.zeros((64,64));rhs=np.zeros(64);sum_y=float(np.sum(y,dtype=np.float64));sum_y2=float(y@y)
    blocks=0;max_rows=0
    for left in range(0,count,BATCH_ROWS):
        x=prepare(raw[left:left+BATCH_ROWS],preprocessing);target=np.asarray(y[left:left+len(x)],dtype=np.float64)
        sum_x+=x.sum(axis=0,dtype=np.float64);gram+=x.T@x;rhs+=x.T@target
        blocks+=1;max_rows=max(max_rows,len(x))
    mean_x=sum_x/count;mean_y=sum_y/count
    centered=gram-np.outer(sum_x,sum_x)/count;centered=(centered+centered.T)*.5
    eigenvalues,vectors=np.linalg.eigh(centered)
    corrected=(vectors*np.maximum(eigenvalues,0.))@vectors.T
    target_cov=rhs-sum_x*mean_y;target_sum_squares=max(sum_y2-sum_y*sum_y/count,1e-12)
    precision=np.full(64,count*cfg['alpha_per_training_row']);noise=float(count/target_sum_squares);previous=np.zeros(64);history=[]
    for iteration in range(cfg['max_iter']):
        system=noise*corrected+np.diag(precision)
        factor=cho_factor(system,lower=True,check_finite=True)
        covariance=cho_solve(factor,np.eye(64),check_finite=True)
        coef=cho_solve(factor,noise*target_cov,check_finite=True)
        effective=np.clip(1.-precision*np.diag(covariance),0.,1.)
        rss=max(target_sum_squares-2.*coef@target_cov+coef@corrected@coef,1e-12)
        next_noise=np.clip((count-effective.sum()+2e-6)/(rss+2e-6),1e-8,1e12)
        if cfg['mode']=='scalar':next_precision=np.full(64,(effective.sum()+2e-6)/(coef@coef+2e-6))
        else:next_precision=(effective+2e-6)/(coef*coef+2e-6)
        next_precision=np.clip(next_precision,1e-6,1e10)
        delta=float(np.max(np.abs(coef-previous)));history.append({'iteration':iteration+1,'coefficient_delta':delta,'effective_features':float(effective.sum()),'noise_precision':float(noise),'residual_sum_squares':float(rss)})
        if iteration>0 and delta<cfg['tol']:break
        precision,noise=next_precision,float(next_noise);previous=coef
    assert np.isfinite(coef).all()
    model=EmpiricalBayes64(cfg,count);model.coef_=coef;model.intercept_=float(mean_y-mean_x@coef)
    model.noise_precision_=float(noise);model.prior_precision_=precision.copy();model.n_iter_=len(history)
    return model,{'training_solver_recipe':'fixed8192_centered_Gram64_empirical_Bayes_scalar_or_diagonal_v1',
      'mode':cfg['mode'],'actual_rows':count,'actual_blocks':blocks,'maximum_actual_block_rows':max_rows,
      'actual_iterations':len(history),'noise_precision':float(noise),'learned_prior_precision':precision.tolist(),
      'initial_prior_precision_only':model.alpha,'alpha_parameter_is_initial_prior_not_final_fixed_Ridge_penalty':True,
      'covariance_negative_eigenvalues_clipped_to_zero_before_iterations':True,'history':history,
      'all_learned_precisions_use_only_own_mature_training_rows':True,'no_full_training_feature_matrix_allocated':True}
