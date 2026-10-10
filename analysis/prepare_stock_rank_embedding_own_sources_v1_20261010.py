"""Controlled new stock-embedding centered rank1d target with Huber.1, own24 epochs and six fits."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
RECIPE='own_mature_stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24_v1_20261010'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def once(text,before,after):
    assert text.count(before)==1,(before,text.count(before));return text.replace(before,after)
def main():
    assert allowed();inputs=[];outputs=[]
    old=A/'stock_embedding_small512_BF16_native_v1_20261010.py';inputs.append(old);text=old.read_text(encoding='utf8')
    text=text.replace('own_mature_stock_embedding16_cross120_return1d_recent252_small512_BF16_e24_v1_20261010',RECIPE)
    text=text.replace("'y_ret_1d'","'y_rank'").replace("'huber_delta': .5","'huber_delta': .1").replace("cfg['huber_delta']==.5","cfg['huber_delta']==.1").replace("'return_target_scale': 20.","'return_target_scale': 1.").replace("cfg['return_target_scale']==20.","cfg['return_target_scale']==1.")
    text=text.replace('prepare_return_targets','prepare_rank_targets')
    text=once(text,'    low,high=np.quantile(y,cfg[\'return_winsor_quantiles\'])',"    assert cfg['target']=='y_rank' and np.min(y)>=-.5 and np.max(y)<=.5\n    low,high=np.quantile(y,cfg['return_winsor_quantiles'])")
    native=save('stock_rank_embedding_small512_BF16_native_v1_20261010.py',text);outputs.append(native)
    old=A/'stock_embedding_saved_tensor_decoder_v1_20261010.py';inputs.append(old);text=old.read_text(encoding='utf8')
    text=text.replace('own_mature_stock_embedding16_cross120_return1d_recent252_small512_BF16_e24_v1_20261010',RECIPE).replace("bundle['target_scale']==20.","bundle['target_scale']==1. and cfg['target']=='y_rank'").replace('/20.','/1.')
    decoder=save('stock_rank_embedding_saved_tensor_decoder_v1_20261010.py',text);outputs.append(decoder)
    old=A/'train_stock_embedding_small512_BF16_bank6_checkpoint_yield_v5_20261010.py';inputs.append(old);text=old.read_text(encoding='utf8')
    text=text.replace('stock_embedding_small512_BF16_native_v1_20261010','stock_rank_embedding_small512_BF16_native_v1_20261010').replace('stock_embedding_small512_BF16_bank6_v1_20261010','stock_rank_embedding_small512_BF16_bank6_v1_20261010').replace('actual_stock_embedding_small512_restart_v1_20261010','actual_stock_rank_embedding_small512_restart_v1_20261010').replace('actual_stock_embedding_small512_restart_location_v1_20261010.json','actual_stock_rank_embedding_small512_restart_location_v1_20261010.json').replace('actual_stock_embedding_small512_bank6_location_v1_20261010.json','actual_stock_rank_embedding_small512_bank6_location_v1_20261010.json')
    text=text.replace('import recent252_mature_training_population_v1_20261010 as population','import stock_rank_embedding_mature_population_v1_20261010 as population')
    text=once(text,"train = population.training_frame(lazy, cutoff, native.CONFIG).select(KEYS + features + ['y_ret_1d'])","train = population.training_frame(lazy, cutoff, native.CONFIG).select(KEYS + features + ['y_rank'])")
    text=once(text,"        y = train['y_ret_1d'].to_numpy()","        y = train['y_rank'].to_numpy();assert np.min(y)>=-.5 and np.max(y)<=.5")
    text=text.replace('durable_stock_embedding_checkpoint_yield','durable_stock_rank_embedding_checkpoint_yield')
    bank=save('train_stock_rank_embedding_small512_BF16_bank6_checkpoint_yield_v1_20261010.py',text);outputs.append(bank)
    old=A/'verify_stock_embedding_small512_restart_v3_20261010.py';inputs.append(old);text=old.read_text(encoding='utf8')
    text=text.replace('stock_embedding_small512_BF16_native_v1_20261010','stock_rank_embedding_small512_BF16_native_v1_20261010').replace('stock_embedding_saved_tensor_decoder_v1_20261010','stock_rank_embedding_saved_tensor_decoder_v1_20261010').replace('stock_embedding_small512_restart_v1_20261010','stock_rank_embedding_small512_restart_v1_20261010')
    text=text.replace('actual_stock_embedding_small512_restart_location_v1_20261010.json','actual_stock_rank_embedding_small512_restart_location_v1_20261010.json')
    text=text.replace("np.load(fixture/'past_return_targets.npy')","np.load(Path(read(A/'actual_stock_rank_embedding_mature_fixture_location_v1_20261010.json')['output'])/'past_rank_targets.npy')")
    text=text.replace("    paths += [embedding/'past_features121.npy'","    rank_fixture=Path(read(A/'actual_stock_rank_embedding_mature_fixture_location_v1_20261010.json')['output'])\n    paths += [rank_fixture/'past_rank_targets.npy',rank_fixture/'verification.json',embedding/'past_features121.npy'")
    restart=save('verify_stock_rank_embedding_small512_restart_v1_20261010.py',text);outputs.append(restart)
    old=A/'verify_stock_embedding_small512_small_CPU_v3_20261010.py';inputs.append(old);text=old.read_text(encoding='utf8')
    text=text.replace('stock_embedding_small512_BF16_native_v1_20261010','stock_rank_embedding_small512_BF16_native_v1_20261010').replace('stock_embedding_saved_tensor_decoder_v1_20261010','stock_rank_embedding_saved_tensor_decoder_v1_20261010').replace('StockEmbeddingSmall512','StockRankEmbeddingSmall512').replace('actual_stock_embedding_small512_restart_v1_20261010','actual_stock_rank_embedding_small512_restart_v1_20261010').replace('actual_stock_embedding_small512_restart_location_v1_20261010.json','actual_stock_rank_embedding_small512_restart_location_v1_20261010.json')
    small=save('verify_stock_rank_embedding_small512_small_CPU_v1_20261010.py',text);outputs.append(small)
    old=A/'verify_stock_embedding_small512_full5_independent_v3_20261010.py';inputs.append(old);text=old.read_text(encoding='utf8')
    text=text.replace('stock_embedding_saved_tensor_decoder_v1_20261010','stock_rank_embedding_saved_tensor_decoder_v1_20261010').replace('stock_embedding_small512_BF16_native_v1_20261010','stock_rank_embedding_small512_BF16_native_v1_20261010').replace('stock_embedding_small512_BF16_bank6_v1_20261010','stock_rank_embedding_small512_BF16_bank6_v1_20261010').replace('actual_stock_embedding_small512_bank6_v1_20261010','actual_stock_rank_embedding_small512_bank6_v1_20261010').replace('actual_stock_embedding_small512_bank6_location_v1_20261010.json','actual_stock_rank_embedding_small512_bank6_location_v1_20261010.json').replace('StockEmbeddingSmall512','StockRankEmbeddingSmall512')
    full=save('verify_stock_rank_embedding_small512_full5_independent_v1_20261010.py',text);outputs.append(full)
    #No new feature fit: the actual49153 mature keys and encoded numeric values
    #are the passed original fixture, with its actual centered rank labels.
    import numpy as np,polars as pl
    from run import FEATURE_FILE
    import stock_rank_embedding_mature_population_v1_20261010 as population
    n=importlib.import_module(native.stem);d=importlib.import_module(decoder.stem)
    assert n.CONFIG['target']=='y_rank' and n.CONFIG['huber_delta']==.1 and n.CONFIG['return_target_scale']==1.
    fixture=Path(read(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json')['output'])
    frame=population.training_frame(pl.scan_parquet(FEATURE_FILE),20191231,n.CONFIG).select('ts_code','trade_date','y_ret_1d','y_rank').limit(49153).collect()
    previous=np.load(fixture/'past_return_targets.npy');assert np.array_equal(frame['y_ret_1d'].to_numpy().view('u4'),previous.view('u4'))
    y=frame['y_rank'].to_numpy();assert np.min(y)>=-.5 and np.max(y)<=.5 and np.isfinite(y).all()
    out=Path('E:/赛题五_本机临时/stock_rank_embedding_mature_fixture_v1_20261010');out.mkdir(exist_ok=False);np.save(out/'past_rank_targets.npy',y,allow_pickle=False)
    paths=[Path(__file__),*inputs,*outputs,Path(population.__file__),FEATURE_FILE,fixture/'verification.json',out/'past_rank_targets.npy']
    create(out/'verification.json',{'status':'passed_actual49153_centered_rank1d_labels_and_exact_original_return_fixture_row_alignment','input_sha256':{str(p):sha(p) for p in paths},'label_range':[float(np.min(y)),float(np.max(y))],'target_already_centered_no_second_minus_half':True,'rows':len(y),'last':int(frame['trade_date'].max()),'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_stock_rank_embedding_mature_fixture_location_v1_20261010.json',{'output':str(out),'verification_sha256':sha(out/'verification.json')})
    create(A/'stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json',{'status':'compiled_own_rank1d_embedding_six_fit_sources_and_actual49153_centered_targets','input_sha256':{str(p):sha(p) for p in [*paths,out/'verification.json']},'configuration':n.CONFIG,'new_quality_scores':0,'actual_GPU_controls_and_training_pending':True})
    print({'fresh_sources':len(outputs),'actual_rank_target_range':[float(np.min(y)),float(np.max(y))],'second_centering':False,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
