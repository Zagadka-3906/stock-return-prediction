from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    import prepare_StockPairRankEmbedding184_complete48_pipeline_v4_20261010 as family
    import stock_pairrank_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    import normalize_completed_stock_pairrank_embedding_complete48_after183_v8_20261010 as normalization
    assert set(stage.BACKENDS)==set(normalization.RECIPES)
    for recipe,(native_name,decoder_name) in stage.BACKENDS.items():
        import importlib
        native=importlib.import_module(native_name);importlib.import_module(decoder_name)
        assert native.CONFIG['recipe']=='own_mature_'+recipe+'_v1_20261010'
        assert native.CONFIG['epochs']==32 and native.CONFIG['stock_embedding_dim']==16 and native.CONFIG['loss']=='same_day_pair_ranknet_Huber_aux'
    check=A/'PairRank184_actual_recipe_backend_schema_CPU_v2_20261010.json'
    create(check,{'status':'passed_actual_native_recipe_decoder_normalizer_consistency_CPU','recipes':list(stage.BACKENDS),'annual_fit_and_quality_pending':True,'test_labels_read':False,'new_quality_scores':0})
    template=A/'publish_verified_seal175_routes7_CPU10_sources_main_v73_20261010.py'
    paths=list(dict.fromkeys([Path(__file__),template,*family.source_paths(),check,A/'stock_pairrank_embedding184_full_execution_sources_admission_v3_20261010.json',A/'verify_same_day_ranknet_loss_actual_CPU_v1_20261010.py',A/'actual_stock_pairrank_training_dates_fixture_location_v1_20261010.json',A/'stock_pairrank_embedding_own32_controls46_sources_admission_v1_20261010.json']))
    text=template.read_text(encoding='utf8');start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('Verified_seal175_routes7_CPU10_sources_v73_20261010','PairRank184_frozen_sources_v2_20261010').replace('Verified_seal175_routes7_CPU10_sources_main_v73_20261010','PairRank184_frozen_sources_main_v2_20261010').replace('Verified_seal175_routes7_CPU10_sources_main_receipt_v73_20261010','PairRank184_frozen_sources_main_receipt_v2_20261010')
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'frozen_distinct_same_day_pairrank_ID16_cross120_own32_complete48_QA95_sources','actual_scalar_loss_gradient_temperature_controls':3,'actual_date_local_pair_draws_CPU':800,'actual_13_parent_callbacks_CPU':True,'actual49153_dates_fixture_exact':True,'full184_records':48,'full184_controls':44,'full184_prefix_controls':132,'full184_expected_board':17306,'full184_QA':95,'actual_future_X_read':False,'scores_and_full_submission_qualification_pending':True,'original_failures_preserved':True}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存已完成175推理及封装修复[^']*'",repr('冻结同日成对排序股票身份120特征32轮独立模型与184轮完整48项QA95；实际独立损失梯度及13父回调CPU检查'),text);assert count==1
    p=A/'publish_PairRank184_frozen_sources_main_v2_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    assert allowed();name='actual_PairRank184_frozen_sources_main_v2_20261010';row=start_service(name,p.name,[],{str(p):sha(p),str(check):sha(check)})
    create(A/(name+'_activation.json'),row);print({'source_files':len(paths),'actual_backend_CPU':'passed','publication':row},flush=True)
if __name__=='__main__':main()
