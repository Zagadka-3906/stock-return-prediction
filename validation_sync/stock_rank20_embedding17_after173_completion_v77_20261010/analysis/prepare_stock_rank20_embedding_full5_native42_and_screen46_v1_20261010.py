"""Predeclare independent full5/native42 and complete17+29 rank20 comparisons to qualified173."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_stock_rank20_embedding_own64_native_and_queue_v1_20261010 import route
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();inputs=[];outputs=[]
    for old,new in [('verify_stock_rank5_embedding_small512_full5_independent_v1_20261010.py','verify_stock_rank20_embedding_small512_full5_independent_v1_20261010.py'),('stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py'),('verify_stock_rank5_embedding_six_state_native42_v1_20261010.py','verify_stock_rank20_embedding_six_state_native42_v1_20261010.py'),('run_stock_rank5_embedding_after171_fast17_screen_v1_20261010.py','run_stock_rank20_embedding_after173_fast17_screen_v1_20261010.py'),('run_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010.py','run_stock_rank20_embedding_after173_large_allocation29_screen_v1_20261010.py')]:
        source=A/old;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        text=text.replace('(169,170,171,172,173,174,175,176)','(169,170,171,172,173,174,175,176,177,178,179)')
        if 'after173' in new:
            text=text.replace('Frontier233171_complete233_family_v2_20261010','StockEmbedding173_complete36_family_v3_20261010').replace("release['scored_records']==233","release['scored_records']==36").replace('171','173')
        if 'large_allocation29' in new:
            oldpointer='actual_StockRank20EmbeddingSmall512_after173_high_impact17_screen_location_v1_20261010';assert text.count(oldpointer)==1
            text=text.replace(oldpointer,'actual_StockRank20EmbeddingSmall512_after173_large_allocation29_screen_location_v1_20261010').replace('own_Top10_BCE','own_rank20_mean_Huber')
        outputs.append(save(new,text))
    for p in outputs:importlib.import_module(p.stem)
    assert len(importlib.import_module(outputs[3].stem).cases())==17 and len(importlib.import_module(outputs[4].stem).cases())==29
    proof=A/'stock_rank20_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json';create(proof,{'status':'compiled_own_rank20_full5_native42_and_actual173_17plus29_TRAIN_only_comparison_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_rank20_embedding_own64_native_sources_preparation_v1_20261010.json']},'baseline_round':173,'expected_native_cases':42,'expected_rows':5635800,'planned_TRAIN_records':46,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})
    original=A/'run_stock_rank5_embedding_full5_native42_and_early17_queue_v1_20261010.py';text=route(original.read_text(encoding='utf8')).replace('after171_fast17','after173_fast17')
    queue=save('run_stock_rank20_embedding_full5_native42_and_early17_queue_v1_20261010.py',text)
    for name,p in [('actual_stock_rank20_embedding_full5_native42_and_early17_queue_v1_20261010',queue),('actual_stock_rank20_embedding_after173_large_allocation29_screen_v1_20261010',outputs[4])]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'own_rank20_full5_native42_and_46_TRAIN_comparisons_queued':True,'quality_pending':True},flush=True)
if __name__=='__main__':main()
