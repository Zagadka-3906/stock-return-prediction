from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read
def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    import prepare_StockPairRankEmbedding184_complete48_pipeline_v1_20261010 as old
    versions={n:n.replace('_v4_','_v5_') for n in old.NAMES}
    versions.update({n:re.sub(r'_v(\d+)_',lambda m:'_v'+str(int(m.group(1))+1)+'_',n) for n in old.EXTRAS[:11]})
    versions.update({n:n.replace('_v2_','_v3_') for n in old.EXTRAS[11:14]})
    for n in ('route_StockPairRank184_exact_verified_children_v1_20261010.py','StockPairRank184_exact_child_sources_v1_20261010.json','stock_pairrank_embedding184_full_execution_sources_admission_v1_20261010.json'):versions[n]=n.replace('_v1_','_v2_')
    source=A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v2_20261010.py'
    text=source.read_text(encoding='utf8');text,count=re.subn(r'^    versions=.*$',lambda m:'    versions='+repr(versions),text,flags=re.M);assert count==1
    p=A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v3_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    assert read(A/'PairRank184_recipe_metadata_recovery_v2_20261010.json')['new_inference']==0
    runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
