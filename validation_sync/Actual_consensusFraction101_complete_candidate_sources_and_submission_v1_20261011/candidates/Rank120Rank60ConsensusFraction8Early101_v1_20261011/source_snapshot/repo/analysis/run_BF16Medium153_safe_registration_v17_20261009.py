"""Only publication guards wrap the verified153 registration3 receiver."""
from pathlib import Path
import sys,os,runpy
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha

def main():
    meta=A/'BF16Medium153_complete_pipeline_preparation_v17_20261009.json'
    for f,d in read(meta)['input_sha256'].items():assert sha(f)==d,f
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
        os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    import prepare_BF16Medium78_round153_sources_v1_20261009 as g
    original=g.source_paths
    def source_paths():
        return list(dict.fromkeys([*original(),meta,Path(__file__),A/'lossless_chunked_safe_main_runtime_v1_20261009.py',
          A/'lossless_chunked_safe_main_runtime_v1_20261009.json',A/'dispatch_BF16Medium153_complete_pipeline_v17_20261009.py']))
    g.source_paths=source_paths
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed
    try:
        with installed(Path('E:/赛题五_本机临时/第153轮_20261009/safe_full_main_v17')):
            runpy.run_path(str(A/'run_BF16Medium78_round153_full_registration_v3_20261009.py'),run_name='__main__')
    finally:g.source_paths=original

if __name__=='__main__':main()
