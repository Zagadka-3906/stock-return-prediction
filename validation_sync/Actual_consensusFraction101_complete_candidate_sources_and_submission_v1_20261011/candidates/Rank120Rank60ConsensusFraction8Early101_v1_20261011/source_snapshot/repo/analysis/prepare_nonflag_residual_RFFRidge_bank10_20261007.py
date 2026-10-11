"""Prepare exact past-only RFF diagnostics and ten actual expanding-window fits."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    codec=A/'nonflag_residual_RFFRidge_codec_20261007.py'
    diagnostic=A/'verify_nonflag_residual_RFFRidge_codec2_20261007.py'
    training=A/'train_nonflag_residual_RFFRidge_bank10_20261007.py'
    assert not diagnostic.exists() and not training.exists()
    original_diagnostic=A/'verify_nonflag_residual_Ridge_codec2_20261007.py'
    original_training=A/'train_nonflag_residual_Ridge_bank10_20261007.py'
    d=original_diagnostic.read_text(encoding='utf8').replace('nonflag_residual_Ridge','nonflag_residual_RFFRidge')
    d=d.replace('from sklearn.linear_model import Ridge','from nonflag_residual_RFFRidge_codec_20261007 import make_model')
    d=d.replace("params={**plan['fixed_parameters'],'alpha':512*cfg['alpha_per_training_row']}","params={**cfg,'alpha':512*cfg['alpha_per_training_row']}")
    d=d.replace('model=Ridge(**params).fit(prepare(x[:512],prep),y[:512])','model=make_model(cfg,512).fit(prepare(x[:512],prep),y[:512])')
    compile(d,str(diagnostic),'exec');diagnostic.write_text(d,encoding='utf8',newline='\n')
    t=original_training.read_text(encoding='utf8').replace('nonflag_residual_Ridge','nonflag_residual_RFFRidge')
    t=t.replace('from sklearn.linear_model import Ridge','from nonflag_residual_RFFRidge_codec_20261007 import make_model')
    t=t.replace("params={**plan['fixed_parameters'],'alpha':len(indices)*cfg['alpha_per_training_row']}","params={**cfg,'alpha':len(indices)*cfg['alpha_per_training_row']}")
    t=t.replace('model=Ridge(**params).fit(bx,train_y)','model=make_model(cfg,len(indices)).fit(bx,train_y)')
    t=t.replace('independent_linear_state','independent_random_fourier_linear_state')
    t=t.replace('linear residual models','random Fourier residual models')
    compile(t,str(training),'exec');training.write_text(t,encoding='utf8',newline='\n')
    plan_path=A/'nonflag_residual_RFFRidge10_plan_20261007.json'
    create(plan_path,{'status':'frozen_before_actual_diagnostics_and10_mature_fits','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'training_population':'nonflag!=1, price_valid, finite own past OOF y_rank; exclusive mature annual cutoff',
        'target':'provided y_rank + .5 - qualified106 current-day all-forecast averageRank/N',
        'features':'63 provided-derived features + qualified106 current-day all-forecast averageRank/N',
        'preprocessing':'reuse identical own-window column finite median/mean/std and clip10 from verified HGB cache',
        'fixed_parameters':{'ridge_solver':'cholesky','fit_intercept':True,'copy_X':True},
        'configurations':{
            'nonflag_residual_rffridge_g003125':{'gamma':.03125,'n_components':32,'random_state':20261007,'alpha_per_training_row':.01},
            'nonflag_residual_rffridge_g025':{'gamma':.25,'n_components':32,'random_state':20261007,'alpha_per_training_row':.01}},
        'native_fit_years':[2021,2022,2023,2024,2025],'actual_declared_native_fits':10,'cpu_threads':2,
        'inference_recipe':'fixed8192 padded rows; native sklearn RBF sampler and Ridge, independent JSON Fourier frequencies offsets and coefficients',
        'resource_gate_available_RAM_GiB':12,'cache_location':'E:/赛题五_本机临时/nonflag_residual_HGB10_20261007',
        'new_large_feature_caches':0,'random_feature_mapping_fit_uses_training_feature_count_and_fixed_seed_no_validation_rows_or_labels':True,
        'official_scoring_requires_later_complete_future_source_admission':True,'test_labels_read':False})
    paths=[Path(__file__),codec,diagnostic,training,original_diagnostic,original_training]
    create(A/'nonflag_residual_RFFRidge_source_preparation_20261007.json',
        {'status':'compiled_new_RFFRidge_sources_before_any_actual_fit','input_sha256':{str(p):sha(p) for p in paths}})
    from verify_nonflag_residual_RFFRidge_codec2_20261007 import main as verify
    verify()
    proof_path=A/'nonflag_residual_RFFRidge_codec2_preflight_20261007/verification.json';proof=read(proof_path)
    assert proof['actual_diagnostic_fits']==2 and proof['status']=='passed_actual2_nonflag_residual_RFFRidge_historical_codec_controls'
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [*paths,proof_path]}}
    admission=A/'nonflag_residual_RFFRidge10_source_admission_20261007.json'
    create(admission,{'status':'passed_actual2_RFFRidge_codec_controls_and10_past_only_fit_admission','input_sha256':pins,
        'declared_native_fits':10,'actual_completed_native_fits':0,'actual_official_scores':0,'full_future_recipe_not_yet_admitted':True,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_residual_RFFRidge_native_bank10',training.name,[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_RFFRidge10_actual_hidden_launch_20261007.json',{'status':'started_actual_single_host_RFFRidge_native_bank','row':row,'input_sha256':pins,'actual_official_scores':0,'test_labels_read':False})
    print({'worker':row['owned_worker_pid'],'status':'started'},flush=True)
if __name__=='__main__':main()
