from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    source=A/'prepare_PairRank184_frozen_sources_main_v1_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('prepare_StockPairRankEmbedding184_complete48_pipeline_v1_20261010','prepare_StockPairRankEmbedding184_complete48_pipeline_v4_20261010').replace('normalize_completed_stock_pairrank_embedding_complete48_after183_v6_20261010','normalize_completed_stock_pairrank_embedding_complete48_after183_v8_20261010').replace('stock_pairrank_embedding184_full_execution_sources_admission_v1_20261010','stock_pairrank_embedding184_full_execution_sources_admission_v3_20261010')
    text=text.replace('PairRank184_actual_recipe_backend_schema_CPU_v1_20261010','PairRank184_actual_recipe_backend_schema_CPU_v2_20261010').replace('PairRank184_frozen_sources_v1_20261010','PairRank184_frozen_sources_v2_20261010').replace('PairRank184_frozen_sources_main_v1_20261010','PairRank184_frozen_sources_main_v2_20261010').replace('PairRank184_frozen_sources_main_receipt_v1_20261010','PairRank184_frozen_sources_main_receipt_v2_20261010')
    p=A/'prepare_PairRank184_frozen_sources_main_v2_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
