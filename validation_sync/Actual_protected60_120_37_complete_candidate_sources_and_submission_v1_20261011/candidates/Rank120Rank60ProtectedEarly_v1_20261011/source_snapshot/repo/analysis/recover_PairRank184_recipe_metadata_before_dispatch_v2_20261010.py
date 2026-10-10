from pathlib import Path
import sys,subprocess,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    import prepare_StockPairRankEmbedding184_complete48_pipeline_v1_20261010 as old
    mapping={}
    for n in old.NAMES:mapping[n]=n.replace('_v4_','_v5_')
    for n in old.EXTRAS[:11]:
        mapping[n]=re.sub(r'_v(\d+)_',lambda m:'_v'+str(int(m.group(1))+1)+'_',n)
    for n in old.EXTRAS[11:14]:mapping[n]=n.replace('_v2_','_v3_')
    for n in ('route_StockPairRank184_exact_verified_children_v1_20261010.py','StockPairRank184_exact_child_sources_v1_20261010.json','stock_pairrank_embedding184_full_execution_sources_admission_v1_20261010.json'):
        mapping[n]=n.replace('_v1_','_v2_')
    original=A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v1_20261010.py'
    text=original.read_text(encoding='utf8')
    # Post-process after all overlapping substitutions; the underlying32-epoch native model is unchanged.
    text=text.replace('    return text\n',"    text=text.replace('stock_pairrank_embedding32_cross120_rank1d_recent252_small512_BF16_e32','stock_pairrank_embedding16_cross120_pairrank1d_recent252_small512_BF16_e32')\n    versions="+repr(mapping)+"\n    text=re.sub('|'.join(re.escape(k) for k in sorted(versions,key=len,reverse=True)),lambda m:versions[m.group()],text)\n    return text\n")
    # Generated literals outside route() also need fresh exclusive names.
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    services={'actual_stock_pairrank_embedding48_after183_normalization_queue_v6_20261010':'actual_stock_pairrank_embedding48_after183_normalization_queue_v7_20261010','StockPairRankEmbedding48_selected_native14_v6_20261010':'StockPairRankEmbedding48_selected_native14_v7_20261010','StockPairRankEmbedding184_complete48_family_v7_20261010':'StockPairRankEmbedding184_complete48_family_v8_20261010'}
    for before,after in services.items():text=text.replace(before,after)
    p=A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v2_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    records=[]
    for name in services:
        row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json')
        result=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True)
        assert result.returncode==0 and '(idle)' in result.stdout and 'closed (' in result.stdout
        retire(row,'Fresh metadata-only source version corrects exact recipe key before any184 scoring or future dispatch; own32 native fits untouched')
        records.append({'identity':row,'actual_idle_closed_stack':result.stdout})
    create(A/'PairRank184_recipe_metadata_recovery_v2_20261010.json',{'status':'preserved_original_frozen_sources_retired_only_three_idle_helpers_new_version_before_future','records':records,'input_sha256':{str(original):sha(original),str(p):sha(p)},'new_fits':0,'new_scores':0,'new_inference':0})
    import runpy
    runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
