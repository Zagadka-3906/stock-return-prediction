"""Correct two inherited status labels before153 admission; keep every scientific source byte pinned."""
from pathlib import Path
from copy import deepcopy
import sys,ast,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'BF16Medium153_registration_guard_labels_v41_20261009.json'
FULL='run_BF16Medium78_round153_full_registration_v3_20261009.py'
DISPATCH='dispatch_BF16Medium153_complete_pipeline_v17_20261009.py'
REPLACEMENTS={
    'passed_actual29_sealed_candidate_and_admitted_full153_QA64_sources':'passed_actual78_sealed_candidate_and_admitted_full153_QA64_sources',
    'passed_actual29_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual78_selected_candidate_full_graph_and_metrics_and_source_bytes'}
def repaired(source):
    s=source
    for old,new in REPLACEMENTS.items():assert s.count(old)==1;s=s.replace(old,new)
    return s
def execute(name):
    import bind_future_import_namespaces_v38_20261009 as current
    import prepare_BF16Medium78_round153_sources_v1_20261009 as generator
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    original_route,original_read,original_paths=current.routed,current.read,generator.source_paths
    def route(number,source):
        s=original_route(number,source)
        if number==153 and next(iter(REPLACEMENTS)) in s:s=repaired(s)
        return s
    def metadata(path):
        value=original_read(path)
        if Path(path)==current.META:
            value=deepcopy(value);value['drivers']['153'][FULL]=m['full_driver'];value['drivers']['153'][DISPATCH]=m['dispatch_driver']
            value['receiver_specs']=[[sid,m['full_driver'] if sid=='BF16Medium78_round153_full_registration_v1_20261009' else driver,args] for sid,driver,args in value['receiver_specs']]
            value['input_sha256'].update(m['input_sha256']);value['input_sha256'][str(META)]=sha(META)
        return value
    current.routed,current.read=route,metadata
    generator.source_paths=lambda:list(dict.fromkeys([*original_paths(),Path(__file__),META,A/m['full_driver'],A/m['dispatch_driver'],A/'BF16Medium153_actual_guard_label_controls_v41_20261009.json']))
    try:current.execute(153,name)
    finally:current.routed,current.read,generator.source_paths=original_route,original_read,original_paths
def main():
    assert not (A/'service_owned_workflows_20261006/BF16Medium78_round153_source_admission_v1_20261009').exists()
    source=A/FULL;before=source.read_text(encoding='utf8');after=repaired(before);compile(after,str(source),'exec')
    left,right=ast.parse(before),ast.parse(after)
    # Compare the full AST after reverting just the two expected status constants.
    reverse={value:key for key,value in REPLACEMENTS.items()}
    for node in ast.walk(right):
        if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value in reverse:node.value=reverse[node.value]
    assert ast.dump(left,include_attributes=False)==ast.dump(right,include_attributes=False)
    import prepare_BF16Medium78_round153_sources_v1_20261009 as generator
    sealer=A/'seal_BF16Medium78_selected_candidate_v1_20261009.py'
    assert list(REPLACEMENTS.values())[0] in Path(generator.__file__).read_text(encoding='utf8')
    assert list(REPLACEMENTS.values())[1] in sealer.read_text(encoding='utf8')
    controls=[]
    tree=ast.parse(after)
    for name in ('prep','ready'):
        node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assert) and ast.unparse(n.test).startswith(name+"['status']"))
        expected=next(c.value for c in ast.walk(node) if isinstance(c,ast.Constant) and isinstance(c.value,str) and c.value.startswith('passed_actual78'))
        code=compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),str(source),'exec')
        for label,accept in ((expected,True),(expected.replace('actual78','actual29'),False)):
            try:exec(code,{name:{'status':label}});passed=True
            except AssertionError:passed=False
            assert passed==accept;controls.append({'field':name,'label':label,'accepted':passed})
    prospective=read(A/'BF16Medium78_prospective_routes_v1_20261009.json')
    current_hashes={str(n):{name:hashlib.sha256(s.encode()).hexdigest() for name,s in generator.generate(n).items()} for n in range(148,153)}
    assert current_hashes==prospective['generated_source_sha256']
    full=A/'run_BF16Medium78_round153_full_registration_guard_v41_20261009.py';dispatch=A/'dispatch_BF16Medium153_complete_pipeline_guard_v41_20261009.py'
    for target,name in ((full,FULL),(dispatch,DISPATCH)):
        assert not target.exists();code="from bind_BF16Medium153_registration_guard_labels_v41_20261009 import execute\nif __name__=='__main__':execute("+repr(name)+")\n"
        compile(code,str(target),'exec');target.write_text(code,encoding='utf8')
    proof=A/'BF16Medium153_actual_guard_label_controls_v41_20261009.json'
    create(proof,{'status':'passed_two_full153_guard_labels_against_actual78_generator_and_sealer_without_scientific_changes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),source,Path(generator.__file__),sealer,A/'BF16Medium78_prospective_routes_v1_20261009.json')},
        'controls':controls,'all40_original_generated_sources_byte_exact':True,'original_full_receiver_source_preserved':True,
        'complete_receiver_AST_changed_only_two_status_strings':True,'new_quality_scores':0,'test_labels_read':False})
    create(META,{'status':'prepared_corrected153_status_guard_binding_before_actual_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),full,dispatch,proof,source,A/'future_import_namespaces_v38_20261009.json')},
        'full_driver':full.name,'dispatch_driver':dispatch.name,'status_label_replacements':REPLACEMENTS,
        'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    old=read(A/'service_owned_workflows_20261006/BF16Medium153_complete_chronological_dispatch_serial_v38_20261009/native_launch.json');assert owned(old)
    line=next(line for line in stack(old['owned_worker_pid']).splitlines() if '    closed (' in line)
    parent,worker,idle=suspended_idle(old,line)
    try:
        row=start('BF16Medium153_complete_chronological_dispatch_guard_v41_20261009',dispatch.name,[],{str(META):sha(META),str(dispatch):sha(dispatch)})
        assert owned(row);retire_suspended(old,row)
    except BaseException:
        if worker.is_running():worker.resume()
        if parent.is_running():parent.resume()
        raise
    create(A/'BF16Medium153_registration_guard_hidden_handoff_v41_20261009.json',{'old':old,'new':row,'old_idle_stack':idle,
        'scientific_jobs_stopped_or_restarted':0,'actual_guard_checks':4,'all40_generated_sources_preserved':True})
    print({'actual_guard_checks':4,'unmodified_original_generated_sources':40,'new_dispatch_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
