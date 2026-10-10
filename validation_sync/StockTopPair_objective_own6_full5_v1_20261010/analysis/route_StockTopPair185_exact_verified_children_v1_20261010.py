from pathlib import Path
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
