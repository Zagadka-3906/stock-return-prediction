"""Independent new five-day target hypothesis; source originals remain immutable."""
from pathlib import Path
import sys, io, tokenize, importlib
A=Path(__file__).resolve().parent; ROOT=A.parent; sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def route(text):
    # Longest first with placeholders prevents a route from being rewritten twice.
    pairs={'Recent252Forward20Huber050170':'Recent252Forward5Huber050171',
           'recent252_forward20':'recent252_forward5','Recent252Forward20':'Recent252Forward5',
           'recent252forward20':'recent252forward5','Forward20':'Forward5','forward20':'forward5',
           'y_ret_20mean':'y_ret_5mean','label_end_20d':'label_end_5d',
           '_calendar20':'_calendar5','mean20':'mean5','twenty_day':'five_day',
           'mature20':'mature5','exact20':'exact5','20-day':'5-day','Last20':'Last5'}
    saved={}
    for i,(before,after) in enumerate(sorted(pairs.items(),key=lambda p:-len(p[0]))):
        token=f'__FIVE_DAY_ROUTE_{i}__';text=text.replace(before,token);saved[token]=after
    for token,after in saved.items():text=text.replace(token,after)
    return tokenize.untokenize([t._replace(string='5' if t.string=='20' else '5.') if t.type==tokenize.NUMBER and t.string in ('20','20.','20.0') else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])

