"""Predeclare new Top10 classifier native42 and17 TRAIN comparisons after qualified174."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();inputs=[];outputs=[]
    specs=[('stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py','stock_top10_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py'),('verify_stock_rank_embedding_six_state_native42_v1_20261010.py','verify_stock_top10_embedding_six_state_native42_v1_20261010.py'),('run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py','run_stock_top10_embedding_after174_fast17_screen_v1_20261010.py')]
    for old,new in specs:
        source=A/old;inputs.append(source);text=source.read_text(encoding='utf8').replace('stock_rank_embedding','stock_top10_embedding').replace('StockRankEmbeddingSmall512','StockTop10EmbeddingSmall512')
        text=text.replace('stock_top10_embedding16_cross120_rank1d_recent252_small512_BF16_e24','stock_top10_embedding16_cross120_top10_BCE_Pos9_recent252_small512_BF16_e24').replace('stock_top10_embedding_rank1d_direct','stock_top10_embedding_BCE_classifier_direct')
        text=text.replace('stock_top10_embedding_native_stage_and_fast17_sources_admission_v1_20261010','stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010')
        text=text.replace('StockEmbedding173_selected_candidate_sealing_v1_20261010','StockRankDual174_selected_candidate_sealing_v1_20261010')
        text=text.replace('rank_MLP512_StockRankEmbedding16_Cross120Recent252RankHuber010_seed09_e24','rank_MLP512_StockTop10Embedding16_Cross120Recent252BCEPos9_seed09_e24')
        if old.startswith('stock_rank_embedding_after'):text=text.replace('in (169,170,171,172,173)','in (169,170,171,172,173,174)')
        if old.startswith('run_stock_rank'):
            text=text.replace("closed('Cross120170_complete132_family_v5_20261010')","closed('StockRankDual174_complete44_family_v2_20261010')")
            text=text.replace('after170','after174').replace('anchor170','anchor174').replace('complete_parent170','complete_parent174').replace('optimization_20261003_r170','optimization_20261003_r174').replace('round170_receipt.json','round174_receipt.json').replace("release['scored_records']==132","release['scored_records']==44").replace("'parent_round':170","'parent_round':174")
        dest=A/new;assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n');outputs.append(dest)
    screen=importlib.import_module(outputs[2].stem);plan=screen.cases();assert len(plan)==17 and plan[0]['kind']=='anchor174'
    import stock_top10_embedding_small512_BF16_native_v1_20261010 as native
    create(A/'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010.json',{'status':'compiled_predeclared_Top10_BCE_Pos9_native42_and17_TRAIN_only_comparisons_before_training_or_scores','cases':plan,'configuration':native.CONFIG,'expected_native':42,'expected_cold':42,'expected_prefit_rejections':7,'expected_scores':17,'nonidentity_full_controls':16,'nonidentity_prefix_controls':48,'highest_fully_qualified_parent_round_required':174,'new_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,'input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_top10_embedding_own_sources_admission_v1_20261010.json']}})
    queue=A/'run_stock_top10_embedding_native42_and_after174_fast17_queue_v1_20261010.py'
    code='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('actual_stock_top10_embedding_own_training_queue_v1_20261010')
    for p,d in read(A/'stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010.json')['input_sha256'].items():assert sha(p)==d,p
    for name,driver in [('actual_stock_top10_embedding_six_state_native42_v1_20261010','verify_stock_top10_embedding_six_state_native42_v1_20261010.py'),('actual_stock_top10_embedding_after174_fast17_screen_v1_20261010','run_stock_top10_embedding_after174_fast17_screen_v1_20261010.py')]:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
'''
    assert not queue.exists();compile(code,str(queue),'exec');queue.write_text(code,encoding='utf8',newline='\n')
    row=start_service('actual_stock_top10_embedding_native42_and_after174_fast17_queue_v1_20261010',queue.name,[],{str(queue):sha(queue)})
    create(A/'actual_stock_top10_embedding_native42_and_after174_fast17_queue_activation_v1_20261010.json',row)
    print({'classifier42_and_TRAIN17':'predeclared_and_queued','new_quality_scores':0},flush=True)
if __name__=='__main__':main()
