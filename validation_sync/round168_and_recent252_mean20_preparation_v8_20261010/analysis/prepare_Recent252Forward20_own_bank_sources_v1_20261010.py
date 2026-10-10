"""New joint recent-window mean20 hypothesis; retain existing target-loss proof honestly."""
from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def route(text):
    pairs={'Forward20Huber050167':'Recent252Forward20Huber050170','Forward20Huber050':'Recent252Forward20Huber050','forward20huber050':'recent252forward20huber050','forward20_own_controls_and_training_queue_v1_20261010':'recent252_forward20_own_controls_and_training_queue_v1_20261010'}
    saved={}
    for i,(old,new) in enumerate(sorted(pairs.items(),key=lambda x:-len(x[0]))):
        token=f'__RECENT20_SOURCE_{i}__';text=text.replace(old,token);saved[token]=new
    for token,new in saved.items():text=text.replace(token,new)
    return text.replace('Recent252Forward20Huber050_independent_targets_loss_gradient_controls_v1_20261010.json','Forward20Huber050_independent_targets_loss_gradient_controls_v1_20261010.json')

def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    import numpy as np,polars as pl,importlib
    assert allowed()
    import recent252_forward20_mature_training_population_v1_20261010 as labels
    originals=[];generated=[]
    old=A/'neural_BF16_medium2048_forward20huber050_seed09_e64_native_v1_20261009.py';originals.append(old)
    text=route(old.read_text(encoding='utf8'));assert text.count("'loss': 'Huber',")==1
    nativepath=save(route(old.name),text.replace("'loss': 'Huber',","'training_calendar_window':252, 'loss': 'Huber',"));generated.append(nativepath)
    native=importlib.import_module(nativepath.stem)
    old=A/'neural_BF16_medium2048_forward20huber050_seed09_independent_forward_v2_20261010.py';originals.append(old);generated.append(save(route(old.name),route(old.read_text(encoding='utf8'))))
    from run import FEATURE_FILE,feature_names,to_matrix
    folder=Path('E:/赛题五_本机临时/Recent252Forward20Huber050_past_fixture_v2_20261010');folder.mkdir(exist_ok=False)
    features=feature_names();cutoff=20191231
    frame=labels.training_frame(pl.scan_parquet(FEATURE_FILE),cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_ret_20mean','label_end_20d']).limit(49153).collect()
    assert len(frame)==49153 and len(features)==63
    x=to_matrix(frame,features);y=frame['y_ret_20mean'].to_numpy();last=int(frame['trade_date'].max());end=int(frame['label_end_20d'].max())
    assert last<end<cutoff and np.isfinite(y).all()
    np.save(folder/'past_features.npy',x,allow_pickle=False);np.save(folder/'past_return_targets.npy',y,allow_pickle=False)
    create(folder/'verification.json',{'status':'passed_real49153_recent252_mature_mean20_training_fixture','rows':49153,'features':features,'first':int(frame['trade_date'].min()),'last':last,'last_label_end':end,'cutoff_exclusive':cutoff,'training_calendar_window':252,'input_sha256':{str(p):sha(p) for p in [Path(__file__),nativepath,Path(labels.__file__),FEATURE_FILE,folder/'past_features.npy',folder/'past_return_targets.npy']},'actual_native_fits':0,'test_labels_read':False})
    create(A/'actual_Recent252Forward20Huber050_past_fixture_location_v2_20261010.json',{'output':str(folder),'verification_sha256':sha(folder/'verification.json')})
    names=['verify_neural_BF16_medium2048_forward20huber050_seed09_restart_v1_20261009.py','verify_BF16Forward20Huber050167_independent_small_CPU_v1_20261009.py','verify_BF16Forward20Huber050167_full5_independent_GPU_v1_20261009.py','BF16Forward20Huber050167_complete_parent_native_stage_v1_20261009.py','verify_BF16Forward20Huber050167_native42_calendar_v1_20261009.py']
    for name in names:
        old=A/name;originals.append(old);generated.append(save(route(name),route(old.read_text(encoding='utf8'))))
    old=A/'train_neural_BF16_medium2048_forward20huber050_seed09_e64_bank6_v1_20261009.py';originals.append(old)
    trainer=route(old.read_text(encoding='utf8')).replace('import forward20_mature_training_labels_v1_20261010 as labels','import recent252_forward20_mature_training_population_v1_20261010 as labels')
    trainer=trainer.replace("'days': train['trade_date'].n_unique(),","'days': train['trade_date'].n_unique(), 'training_calendar_window':252,")
    trainer=trainer.replace("assert last < cutoff and label_end < cutoff and np.isfinite(y).all()","assert last < cutoff and label_end < cutoff and np.isfinite(y).all() and train['trade_date'].n_unique()<=252")
    trainer=trainer.replace("Path(labels.__file__), A/'forward20_mature_training_labels_actual_CPU_controls_v1_20261010.json'","Path(labels.__file__), A/'recent252_forward20_mature_population_actual_CPU_controls_v1_20261010.json', A/'forward20_mature_training_labels_v1_20261010.py', A/'forward20_mature_training_labels_actual_CPU_controls_v1_20261010.json'")
    trainer=trainer.replace('full annual expanding OOF 2020-2024','full annual rolling252-calendar mean20 OOF 2020-2024')
    generated.append(save(route(old.name),trainer))
    proofname='Recent252Forward20Huber050_own_bank_controls_source_admission_v1_20261010.json'
    create(A/proofname,{'status':'compiled_own_recent252_mean20_bank_controls_with_real49153_fixture_and7_joint_population_CPU_cases','input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*generated,Path(labels.__file__),A/'recent252_forward20_mature_population_actual_CPU_controls_v1_20261010.json',A/'forward20_mature_training_labels_v1_20261010.py',A/'Forward20Huber050_independent_targets_loss_gradient_controls_v1_20261010.json',folder/'verification.json']},'existing_target_loss_CPU20_reused_not_claimed_new':True,'new_quality_scores':0,'actual_native_fits':0,'GPU_controls_pending':True,'test_labels_read':False})
    old=A/'run_forward20_own_controls_and_training_queue_v1_20261010.py'
    queue=route(old.read_text(encoding='utf8')).replace('Recent252Forward20Huber050_own_bank_controls_source_admission_v2_20261010.json',proofname)
    needle='    assert allowed();OUT.mkdir(exist_ok=False)';assert queue.count(needle)==1
    queue=queue.replace(needle,"    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed\n    assert allowed()\n    closed('RecentReturn252Protected168_selected_candidate_sealing_v1_20261010')\n"+needle)
    q=save(route(old.name),queue)
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed()
    row=start_service('actual_recent252_forward20_own_controls_and_training_queue_v1_20261010',q.name,[],{str(q):sha(q),str(A/proofname):sha(A/proofname)})
    create(A/'actual_recent252_forward20_own_controls_and_training_queue_activation_v1_20261010.json',row)
    print({'new_recent252_mean20_fixture_rows':49153,'queue_worker':row['owned_worker_pid'],'GPU_waits_exact168_sealing':True},flush=True)
if __name__=='__main__':main()
