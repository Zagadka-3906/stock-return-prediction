"""Freeze a real mature return fixture and own replay controls; no new GPU consumer."""
from pathlib import Path
import sys,time,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected162_candidate_sources_v2_20261010 import change
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    import numpy as np,polars as pl
    import neural_BF16_medium2048_returnhuber050_seed09_e64_native_v1_20261009 as native
    from run import FEATURE_FILE,feature_names,to_matrix
    folder=Path('E:/赛题五_本机临时/ReturnHuber050_past_fixture_v1_20261010');folder.mkdir(exist_ok=False)
    features=feature_names();cutoff=20191231
    lazy=pl.scan_parquet(FEATURE_FILE)
    frame=native.architecture.training_frame(lazy,cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_ret_1d']).sort('trade_date','ts_code').limit(49153).collect()
    assert len(frame)==49153 and len(features)==63
    x=to_matrix(frame,features);y=frame['y_ret_1d'].to_numpy()
    dates=lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    last=int(frame['trade_date'].max());label_end=int(dates[np.searchsorted(dates,last)+1])
    assert last<cutoff and label_end<=cutoff and np.isfinite(y).all()
    np.save(folder/'past_features.npy',x,allow_pickle=False);np.save(folder/'past_return_targets.npy',y,allow_pickle=False)
    create(folder/'verification.json',{'status':'passed_actual49153_real_mature_return_targets_and63_feature_fixture','rows':49153,'features':features,'first':int(frame['trade_date'].min()),'last':last,'last_label_end':label_end,'cutoff_exclusive':cutoff,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(native.__file__),FEATURE_FILE,folder/'past_features.npy',folder/'past_return_targets.npy']},'actual_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})
    create(A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json',{'output':str(folder),'verification_sha256':sha(folder/'verification.json')})
    originals=['verify_neural_BF16_medium2048_huber010_seed09_restart_v1_20261009.py','verify_BF16Huber010161_independent_small_CPU_v1_20261009.py','verify_BF16Huber010161_full5_independent_GPU_v1_20261009.py','BF16Huber010161_complete_parent_native_stage_v1_20261009.py','verify_BF16Huber010161_native42_calendar_v1_20261009.py']
    route=lambda s:s.replace('huber010','returnhuber050').replace('Huber010161','ReturnHuber050166')
    outputs={}
    for name in originals:
        text=route((A/name).read_text(encoding='utf8'))
        if name.startswith('verify_neural_'):
            text=change(text,'return x, rng.uniform(size=1024).astype(np.float64)',"return x, np.clip(rng.normal(0.,.03,1024),-.1,.1).astype(np.float64)")
            start=text.index("    bank = Path(read(A / 'actual_wide_GPU_precision3")
            end=text.index('\n\n\ndef phase',start)
            text=text[:start]+"    fixture=Path(read(A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json')['output'])\n    assert read(fixture/'verification.json')['last_label_end']<=20191231\n    return np.load(fixture/'past_features.npy'),np.load(fixture/'past_return_targets.npy')\n"+text[end:]
            needle='    pins = {str(p): sha(p) for p in paths}';assert text.count(needle)==1
            text=text.replace(needle,"    fixture=Path(read(A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json')['output'])\n    paths += [fixture/'past_features.npy',fixture/'past_return_targets.npy',fixture/'verification.json',A/'actual_ReturnHuber050_past_fixture_location_v1_20261010.json',A/'ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json']\n"+needle)
        outputs[route(name)]=text
    outputs['build_reused_return_neural_frontier_v11_20261010.py']=route((A/'build_reused_neural_frontier_v9_20261010.py').read_text(encoding='utf8'))
    for name,text in outputs.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
    for name,text in outputs.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json',{'status':'passed_real_past_return_fixture_and_compiled_own_restart_CPU_full5_native42_dedicated_builder','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in originals],*[A/n for n in outputs],A/'ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json',A/'neural_BF16_medium2048_returnhuber050_seed09_e64_frontier_v1_20261010.json',folder/'verification.json']},'actual_annual_fits':0,'GPU_controls_and_own_six_training_states_pending':True,'new_quality_scores':0,'test_labels_read':False})
    print('PASS real49153 mature return fixture and compiled own controls; no GPU work',flush=True)
if __name__=='__main__':main()
