from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
def main():
    import prepare_ReusedNN161Quality19_round161_sources_v1_20261009 as source_generator
    original_sources=source_generator.source_paths
    source_generator.source_paths=lambda:list(dict.fromkeys([*original_sources(),Path(__file__),A/'actual_QA_collector_path_runtime_v44_20261010.py',A/'actual_QA_collector_path_controls_v44_20261010.json',A/'byte_exact_ranking_stream_runtime_v1_20261010.py',A/'byte_exact_publication_encoder_runtime_v1_20261010.py',A/'byte_exact_publication_encoder_controls_v1_20261010.json',A/'owned_idle_publication_wait_runtime_v1_20261010.py',*([publication_proof_path] if publication_proof_path.is_file() else []),*([proof_path] if proof_path.is_file() else [])]))
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from ReusedNN161Stage_storage_v1_20261009 import installed_transfer
    from actual_QA_collector_path_runtime_v44_20261010 import installed as qa_paths
    from contextlib import nullcontext
    from owned_idle_publication_wait_runtime_v1_20261010 import installed as idle_waiters
    from run_dependency_queue_v3_20261006 import read as read_speed_proof
    proof_path=A/'byte_exact_ranking_stream_benchmark_v1_20261010.json'
    accelerated_writer=nullcontext()
    if proof_path.is_file() and read_speed_proof(proof_path).get('adopt'):
        from byte_exact_ranking_stream_runtime_v1_20261010 import installed as stream_writer
        accelerated_writer=stream_writer()
    publication_encoder=nullcontext()
    publication_proof_path=A/'full_ranking_JSON_decoder_benchmark_v2_20261010.json'
    if publication_proof_path.is_file() and read_speed_proof(publication_proof_path).get('adopt_parameter_encoder'):
        from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encode_publication
        publication_encoder=encode_publication()
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    log=Path('E:/赛题五_本机临时/第161轮_20261009/safe_full_main_v1')
    with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'),installed_transfer(),qa_paths(),accelerated_writer,publication_encoder,idle_waiters(log/'owned_idle_watcher_waits.json'):
        import run_ReusedNN161Quality19_round161_full_registration_v1_20261009 as receiver
        receiver.main()
if __name__=='__main__':main()
