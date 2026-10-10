"""Retain the common proven CDF import while preparing RFFSparse151 under fresh codec names."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]

def main():
    original=A/'prepare_RFFSparse151_frontier_v1_20261009.py';source=original.read_text(encoding='utf8')
    before=".replace('Huber','RFF')";after=".replace('Signed Huber and sparse','Signed RFF and sparse')"
    assert source.count(before)==1;source=source.replace(before,after)
    source=source.replace('RFFSparse_complete_parent_CDF_v1_20261009','RFFSparse_complete_parent_CDF_v2_20261009')
    source=source.replace('RFFSparse_complete_parent_native_stage_v1_20261009','RFFSparse_complete_parent_native_stage_v2_20261009')
    source=source.replace('inputs=[Path(__file__),original,','inputs=[Path(__file__),A/\'prepare_RFFSparse151_frontier_v1_20261009.py\',original,')
    ns={'__name__':'actual_RFFSparse151_common_CDF_import_preserved','__file__':str(Path(__file__))}
    exec(compile(source,str(original),'exec'),ns);ns['main']()
if __name__=='__main__':main()
