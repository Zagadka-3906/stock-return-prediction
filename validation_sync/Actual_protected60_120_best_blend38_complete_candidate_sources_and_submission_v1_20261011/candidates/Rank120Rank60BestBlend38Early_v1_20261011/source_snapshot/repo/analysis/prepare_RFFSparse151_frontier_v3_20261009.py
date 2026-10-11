"""Prepare151 with the preserved common CDF and explicit native/storage kind for all four heads."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]

def main():
    original=A/'prepare_RFFSparse151_frontier_v1_20261009.py';source=original.read_text(encoding='utf8')
    before=".replace('Huber','RFF')";after=".replace('Signed Huber and sparse','Signed RFF and sparse')"
    assert source.count(before)==1;source=source.replace(before,after)
    source=source.replace('RFFSparse_complete_parent_CDF_v1_20261009','RFFSparse_complete_parent_CDF_v3_20261009')
    source=source.replace('RFFSparse_complete_parent_native_stage_v1_20261009','RFFSparse_complete_parent_native_stage_v3_20261009')
    marker="    heads.update({h:copy.deepcopy(sparse['heads'][h]) for h in ('sparse_l1','sparse_elastic')})"
    assert source.count(marker)==1;source=source.replace(marker,marker+"\n    for row in heads.values():row.setdefault('native_stage_state_kind',row['state_kind'])")
    source=source.replace('inputs=[Path(__file__),original,','inputs=[Path(__file__),A/\'prepare_RFFSparse151_frontier_v1_20261009.py\',A/\'prepare_RFFSparse151_frontier_v2_20261009.py\',original,')
    ns={'__name__':'actual_RFFSparse151_CDF_and_explicit_native_kind','__file__':str(Path(__file__))}
    exec(compile(source,str(original),'exec'),ns);ns['main']()
if __name__=='__main__':main()
