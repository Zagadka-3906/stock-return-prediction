"""Serialize full156 publication and preserve frozen source bytes across D/E volumes."""
from pathlib import Path
import sys,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
def main():
    meta=A/'BF16Drop05_156_complete_pipeline_preparation_v3_20261009.json'
    for f,d in read(meta)['input_sha256'].items():assert sha(f)==d,f
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    import prepare_BF16Drop05_81_round156_sources_v2_20261010 as g
    original=g.source_paths
    g.source_paths=lambda:list(dict.fromkeys([*original(),meta,Path(__file__),A/'run_BF16Drop05_81_round156_full_registration_v2_20261010.py',A/'BF16Drop05_156_registration_count_correction_v1_20261010.json',A/'dispatch_BF16Drop05_156_complete_pipeline_v2_20261009.py',A/'verify_BF16Drop05_81_prospective_routes_v3_20261009.py',A/'BF16Drop05_156_prospective_assertion_correction_v2_20261009.json']))
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from BF16Drop05_156_storage_v1_20261009 import installed_transfer
    log=Path('E:/赛题五_本机临时/第156轮_20261009/safe_full_main_v4_20261010')
    try:
        from actual_QA_collector_path_runtime_v43_20261009 import installed as qa_paths
        with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),installed_transfer(),qa_paths():
            import run_BF16Drop05_81_round156_full_registration_v2_20261010 as receiver
            receiver.main()
    finally:g.source_paths=original
if __name__=='__main__':main()
