from pathlib import Path
import sys,ast,re,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    source=A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v3_20261010.py';text=source.read_text(encoding='utf8')
    node=next(n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='versions' for t in n.targets))
    previous=ast.literal_eval(node.value)
    def bump(n):return re.sub(r'_v(\d+)(?=[_.])',lambda m:'_v'+str(int(m.group(1))+1),n)
    versions={k:bump(v) for k,v in previous.items()}
    relocation={v:versions[k] for k,v in previous.items()}
    text=re.sub('|'.join(re.escape(k) for k in sorted(relocation,key=len,reverse=True)),lambda m:relocation[m.group()],text)
    text,count=re.subn(r'^    versions=.*$',lambda m:'    versions='+repr(versions),text,flags=re.M);assert count==1
    text=text.replace('actual_stock_pairrank_embedding48_after183_normalization_queue_v7_20261010','actual_stock_pairrank_embedding48_after183_normalization_queue_v8_20261010').replace('StockPairRankEmbedding48_selected_native14_v7_20261010','StockPairRankEmbedding48_selected_native14_v8_20261010').replace('StockPairRankEmbedding184_complete48_family_v8_20261010','StockPairRankEmbedding184_complete48_family_v9_20261010')
    p=A/'prepare_StockPairRankEmbedding184_complete48_pipeline_v4_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
