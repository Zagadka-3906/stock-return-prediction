"""Freeze the new family, execute diagnostics, then launch one local native bank."""
from pathlib import Path
import sys,time,py_compile
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    plan_path=A/'nonflag_residual_Ridge10_plan_20261007.json'
    paths=[A/'nonflag_residual_Ridge_codec_20261007.py',A/'verify_nonflag_residual_Ridge_codec2_20261007.py',A/'train_nonflag_residual_Ridge_bank10_20261007.py',Path(__file__)]
    for p in paths: py_compile.compile(str(p),cfile=str(ROOT/'tmp'/('ridge_check_'+p.stem+'.pyc')),doraise=True)
    create(plan_path,{'status':'frozen_before_actual_diagnostics_and10_mature_fits','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'training_population':'nonflag!=1, price_valid, finite own past OOF y_rank; exclusive mature annual cutoff',
        'target':'provided y_rank + .5 - qualified106 current-day all-forecast averageRank/N',
        'features':'63 provided-derived features + qualified106 current-day all-forecast averageRank/N',
        'preprocessing':'reuse identical own-window column finite median/mean/std and clip10 from verified HGB cache',
        'fixed_parameters':{'solver':'cholesky','fit_intercept':True,'copy_X':True},
        'configurations':{'nonflag_residual_ridge_l001':{'alpha_per_training_row':.01},'nonflag_residual_ridge_l025':{'alpha_per_training_row':.25}},
        'native_fit_years':[2021,2022,2023,2024,2025],'actual_declared_native_fits':10,'cpu_threads':2,
        'inference_recipe':'fixed8192 padded rows; native sklearn predict and independent JSON coefficients',
        'resource_gate_available_RAM_GiB':12,'cache_location':'E:/赛题五_本机临时/nonflag_residual_HGB10_20261007',
        'new_large_feature_caches':0,'official_scoring_requires_later_complete_future_source_admission':True,'test_labels_read':False})
    from verify_nonflag_residual_Ridge_codec2_20261007 import main as diagnostic
    diagnostic()
    proof_path=A/'nonflag_residual_Ridge_codec2_preflight_20261007/verification.json'
    proof=read(proof_path); assert proof['actual_diagnostic_fits']==2 and proof['status']=='passed_actual2_nonflag_residual_Ridge_historical_codec_controls'
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [*paths,proof_path]}}
    admission=A/'nonflag_residual_Ridge10_source_admission_20261007.json'
    create(admission,{'status':'passed_actual2_Ridge_codec_controls_and10_past_only_fit_admission','input_sha256':pins,
        'declared_native_fits':10,'actual_completed_native_fits':0,'actual_official_scores':0,'full_future_recipe_not_yet_admitted':True,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_residual_Ridge_native_bank10','train_nonflag_residual_Ridge_bank10_20261007.py',[],{**pins,str(admission):sha(admission)})
    create(A/'nonflag_residual_Ridge10_actual_hidden_launch_20261007.json',{'status':'started_actual_single_host_Ridge_native_bank','row':row,'input_sha256':pins,'actual_official_scores':0,'test_labels_read':False})
    print({'worker':row['owned_worker_pid'],'status':'started'},flush=True)
if __name__=='__main__':main()
