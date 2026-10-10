"""Five-day rank target instead of absolute return; own loss admission, restart and six fits."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def route(text):
    pairs={'Recent252Forward5Huber050171':'Recent252Rank5Huber050172','recent252_forward5':'recent252_rank5',
        'Recent252Forward5':'Recent252Rank5','recent252forward5':'recent252rank5','y_ret_5mean':'y_rank_5mean',
        'Forward5Huber050_independent_targets_loss_gradient':'Rank5Huber050_independent_targets_loss_gradient',
        'forward5_model_target_plan':'rank5_model_target_plan'}
    saved={}
    for i,(before,after) in enumerate(sorted(pairs.items(),key=lambda p:-len(p[0]))):
        token=f'__RANK5_ROUTE_{i}__';text=text.replace(before,token);saved[token]=after
    for token,after in saved.items():text=text.replace(token,after)
    return text

def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed();generated=[];originals=[]
    importlib.import_module('verify_recent252_rank5_mature_population_v1_20261010').main()
    for name in ['neural_BF16_medium2048_recent252forward5huber050_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_recent252forward5huber050_seed09_independent_forward_v2_20261010.py']:
        old=A/name;originals.append(old);text=route(old.read_text(encoding='utf8')).replace('100.','1.')
        if name.endswith('native_v1_20261009.py'):
            needle='y=np.asarray(y);assert y.ndim==1 and len(y) and np.isfinite(y).all()';assert text.count(needle)==1
            text=text.replace(needle,needle+"\n    assert np.all((y>=0.)&(y<=1.))")
        generated.append(save(route(name),text))
    native=importlib.import_module(generated[0].stem);assert native.CONFIG['target']=='y_rank_5mean' and native.CONFIG['return_target_scale']==1.
    plan=A/'rank5_model_target_plan_v1_20261010.json'
    create(plan,{'status':'frozen_new_rank5_target_before_CPU_loss_controls_and_GPU','configuration':native.CONFIG,'input_sha256':{str(p):sha(p) for p in [Path(__file__),*generated,A/'recent252_rank5_mature_training_population_v1_20261010.py',A/'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json']},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    old=A/'verify_medium_forward5_Huber050_targets_and_loss_v1_20261010.py';originals.append(old)
    text=route(old.read_text(encoding='utf8')).replace('rng.normal(0,.04,n)','rng.uniform(0.,1.,n)').replace('y[0]=-.8','y[0]=0.').replace('y[-1]=.9','y[-1]=1.').replace(')*100.',')*1.')
    text=text.replace('np.array([np.inf]))','np.array([np.inf]),np.array([-.001]),np.array([1.001]))')
    loss=save('verify_medium_rank5_Huber050_targets_and_loss_v1_20261010.py',text);generated.append(loss);importlib.import_module(loss.stem).main()
    import numpy as np,polars as pl
    import recent252_rank5_mature_training_population_v1_20261010 as labels
    from run import FEATURE_FILE,feature_names,to_matrix
    folder=Path('E:/赛题五_本机临时/Recent252Rank5Huber050_past_fixture_v2_20261010');folder.mkdir(exist_ok=False)
    features=feature_names();cutoff=20191231
    frame=labels.training_frame(pl.scan_parquet(FEATURE_FILE),cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_rank_5mean','label_end_5d']).limit(49153).collect()
    x=to_matrix(frame,features);y=frame['y_rank_5mean'].to_numpy();last=int(frame['trade_date'].max());end=int(frame['label_end_5d'].max())
    assert len(frame)==49153 and last<end<cutoff and np.isfinite(y).all() and np.all((y>0.)&(y<=1.))
    np.save(folder/'past_features.npy',x,allow_pickle=False);np.save(folder/'past_return_targets.npy',y,allow_pickle=False)
    create(folder/'verification.json',{'status':'passed_real49153_recent252_mature_mean5_rank_fixture','rows':49153,'last':last,'last_label_end':end,'cutoff_exclusive':cutoff,'training_calendar_window':252,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(labels.__file__),FEATURE_FILE,folder/'past_features.npy',folder/'past_return_targets.npy']},'actual_native_fits':0,'test_labels_read':False})
    create(A/'actual_Recent252Rank5Huber050_past_fixture_location_v2_20261010.json',{'output':str(folder),'verification_sha256':sha(folder/'verification.json')})
    for name in ['verify_neural_BF16_medium2048_recent252forward5huber050_seed09_restart_v1_20261009.py','verify_BF16Recent252Forward5Huber050171_independent_small_CPU_v1_20261009.py','verify_BF16Recent252Forward5Huber050171_full5_independent_GPU_v1_20261009.py','BF16Recent252Forward5Huber050171_complete_parent_native_stage_v1_20261009.py','verify_BF16Recent252Forward5Huber050171_native42_calendar_v1_20261009.py','train_neural_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009.py']:
        old=A/name;originals.append(old);text=route(old.read_text(encoding='utf8'))
        if name.startswith('verify_neural_'):
            text=text.replace("np.clip(rng.normal(0.,.03,1024),-.1,.1).astype(np.float64)","rng.uniform(0.,1.,1024).astype(np.float64)")
        if name.startswith('train_neural_'):
            text=text.replace("'y_rank_5mean','label_end_5d'","'y_rank_5mean','label_end_5d'")
            text=text.replace("A/'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json'","A/'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json', A/'recent252_rank5_mature_training_population_v1_20261010.py'")
        generated.append(save(route(name),text))
    proof=A/'Recent252Rank5Huber050_own_bank_controls_source_admission_v1_20261010.json'
    create(proof,{'status':'compiled_own_mean5_rank_six_fit_bank_after7_scalar_daily_rank_and20_loss_CPU_cases_real49153_fixture','input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*generated,plan,folder/'verification.json',A/'recent252_rank5_mature_training_population_v1_20261010.py',A/'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json',A/'Rank5Huber050_independent_targets_loss_gradient_controls_v1_20261010.json']},'actual_native_fits':0,'new_quality_scores':0,'GPU_controls_pending':True,'test_labels_read':False})
    old=A/'run_recent252_forward5_own_controls_and_training_queue_v1_20261010.py';text=route(old.read_text(encoding='utf8'))
    text=text.replace("closed('actual_recent252_forward20_own_controls_and_training_queue_v1_20261010')","closed('actual_recent252_forward5_own_controls_and_training_queue_v1_20261010')")
    queue=save(route(old.name),text)
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed();row=start_service('actual_recent252_rank5_own_controls_and_training_queue_v1_20261010',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)})
    create(A/'actual_recent252_rank5_own_controls_and_training_queue_activation_v1_20261010.json',row)
    print({'new_rank5_scalar_controls':7,'new_loss_controls':20,'real_fixture_rows':49153,'queue_worker':row['owned_worker_pid'],'waits_mean5_full_GPU_queue':True},flush=True)
if __name__=='__main__':main()
