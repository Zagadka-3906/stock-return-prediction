"""Predeclared top-decile weighted rank-gap objective; keep all official evaluation rules."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def route(text):
    text=text.replace('stock_pairrank_embedding','stock_toppair_embedding').replace('StockPairRankEmbeddingSmall512','StockTopPairEmbeddingSmall512')
    text=text.replace('cross120_pairrank1d','cross120_toppair1d').replace('same_day_ranknet_loss_v1_20261010','same_day_top_ranknet_loss_v1_20261010').replace('same_day_ranknet_loss_actual_CPU_controls_v1_20261010','same_day_top_ranknet_loss_actual_CPU_controls_v1_20261010')
    # Verified date/feature/target fixture is reused without relabeling or changing rows.
    return text.replace('actual_stock_toppair_training_dates_fixture_location','actual_stock_pairrank_training_dates_fixture_location')

def main():
    assert allowed();inputs=[];outputs=[]
    source=A/'same_day_ranknet_loss_v1_20261010.py';inputs.append(source);text=source.read_text(encoding='utf8')
    text=text.replace('    pair=torch.nn.functional.softplus',"    emphasis=torch.where(torch.maximum(target,partner_target)>.4,10.,1.)\n    pair=emphasis*torch.nn.functional.softplus")
    outputs.append(save('same_day_top_ranknet_loss_v1_20261010.py',text))
    source=A/'verify_same_day_ranknet_loss_actual_CPU_v1_20261010.py';inputs.append(source);text=source.read_text(encoding='utf8')
    text=text.replace('same_day_ranknet_loss','same_day_top_ranknet_loss')
    text=text.replace('expected+=(abs(gap)*soft+.1*h)/len(y)',"emphasis=10. if max(c,d)>.4 else 1.\n            expected+=(emphasis*abs(gap)*soft+.1*h)/len(y)")
    text=text.replace('pairgrad=-abs(gap)*sign*sigmoid/temp/len(y)','pairgrad=-emphasis*abs(gap)*sign*sigmoid/temp/len(y)')
    text=text.replace("'passed_independent_scalar_loss_both_gradients_and_date_local_pairing_CPU'","'passed_independent_top_decile_weighted_scalar_loss_both_gradients_and_date_local_pairing_CPU'")
    outputs.append(save('verify_same_day_top_ranknet_loss_actual_CPU_v1_20261010.py',text))
    import runpy
    runpy.run_path(str(outputs[-1]),run_name='__main__')
    originals=['stock_pairrank_embedding_small512_BF16_native_v1_20261010.py','stock_pairrank_embedding_saved_tensor_decoder_v1_20261010.py','verify_stock_pairrank_embedding_small512_restart_v1_20261010.py','verify_stock_pairrank_embedding_small512_small_CPU_v1_20261010.py','train_stock_pairrank_embedding_small512_BF16_bank6_checkpoint_yield_priority173_v2_20261010.py','verify_stock_pairrank_embedding_small512_full5_independent_v1_20261010.py','stock_pairrank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','verify_stock_pairrank_embedding_six_state_native42_v1_20261010.py','run_stock_pairrank_embedding_after174_fast17_screen_v1_20261010.py','run_stock_pairrank_embedding_after174_large_allocation29_screen_v1_20261010.py']
    for name in originals:
        p=A/name;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        if name.startswith('stock_pairrank_embedding_small512_BF16_native'):
            text=text.replace('same_day_pair_ranknet_Huber_aux','same_day_top_decile_pair_ranknet_Huber_aux')
            text=text.replace("'pair_aux_weight': .1","'pair_aux_weight': .1, 'pair_top_threshold': .4, 'pair_top_multiplier': 10.")
            text=text.replace("cfg['pair_aux_weight']==.1","cfg['pair_aux_weight']==.1 and cfg['pair_top_threshold']==.4 and cfg['pair_top_multiplier']==10.")
        outputs.append(save(route(name),text))
    native=importlib.import_module(route(originals[0])[:-3])
    for p in outputs[2:]:importlib.import_module(p.stem)
    assert native.CONFIG['epochs']==32 and native.CONFIG['loss']=='same_day_top_decile_pair_ranknet_Huber_aux'
    proof=A/'stock_toppair_embedding_own32_controls46_sources_admission_v1_20261010.json'
    create(proof,{'status':'frozen_top_decile_weighted_pairrank_ID16_cross120_recent252_own32_before_GPU_fits_and_scores','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'same_day_top_ranknet_loss_actual_CPU_controls_v1_20261010.json']},'configuration':native.CONFIG,'top_emphasis_applies_only_to_training_surrogate':True,'official_scoring_rules_unchanged':True,'actual_future_X_read':False,'test_labels_read':False,'new_quality_scores':0,'own6_GPU_and_official46_pending':True})
    tasks=[('actual_stock_toppair_embedding_small512_restart_v1_20261010',route(originals[2])),('StockTopPairEmbeddingSmall512_independent_small_CPU_v1_20261009',route(originals[3])),('actual_stock_toppair_embedding_small512_bank6_v1_20261010',route(originals[4])),('StockTopPairEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',route(originals[5])),('actual_stock_toppair_embedding_six_state_native42_v1_20261010',route(originals[7])),('actual_stock_toppair_embedding_after174_fast17_screen_v1_20261010',route(originals[8])),('actual_stock_toppair_embedding_after174_large_allocation29_screen_v1_20261010',route(originals[9]))]
    source=A/'run_stock_pairrank_embedding_own32_controls46_queue_v1_20261010.py';inputs.append(source)
    queue=route(source.read_text(encoding='utf8'))
    start=queue.index('    for name,driver in ');end=queue.index(':\n',start)
    queue=queue[:start]+'    for name,driver in '+repr(tasks)+queue[end:]
    queue=queue.replace("closed('actual_stock_rank_wide32_embedding_after174_large_allocation29_screen_v1_20261010')","closed('actual_stock_pairrank_embedding_six_state_native42_v1_20261010')")
    driver=save('run_stock_toppair_embedding_own32_controls46_queue_v1_20261010.py',queue)
    assert allowed();name='actual_stock_toppair_embedding_own32_controls46_queue_v1_20261010';row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/(name+'_activation.json'),row);print({'actual_independent_weighted_loss_CPU':'passed','configuration':native.CONFIG,'actual_GPU_and_scores_pending':True,'queue':row},flush=True)
if __name__=='__main__':main()
