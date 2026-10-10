"""Prepare the previously untested120-channel one-day-return model, with its own admission and saved states."""
from pathlib import Path
import sys,importlib,io,tokenize
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def route(text):
    pairs={'RecentReturn252Huber050169':'Cross120RecentReturn252Huber050175','RecentReturn252':'Cross120RecentReturn252',
        'recent252return':'cross120recent252return','recent252_return_own':'cross120_recent252_return_own'}
    saved={}
    for index,(old,new) in enumerate(sorted(pairs.items(),key=lambda pair:-len(pair[0]))):
        token=f'__RETURN120_ROUTE_{index}__';text=text.replace(old,token);saved[token]=new
    for token,new in saved.items():text=text.replace(token,new)
    return text

def save(name,text):
    path=A/name;assert not path.exists(),path;compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path

def once(text,before,after):
    assert text.count(before)==1,(before,text.count(before));return text.replace(before,after)

def width(text):
    return tokenize.untokenize([token._replace(string='120') if token.type==tokenize.NUMBER and token.string=='63' else token for token in tokenize.generate_tokens(io.StringIO(text).readline)])

def main():
    assert allowed();generated=[];originals=[]
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    import mature_population_cross120_training_matrix_v1_20261010 as matrix
    import recent252_mature_training_population_v1_20261010 as labels
    old=A/'neural_BF16_medium2048_recent252returnhuber050_seed09_e64_native_v1_20261009.py';originals.append(old)
    text=route(old.read_text(encoding='utf8'))
    text=once(text,"'training_calendar_window': 252,","'raw_feature_count':63,'encoded_feature_count':120,'feature_encoder_module':'daily_cross_sectional_feature_encoder120_v1_20261010','training_calendar_window':252,")
    text=once(text,'    assert len(x) == len(y) and len(y) > 0 and np.isfinite(y).all()',"    assert len(x) == len(y) and len(y) > 0 and np.isfinite(y).all()\n    assert x.ndim==2 and x.shape[1]==cfg['encoded_feature_count']==120")
    nativepath=save(route(old.name),text);generated.append(nativepath);native=importlib.import_module(nativepath.stem)
    assert native.CONFIG['target']=='y_ret_1d' and native.CONFIG['return_target_scale']==20. and native.CONFIG['epochs']==64
    old=A/'neural_BF16_medium2048_recent252returnhuber050_seed09_independent_forward_v1_20261009.py';originals.append(old);generated.append(save(route(old.name),route(old.read_text(encoding='utf8'))))
    import numpy as np,polars as pl
    from run import FEATURE_FILE,feature_names
    features=feature_names();cutoff=20191231;lazy=pl.scan_parquet(FEATURE_FILE)
    train=labels.training_frame(lazy,cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_ret_1d']).limit(49153).collect()
    x,alignment=matrix.matrix(lazy,train,features);y=train['y_ret_1d'].to_numpy()
    dates=lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    last=int(train['trade_date'].max());end=int(dates[np.searchsorted(dates,last)+1]);assert len(y)==49153 and last<end<cutoff and x.shape==(49153,120)
    out=Path('E:/赛题五_本机临时/Cross120RecentReturn252Huber050_past_fixture_v1_20261010');out.mkdir(exist_ok=False)
    np.save(out/'past_features.npy',x,allow_pickle=False);np.save(out/'past_return_targets.npy',y,allow_pickle=False)
    create(out/'verification.json',{'status':'passed_real49153_mature_one_day_return_rows_encoder120_before_target_selection','rows':len(y),'last':last,'last_label_end':end,
        'cutoff_exclusive':cutoff,'training_calendar_window':252,'alignment':alignment,'target':'y_ret_1d','return_target_scale':20.,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),nativepath,Path(encoder.__file__),Path(matrix.__file__),Path(labels.__file__),FEATURE_FILE,out/'past_features.npy',out/'past_return_targets.npy']},'actual_native_fits':0,'test_labels_read':False})
    create(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json',{'output':str(out),'verification_sha256':sha(out/'verification.json')})
    for name in ['verify_neural_BF16_medium2048_recent252returnhuber050_seed09_restart_v1_20261009.py','verify_BF16RecentReturn252Huber050169_independent_small_CPU_v1_20261009.py','BF16RecentReturn252Huber050169_complete_parent_native_stage_v1_20261009.py']:
        old=A/name;originals.append(old);generated.append(save(route(name),width(route(old.read_text(encoding='utf8')))))
    old=A/'train_neural_BF16_medium2048_recent252returnhuber050_seed09_e64_bank6_v1_20261009.py';originals.append(old);text=route(old.read_text(encoding='utf8'))
    text=once(text,'import recent252_mature_training_population_v1_20261010 as population','import recent252_mature_training_population_v1_20261010 as population\nimport daily_cross_sectional_feature_encoder120_v1_20261010 as encoder\nimport mature_population_cross120_training_matrix_v1_20261010 as encoded_population')
    text=once(text,'    features = feature_names()','    features = feature_names();encoded_features=encoder.names(features)[0]')
    text=once(text,"             FEATURE_FILE, MANIFEST, control / 'verification.json'","             Path(encoder.__file__), Path(encoded_population.__file__), A/'daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json', FEATURE_FILE, MANIFEST, control / 'verification.json'")
    text=once(text,"        x, y = to_matrix(train, features), train['y_ret_1d'].to_numpy()","        x, feature_alignment = encoded_population.matrix(lazy,train,features)\n        y = train['y_ret_1d'].to_numpy()")
    text=once(text,"'features': features, 'training_matrix_sha256'","'features': encoded_features, 'raw_features':features, 'cross_sectional_feature_alignment':feature_alignment, 'training_matrix_sha256'")
    text=once(text,'            vx = to_matrix(valid, features)',"            vx = encoder.encode(to_matrix(valid,features),valid['trade_date'].to_numpy(),features)")
    generated.append(save(route(old.name),text))
    old=A/'verify_BF16RecentReturn252Huber050169_full5_independent_GPU_v1_20261009.py';originals.append(old);text=route(old.read_text(encoding='utf8'))
    text=once(text,'    features = feature_names()',"    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder\n    features = feature_names();encoded_features=encoder.names(features)[0]")
    text=once(text,"        assert meta['features'] == features","        assert meta['features'] == encoded_features and meta['raw_features']==features")
    text=once(text,'        x = to_matrix(frame, features)',"        raw_x = to_matrix(frame,features)\n        x = encoder.encode(raw_x,frame['trade_date'].to_numpy(),features)\n        oracle=encoder.pandas_oracle(raw_x,frame['trade_date'].to_numpy(),features)\n        assert np.array_equal(x.view('u4'),oracle.view('u4'));del raw_x,oracle")
    generated.append(save(route(old.name),text))
    old=A/'verify_BF16RecentReturn252Huber050169_native42_calendar_v1_20261009.py';originals.append(old);text=route(old.read_text(encoding='utf8'))
    text=once(text,"    features=feature_names();keys=['ts_code','trade_date']","    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder\n    features=feature_names();encoded_features=encoder.names(features)[0];keys=['ts_code','trade_date']")
    text=once(text,'sourceparent=np.asarray(parent[idx],dtype=np.float64);x=to_matrix(xframe,features)',"sourceparent=np.asarray(parent[idx],dtype=np.float64);raw_x=to_matrix(xframe,features)\n        x=encoder.encode(raw_x,panel['trade_date'].to_numpy(),features)\n        oracle=encoder.pandas_oracle(raw_x,panel['trade_date'].to_numpy(),features)\n        assert np.array_equal(x.view('u4'),oracle.view('u4'));del raw_x,oracle")
    text=once(text,'_BF16_feature_names=features,_BF16_raw_features=x','_BF16_feature_names=encoded_features,_BF16_raw_features=x')
    generated.append(save(route(old.name),text))
    proof=A/'Cross120RecentReturn252Huber050_own_bank_controls_source_admission_v1_20261010.json'
    create(proof,{'status':'compiled_own120_return1d_bank_and_real49153_complete_peer_mature_feature_alignment','input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*generated,Path(encoder.__file__),Path(matrix.__file__),out/'verification.json',A/'daily_feature_encoder120_actual_CPU_and_TRAIN_controls_v1_20261010.json']},
        'raw_features':63,'encoded_features':120,'target':'y_ret_1d','return_target_scale':20.,'new_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,'GPU_admission_and_training_pending':True})
    old=A/'run_recent252_return_own_controls_and_training_queue_v2_20261010.py';text=route(old.read_text(encoding='utf8'))
    text=once(text,"ReturnProtected167_selected_candidate_sealing_v1_20261010","Cross120170_selected_candidate_sealing_v1_20261010")
    queue=save(route(old.name),text)
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed();row=start_service('actual_cross120_recent252_return_own_controls_and_training_queue_v2_20261010',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)})
    create(A/'actual_cross120_recent252_return_own_controls_and_training_queue_activation_v2_20261010.json',row)
    print({'fresh_sources':len(generated),'real_mature_fixture_rows':len(y),'encoded_features':120,'actual_target':'y_ret_1d','queue_worker':row['owned_worker_pid'],'GPU_waits_actual170_candidate_sealing':True},flush=True)

if __name__=='__main__':main()
