from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
def main():
    import prepare_ReusedNN158Quality23_round158_sources_v1_20261009 as generator
    original_sources=generator.source_paths
    generator.source_paths=lambda:list(dict.fromkeys([*original_sources(),A/'failed_dependency_and_cold80_recovery_v2_20261010/manifest.json',*map(Path,__import__('run_dependency_queue_v3_20261006').read(A/'failed_dependency_and_cold80_recovery_v2_20261010/manifest.json')['corrected_source_sha256'])]))
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from ReusedNN158Stage_storage_v1_20261009 import installed_transfer
    from actual_QA_collector_path_runtime_v43_20261009 import installed as qa_paths
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    log=Path('E:/赛题五_本机临时/第158轮_20261009/safe_full_main_v2')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),installed_transfer(),qa_paths():
        import run_ReusedNN158Quality23_round158_full_registration_v2_20261010 as receiver
        receiver.main()
if __name__=='__main__':main()
