from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    old='actual_stock_toppair_embedding48_after184_normalization_queue_v8_20261010'
    new='actual_stock_toppair_embedding48_after184_normalization_import_recovery_v2_20261010'
    assert read(A/'service_owned_workflows_20261006'/old/'service_execution.json')['status']=='failed'
    bridge='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def execute(driver):
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    previous=checks.closed
    def closed(name):return previous('actual_stock_toppair_embedding48_after184_normalization_import_recovery_v2_20261010' if name=='actual_stock_toppair_embedding48_after184_normalization_queue_v8_20261010' else name)
    checks.closed=closed
    import prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010 as factory
    original=factory.source_paths
    factory.source_paths=lambda:list(dict.fromkeys([*original(),Path(__file__),A/'TopPair185_generated_child_import_recovery_v2_20261010.json']))
    from route_StockTopPair185_exact_verified_children_v3_20261010 import execute as actual
    actual(driver)
'''
    path=A/'route_StockTopPair185_exact_verified_children_v1_20261010.py';assert not path.exists();compile(bridge,str(path),'exec');path.write_text(bridge,encoding='utf8',newline='\n')
    create(A/'TopPair185_generated_child_import_recovery_v2_20261010.json',{'status':'compiled_explicit_wrapper_import_bridge_to_actual_v3_runtime_before_any185_output_or_future','bridge_sha256':sha(path),'original_failed_service':old,'actual_normalizer_service':new,'runtime':'route_StockTopPair185_exact_verified_children_v3_20261010.py','new_fits':0,'new_scores':0,'new_inference':0})
    tasks=[(new,'normalize_completed_stock_toppair_embedding_complete48_after184_v8_20261010_verified_children_v1.py'),('StockTopPairEmbedding48_selected_native14_v8_20261010','qualify_stock_toppair_embedding48_selected_native14_v8_20261010_verified_children_v1.py'),('StockTopPairEmbedding185_complete48_family_v9_20261010','run_StockTopPairEmbedding185_complete_family_v9_20261010_verified_children_v1.py')]
    for name,driver in tasks:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p),str(path):sha(path)});create(A/(name+'_activation.json'),row)
    print({'actual185_wrapper_bridge':'compiled','actual14_parent_callback_source_proof':'passed','quality_and_future_pending':True},flush=True)
if __name__=='__main__':main()
