"""Wrap the frozen154 full receiver in verified serial, volume-transfer and index guards."""
from pathlib import Path
import sys,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
def main():
    meta=A/'BF16TwoSeed154_complete_pipeline_preparation_v3_20261009.json'
    for f,d in read(meta)['input_sha256'].items():assert sha(f)==d,f
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
        os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    import prepare_BF16TwoSeed79_round154_sources_v1_20261009 as g
    original=g.source_paths
    g.source_paths=lambda:list(dict.fromkeys([*original(),meta,Path(__file__),A/'dispatch_BF16TwoSeed154_complete_pipeline_v2_20261009.py',
        A/'prepare_BF16TwoSeed79_selected_candidate_v2_20261009.py',A/'run_BF16TwoSeed79_round154_full_registration_v3_20261009.py',
        A/'verify_BF16TwoSeed79_round154_sources_v2_20261009.py',A/'BF16TwoSeed154_actual_parent_guard_controls_v2_20261009.json']))
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from BF16TwoSeed154_storage_v1_20261009 import installed_transfer
    log=Path('E:/赛题五_本机临时/第154轮_20261009/safe_full_main_v3')
    try:
        from actual_QA_collector_path_runtime_v43_20261009 import installed as qa_paths
        with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),installed_transfer(),qa_paths():
            import run_BF16TwoSeed79_round154_full_registration_v2_20261009 as receiver
            receiver.main()
    finally:g.source_paths=original
if __name__=='__main__':main()
