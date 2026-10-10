"""Prepare actual restart, independent CPU and own64-epoch six-year rank5 fits."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def rename(text):return text.replace('stock_rank_embedding','stock_rank5_embedding').replace('StockRankEmbedding','StockRank5Embedding')
def main():
    assert allowed();inputs=[];outputs=[]
    source=A/'verify_stock_rank_embedding_small512_restart_priority173_v2_20261010.py';inputs.append(source);text=rename(source.read_text(encoding='utf8'))
    text=text.replace("np.clip(rng.normal(0.,.03,1024),-.1,.1).astype(np.float64)","rng.uniform(.0001,1.,1024).astype(np.float64)")
    start=text.index("    fixture=Path(read(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json')",text.index('def inputs'));end=text.index('\n\n\ndef phase',start)
    text=text[:start]+"    fixture=Path(read(A/'actual_stock_rank5_embedding_mature_fixture_location_v1_20261010.json')['output'])\n    assert read(fixture/'verification.json')['last_label_end']<20191231\n    return np.load(fixture/'past_features121.npy'),np.load(fixture/'past_rank5_targets.npy')\n"+text[end:]
    start=text.index("    fixture=Path(read(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json')",text.index('def main'));end=text.index('    pins = ',start)
    text=text[:start]+"    fixture=Path(read(A/'actual_stock_rank5_embedding_mature_fixture_location_v1_20261010.json')['output'])\n    paths += [fixture/'past_features121.npy',fixture/'past_rank5_targets.npy',fixture/'verification.json',A/'stock_rank5_embedding_saved_tensor_decoder_v1_20261010.py',A/'stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json']\n"+text[end:]
    text=''.join(line for line in text.splitlines(keepends=True)if not (".exists():closed('StockEmbedding173_selected_candidate_sealing_v1_20261010')"in line))
    text=text.replace('def main():\n','def main():\n    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed\n    assert allowed();closed(\'StockRank5Embedding_actual_mature_fixture_CPU_v1_20261010\')\n')
    restart=save('verify_stock_rank5_embedding_small512_restart_v1_20261010.py',text);outputs.append(restart)
    source=A/'verify_stock_rank_embedding_small512_small_CPU_v1_20261010.py';inputs.append(source);small=save('verify_stock_rank5_embedding_small512_small_CPU_v1_20261010.py',rename(source.read_text(encoding='utf8')));outputs.append(small)
    source=A/'train_stock_rank_embedding_small512_BF16_bank6_checkpoint_yield_priority173_v2_20261010.py';inputs.append(source);text=rename(source.read_text(encoding='utf8'))
    text=text.replace('stock_rank5_embedding_mature_population_v1_20261010','recent252_rank5_mature_training_population_v1_20261010').replace("KEYS + features + ['y_rank']","KEYS + features + ['y_rank_5mean','label_end_5d']").replace("train['y_rank'].to_numpy();assert np.min(y)>=-.5 and np.max(y)<=.5","train['y_rank_5mean'].to_numpy();assert np.min(y)>0. and np.max(y)<=1.")
    old="label_end = int(all_dates[np.searchsorted(all_dates, last) + 1])";assert text.count(old)==1;text=text.replace(old,"label_end = int(train['label_end_5d'].max())")
    start=text.index('        # Actual future-label poisoning');end=text.index("        meta = ",start)
    text=text[:start]+"        assert native.CONFIG['label_horizon_trading_days']==5\n        maturity_proof=A/'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json'\n        assert read(maturity_proof)['status']=='passed7_independent_mean5_tied_daily_rank_and_recent252_maturity_CPU_controls'\n"+text[end:]
    text=text.replace("'actual_future_training_label_poisoning_population_exact': True","'five_day_population_future_poisoning_controls_source':str(maturity_proof),'label_horizon_trading_days':5").replace('del train, past, later, sample, poisoned','del train').replace('24 fixed epochs','64 fixed epochs')
    text=''.join(line for line in text.splitlines(keepends=True)if not ("closed('StockEmbedding173_selected_candidate_sealing_v1_20261010')"in line))
    text=text.replace('durable_stock_rank5_embedding_checkpoint_yield_waiting_actual172_candidate_seal','durable_stock_rank5_embedding_completed_epoch_boundary').replace("'one_day_label_boundary_purged': True","'five_day_label_boundary_purged': True")
    text=text.replace("Path(population.__file__), A/'recent252_mature_population_actual_CPU_controls_v1_20261010.json'","Path(population.__file__), A/'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json', A/'forward5_mature_training_labels_v1_20261010.py'")
    bank=save('train_stock_rank5_embedding_small512_BF16_bank6_own64_v1_20261010.py',text);outputs.append(bank)
    for p in outputs:importlib.import_module(p.stem)
    proof=A/'stock_rank5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_actual_rank5_mature_fixture_restart_smallCPU_and_six_own64_epoch_training_sources_no_training_completion_claimed','input_sha256':{str(p):sha(p)for p in [Path(__file__),*inputs,*outputs,A/'stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json']},'fixed_epochs':64,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    text="""from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('StockRank5Embedding_actual_mature_fixture_CPU_v1_20261010')
    for p,d in read(A/'stock_rank5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json')['input_sha256'].items():assert sha(p)==d,p
    tasks=TASKS
    for name,driver in tasks:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
""".replace('TASKS',repr([('actual_stock_rank5_embedding_small512_restart_v1_20261010',restart.name),('StockRank5EmbeddingSmall512_independent_small_CPU_v1_20261009',small.name),('actual_stock_rank5_embedding_small512_bank6_v1_20261010',bank.name)]))
    driver=save('run_stock_rank5_embedding_own_training_queue_v1_20261010.py',text);row=start_service('actual_stock_rank5_embedding_own_training_queue_v1_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_stock_rank5_embedding_own_training_queue_activation_v1_20261010.json',row);print({'actual_own64_six_fit_queue_started':True,'actual_GPU_checks_pending_mature_fixture':True},flush=True)
if __name__=='__main__':main()
