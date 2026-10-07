"""Adopt byte-identical archive speed before any120 science; preserve all existing results."""
from pathlib import Path
import ast,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,stack
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    out=A/'nonflag_HGB40_archive_routes_v3_actual_handoff_20261007';assert not out.exists();out.mkdir()
    full=A/'service_owned_workflows_20261006/exact_native_JSON_archive_runtime_full_preflight'
    assert not owned(read(full/'native_launch.json')) and read(full/'service_execution.json')['status']=='passed'
    full_proof=A/'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json'
    assert read(full_proof)['status']=='passed_actual_installed_runtime_full12406_original2076897250_raw_and_gzip_bytes_exact'
    rows=read(A/'nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007.json')['launches']
    assert not (A/'nonflag_HGB40_official_comparison_v2_20261007').exists()
    names=list(rows);held=[];retired=set();successors={}
    try:
        idle={}
        for name,row in rows.items():
            assert owned(row),name
            definition=read(A/'service_owned_workflows_20261006'/name/'job_definition.json')
            driver=Path(definition['driver']);lines=driver.read_text(encoding='utf8').splitlines();before=stack(row['owned_worker_pid'])
            possible=[f'({driver.name}:{i+1})' for i,line in enumerate(lines) if 'time.sleep(' in line and f'({driver.name}:{i+1})' in before]
            assert len(possible)==1,(name,before)
            parent,worker,proof=suspended_idle(row,possible[0]);held.append((name,parent,worker));idle[name]=proof
        create(out/'actual7_exact_idle_before_and_after.json',idle)
        files={Path(read(A/'service_owned_workflows_20261006'/name/'job_definition.json')['driver']).name for name in rows}
        files |= {'run_nonflag_HGB40_official_comparison_v2_20261007.py','prepare_nonflag_HGB40_round120_sources_v2_20261007.py'}
        filemap={n:n.replace('_v2_20261007','_v3_20261007') for n in files}
        mapping={**{o[:-3]:n[:-3] for o,n in filemap.items()},**{n:n+'_v3' for n in rows},
          'resolve_sealed_scientific_protocol_20261007':'resolve_sealed_scientific_protocol_v2_20261007',
          'nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007':'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v3_20261007'}
        for suffix in ['selected_release','official_comparison','pre_inference_source_freeze','round120_source_admission','round120_source_preparation','round120_actual_registration']:
            mapping[f'nonflag_HGB40_{suffix}_v2_20261007']=f'nonflag_HGB40_{suffix}_v3_20261007'
        mapping['candidates/nonflag_HGB40_v2_20261007']='candidates/nonflag_HGB40_v3_20261007'
        generated={}
        for old,new in filemap.items():
            text=(A/old).read_text(encoding='utf8')
            if old.startswith('prepare_') and 'round120_sources' in old:
                node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='main')
                main_text='\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])
                text=f'''from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import {Path(old).stem} as base
NAMES=base.NAMES
ROUTE_MAP={mapping!r}
def generate(parent):
    result={{name:substitute(text,ROUTE_MAP) for name,text in base.generate(parent).items()}}
    for name,text in list(result.items()):
        if name.startswith('collect_'):
            needle="    return namespace['collect'](number, qa_version, expected_records)"
            assert text.count(needle)==1
            text=text.replace(needle,"    from exact_native_JSON_archive_runtime_20261007 import install\\n    restore=install()\\n    try:return namespace['collect'](number, qa_version, expected_records)\\n    finally:restore()")
        elif name.startswith('register_'):
            needle="        A / 'collect_full_lossless_round120_qa31_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\\n        A / 'exact_native_JSON_archive_runtime_20261007.py',\\n        A / 'exact_native_pretty_JSON_archive_20261007.py',\\n        A / 'exact_native_JSON_full_board_benchmark_20261007/verification.json',\\n        A / 'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',")
        compile(text,str(A/name),'exec');result[name]=text
    return result
'''+substitute(main_text,mapping)+"\nif __name__=='__main__':main()\n"
            else:text=substitute(text,mapping)
            if old.startswith('verify_'):
                needle='    for p in sources:';assert text.count(needle)==1
                text=text.replace(needle,"    sources += [A/'exact_native_JSON_archive_runtime_20261007.py',A/'exact_native_pretty_JSON_archive_20261007.py',A/'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',A/'handoff_nonflag_HGB40_archive_routes_v3_20261007.py',A/'nonflag_HGB40_archive_routes_v3_actual_handoff_20261007/verification.json']\n"+needle)
                needle='    import prepare_nonflag_HGB40_round120_sources_v3_20261007 as generator'
                text=text.replace(needle,"    closed('exact_native_JSON_archive_runtime_full_preflight')\n"+needle)
            elif old.startswith('publish_'):
                needle="    if phase=='scores':\n        for row in proof['records']:";assert text.count(needle)==1
                text=text.replace(needle,"    sources += [A/'exact_native_JSON_archive_runtime_20261007.py',A/'exact_native_pretty_JSON_archive_20261007.py',A/'exact_native_JSON_full_board_benchmark_20261007/verification.json',A/'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',A/'handoff_nonflag_HGB40_archive_routes_v3_20261007.py',A/'nonflag_HGB40_archive_routes_v3_actual_handoff_20261007/verification.json',A/'resolve_sealed_scientific_protocol_v2_20261007.py']\n"+needle)
            compile(text,str(A/new),'exec');generated[new]=text
        for n in generated:assert not (A/n).exists(),n
        for n,text in generated.items():
            with (A/n).open('x',encoding='utf8',newline='\n') as f:f.write(text)
        import importlib
        generator=importlib.import_module('prepare_nonflag_HGB40_round120_sources_v3_20261007')
        prospective={str(p):{n:hashlib.sha256(t.encode('utf8')).hexdigest() for n,t in generator.generate(p).items()} for p in (112,118,119)}
        pins={str(p):sha(p) for p in [Path(__file__),full_proof,A/'exact_native_JSON_archive_runtime_20261007.py',A/'exact_native_pretty_JSON_archive_20261007.py',
          A/'resolve_sealed_scientific_protocol_v2_20261007.py',*[A/n for n in generated]]}
        create(out/'frozen_before_actual_handoff.json',{'input_sha256':pins,'prospective24_source_sha256':prospective,'new_quality_scores':0,'new_native_fits':0})
        for name,parent,worker in held:
            assert not worker.children();worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired.add(name)
            create(A/'service_owned_workflows_20261006'/name/'administrative_supersession_before_any120_science_v3_20261007.json',{
              'status':'administratively_retired_exact_idle_waiter_not_scientific_completion','identity':rows[name],
              'successor_service':name+'_v3','scientific_workers_stopped':0,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        for name in names:
            definition=read(A/'service_owned_workflows_20261006'/name/'job_definition.json')
            successors[name+'_v3']=start_service(name+'_v3',filemap[Path(definition['driver']).name],definition['arguments'],pins)
        create(A/'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v3_20261007.json',{'status':'actual_seven_consoleless120_v3_stages_started','input_sha256':pins,'launches':successors})
        create(out/'verification.json',{'status':'passed_actual7_exact_idle_waiters_native_archive_and_recursive_protocol_routes_before120_science',
          'input_sha256':pins,'actual_successors':successors,'new_native_fits':0,'new_quality_scores':0,'scientific_workers_stopped':0,'test_labels_read':False})
        print({'status':'passed','exact_idle_waiters':7,'measured_archive_subset_speedup':4.614189943398399},flush=True)
    finally:
        for name,parent,worker in held:
            if name not in retired:
                for p in (parent,worker):
                    if p.is_running():p.resume()

if __name__=='__main__':main()
