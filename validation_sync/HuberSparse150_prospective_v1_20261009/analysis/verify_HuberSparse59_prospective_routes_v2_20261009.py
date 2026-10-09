"""Execute unchanged prospective150 checks with the corrected150/61/59 collector invocation."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    original=A/'verify_HuberSparse59_prospective_routes_v1_20261009.py'
    source=original.read_text(encoding='utf8')
    before="ns['collect'](145,56,125)";after="ns['collect'](150,61,59)"
    assert source.count(before)==1
    source=source.replace(before,after)
    namespace={'__name__':'actual_prospective150_corrected_collector_invocation','__file__':str(Path(__file__))}
    exec(compile(source,str(original),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
