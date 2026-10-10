"""Start early native controls for a fixed scored case; search winner remains undecided."""
from pathlib import Path
import sys, ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    template=A/'qualify_stock_rank60_direct_embedding35_selected_native14_v6_20261011.py'
    score=Path('E:/赛题五_本机临时/StockRank60EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011/case017_official.json')
    row=read(score);assert row['case']==17 and row['connected_final_score']==0.4514355480841008
    assert row['configuration']=={'kind':'valid_pool_protection_v1','role':'nonflag_valid','weight':0.016,'sign':1.0,'protect_fraction':0.15}
    control=score.with_name('case017_controls.json');capsule=Path(row['official_score_cache']['official_metrics_source'])
    assert sha(control)==row['control_sha256'] and sha(capsule)==row['official_metric_capsule_sha256']
    assert read(capsule)['metrics']==row['metrics']
    source=template.read_text(encoding='utf8')
    source=source.replace('stock_rank60_direct_embedding35_selected_native14_v1_20261011','stock_rank60_fixed_leading_case17_native14_v1_20261011')
    gate="    closed('actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011')"
    assert source.count(gate)==1;source=source.replace(gate,'    # Fixed already-scored case: complete-family selection is deliberately not claimed.')
    start=source.index('    original=Path(read(');end=source.index('    for source in [Path(__file__)',start)
    block="""    import psutil
    while psutil.virtual_memory().available < 3*2**30:
        assert allowed();time.sleep(15)
    original=Path(SCORE_FILE)
    raw=read(original);assert raw['case']==17 and raw['connected_final_score']==0.4514355480841008
    recipe=raw['recipe'];model=recipes[recipe][0]
    best={**raw,'configuration':{**raw['configuration'],'recipe':recipe,'model':model,'codec':raw['configuration']['kind'],'anchor_round':183,'first2020_active':True,'stage_kind':'stock_rank60_embedding_rank60mean_direct'}}
    pins={str(p):sha(p) for p in [original,original.with_name('case017_controls.json'),Path(raw['official_score_cache']['official_metrics_source']),Path(PREPARATION_PROOF)]}
    assert pins[str(original.with_name('case017_controls.json'))]==raw['control_sha256']
    assert pins[str(Path(raw['official_score_cache']['official_metrics_source']))]==raw['official_metric_capsule_sha256']
    pilot={'records':[best],'best':best,'input_sha256':pins,'fixed_case_only':True,'search_winner_not_claimed':True}
"""
    source=source[:start]+block+source[end:]
    source=source.replace("OUT.mkdir(exist_ok=False)","OUT.mkdir(exist_ok=False)")
    source=source.replace('pilot35.json','fixed_case17.json').replace('passed_normalized35_actual_TRAIN_official_records_selected_stage_and_full_inference_pending','passed_single_fixed_scored_case17_native_checks_pending')
    source=source.replace('passed_selected_protected_tail_six_states14_native_and14_cold_and7_prefit_rejections','passed_fixed_case17_six_states14_native_and14_cold_and7_prefit_rejections')
    proof=A/'stock_rank60_fixed_leading_case17_native14_preparation_v1_20261011.json'
    source=source.replace("from run_dependency_queue_v3_20261006 import read,sha,create,owned", "from run_dependency_queue_v3_20261006 import read,sha,create,owned\nSCORE_FILE="+repr(str(score))+"\nPREPARATION_PROOF="+repr(str(proof)))
    driver=A/'verify_stock_rank60_fixed_leading_case17_native14_v1_20261011.py'
    ast.parse(source);assert not driver.exists() and not proof.exists()
    driver.write_text(source,encoding='utf8')
    pins={str(p):sha(p) for p in [Path(__file__),template,score,control,capsule,driver]}
    create(proof,{'status':'fixed_actual_scored_case17_source_and_capsule_pins_before_native_controls',
       'input_sha256':pins,'fixed_case':17,'S':row['connected_final_score'],
       'search_winner_not_claimed':True,'new_fits':0,'new_scores':0,
       'full_candidate_graph_and_actual_future_inference_still_required':True,'test_labels_read':False})
    from start_fast_completed_owned_service_v1_20261011 import start_service
    assert allowed()
    print(start_service('actual_stock_rank60_fixed_leading_case17_native14_v1_20261011',driver.name,[],{**pins,str(proof):sha(proof)}),flush=True)

if __name__=='__main__':main()
