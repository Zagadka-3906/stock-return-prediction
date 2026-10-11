"""Bind metadata spellings to existing sealed-flow sources without inventing validation completion."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    pairs=[('seal_stock_embedding173_selected_candidate_v1_20261010','seal_StockEmbedding173_selected_candidate_v1_20261010'),('seal_stock_rank_dual174_selected_candidate_v1_20261010','seal_StockRankDual174_selected_candidate_v1_20261010')]
    for alias,actual in pairs:
        assert importlib.import_module(alias).main is importlib.import_module(actual).main
    source=A/'stock_rank_dual174_full_registry_sources_preparation_v1_20261010.json';old=read(source)
    for p,d in old['input_sha256'].items():assert sha(p)==d,p
    metadata={**old,'status':'compiled_actual174_v1_eight_source_inventory_with_v2_compatibility_import_no_scientific_execution_claimed','actual_inventory_receipt_source':str(source),'actual_inventory_receipt_sha256':sha(source),'compatibility_inventory_module':'prepare_stock_rank_dual174_full_registry_sources_v2_20261010.py'}
    metadata['input_sha256']={**old['input_sha256'],str(source):sha(source),str(A/'prepare_stock_rank_dual174_full_registry_sources_v2_20261010.py'):sha(A/'prepare_stock_rank_dual174_full_registry_sources_v2_20261010.py')}
    create(A/'stock_rank_dual174_full_registry_sources_preparation_v2_20261010.json',metadata)
    paths=[Path(__file__),source,A/'stock_rank_dual174_full_registry_sources_preparation_v2_20261010.json',*[A/(module+'.py') for pair in pairs for module in pair]]
    create(A/'stock173174_exact_source_name_compatibility_admission_v1_20261010.json',{'status':'passed_exact_same_sealer_main_objects_and_actual174_v1_metadata_SHA_bound_compatibility_names','input_sha256':{str(p):sha(p) for p in paths},'model_parameters_changed':False,'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'exact_sealer_import_aliases':2,'metadata_inventory_bytes_verified':True,'new_scientific_completion_claims':0},flush=True)
if __name__=='__main__':main()
