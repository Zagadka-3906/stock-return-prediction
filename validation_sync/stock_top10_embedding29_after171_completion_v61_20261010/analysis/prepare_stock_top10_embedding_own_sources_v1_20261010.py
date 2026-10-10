"""New weighted Top10 classifier using mature centered-rank labels; all GPU phases wait174 seal."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def rename(text):
    text=text.replace('stock_rank_embedding','stock_top10_embedding').replace('StockRankEmbeddingSmall512','StockTop10EmbeddingSmall512')
    #Use the already verified raw mature centered-rank fixture/population; the native
    #classifier alone converts raw labels to the frozen binary target.
    text=text.replace('stock_top10_embedding_mature_population_v1_20261010','stock_rank_embedding_mature_population_v1_20261010').replace('actual_stock_top10_embedding_mature_fixture_location_v1_20261010','actual_stock_rank_embedding_mature_fixture_location_v1_20261010')
    text=text.replace('StockEmbedding173_selected_candidate_sealing_v1_20261010','StockRankDual174_selected_candidate_sealing_v1_20261010')
    return text
def main():
    assert allowed();inputs=[];outputs=[]
    source=A/'stock_rank_embedding_small512_BF16_native_v1_20261010.py';inputs.append(source);text=rename(source.read_text(encoding='utf8'))
    text=text.replace("'loss': 'Huber', 'huber_delta': .1","'loss': 'BCEWithLogits', 'huber_delta': None, 'positive_weight':9., 'top_rank_threshold':.4, 'derived_target':'I_centered_rank_gt_0p4'")
    text=text.replace("'return_winsor_quantiles': [.005,.995]","'return_winsor_quantiles': None")
    text=text.replace('own_mature_stock_top10_embedding16_cross120_rank1d_recent252_small512_BF16_e24_v1_20261010','own_mature_stock_top10_embedding16_cross120_BCE_Pos9_recent252_small512_BF16_e24_v1_20261010')
    old="assert cfg['loss']=='Huber' and cfg['huber_delta']==.1 and cfg['return_target_scale']==1. and cfg['return_winsor_quantiles']==[.005,.995]"
    assert old in text;text=text.replace(old,"assert cfg['loss']=='BCEWithLogits' and cfg['positive_weight']==9. and cfg['top_rank_threshold']==.4 and cfg['return_target_scale']==1. and cfg['return_winsor_quantiles'] is None")
    old="torch.nn.functional.huber_loss(pred.float(), yt[part], delta=cfg['huber_delta'])"
    assert old in text;text=text.replace(old,"torch.nn.functional.binary_cross_entropy_with_logits(pred.float(), yt[part], pos_weight=torch.tensor(cfg['positive_weight'],dtype=torch.float32,device=device))")
    begin=text.index("    low,high=np.quantile(y,cfg['return_winsor_quantiles'])")
    text=text[:begin]+"    assert cfg['top_rank_threshold']==.4 and cfg['positive_weight']==9.\n    target=(y>cfg['top_rank_threshold']).astype(np.float32)\n    return target,[0.,1.]\n"
    native=save('stock_top10_embedding_small512_BF16_native_v1_20261010.py',text);outputs.append(native)
    source=A/'stock_rank_embedding_saved_tensor_decoder_v1_20261010.py';inputs.append(source);text=rename(source.read_text(encoding='utf8')).replace('own_mature_stock_top10_embedding16_cross120_rank1d_recent252_small512_BF16_e24_v1_20261010','own_mature_stock_top10_embedding16_cross120_BCE_Pos9_recent252_small512_BF16_e24_v1_20261010')
    outputs.append(save('stock_top10_embedding_saved_tensor_decoder_v1_20261010.py',text))
    templates=[('verify_stock_rank_embedding_small512_restart_priority173_v2_20261010.py','verify_stock_top10_embedding_small512_restart_priority174_v1_20261010.py'),('train_stock_rank_embedding_small512_BF16_bank6_checkpoint_yield_priority173_v2_20261010.py','train_stock_top10_embedding_small512_BF16_bank6_checkpoint_yield_priority174_v1_20261010.py'),('verify_stock_rank_embedding_small512_small_CPU_v1_20261010.py','verify_stock_top10_embedding_small512_small_CPU_v1_20261010.py'),('verify_stock_rank_embedding_small512_full5_independent_v1_20261010.py','verify_stock_top10_embedding_small512_full5_independent_v1_20261010.py')]
    for old,new in templates:
        source=A/old;inputs.append(source);text=rename(source.read_text(encoding='utf8'))
        if 'restart' in old:text=text.replace("np.clip(rng.normal(0.,.03,1024),-.1,.1).astype(np.float64)","rng.uniform(-.5,.5,1024).astype(np.float64)")
        outputs.append(save(new,text))
    import numpy as np
    import stock_top10_embedding_small512_BF16_native_v1_20261010 as module
    fixture=Path(read(A/'actual_stock_rank_embedding_mature_fixture_location_v1_20261010.json')['output']);labels=np.load(fixture/'past_rank_targets.npy')
    target,bounds=module.prepare_rank_targets(labels,module.CONFIG)
    assert len(target)==49153 and bounds==[0.,1.] and np.array_equal(target,(labels>.4).astype(np.float32))
    assert 0<int(target.sum())<len(target)
    create(A/'stock_top10_embedding_own_sources_admission_v1_20261010.json',{'status':'compiled_new_Top10_BCE_Pos9_sources_and_actual49153_binary_target_conversion_CPU_passed_GPU_controls_six_fits_pending','configuration':module.CONFIG,'actual_rows':len(target),'actual_positive_labels':int(target.sum()),'derived_label_rule':'mature centered y_rank > 0.4; never recenter already centered labels','inference':'raw saved network logits; ranking invariant to sigmoid, no future labels used','all_same_stock_vocabulary_and_full_daily120_encoder':True,'new_fits':0,'new_quality_scores':0,'input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,fixture/'past_rank_targets.npy',fixture/'verification.json']},'GPU_priority':'all new phases wait actual selected174 sealer PAS','test_labels_read':False})
    queuecode='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('StockRankDual174_selected_candidate_sealing_v1_20261010')
    proof=read(A/'stock_top10_embedding_own_sources_admission_v1_20261010.json')
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_stock_top10_embedding_small512_restart_v1_20261010','verify_stock_top10_embedding_small512_restart_priority174_v1_20261010.py'),('StockTop10EmbeddingSmall512_independent_small_CPU_v1_20261009','verify_stock_top10_embedding_small512_small_CPU_v1_20261010.py'),('actual_stock_top10_embedding_small512_bank6_v1_20261010','train_stock_top10_embedding_small512_BF16_bank6_checkpoint_yield_priority174_v1_20261010.py'),('StockTop10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','verify_stock_top10_embedding_small512_full5_independent_v1_20261010.py')]
    for name,driver in tasks:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
'''
    queue=save('run_stock_top10_embedding_own_training_queue_v1_20261010.py',queuecode)
    row=start_service('actual_stock_top10_embedding_own_training_queue_v1_20261010',queue.name,[],{str(queue):sha(queue)})
    create(A/'actual_stock_top10_embedding_own_training_queue_activation_v1_20261010.json',row)
    print({'actual_binary_label_CPU_passed':49153,'positive_rows':int(target.sum()),'new_GPU_training':'queued_after174_seal'},flush=True)
if __name__=='__main__':main()
