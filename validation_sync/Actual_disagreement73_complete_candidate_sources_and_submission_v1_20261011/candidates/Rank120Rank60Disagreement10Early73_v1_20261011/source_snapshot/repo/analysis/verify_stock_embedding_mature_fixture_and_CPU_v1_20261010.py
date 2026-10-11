"""Real mature-stock vocabulary, unknown handling and independent CPU replay controls."""
from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_embedding_mature_fixture_CPU_v1_20261010')
for key in ('TEMP','TMP','TMPDIR','TORCH_HOME','TORCHINDUCTOR_CACHE_DIR','TRITON_CACHE_DIR','CUDA_CACHE_PATH'):os.environ[key]=str(OUT/'tmp'/key)
os.environ['CUDA_CACHE_DISABLE']='1';os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    import numpy as np,polars as pl,torch
    import stock_identity_embedding_network_v1_20261010 as embedding
    import stock_embedding_small512_BF16_native_v1_20261010 as native
    from stock_embedding_saved_tensor_decoder_v1_20261010 import predict_saved_tensors
    import recent252_mature_training_population_v1_20261010 as population
    from run import FEATURE_FILE
    fixture=Path(read(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json')['output'])
    proof=read(fixture/'verification.json');assert proof['last_label_end']<20191231
    lazy=pl.scan_parquet(FEATURE_FILE)
    frame=population.training_frame(lazy,20191231,native.CONFIG).select('ts_code','trade_date','y_ret_1d').limit(49153).collect()
    assert len(frame)==proof['rows'] and frame['trade_date'].max()==proof['last']
    y=np.load(fixture/'past_return_targets.npy')
    assert np.array_equal(frame['y_ret_1d'].to_numpy().view('u4'),y.view('u4'))
    vocabulary=sorted(set(frame['ts_code'].to_list()));numerical=np.load(fixture/'past_features.npy')
    x=embedding.attach(numerical,frame['ts_code'].to_list(),vocabulary)
    assert np.array_equal(numerical.view('u4'),x[:,:120].copy().view('u4'))
    mapping={code:i+1 for i,code in enumerate(vocabulary)}
    assert np.array_equal(x[:,-1],np.asarray([mapping[code] for code in frame['ts_code']],dtype=np.float32))
    unknown=embedding.attach(numerical[:3],['future_unseen','unknown','not_in_mature_fit'],vocabulary)
    assert np.all(unknown[:,-1]==0)
    # Vocabulary fit sees only this mature frame; later identities are transform-only.
    expanded=embedding.attach(numerical[:3],[vocabulary[0],'future_unseen',vocabulary[-1]],vocabulary)
    assert expanded[0,-1]==1 and expanded[1,-1]==0 and expanded[2,-1]==len(vocabulary)
    torch.manual_seed(20261010);cfg=dict(native.CONFIG)
    model=embedding.network(121,cfg)
    state={k:v.detach().clone() for k,v in model.state_dict().items()}
    mean=np.zeros(121,dtype=np.float32);scale=np.ones(121,dtype=np.float32)
    bundle={'kind':'mlp','config':cfg,'state':state,'mean':mean,'scale':scale,'target_scale':20.}
    actual=torch.cuda.is_available;torch.cuda.is_available=lambda:False
    try:
        sample=x[:10017].copy();sample[::13,4]=np.nan;sample[::17,5]=np.inf;sample[::19,6]=-np.inf
        raw=native.predict_arrays(bundle,sample);oracle=predict_saved_tensors(bundle,sample,device='cpu')
        assert np.array_equal(raw.view('u8'),oracle.view('u8'))
        controls=[]
        for n in (0,1,4097,8192):
            primary=native.predict_arrays(bundle,sample[:n]);independent=predict_saved_tensors(bundle,sample[:n],device='cpu')
            assert np.array_equal(primary.view('u8'),raw[:n].view('u8')) and np.array_equal(independent.view('u8'),raw[:n].view('u8'))
            controls.append({'rows':n,'native_independent_cold_prefix_bits_exact':True})
        rejected=[]
        for value in (-1.,4651.,.5,float('nan')):
            bad=sample[:1].copy();bad[0,-1]=value
            try:embedding.validate_ids(bad)
            except AssertionError:rejected.append(str(value))
            else:raise AssertionError('invalid_stock_id_accepted')
    finally:torch.cuda.is_available=actual
    assert not OUT.exists();OUT.mkdir(parents=True)
    np.save(OUT/'past_features121.npy',x,allow_pickle=False)
    pins={str(p):sha(p) for p in [Path(__file__),Path(embedding.__file__),Path(native.__file__),A/'stock_embedding_saved_tensor_decoder_v1_20261010.py',fixture/'verification.json',fixture/'past_features.npy',fixture/'past_return_targets.npy',OUT/'past_features121.npy']}
    create(OUT/'verification.json',{'status':'passed_actual_mature49153_stock_mapping_and10017_CPU_independent_replay','input_sha256':pins,'mature_vocabulary':vocabulary,'vocabulary_fit_uses_only_mature_training_rows':True,'unknown_id':0,'unknown_embedding_exact_zero':True,'CPU_prefix_controls':controls,'invalid_ID_rejections':rejected,'new_quality_scores':0,'actual_native_fits':0,'test_labels_read':False,'GPU_training_and_restart_pending':True})
    create(A/'actual_stock_embedding_mature_fixture_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print('PASS actual49153 mature vocabulary, unknown0, independent CPU10017 and4 cold prefixes; GPU/annual scoring pending',flush=True)
if __name__=='__main__':main()
