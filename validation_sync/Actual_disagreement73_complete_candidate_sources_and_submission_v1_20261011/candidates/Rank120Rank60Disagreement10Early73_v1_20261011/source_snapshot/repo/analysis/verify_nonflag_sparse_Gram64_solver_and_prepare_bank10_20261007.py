"""Independent sklearn objective/KKT controls before ten past-only residual fits."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    import numpy as np,joblib
    from sklearn.linear_model import ElasticNet
    from threadpoolctl import threadpool_limits
    from nonflag_sparse_Gram64_codec_20261007 import fit_streamed,export,predict_native,predict_decoded
    from nonflag_residual_HGB_preprocessing_20261007 import fit_preprocessing,prepare
    cfgs={'nonflag_residual_sparseGram64_L1':{'l1_ratio':1.,'alpha_max_fraction':.02,'max_iter':10000,'tol':1e-10,'kkt_tol':1e-8},
      'nonflag_residual_sparseGram64_Elastic':{'l1_ratio':.5,'alpha_max_fraction':.02,'max_iter':10000,'tol':1e-10,'kkt_tol':1e-8}}
    out=A/'nonflag_sparse_Gram64_actual_solver_controls_20261007';assert not out.exists();out.mkdir()
    rng=np.random.default_rng(20261007);raw=rng.normal(size=(1025,64));raw[:,1]=raw[:,0]+rng.normal(scale=.03,size=len(raw));raw[4,8]=np.nan;raw[9,3]=np.inf
    y=.12*raw[:,0]-.075*raw[:,4]+.02*raw[:,12]+rng.normal(scale=.02,size=len(raw));prep=fit_preprocessing(raw);x=prepare(raw,prep);records=[]
    with threadpool_limits(limits=2):
        for name,cfg in cfgs.items():
            model,info=fit_streamed(raw,prep,y,cfg);reference=ElasticNet(alpha=model.alpha_,l1_ratio=cfg['l1_ratio'],fit_intercept=True,max_iter=20000,tol=1e-12,selection='cyclic').fit(x,y)
            error=float(np.max(np.abs(model.coef_-reference.coef_)));assert error<1e-7,(name,error)
            assert abs(model.intercept_-reference.intercept_)<1e-8
            objective=lambda c,i:float(np.mean((y-x@c-i)**2)/2+model.alpha_*cfg['l1_ratio']*np.abs(c).sum()+model.alpha_*(1.-cfg['l1_ratio'])*(c@c)/2)
            obj=objective(model.coef_,model.intercept_);refobj=objective(reference.coef_,reference.intercept_);assert abs(obj-refobj)<1e-10
            bundle={'model':model,'preprocessing':prep,'features':[f'provided_{i}' for i in range(64)]};path=out/(name+'.joblib');joblib.dump(bundle,path);saved=joblib.load(path);state=export(bundle);full=predict_native(bundle,raw)
            assert np.array_equal(full.view('u8'),predict_native(saved,raw).view('u8')) and np.array_equal(full.view('u8'),predict_decoded(state,raw).view('u8'))
            for n in (1,80,260,975):assert np.array_equal(full[:n].view('u8'),predict_decoded(state,raw[:n]).view('u8'))
            bad=y.copy();bad[0]=np.nan
            try:fit_streamed(raw,prep,bad,cfg)
            except AssertionError:pass
            else:raise AssertionError('nonfinite training target accepted')
            records.append({'model':name,'maximum_coefficient_error_vs_sklearn':error,'objective':obj,'reference_objective':refobj,'maximum_KKT_violation':info['maximum_KKT_violation'],'native_reload_and_independent_decoded_all_bits_exact':True,'cold_prefixes':[1,80,260,975],'nonfinite_target_rejected':True})
    old=A/'train_nonflag_residual_EmpiricalBayes64_bank10_v1_20261007.py';new=A/'train_nonflag_residual_SparseGram64_bank10_v1_20261007.py'
    text=old.read_text(encoding='utf8').replace('EmpiricalBayes64','SparseGram64').replace('EmpiricalBayes6410','SparseGram6410').replace('nonflag_empirical_Bayes64_codec','nonflag_sparse_Gram64_codec')
    text=text.replace("params={**cfg,'alpha':len(indices)*cfg['alpha_per_training_row']}","params=dict(cfg)")
    text=text.replace("create(state_path,export(bundle))","create(state_path,export(bundle));params.update(model.get_params())")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    plan=A/'nonflag_residual_SparseGram6410_plan_20261007.json'
    create(plan,{'status':'frozen_new_sparse_residual_Gram64_L1_and_Elastic_before_actual_fits','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'configurations':cfgs,'native_fit_years':[2021,2022,2023,2024,2025],'actual_declared_native_fits':10,
      'target':'provided y_rank+.5-qualified106 same-day all-forecast averageRank/N',
      'features':'63 provided-derived plus teacher106 same-day averageRank/N','training_population':'nonflag!=1, price_valid, finite target, own exclusive mature annual cutoff',
      'penalty_scaling':'alpha_max from own training covariance times .02; L1 ratio1 or.5',
      'preprocessing':'unchanged verified own-window medians/means/scales/clip10',
      'inference_recipe':'fixed8192 padded rows and independent64 coefficients',
      'new_large_feature_caches':0,'test_labels_read':False,'actual_official_scores':0,
      'new_floating_point_solver_recipe_not_claimed_bit_equal_to_sklearn':True})
    pins={str(p):sha(p) for p in [Path(__file__),A/'nonflag_sparse_Gram64_codec_20261007.py',new,plan,A/'nonflag_residual_Ridge_codec_20261007.py',A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'nonflag_RFF128_streamed_gram_fitter_20261007.py']}
    create(out/'verification.json',{'status':'passed_actual2_sparseGram64_independent_sklearn_objective_KKT_and_native_codec_controls','input_sha256':pins,'records':records,'new_official_scores':0,'not_real_validation_scores':True})
    admission=A/'nonflag_residual_SparseGram6410_source_admission_v1_20261007.json'
    create(admission,{'status':'passed_actual2_SparseGram64_codec_controls_and10_past_only_fit_admission','input_sha256':{**pins,str(out/'verification.json'):sha(out/'verification.json')},'actual_solver_control_cases':2,'real_train_fits_not_yet_claimed':True,'new_official_scores':0})
    row=start('nonflag_residual_SparseGram64_native_bank10',new.name,[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_SparseGram64_native_bank10_hidden_launch_20261007.json',{'status':'started_hidden_actual10_sparse_residual_fits','identity':row})
    print('PASS independent sparse solver controls; started ten actual own mature fits',flush=True)

if __name__=='__main__':main()
