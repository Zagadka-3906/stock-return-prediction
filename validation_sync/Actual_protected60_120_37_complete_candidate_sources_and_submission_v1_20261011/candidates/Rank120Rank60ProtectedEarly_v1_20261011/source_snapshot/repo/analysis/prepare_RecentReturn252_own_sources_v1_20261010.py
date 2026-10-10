"""Prepare one-year rolling return networks with fresh sources and a genuine own mature fixture."""
from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,s):
    p=A/name;assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p
def route(s):return s.replace('returnhuber050','recent252returnhuber050').replace('ReturnHuber050166','RecentReturn252Huber050169').replace('ReturnHuber050','RecentReturn252Huber050')
def main():
    assert allowed()
    old=A/'neural_BF16_medium2048_returnhuber050_seed09_e64_native_v1_20261009.py'
    s=route(old.read_text(encoding='utf8')).replace("'loss': 'Huber',","'training_calendar_window': 252, 'loss': 'Huber',")
    nativepath=save(route(old.name),s)
    decoder=A/'neural_BF16_medium2048_returnhuber050_seed09_independent_forward_v1_20261009.py'
    decoderpath=save(route(decoder.name),route(decoder.read_text(encoding='utf8')))
    import importlib,numpy as np,polars as pl
    native=importlib.import_module(nativepath.stem)
    import recent252_mature_training_population_v1_20261010 as population
    from run import FEATURE_FILE,feature_names,to_matrix
    folder=Path('E:/赛题五_本机临时/RecentReturn252Huber050_past_fixture_v1_20261010');folder.mkdir(exist_ok=False)
    features=feature_names();cutoff=20191231;lazy=pl.scan_parquet(FEATURE_FILE)
    frame=population.training_frame(lazy,cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_ret_1d']).limit(49153).collect()
    assert len(frame)==49153 and len(features)==63
    dates=lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    last=int(frame['trade_date'].max());end=int(dates[np.searchsorted(dates,last)+1]);assert last<cutoff and end<=cutoff
    x=to_matrix(frame,features);y=frame['y_ret_1d'].to_numpy();assert np.isfinite(y).all()
    np.save(folder/'past_features.npy',x,allow_pickle=False);np.save(folder/'past_return_targets.npy',y,allow_pickle=False)
    create(folder/'verification.json',{'status':'passed_real49153_mature_recent252_training_fixture','rows':49153,'features':features,'last':last,'first':int(frame['trade_date'].min()),'last_label_end':end,'cutoff_exclusive':cutoff,'training_calendar_window':252,'input_sha256':{str(p):sha(p) for p in [Path(__file__),FEATURE_FILE,nativepath,Path(population.__file__),folder/'past_features.npy',folder/'past_return_targets.npy']},'actual_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_RecentReturn252Huber050_past_fixture_location_v1_20261010.json',{'output':str(folder),'verification_sha256':sha(folder/'verification.json')})
    names=['verify_neural_BF16_medium2048_returnhuber050_seed09_restart_v1_20261009.py','verify_BF16ReturnHuber050166_independent_small_CPU_v1_20261009.py','verify_BF16ReturnHuber050166_full5_independent_GPU_v1_20261009.py','BF16ReturnHuber050166_complete_parent_native_stage_v1_20261009.py','verify_BF16ReturnHuber050166_native42_calendar_v1_20261009.py']
    generated=[nativepath,decoderpath]
    # Target and loss are unchanged; require the existing actual independent20-case proof explicitly.
    for name in names:
        s=route((A/name).read_text(encoding='utf8'))
        s=s.replace('RecentReturn252Huber050_independent_targets_loss_gradient_controls_v1_20261010.json','ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json')
        generated.append(save(route(name),s))
    original=A/'train_neural_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009.py';s=route(original.read_text(encoding='utf8'))
    s=s.replace('\n\ndef main():','\nimport recent252_mature_training_population_v1_20261010 as population\n\ndef main():',1).replace('native.architecture.training_frame','population.training_frame')
    s=s.replace("FEATURE_FILE, MANIFEST, control / 'verification.json'","FEATURE_FILE, MANIFEST, control / 'verification.json', Path(population.__file__), A/'recent252_mature_population_actual_CPU_controls_v1_20261010.json'")
    s=s.replace("assert last < cutoff and label_end <= cutoff and np.isfinite(y).all()","assert last < cutoff and label_end <= cutoff and np.isfinite(y).all() and train['trade_date'].n_unique()<=252")
    s=s.replace("'days': train['trade_date'].n_unique(),","'days': train['trade_date'].n_unique(), 'training_calendar_window':252,")
    s=s.replace("'validation': 'full annual expanding OOF 2020-2024'","'validation': 'full annual rolling252-session OOF 2020-2024'")
    s=s.replace("'one_day_label_boundary_purged': True","'one_day_label_boundary_purged': True, 'training_calendar_window':252")
    generated.append(save(route(original.name),s))
    create(A/'RecentReturn252Huber050_own_bank_controls_source_admission_v1_20261010.json',{'status':'compiled_recent252_own_trainer_and_controls_with_real49153_mature_fixture_CPU_population_checks_passed','input_sha256':{str(p):sha(p) for p in [Path(__file__),*generated,Path(population.__file__),A/'recent252_mature_population_actual_CPU_controls_v1_20261010.json',A/'ReturnHuber050_independent_targets_loss_gradient_controls_v1_20261010.json',folder/'verification.json']},'actual_native_fits':0,'new_quality_scores':0,'GPU_controls_pending':True,'test_labels_read':False,'target_loss_CPU20_proof_reused_not_claimed_as_new':True})
    print('PASS compiled recent252 own native/decoder/trainer/controls and real49153 mature fixture; GPU admission pending',flush=True)
if __name__=='__main__':main()
