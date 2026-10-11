"""Isolated full-report parser benchmark; this never changes actual ranking QA."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, os, time, json, hashlib, gc, argparse
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/full_ranking_JSON_decoder_benchmark_v2_20261010')
REPORT=ROOT/'results/all_model_rankings_20261003.json'
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(OUT/'tmp'/key)
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def allowed():
    c=read(A/'current_user_runtime_control_20261010.json')
    return c['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(c['stop_at_local'])

def phase(method):
    import psutil, msgspec
    from exact_native_pretty_JSON_archive_20261007 import pieces,native_block
    assert allowed()
    frozen=read(OUT/'frozen_before_actual_benchmark.json');assert sha(REPORT)==frozen['original_native_report_sha256']
    started=time.perf_counter()
    if method=='original':report=json.loads(REPORT.read_text(encoding='utf-8'))
    else:
        assert method=='msgspec';report=msgspec.json.decode(REPORT.read_bytes())
    elapsed=time.perf_counter()-started
    memory=psutil.Process().memory_info(); digest=hashlib.sha256();count=0;encoding_start=time.perf_counter()
    for raw in pieces(report):digest.update(raw);count+=len(raw)
    assert count==frozen['original_native_report_bytes'] and digest.hexdigest()==frozen['original_native_report_sha256']
    assert report['summary']['connected_exact_records']==frozen['connected_records']
    record={'method':method,'read_and_decode_seconds':elapsed,'full_reencoded_native_bytes':count,'full_native_sha256':digest.hexdigest(),'all_values_types_key_order_and_float_spellings_exact':True,'connected_records':report['summary']['connected_exact_records'],'decoded_process_RSS_bytes':memory.rss,'decoded_process_private_bytes':getattr(memory,'private',None),'full_encoding_verification_seconds':time.perf_counter()-encoding_start,'msgspec_version':msgspec.__version__}
    # Audit the actual repeated publication parameter hashes on every connected row.
    started=time.perf_counter();parameter_digest=hashlib.sha256();parameter_bytes=0
    for row in report['connected']:
        value=row.get('parameters',{})
        if method=='original':blob=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf8')
        else:
            try:blob=native_block(value,0).replace(b'\r\n',b'\n')+b'\n'
            except ValueError:blob=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf8')
        parameter_digest.update(len(blob).to_bytes(8,'little'));parameter_digest.update(blob);parameter_bytes+=len(blob)
    record.update(actual_parameter_encoder_seconds=time.perf_counter()-started,all_parameter_encoded_bytes=parameter_bytes,all_parameter_row_boundary_and_bytes_sha256=parameter_digest.hexdigest(),actual_parameter_rows=len(report['connected']))
    create(OUT/(method+'_actual.json'),record);print(record,flush=True)

def main():
    import subprocess, psutil
    assert allowed();assert not OUT.exists();OUT.mkdir(parents=True)
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from hidden_windows_child_creation_20261006 import install
    create(OUT/'initial_pending.json',{'status':'queued_global_heavy_ranking_mutex_before_benchmark','no_runtime_adoption_or_speedup_claimed':True})
    with serial(OUT/'serial_mutex.json') as mutex:
        mutex.acquire();assert allowed()
        folder=A/'service_owned_workflows_20261006/ReusedNN158Quality23_round158_full_registration_v1_20261009'
        while owned(read(folder/'native_launch.json')):time.sleep(5)
        assert read(folder/'service_execution.json')['status']=='passed'
        while psutil.virtual_memory().available<19*2**30:
            assert allowed();time.sleep(10)
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        restore=None
        try:
            import build_all_model_rankings_20261003 as ranking
            size=REPORT.stat().st_size;digest=sha(REPORT)
            # Confirm the current published immutable snapshot actually matches this entire input.
            latest=None
            for number in range(158,1001):
                p=A/f'lossless_ranking_display_v2_20261006/round{number}/full_report_publication_snapshot_verification.json'
                if p.is_file():
                    proof=read(p)
                    if proof['original_report_sha256']==digest:latest=(number,p,proof)
            assert latest is not None,'current native report has no fully verified immutable snapshot'
            number,snapshot,proof=latest;assert proof['full_original_bytes']==size
            pins={str(p):sha(p) for p in (Path(__file__),A/'verify_all_model_rankings_20261003.py',A/'exact_native_pretty_JSON_archive_20261007.py',snapshot)}
            create(OUT/'frozen_before_actual_benchmark.json',{'input_sha256':pins,'source_round':number,'original_native_report_sha256':digest,'original_native_report_bytes':size,'connected_records':proof['connected_records'],'two_fresh_process_methods':['original','msgspec'],'source_text_newline_handling_original_unchanged':True,'all_original_QA_checks_not_modified':True,'no_scientific_workflow_suspended_or_restarted':True})
            restore=install();records=[]
            for method in ('original','msgspec'):
                assert allowed()
                with (OUT/(method+'.stdout.log')).open('wb') as stdout,(OUT/(method+'.stderr.log')).open('wb') as stderr:
                    result=subprocess.run([sys.executable,'-B','-X','utf8',str(Path(__file__)),'--phase',method],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,close_fds=True,timeout=1800)
                assert result.returncode==0,(OUT/(method+'.stderr.log')).read_text(encoding='utf8',errors='replace')[-4000:]
                records.append(read(OUT/(method+'_actual.json')))
            assert len({r['full_native_sha256'] for r in records})==1
            for p,d in pins.items():assert sha(p)==d,p
            assert sha(REPORT)==digest
            assert records[0]['all_parameter_row_boundary_and_bytes_sha256']==records[1]['all_parameter_row_boundary_and_bytes_sha256']
            assert records[0]['all_parameter_encoded_bytes']==records[1]['all_parameter_encoded_bytes']
            encoding_speedup=records[0]['actual_parameter_encoder_seconds']/records[1]['actual_parameter_encoder_seconds']
            speedup=records[0]['read_and_decode_seconds']/records[1]['read_and_decode_seconds']
            verification={'status':'passed_actual_complete_native_report_two_fresh_decoder_processes_and_byte_exact_full_reencoding','input_sha256':pins,'source_round':number,'records':records,'actual_full_read_decode_speedup':speedup,'actual_all_parameter_encode_speedup':encoding_speedup,'adopt_parameter_encoder':encoding_speedup>1.05,'adopt':speedup>1.05 and records[1]['decoded_process_RSS_bytes']<=records[0]['decoded_process_RSS_bytes']*1.05,'runtime_adoption_not_yet_performed':True,'new_quality_scores':0,'test_labels_read':False,'all_original_QA_preserved':True}
            create(OUT/'verification.json',verification);create(A/'full_ranking_JSON_decoder_benchmark_v2_20261010.json',verification)
            print({'status':verification['status'],'speedup':speedup,'adopt':verification['adopt']},flush=True)
        finally:
            if restore:create(OUT/'actual_hidden_children.json',{'events':restore()})
            for process in (parent,worker):
                if process.is_running():process.resume()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['original','msgspec']);args=parser.parse_args()
    if args.phase:phase(args.phase)
    else:main()
