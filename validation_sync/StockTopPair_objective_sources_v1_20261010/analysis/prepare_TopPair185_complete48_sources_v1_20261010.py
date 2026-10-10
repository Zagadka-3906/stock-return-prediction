from pathlib import Path
import sys,re,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v4_20261010.py'
    text=source.read_text(encoding='utf8').replace('stock_pairrank_embedding','stock_toppair_embedding').replace('StockPairRankEmbedding','StockTopPairEmbedding').replace('StockPairRank184','StockTopPair185').replace('STOCK_PAIRRANK_EMBEDDING','STOCK_TOPPAIR_EMBEDDING').replace('StockPairRank_objective','StockTopPair_objective').replace('pairrank1d','toppair1d').replace('same_day_ranknet_loss','same_day_top_ranknet_loss')
    text=re.sub(r'(?<!\d)(184|183|17306|467|95)(?!\d)',lambda m:{'184':'185','183':'184','17306':'17354','467':'468','95':'96'}[m.group()],text)
    text=text.replace("'twelve_parent':'thirteen_parent'","'twelve_parent':'fourteen_parent'")
    text=text.replace("'StockRank20Embedding184_complete85_family_v6_20261010'","'StockPairRankEmbedding184_complete48_family_v9_20261010'")
    text=text.replace("from route_verified_Dual25_recovery_dependencies_v7_20261010", "from route_actual_PairRank_native42_admission_v8_20261010")
    text=text.replace('import route_verified_Dual25_recovery_dependencies_v7_20261010 as parent','import route_actual_PairRank_native42_admission_v8_20261010 as parent')
    needle='    text=text.replace(needle,needle+"'
    assert text.count(needle)==1
    text=text.replace(needle,needle+'    from stock_pairrank_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as pair_parent_key\\n    if pair_parent_key in graph:return \'predict_stock_pairrank_embedding_complete_qualified_parent_scheme_v4_20261010.py\'\\n',1)
    text=text.replace("+[original.name];rows=[]","+[original.name,'predict_stock_pairrank_embedding_complete_qualified_parent_scheme_v4_20261010.py'];rows=[]")
    text=text.replace('len(rows)==13','len(rows)==14').replace('actual_thirteen_complete_parent','actual_fourteen_complete_parent').replace("'actual_callbacks_CPU':13","'actual_callbacks_CPU':14").replace("'actual_CPU_parent_callbacks':13","'actual_CPU_parent_callbacks':14")
    # Source paths and the candidate freeze retain the recovery runtime used to resolve the184 parent.
    text=text.replace("EXTRAS += [", "EXTRAS += ['actual_PairRank_native42_admission_routes_v8_20261010.json','route_actual_PairRank_native42_admission_v8_20261010.py',")
    # Existing positional extras[:17] remain unchanged; added entries are append-only.
    text=text.replace("    assert '(185, 96, 48)'", "    import stock_toppair_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as native_stage\n    normalized=importlib.import_module(Path(EXTRAS[0]).stem)\n    assert set(native_stage.BACKENDS)==set(normalized.RECIPES)\n    assert '(185, 96, 48)'")
    p=A/'prepare_StockTopPairEmbedding185_complete48_pipeline_v1_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    module=importlib.import_module(p.stem)
    assert all('185' in n for n in module.NAMES)
    assert module.route('stock_rank_wide32_embedding32_cross120_rank1d_recent252_wide1024_BF16_e64')=='stock_toppair_embedding16_cross120_toppair1d_recent252_small512_BF16_e32'
    runpy.run_path(str(p),run_name='__main__')
    create(A/'TopPair185_full48_QA96_sources_generation_v1_20261010.json',{'status':'compiled_actual14_parent_callbacks_and_exact_native_recipe_schema_before_future','input_sha256':{str(source):sha(source),str(p):sha(p)},'expected_records':48,'expected_board':17354,'QA':96,'actual_new_future_inference':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
