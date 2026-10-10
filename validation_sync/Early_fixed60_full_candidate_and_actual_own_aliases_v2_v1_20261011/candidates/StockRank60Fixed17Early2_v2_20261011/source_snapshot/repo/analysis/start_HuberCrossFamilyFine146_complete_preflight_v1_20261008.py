"""Run own30 calendar cases, actual32 prospective paths, and the gated complete146 dispatcher."""
from pathlib import Path
import sys
import json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    prep=A/'HuberCrossFamilyFine146_complete_receiver_preparation_v1_20261008.json';p=read(prep)
    for path,digest in p['input_sha256'].items():assert sha(path)==digest,path
    scope=A/'verify_HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.py'
    ns={'__file__':str(scope),'__name__':'actual146_scoring_cache_scope'}
    exec(compile(scope.read_text(encoding='utf8'),str(scope),'exec'),ns);ns['main']()
    old=A/'verify_HuberCrossFamilyFine125_prospective_routes_v1_20261008.py'
    text=old.read_text(encoding='utf8').replace('graph134','graph136').replace("'actual134'","'actual136'")
    target=A/'verify_HuberCrossFamilyFine125_prospective_routes_v2_20261008.py';compile(text,str(target),'exec')
    with target.open('x',encoding='utf8',newline='') as stream:stream.write(text)
    pins={**p['input_sha256'],**{str(path):sha(path) for path in [Path(__file__),prep,scope,target,A/'HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.json']}}
    rows={}
    specs=[('HuberCrossFamilyFine30_multiyear_calendar_controls_v1_20261008','verify_HuberCrossFamilyFine_multiyear_native_calendar_v1_20261008.py'),
           ('HuberCrossFamilyFine146_complete_prospective_controls_v1_20261008',target.name),
           ('HuberCrossFamilyFine146_complete_chronological_dispatch_v1_20261008','dispatch_HuberCrossFamilyFine146_complete_pipeline_v1_20261008.py')]
    for name,driver in specs:rows[name]=start(name,driver,[],pins)
    create(A/'HuberCrossFamilyFine146_complete_preflight_hidden_launches_v1_20261008.json',{
        'status':'started_own_calendar_prospective_and_gated_complete146_dispatch_before_quality',
        'launches':rows,'input_sha256':pins,'actual_prospective_driver_version':2,
        'old_prospective1_draft_preserved_with_no_scoring_run':True,
        'actual145_full_and_benchmark_process_closure_required_before146_dispatch':True,
        'original146_ranking_runtime_retained':True,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'started':{name:row['owned_worker_pid'] for name,row in rows.items()}},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
