"""Declare distinct centered-rank saved-state replay and bounded TRAIN-only17 screen."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    mapping={
      'stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010':'stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010',
      'stock_embedding_after_complete_qualified_parent_v1_20261010':'stock_rank_embedding_after_complete_qualified_parent_v1_20261010',
      'stock_embedding_small512_BF16_native_v1_20261010':'stock_rank_embedding_small512_BF16_native_v1_20261010',
      'stock_embedding_saved_tensor_decoder_v1_20261010':'stock_rank_embedding_saved_tensor_decoder_v1_20261010',
      'stock_embedding16_cross120_return1d_recent252_small512_BF16_e24':'stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24',
      'stock_embedding_return1d_direct':'stock_rank_embedding_rank1d_direct',
      'stock_embedding_small512_BF16_bank6_v1_20261010':'stock_rank_embedding_small512_BF16_bank6_v1_20261010',
      'actual_stock_embedding_small512_bank6_v1_20261010':'actual_stock_rank_embedding_small512_bank6_v1_20261010',
      'actual_stock_embedding_small512_bank6_location_v1_20261010':'actual_stock_rank_embedding_small512_bank6_location_v1_20261010',
      'StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009':'StockRankEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',
      'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009':'actual_StockRankEmbeddingSmall512_full5_independent_location_v1_20261009',
      'stock_embedding_six_state_native42_v1_20261010':'stock_rank_embedding_six_state_native42_v1_20261010',
      'actual_stock_embedding_six_state_native42_v2_20261010':'actual_stock_rank_embedding_six_state_native42_v1_20261010',
      'actual_stock_embedding_six_state_native42_location_v1_20261010':'actual_stock_rank_embedding_six_state_native42_location_v1_20261010',
      'stock_embedding_native_stage_and_four_parent_routes_admission_v1_20261010':'stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010',
      'rank_MLP512_StockEmbedding16_Cross120Recent252ReturnHuber050_seed09_e24':'rank_MLP512_StockRankEmbedding16_Cross120Recent252RankHuber010_seed09_e24',
      'Frontier133172_selected_candidate_sealing_v1_20261010':'StockEmbedding173_selected_candidate_sealing_v1_20261010',
      'StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010':'StockRankEmbeddingSmall512_after170_high_impact17_screen_v1_20261010',
      'actual_StockEmbeddingSmall512_after170_high_impact17_screen_location_v1_20261010':'actual_StockRankEmbeddingSmall512_after170_high_impact17_screen_location_v1_20261010',
    }
    specs=[('stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py'),('verify_stock_embedding_six_state_native42_v2_20261010.py','verify_stock_rank_embedding_six_state_native42_v1_20261010.py'),('run_stock_embedding_after170_fast17_screen_v2_20261010.py','run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py')]
    paths=[Path(__file__),A/'stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json']
    for source,destination in specs:
        original=A/source;text=original.read_text(encoding='utf8')
        # Simultaneous replacements prevent a newly renamed route matching a later key.
        import re
        text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
        if destination.startswith('stock_rank_embedding_after'):text=text.replace('in (169,170,171,172)','in (169,170,171,172,173)')
        dest=A/destination;assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n');paths.extend([original,dest])
    screen=__import__('run_stock_rank_embedding_after170_fast17_screen_v1_20261010');cases=screen.cases()
    assert len(cases)==17 and cases[0]['kind']=='anchor170'
    native=__import__('stock_rank_embedding_small512_BF16_native_v1_20261010')
    assert native.CONFIG['target']=='y_rank' and native.CONFIG['target_scale']==1.
    create(A/'stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json',{'status':'passed_compiled_distinct_rank_stage_and_predeclared17_TRAIN_screen_actual42_and_scores_pending','cases':cases,'configuration':native.CONFIG,'expected_saved_states':6,'expected_native_cases':42,'expected_cold_cases':42,'expected_prefit_rejections':7,'expected_official_scores':17,'nonidentity_full_controls':16,'nonidentity_cold_controls':48,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,'input_sha256':{str(p):sha(p) for p in paths}})
    from handoff_ready_goss_full_execution_20261006 import start_service
    driver=A/'run_stock_rank_embedding_native42_and_fast17_queue_v1_20261010.py'
    code='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('actual_stock_rank_embedding_own_training_queue_v2_20261010')
    proof=read(A/'stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json')
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    for name,source in [('actual_stock_rank_embedding_six_state_native42_v1_20261010','verify_stock_rank_embedding_six_state_native42_v1_20261010.py'),('actual_stock_rank_embedding_after170_fast17_screen_v1_20261010','run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py')]:
        assert allowed();p=A/source;row=start_service(name,p.name,[],{str(p):sha(p)})
        create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
'''
    assert not driver.exists();compile(code,str(driver),'exec');driver.write_text(code,encoding='utf8',newline='\n')
    row=start_service('actual_stock_rank_embedding_native42_and_fast17_queue_v1_20261010',driver.name,[],{str(driver):sha(driver)})
    create(A/'actual_stock_rank_embedding_native42_and_fast17_queue_activation_v1_20261010.json',row)
    print({'status':'rank_stage42_and_TRAIN17_predeclared_and_queued','new_quality_scores':0},flush=True)
if __name__=='__main__':main()
