"""Compare full native report codec in two fresh processes; never adopt a fixture-only optimization."""
from pathlib import Path
from datetime import datetime
import sys,os,json,time,hashlib,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
OUT=Path('E:/赛题五_本机临时/shared_string_pack_full167_benchmark_v1_20261010')

def worker(mode):
    import build_lossless_ranking_display_round167_v2_20261008 as original
    import byte_exact_shared_string_pack_prototype_v1_20261010 as proposed
    assert allowed()
    frozen=read(OUT/'frozen_before_actual_benchmark.json')
    for p,d in frozen['input_sha256'].items():assert sha(p)==d,p
    begin=time.perf_counter();report=json.loads(original.REPORT.read_text(encoding='utf8'));load=time.perf_counter()-begin
    assert len(report['connected'])==15919
    fn=original.pack_report if mode=='original' else proposed.pack_report
    begin=time.perf_counter();packed=fn(report);elapsed=time.perf_counter()-begin
    compact=json.dumps(packed,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf8')
    assert original.unpack_report(packed)==report
    existing=A/'lossless_ranking_display_v2_20261006/round167/complete_rankings_lossless.html'
    html=existing.read_text(encoding='utf8')
    import re
    matches=re.findall(r'<script[^>]*id="data"[^>]*>(.*?)</script>',html,re.S)
    assert len(matches)==1
    native=json.loads(matches[0].replace('<\\/','</'))
    assert json.dumps(native,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf8')==compact
    for p,d in frozen['input_sha256'].items():assert sha(p)==d,p
    create(OUT/(mode+'_result.json'),{'mode':mode,'load_seconds':load,'pack_seconds':elapsed,'codec_sha256':hashlib.sha256(compact).hexdigest(),'codec_bytes':len(compact),'nodes':len(packed['nodes']),'root':packed['root'],'connected_records':15919,'full_existing_qualified_codec_bytes_exact':True,'all_report_values_and_six_views_roundtrip_exact':True})

def main():
    import psutil
    import build_lossless_ranking_display_round167_v2_20261008 as original
    import byte_exact_shared_string_pack_prototype_v1_20261010 as proposed
    assert allowed();OUT.mkdir(exist_ok=False)
    fixtures=[None,True,False,0,1,1.,-0.,'x'*512,'x'*513,'中😀</script>'*200]
    for n in (513,767,768,769,1024):
        s=('中😀x'*(n//3+1))[:n]
        fixtures.extend([s,[s,s[:256],s],{'a':s,'b':[s,s]}])
    for fixture in fixtures:
        lhs=original.pack_report(fixture);rhs=proposed.pack_report(fixture)
        assert json.dumps(lhs,ensure_ascii=False,allow_nan=False)==json.dumps(rhs,ensure_ascii=False,allow_nan=False)
        assert original.unpack_report(rhs)==fixture
    inputs=[Path(__file__),Path(original.__file__),Path(proposed.__file__),original.REPORT,A/'lossless_ranking_display_v2_20261006/round167/complete_rankings_lossless.html',A/'lossless_ranking_display_v2_20261006/round167/verification.json']
    create(OUT/'frozen_before_actual_benchmark.json',{'input_sha256':{str(p):sha(p) for p in inputs},'actual_small_fixture_controls':len(fixtures),'full_fresh_original_and_proposed_processes_pending':True,'science_scores_models_predictions_and_existing_report_unchanged':True,'at_local':datetime.now().isoformat()})
    resources=[]
    for mode in ('original','proposed'):
        while psutil.virtual_memory().available<16*2**30:assert allowed();time.sleep(15)
        assert allowed()
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
        for key in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):env[key]=str(OUT)
        with (OUT/(mode+'_stdout.log')).open('xb') as out,(OUT/(mode+'_stderr.log')).open('xb') as err:
            process=subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-B','-X','utf8',str(Path(__file__)),mode],cwd=ROOT,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
            peak=0
            while process.poll() is None:
                assert allowed()
                try:
                    p=psutil.Process(process.pid);peak=max(peak,sum(x.memory_info().rss for x in [p,*p.children(recursive=True)] if x.is_running()))
                except psutil.Error:pass
                time.sleep(2)
            assert process.returncode==0,(mode,(OUT/(mode+'_stderr.log')).read_text(encoding='utf8'))
        resources.append({'mode':mode,'peak_process_tree_RSS_bytes':peak})
    lhs=read(OUT/'original_result.json');rhs=read(OUT/'proposed_result.json')
    assert lhs['codec_sha256']==rhs['codec_sha256'] and lhs['nodes']==rhs['nodes']==289642
    speed=lhs['pack_seconds']/rhs['pack_seconds']
    create(OUT/'verification.json',{'status':'passed_two_fresh_processes_actual_full167_report_exact_codec_bytes_and_all_values','records':[lhs,rhs],'resources':resources,'pack_speedup':speed,'adopt_for_future_rounds':speed>1.1 and resources[1]['peak_process_tree_RSS_bytes']<=resources[0]['peak_process_tree_RSS_bytes']*1.05,'input_sha256':read(OUT/'frozen_before_actual_benchmark.json')['input_sha256'],'new_quality_scores':0,'new_native_fits':0,'at_local':datetime.now().isoformat()})
    create(A/'shared_string_pack_full167_benchmark_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print({'pack_speedup':speed,'status':'passed_actual_full_codec_bytes'},flush=True)
if __name__=='__main__':
    if len(sys.argv)>1:worker(sys.argv[1])
    else:main()
