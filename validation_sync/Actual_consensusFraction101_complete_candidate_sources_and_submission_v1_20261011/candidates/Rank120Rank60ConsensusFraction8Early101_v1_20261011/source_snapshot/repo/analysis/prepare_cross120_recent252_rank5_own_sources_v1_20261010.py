"""New120-channel model, own restarts and six fits; GPU follows the other own120-channel bank without concurrent training."""
from pathlib import Path
import sys,importlib,io,tokenize
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def route(text):
    pairs={'Recent252Rank5Huber050172':'Cross120Recent252Rank5Huber050174','Recent252Rank5':'Cross120Recent252Rank5',
        'recent252rank5':'cross120recent252rank5','recent252_rank5_own':'cross120_recent252_rank5_own'}
    saved={}
    for i,(old,new) in enumerate(sorted(pairs.items(),key=lambda p:-len(p[0]))):
        token=f'__CROSS120_ROUTE_{i}__';text=text.replace(old,token);saved[token]=new
    for token,new in saved.items():text=text.replace(token,new)
    return text

def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def once(text,before,after):
    assert text.count(before)==1,(before,text.count(before));return text.replace(before,after)

def width(text):
    return tokenize.untokenize([t._replace(string='120') if t.type==tokenize.NUMBER and t.string=='63' else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])

