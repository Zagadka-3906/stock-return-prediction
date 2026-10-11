"""Adapt the audited single-model full-family factory to actual504-day configuration and175/187 anchors."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    source=A/'prepare_StockRank20Seed10Embedding186_complete48_pipeline_v2_20261011.py'
    text=source.read_text(encoding='utf8')
    text=text.replace('stock_rank20seed10_embedding','stock_rank20long_embedding').replace('StockRank20Seed10Embedding','StockRank20LongEmbedding').replace('STOCK_RANK20SEED10_EMBEDDING','STOCK_RANK20LONG_EMBEDDING')
    text=text.replace('rank20mean_recent252','rank20mean_recent504').replace('Cross120Recent252Rank20Mean_seed10_e64','Cross120Recent504Rank20Mean_seed09_e64')
    exact={
        'complete48_after185':'complete48_after187',
        "'17402'":"'17538'", "'qa97'":"'qa99'", "'QA97'":"'QA99'", "'qa_v97'":"'qa_v99'",
        "'180':'186','179':'185','173':'175','463':'469','91':'97'":"'180':'188','179':'187','173':'175','463':'471','91':'99'",
        "(186,185,(469,))":"(188,187,(471,))", "'(186, 97, 48)'":"'(188, 99, 48)'",
        'stock_rank20long_embedding186':'stock_rank20long_embedding188',
        "name='StockRank20LongEmbedding186_complete48_family_v2_20261011'":"name='StockRank20LongEmbedding188_complete48_family_v1_20261011'",
        'optimization_20261003_r186':'optimization_20261003_r188','第186轮_20261010':'第188轮_20261010',
        "native.CONFIG['seed']==20261010":"native.CONFIG['seed']==20261009",
        "native.CONFIG['training_calendar_window']==252":"native.CONFIG['training_calendar_window']==504",
        "'expected_full_board':17402":"'expected_full_board':17538","'parent_rounds':[175,185]":"'parent_rounds':[175,187]",
        'seed10_complete48_normalization_native14_sources_admission_v1_20261011.json':'rank20long_complete48_normalization_native14_sources_admission_v1_20261011.json',
        'PairTop184185_complete_reference_routes_v9_20261010.json':'rank20_two_seed187_full_execution_sources_admission_v2_20261011.json',
        'StockForward20Embedding185_complete48_family_v6_after_Dual25_recovery_v1_20261010':'StockForward20Embedding187_complete48_family_v6_after_Dual25_recovery_v1_20261010',
        'StockTopPairEmbedding185_complete48_family_v9_complete_references_v9_20261010':'Rank20TwoSeed187_complete88_family_v2_20261011',
        'actual_stock_rank20long_embedding_own64_controls46_queue_v2_20261010':'actual_run_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011',
    }
    for old,new in exact.items():
        assert old in text,old;text=text.replace(old,new)
    text=text.replace("'_v2_20261011.py',new)","'_v1_20261011.py',new)")
    for prefix in ['full_execution_sources_admission','full_family_preflight','candidate_sources_preparation','full_registry_sources_preparation']:
        text=text.replace('stock_rank20long_embedding188_'+prefix+'_v2_20261011.json','stock_rank20long_embedding188_'+prefix+'_v1_20261011.json')
    text=text.replace("'actual_callback_CPU_count':11","'actual_callback_CPU_count':11")
    text=text.replace("'full186_pipeline_queued'","'full188_pipeline_queued'")
    driver=A/'prepare_StockRank20LongEmbedding188_complete48_pipeline_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    admission=A/'rank20long_complete188_factory_source_admission_v1_20261011.json'
    create(admission,{'status':'compiled_long504_single_model_complete188_factory_before_candidate_source_generation',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,A/'rank20long_complete48_normalization_native14_sources_admission_v1_20261011.json']},
        'expected_records':48,'expected_full_board':17538,'QA':99,'parent_rounds':[175,187],'training_calendar_window':504,
        'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'long504_full188_factory_created':True,'actual_candidate_and_future_sources_not_yet_dispatched':True},flush=True)

if __name__=='__main__':main()
