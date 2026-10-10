from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    import prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010 as family
    import stock_toppair_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    import normalize_completed_stock_toppair_embedding_complete48_after184_v8_20261010 as normalizer
    assert set(stage.BACKENDS)==set(normalizer.RECIPES)
    import importlib
    for recipe,(n,d) in stage.BACKENDS.items():
        native=importlib.import_module(n);importlib.import_module(d)
        assert native.CONFIG['recipe']=='own_mature_'+recipe+'_v1_20261010' and native.CONFIG['epochs']==32 and native.CONFIG['pair_top_multiplier']==10.
    proof=read(A/'actual_PairRank_native42_admission_routes_v8_20261010.json')
    for r in proof['admission_copies']:assert sha(r['actual_admission'])==sha(r['reference_copy'])==r['sha256']
    check=A/'PairTop185_actual_native_recipe_and_exact_admission_CPU_v1_20261010.json'
    create(check,{'status':'passed_actual_toppair_recipe_backend_normalizer_and_two_exact_source_admission_copies_CPU','recipes':list(stage.BACKENDS),'actual_top_loss_CPU':read(A/'same_day_top_ranknet_loss_actual_CPU_controls_v1_20261010.json')['status'],'actual13_pair_parent_callbacks':True,'actual14_top_parent_callbacks':True,'top_own6_and_quality_pending':True,'new_quality_scores':0,'test_labels_read':False})
    template=A/'publish_verified_seal175_routes7_CPU10_sources_main_v73_20261010.py'
    paths=list(dict.fromkeys([Path(__file__),template,*family.source_paths(),check,A/'route_StockTopPair185_exact_verified_children_v1_20261010.py',A/'TopPair185_generated_child_import_recovery_v2_20261010.json',A/'actual_PairRank_native42_admission_routes_v8_20261010.json',*[Path(p) for p in proof['input_sha256']],A/'PairRank184_native42_three_idle_helper_recovery_v8_20261010.json',A/'stock_toppair_embedding185_full_execution_sources_admission_v3_20261010.json',A/'stock_toppair_embedding_own32_controls46_sources_admission_v1_20261010.json',A/'same_day_top_ranknet_loss_actual_CPU_controls_v1_20261010.json',A/'verify_same_day_top_ranknet_loss_actual_CPU_v1_20261010.py',A/'prepare_stock_toppair_embedding_own32_controls46_v1_20261010.py',A/'recover_TopPair185_generated_child_import_v2_20261010.py']))
    text=template.read_text(encoding='utf8');start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('Verified_seal175_routes7_CPU10_sources_v73_20261010','PairTop185_native_admission_sources_v1_20261010').replace('Verified_seal175_routes7_CPU10_sources_main_v73_20261010','PairTop185_native_admission_sources_main_v1_20261010').replace('Verified_seal175_routes7_CPU10_sources_main_receipt_v73_20261010','PairTop185_native_admission_sources_main_receipt_v1_20261010')
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'actual_pair_own6_full5_preserved_native42_admission_recovery_and_top_emphasis185_predeclared_sources','actual_pair_own_fits':6,'actual_pair_independent_annual_controls':5,'actual_top_loss_CPU_temperature_controls':3,'actual_top_date_local_pair_draws_CPU':800,'actual_top_parent_callbacks_CPU':14,'actual_pair_parent_callbacks_CPU':13,'full185_records':48,'full185_controls':44,'full185_prefix_controls':132,'full185_expected_board':17354,'full185_QA':96,'actual_future_X_read':False,'top_own6_and_official_scores_pending':True,'original_missing_admission_and_import_failures_preserved':True,'official_score_weights_and_pool_rules_unchanged':True}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存已完成175推理及封装修复[^']*'",repr('保留同日排序六模型与完整五年度独立推理；补齐实际源码验证引用；冻结Top组加权排序新目标及185轮48项QA96'),text);assert count==1
    p=A/'publish_PairTop185_native_admission_sources_main_v1_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    assert allowed();name='actual_PairTop185_native_admission_sources_main_v1_20261010';row=start_service(name,p.name,[],{str(p):sha(p),str(check):sha(check)})
    create(A/(name+'_activation.json'),row);print({'frozen_source_files':len(paths),'actual_schema_CPU':'passed','publication':row},flush=True)
if __name__=='__main__':main()