def main():
    assert allowed();generated=[];originals=[]
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    import mature_population_cross120_training_matrix_v1_20261010 as population
    import recent252_rank5_mature_training_population_v1_20261010 as labels
    old=A/'neural_BF16_medium2048_recent252rank5huber050_seed09_e64_native_v1_20261009.py';originals.append(old)
    text=route(old.read_text(encoding='utf8'))
    text=once(text,"'training_calendar_window':252,","'raw_feature_count':63,'encoded_feature_count':120,'feature_encoder_module':'daily_cross_sectional_feature_encoder120_v1_20261010','training_calendar_window':252,")
    text=once(text,'    assert len(x) == len(y) and len(y) > 0 and np.isfinite(y).all()',"    assert len(x) == len(y) and len(y) > 0 and np.isfinite(y).all()\n    assert x.ndim==2 and x.shape[1]==cfg['encoded_feature_count']==120")
    nativepath=save(route(old.name),text);generated.append(nativepath)
    old=A/'neural_BF16_medium2048_recent252rank5huber050_seed09_independent_forward_v2_20261010.py';originals.append(old);generated.append(save(route(old.name),route(old.read_text(encoding='utf8'))))
    native=importlib.import_module(nativepath.stem)
    import numpy as np,polars as pl
    from run import FEATURE_FILE,feature_names
    features=feature_names();cutoff=20191231;lazy=pl.scan_parquet(FEATURE_FILE)
    train=labels.training_frame(lazy,cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_rank_5mean','label_end_5d']).limit(49153).collect()
    x,alignment=population.matrix(lazy,train,features);y=train['y_rank_5mean'].to_numpy()
    last=int(train['trade_date'].max());end=int(train['label_end_5d'].max());assert len(y)==49153 and last<end<cutoff and x.shape==(49153,120)
    out=Path('E:/赛题五_本机临时/Cross120Recent252Rank5Huber050_past_fixture_v2_20261010');out.mkdir(exist_ok=False)
    np.save(out/'past_features.npy',x,allow_pickle=False);np.save(out/'past_return_targets.npy',y,allow_pickle=False)
    create(out/'verification.json',{'status':'passed_real49153_mature_rank5_rows_with_all_same_date_cohort_encoder120_before_target_selection','rows':49153,'last':last,'last_label_end':end,'cutoff_exclusive':cutoff,'training_calendar_window':252,'alignment':alignment,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),nativepath,Path(encoder.__file__),Path(population.__file__),Path(labels.__file__),FEATURE_FILE,out/'past_features.npy',out/'past_return_targets.npy']},'actual_native_fits':0,'test_labels_read':False})
    create(A/'actual_Cross120Recent252Rank5Huber050_past_fixture_location_v2_20261010.json',{'output':str(out),'verification_sha256':sha(out/'verification.json')})
    names=['verify_neural_BF16_medium2048_recent252rank5huber050_seed09_restart_v1_20261009.py','verify_BF16Recent252Rank5Huber050172_independent_small_CPU_v1_20261009.py','BF16Recent252Rank5Huber050172_complete_parent_native_stage_v1_20261009.py']
    for name in names:
        old=A/name;originals.append(old);generated.append(save(route(name),width(route(old.read_text(encoding='utf8')))))
    old=A/'train_neural_BF16_medium2048_recent252rank5huber050_seed09_e64_bank6_v1_20261009.py';originals.append(old);text=route(old.read_text(encoding='utf8'))
    text=once(text,'import recent252_rank5_mature_training_population_v1_20261010 as labels','import recent252_rank5_mature_training_population_v1_20261010 as labels\nimport daily_cross_sectional_feature_encoder120_v1_20261010 as encoder\nimport mature_population_cross120_training_matrix_v1_20261010 as population')
    text=once(text,'    features = feature_names()','    features = feature_names();encoded_features=encoder.names(features)[0]')
    text=once(text,"             FEATURE_FILE, MANIFEST, control / 'verification.json'","             Path(encoder.__file__), Path(population.__file__), A/'daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json', FEATURE_FILE, MANIFEST, control / 'verification.json'")
    text=once(text,"        x, y = to_matrix(train, features), train['y_rank_5mean'].to_numpy()","        x, feature_alignment = population.matrix(lazy,train,features)\n        y = train['y_rank_5mean'].to_numpy()")
    text=once(text,"'features': features, 'training_matrix_sha256'","'features': encoded_features, 'raw_features':features, 'cross_sectional_feature_alignment':feature_alignment, 'training_matrix_sha256'")
    text=once(text,'            vx = to_matrix(valid, features)',"            vx = encoder.encode(to_matrix(valid,features),valid['trade_date'].to_numpy(),features)")
    generated.append(save(route(old.name),text))
    old=A/'verify_BF16Recent252Rank5Huber050172_full5_independent_GPU_v1_20261009.py';originals.append(old);text=route(old.read_text(encoding='utf8'))
    text=once(text,'    features = feature_names()',"    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder\n    features = feature_names();encoded_features=encoder.names(features)[0]")
    text=once(text,"        assert meta['features'] == features","        assert meta['features'] == encoded_features and meta['raw_features']==features")
    text=once(text,'        x = to_matrix(frame, features)',"        raw_x = to_matrix(frame,features)\n        x = encoder.encode(raw_x,frame['trade_date'].to_numpy(),features)\n        feature_oracle=encoder.pandas_oracle(raw_x,frame['trade_date'].to_numpy(),features)\n        assert np.array_equal(x.view('u4'),feature_oracle.view('u4'))\n        del raw_x,feature_oracle")
    generated.append(save(route(old.name),text))
    old=A/'verify_BF16Recent252Rank5Huber050172_native42_calendar_v1_20261009.py';originals.append(old);text=route(old.read_text(encoding='utf8'))
    text=once(text,"    features=feature_names();keys=['ts_code','trade_date']","    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder\n    features=feature_names();encoded_features=encoder.names(features)[0];keys=['ts_code','trade_date']")
    text=once(text,'sourceparent=np.asarray(parent[idx],dtype=np.float64);x=to_matrix(xframe,features)',"sourceparent=np.asarray(parent[idx],dtype=np.float64);raw_x=to_matrix(xframe,features)\n        x=encoder.encode(raw_x,panel['trade_date'].to_numpy(),features)\n        oracle=encoder.pandas_oracle(raw_x,panel['trade_date'].to_numpy(),features)\n        assert np.array_equal(x.view('u4'),oracle.view('u4'));del raw_x,oracle")
    text=once(text,'_BF16_feature_names=features,_BF16_raw_features=x','_BF16_feature_names=encoded_features,_BF16_raw_features=x')
    generated.append(save(route(old.name),text))
    proof=A/'Cross120Recent252Rank5Huber050_own_bank_controls_source_admission_v1_20261010.json'
    create(proof,{'status':'compiled_own_encoder120_recent252_mean5_bank_after_scalar7_and_real13950_feature_oracles_and_real49153_mature_cohort_alignment',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*generated,Path(encoder.__file__),Path(population.__file__),out/'verification.json',A/'daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json',A/'Rank5Huber050_independent_targets_loss_gradient_controls_v1_20261010.json']},
        'existing_mean5_loss_controls_reused_not_claimed_new':True,'raw_features':63,'encoded_features':120,'new_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,'GPU_admission_and_training_pending':True})
    old=A/'run_recent252_rank5_own_controls_and_training_queue_v1_20261010.py';text=route(old.read_text(encoding='utf8'))
    text=text.replace("closed('actual_recent252_forward5_own_controls_and_training_queue_v1_20261010')","closed('actual_cross120_recent252_forward5_own_controls_and_training_queue_v1_20261010')")
    queue=save(route(old.name),text)
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed();row=start_service('actual_cross120_recent252_rank5_own_controls_and_training_queue_v1_20261010',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)})
    create(A/'actual_cross120_recent252_rank5_own_controls_and_training_queue_activation_v1_20261010.json',row)
    print({'fresh_sources':len(generated),'real_fixture_rows':49153,'encoded_features':120,'queue_worker':row['owned_worker_pid'],'GPU_waits_completed_own_cross120_mean5_bank':True},flush=True)
if __name__=='__main__':main()
