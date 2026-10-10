"""Separate ordered model heads from the local sorted CDF variable; retain failedV1."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def new_file(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    return p

def main():
    old=A/'service_owned_workflows_20261006/weighted_flagged_HGB_native_hook_preflight'
    assert not owned(read(old/'native_launch.json')) and read(old/'service_execution.json')['failure']=="UnboundLocalError: cannot access local variable 'ordered' where it is not associated with a value"
    source=A/'predict_flagged_CPU_HGB_weighted_quarters_scheme_20261007.py'
    text=source.read_text(encoding='utf8')
    changes={'ordered = spec[':'ordered_heads = spec[','len(ordered)':'len(ordered_heads)',
        'len(set(ordered))':'len(set(ordered_heads))','list(dict.fromkeys(ordered))':'list(dict.fromkeys(ordered_heads))','for name in ordered:':'for name in ordered_heads:'}
    for before,after in changes.items():
        assert before in text,before;text=text.replace(before,after)
    native=new_file('predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',text)
    lower_source=A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_20261007.py'
    lower=new_file('predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',lower_source.read_text(encoding='utf8').replace(source.name,native.name))
    diag_source=A/'verify_weighted_flagged_HGB_native_hook_20261007.py'
    text=diag_source.read_text(encoding='utf8').replace(source.stem,native.stem).replace(lower_source.name,lower.name).replace(lower_source.stem,lower.stem)
    text=text.replace('weighted_flagged_HGB_native_hook_preflight_20261007','weighted_flagged_HGB_native_hook_preflight_v2_20261007')
    diag=new_file('verify_weighted_flagged_HGB_native_hook_v2_20261007.py',text)
    wrapper_source=A/'run_weighted_flagged_HGB_controls_after116_20261007.py'
    text=wrapper_source.read_text(encoding='utf8').replace('weighted_flagged_HGB_native_hook_preflight_20261007','weighted_flagged_HGB_native_hook_preflight_v2_20261007').replace('/weighted_flagged_HGB_native_hook_preflight\'','/weighted_flagged_HGB_native_hook_preflight_v2\'')
    wrapper=new_file('run_weighted_flagged_HGB_controls_after116_v2_20261007.py',text)
    pins={str(p):sha(p) for p in (Path(__file__),source,native,lower_source,lower,diag_source,diag,wrapper_source,wrapper,old/'service_execution.json',old/'stderr.log')}
    records=[]
    for name,p in [('weighted_flagged_HGB_native_hook_preflight_v2',diag),('weighted_flagged_HGB_full337_transform_preflight_v2',wrapper)]:
        records.append({'name':name,'native_launch':start_service(name,p.name,[],pins)})
    create(A/'weighted_flagged_HGB_native_hook_recovery_v2_actual_launch_20261007.json',{'input_sha256':pins,'services':records,
        'original_failure_preserved':True,'new_native_fits':0,'new_quality_scores':0,'original_scientific_workers_stopped':0})
    print({'status':'launched_two_fresh_controls','workers':[r['native_launch']['owned_worker_pid'] for r in records]},flush=True)

if __name__=='__main__':main()
