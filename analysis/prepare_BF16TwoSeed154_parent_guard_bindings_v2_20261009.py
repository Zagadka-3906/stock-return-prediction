"""Correct target/parent153 collision before any quality score; preserve frozen original drafts."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    assert not (A/'BF16TwoSeed79_official_comparison_v1_20261009/verification.json').exists()
    created=[];checks=[];originals=[]
    for oldname in ('prepare_BF16TwoSeed79_selected_candidate_v1_20261009.py','run_BF16TwoSeed79_round154_full_registration_v1_20261009.py'):
        src=A/oldname;dst=A/oldname.replace('_v1_','_v2_');s=src.read_text(encoding='utf8')
        needle='assert parent_number in (148,149,150,151,152,154)';assert s.count(needle)==1
        correct='assert parent_number in (148,149,150,151,152,153)'
        fixed=s.replace(needle,correct)
        if oldname.startswith('run_'):fixed=fixed.replace('五个合格锚点','六个合格锚点')
        assert not dst.exists();compile(fixed,str(dst),'exec');dst.write_text(fixed,encoding='utf8');created.append(dst);originals.append(src)
        tree=ast.parse(fixed);guard=next(n for n in ast.walk(tree) if isinstance(n,ast.Assert) and ast.unparse(n.test).startswith('parent_number in'))
        code=compile(ast.fix_missing_locations(ast.Module(body=[guard],type_ignores=[])),str(dst),'exec')
        for number in (147,148,149,150,151,152,153,154):
            try:exec(code,{'parent_number':number});accepted=True
            except AssertionError:accepted=False
            assert accepted==(number in range(148,154))
            checks.append({'source':dst.name,'comparison_parent':number,'accepted':accepted})
    proof=A/'BF16TwoSeed154_actual_parent_guard_controls_v2_20261009.json'
    create(proof,{'status':'passed_actual_two_receiver_guards_all6_parents_and_rejected_target154',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*created]},
        'controls':checks,'original_frozen_drafts_preserved':True,'scientific_transformations_and_scoring_unchanged':True,
        'new_quality_scores':0,'actual_future_X_read':False})
    src=A/'verify_BF16TwoSeed79_round154_sources_v1_20261009.py';dst=A/src.name.replace('_v1_','_v2_')
    s=src.read_text(encoding='utf8').replace('BF16TwoSeed154_complete_pipeline_preparation_v1','BF16TwoSeed154_complete_pipeline_preparation_v2')
    needle="    inputs=[Path(__file__),";assert s.count(needle)==1
    s=s.replace(needle,"    guardproof=A/'BF16TwoSeed154_actual_parent_guard_controls_v2_20261009.json'\n    assert len(read(guardproof)['controls'])==16\n    for f,d in read(guardproof)['input_sha256'].items():assert sha(f)==d,f\n    inputs=[guardproof,Path(__file__),")
    assert not dst.exists();compile(s,str(dst),'exec');dst.write_text(s,encoding='utf8');created.append(dst);originals.append(src)
    src=A/'run_BF16TwoSeed154_safe_registration_v1_20261009.py';dst=A/src.name.replace('_v1_','_v2_')
    s=src.read_text(encoding='utf8').replace('BF16TwoSeed154_complete_pipeline_preparation_v1','BF16TwoSeed154_complete_pipeline_preparation_v2')
    s=s.replace('dispatch_BF16TwoSeed154_complete_pipeline_v1','dispatch_BF16TwoSeed154_complete_pipeline_v2')
    s=s.replace('safe_full_main_v1','safe_full_main_v2').replace('import run_BF16TwoSeed79_round154_full_registration_v1','import run_BF16TwoSeed79_round154_full_registration_v2')
    s=s.replace("A/'dispatch_BF16TwoSeed154_complete_pipeline_v2_20261009.py']", "A/'dispatch_BF16TwoSeed154_complete_pipeline_v2_20261009.py',\n        A/'prepare_BF16TwoSeed79_selected_candidate_v2_20261009.py',A/'run_BF16TwoSeed79_round154_full_registration_v2_20261009.py',\n        A/'verify_BF16TwoSeed79_round154_sources_v2_20261009.py',A/'BF16TwoSeed154_actual_parent_guard_controls_v2_20261009.json']")
    assert not dst.exists();compile(s,str(dst),'exec');dst.write_text(s,encoding='utf8');created.append(dst);originals.append(src)
    src=A/'dispatch_BF16TwoSeed154_complete_pipeline_v1_20261009.py';dispatch=A/src.name.replace('_v1_','_v2_')
    s=src.read_text(encoding='utf8').replace('BF16TwoSeed154_complete_pipeline_preparation_v1','BF16TwoSeed154_complete_pipeline_preparation_v2')
    s=s.replace('BF16TwoSeed154_complete_hidden_launches_v1','BF16TwoSeed154_complete_hidden_launches_v2')
    assert not dispatch.exists();compile(s,str(dispatch),'exec');dispatch.write_text(s,encoding='utf8');created.append(dispatch);originals.append(src)
    oldmeta=A/'BF16TwoSeed154_complete_pipeline_preparation_v1_20261009.json';m=read(oldmeta)
    remap={'verify_BF16TwoSeed79_round154_sources_v1_20261009.py':'verify_BF16TwoSeed79_round154_sources_v2_20261009.py',
        'prepare_BF16TwoSeed79_selected_candidate_v1_20261009.py':'prepare_BF16TwoSeed79_selected_candidate_v2_20261009.py',
        'run_BF16TwoSeed154_safe_registration_v1_20261009.py':'run_BF16TwoSeed154_safe_registration_v2_20261009.py'}
    m['receiver_specs']=[[name,remap.get(driver,driver),args] for name,driver,args in m['receiver_specs']]
    m.update(status='prepared_complete154_guard_corrected_receivers_before_any_quality',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        input_sha256={**m['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),oldmeta,proof,*created]}})
    meta=A/'BF16TwoSeed154_complete_pipeline_preparation_v2_20261009.json';create(meta,m)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    old=read(A/'service_owned_workflows_20261006/BF16TwoSeed154_complete_chronological_dispatch_v1_20261009/native_launch.json')
    assert owned(old) and not (A/'BF16TwoSeed154_complete_hidden_launches_v1_20261009.json').exists()
    line=next(line for line in stack(old['owned_worker_pid']).splitlines() if '    closed (' in line)
    parent,worker,idle=suspended_idle(old,line)
    try:
        row=start('BF16TwoSeed154_complete_chronological_dispatch_v2_20261009',dispatch.name,[],{str(meta):sha(meta),str(dispatch):sha(dispatch)})
        assert owned(row);retire_suspended(old,row)
    except BaseException:
        if worker.is_running():worker.resume()
        if parent.is_running():parent.resume()
        raise
    create(A/'BF16TwoSeed154_parent_guard_corrected_hidden_handoff_v2_20261009.json',{
        'status':'corrected_154_candidate_and_full_comparison_parent_guards_before_quality_and_retired_owned_idle_dispatcher',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'old':old,'new':row,'old_idle_stack':idle,
        'actual_guard_controls':16,'input_sha256':{str(p):sha(p) for p in [Path(__file__),meta,proof,*created]},
        'scientific_jobs_stopped_or_restarted':0,'actual_future_X_read':False,'new_quality_scores':0})
    print({'new_dispatch_worker':row['owned_worker_pid'],'actual_guard_controls':16,'quality_scores':0},flush=True)
if __name__=='__main__':main()