def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed(); originals=[]; generated=[]
    # Each new helper derives five returns and an endpoint five trading dates later.
    for name in ['forward20_mature_training_labels_v1_20261010.py','recent252_forward20_mature_training_population_v1_20261010.py',
                 'verify_forward20_mature_training_labels_v1_20261010.py','verify_recent252_forward20_mature_population_v1_20261010.py',
                 'neural_BF16_medium2048_recent252forward20huber050_seed09_e64_native_v1_20261009.py',
                 'neural_BF16_medium2048_recent252forward20huber050_seed09_independent_forward_v2_20261010.py']:
        old=A/name;originals.append(old);text=route(old.read_text(encoding='utf8'))
        if name.startswith('verify_forward20_'):text=text.replace('(19,20,21,24,45,65,79)','(4,5,6,24,45,65,79)') # Original token20 is now5.
        if name.startswith('verify_forward20_'):text=text.replace('(19,5,21,24,45,65,79)','(4,5,6,24,45,65,79)')
        if name.startswith('verify_recent252_'):text=text.replace('(1,19,251,252,253,301,401)','(1,4,5,6,253,301,401)')
        generated.append(save(route(name),text))
    # Run actual independent scalar and joint-window CPU population controls now.
    importlib.import_module('verify_forward5_mature_training_labels_v1_20261010').main()
    importlib.import_module('verify_recent252_forward5_mature_population_v1_20261010').main()
    native=importlib.import_module('neural_BF16_medium2048_recent252forward5huber050_seed09_e64_native_v1_20261009')
    assert native.CONFIG['target']=='y_ret_5mean' and native.CONFIG['label_horizon_trading_days']==5
    plan=A/'forward5_model_target_plan_v1_20261010.json'
    create(plan,{'status':'frozen_new_recent252_five_day_mean_target_loss_before_GPU',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*generated]},'configuration':native.CONFIG,
        'hypothesis':'Five-day average reduces daily noise while retaining shorter-term signal than mean20; official score decides',
        'test_labels_read':False,'new_quality_scores':0})
    old=A/'verify_medium_forward20_Huber050_targets_and_loss_v1_20261010.py';originals.append(old)
    text=route(old.read_text(encoding='utf8')).replace('neural_BF16_medium2048_forward5huber050_seed09_e64_native_v1_20261009','neural_BF16_medium2048_recent252forward5huber050_seed09_e64_native_v1_20261009')
    # There are still twenty real loss/gradient cases, independent of target horizon.
    generated.append(save(route(old.name),text))
    importlib.import_module('verify_medium_forward5_Huber050_targets_and_loss_v1_20261010').main()
    import numpy as np, polars as pl
    import recent252_forward5_mature_training_population_v1_20261010 as labels
    from run import FEATURE_FILE,feature_names,to_matrix
    folder=Path('E:/赛题五_本机临时/Recent252Forward5Huber050_past_fixture_v2_20261010');folder.mkdir(exist_ok=False)
    features=feature_names();cutoff=20191231
    frame=labels.training_frame(pl.scan_parquet(FEATURE_FILE),cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_ret_5mean','label_end_5d']).limit(49153).collect()
    assert len(frame)==49153 and len(features)==63
    x=to_matrix(frame,features);y=frame['y_ret_5mean'].to_numpy();last=int(frame['trade_date'].max());end=int(frame['label_end_5d'].max())
    assert last<end<cutoff and np.isfinite(y).all()
    np.save(folder/'past_features.npy',x,allow_pickle=False);np.save(folder/'past_return_targets.npy',y,allow_pickle=False)
    create(folder/'verification.json',{'status':'passed_real49153_recent252_mature_mean5_training_fixture','rows':49153,'features':features,'last':last,'last_label_end':end,'cutoff_exclusive':cutoff,'training_calendar_window':252,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(labels.__file__),FEATURE_FILE,folder/'past_features.npy',folder/'past_return_targets.npy']},'actual_native_fits':0,'test_labels_read':False})
    create(A/'actual_Recent252Forward5Huber050_past_fixture_location_v2_20261010.json',{'output':str(folder),'verification_sha256':sha(folder/'verification.json')})
    for name in ['verify_neural_BF16_medium2048_recent252forward20huber050_seed09_restart_v1_20261009.py',
                 'verify_BF16Recent252Forward20Huber050170_independent_small_CPU_v1_20261009.py',
                 'verify_BF16Recent252Forward20Huber050170_full5_independent_GPU_v1_20261009.py',
                 'BF16Recent252Forward20Huber050170_complete_parent_native_stage_v1_20261009.py',
                 'verify_BF16Recent252Forward20Huber050170_native42_calendar_v1_20261009.py',
                 'train_neural_BF16_medium2048_recent252forward20huber050_seed09_e64_bank6_v1_20261009.py']:
        old=A/name;originals.append(old);text=route(old.read_text(encoding='utf8'))
        # Five-day trainer now pins its own new horizon-specific CPU proofs.
        generated.append(save(route(name),text))
    proof=A/'Recent252Forward5Huber050_own_bank_controls_source_admission_v1_20261010.json'
    create(proof,{'status':'compiled_new_recent252_mean5_own_bank_after14_population_and20_loss_CPU_controls_real49153_fixture',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*generated,plan,folder/'verification.json',A/'forward5_mature_training_labels_actual_CPU_controls_v1_20261010.json',A/'recent252_forward5_mature_population_actual_CPU_controls_v1_20261010.json',A/'Forward5Huber050_independent_targets_loss_gradient_controls_v1_20261010.json']},
        'actual_native_fits':0,'new_quality_scores':0,'GPU_controls_pending':True,'future_X_read':False,'test_labels_read':False})
    old=A/'run_recent252_forward20_own_controls_and_training_queue_v1_20261010.py'
    text=route(old.read_text(encoding='utf8'))
    # Wait for the completed mean20 GPU queue; CPU scoring may continue independently.
    text=text.replace("closed('RecentReturn252Protected168_selected_candidate_sealing_v1_20261010')","closed('actual_recent252_forward20_own_controls_and_training_queue_v1_20261010')")
    queue=save(route(old.name),text)
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed()
    row=start_service('actual_recent252_forward5_own_controls_and_training_queue_v1_20261010',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)})
    create(A/'actual_recent252_forward5_own_controls_and_training_queue_activation_v1_20261010.json',row)
    print({'new_mean5_actual_CPU_population_cases':14,'loss_gradient_cases':20,'real_fixture_rows':49153,'queue_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
