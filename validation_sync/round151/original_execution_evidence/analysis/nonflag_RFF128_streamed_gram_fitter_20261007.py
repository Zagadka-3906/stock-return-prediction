"""New scientific recipe: fixed8192-row Fourier blocks and centered float64 Gram accumulation."""
import hashlib
import numpy as np
from nonflag_residual_RFF128_codec_20261007 import make_model,BATCH_ROWS
from nonflag_residual_HGB_preprocessing_20261007 import prepare

def prepared_sha(raw,preprocessing):
    digest=hashlib.sha256()
    for left in range(0,len(raw),BATCH_ROWS):
        block=prepare(raw[left:left+BATCH_ROWS],preprocessing)
        digest.update(memoryview(np.ascontiguousarray(block)).cast('B'))
    return digest.hexdigest()

def fit_streamed(raw,preprocessing,y,cfg):
    from scipy.linalg import cho_factor,cho_solve
    assert raw.shape==(len(y),64) and len(y)>0 and cfg['n_components']==128
    assert np.isfinite(y).all()
    model=make_model(cfg,len(y));projection=model.named_steps['rbf'];linear=model.named_steps['ridge']
    projection.fit(prepare(raw[:1],preprocessing))
    width=cfg['n_components'];sum_z=np.zeros(width);gram=np.zeros((width,width));rhs=np.zeros(width)
    sum_y=float(np.sum(y,dtype=np.float64));blocks=0;max_rows=0
    for left in range(0,len(raw),BATCH_ROWS):
        count=min(BATCH_ROWS,len(raw)-left);block=np.zeros((BATCH_ROWS,64),dtype=np.float64)
        block[:count]=prepare(raw[left:left+count],preprocessing)
        mapped=projection.transform(block)[:count]
        sum_z+=mapped.sum(axis=0,dtype=np.float64)
        gram+=mapped.T@mapped;rhs+=mapped.T@np.asarray(y[left:left+count],dtype=np.float64)
        blocks+=1;max_rows=max(max_rows,count)
    center=sum_z/len(y);target_mean=sum_y/len(y)
    covariance=gram-np.outer(sum_z,sum_z)/len(y)
    target_covariance=rhs-sum_z*target_mean
    covariance.flat[::width+1]+=len(y)*cfg['alpha_per_training_row']
    coef=cho_solve(cho_factor(covariance,lower=True,check_finite=True),target_covariance,check_finite=True)
    assert np.isfinite(coef).all()
    linear.coef_=coef;linear.intercept_=float(target_mean-center@coef);linear.n_features_in_=width;linear.n_iter_=None
    return model,{'training_solver_recipe':'fixed8192_padded_RBF128_centered_float64_Gram_cholesky_v1',
      'actual_rows':len(y),'actual_blocks':blocks,'maximum_actual_block_rows':max_rows,
      'no_full_training_random_feature_matrix_allocated':True,'alpha':len(y)*cfg['alpha_per_training_row'],
      'new_floating_point_accumulation_recipe_not_claimed_identical_to_dense_fit':True}
