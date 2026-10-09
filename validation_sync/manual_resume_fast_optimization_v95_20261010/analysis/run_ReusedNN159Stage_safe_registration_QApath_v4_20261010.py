from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
def main():
    import prepare_ReusedNN159Quality19_round159_sources_v1_20261009 as paths_generator
    previous_paths=paths_generator.source_paths
    paths_generator.source_paths=lambda:list(dict.fromkeys([*previous_paths(),Path(__file__),A/'run_ReusedNN159Quality19_round159_full_registration_QApath_v3_20261010.py',A/'actual_QA_collector_path_runtime_v44_20261010.py',A/'actual_QA_collector_path_controls_v44_20261010.json',A/'byte_exact_ranking_stream_runtime_v1_20261010.py',*([proof_path] if proof_path.is_file() else [])]))
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from ReusedNN159Stage_storage_v1_20261009 import installed_transfer
    from actual_QA_collector_path_runtime_v44_20261010 import installed as qa_paths
    from contextlib import nullcontext
    from run_dependency_queue_v3_20261006 import read as read_speed_proof
    proof_path=A/'byte_exact_ranking_stream_benchmark_v1_20261010.json'
    accelerated_writer=nullcontext()
    if proof_path.is_file() and read_speed_proof(proof_path).get('adopt'):
        from byte_exact_ranking_stream_runtime_v1_20261010 import installed as stream_writer
        accelerated_writer=stream_writer()
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    log=Path('E:/赛题五_本机临时/第159轮_20261009/safe_full_main_QApath_v3_20261010')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),installed_transfer(),qa_paths(),accelerated_writer:
        import run_ReusedNN159Quality19_round159_full_registration_QApath_v3_20261010 as receiver
        receiver.main()
if __name__=='__main__':main()
