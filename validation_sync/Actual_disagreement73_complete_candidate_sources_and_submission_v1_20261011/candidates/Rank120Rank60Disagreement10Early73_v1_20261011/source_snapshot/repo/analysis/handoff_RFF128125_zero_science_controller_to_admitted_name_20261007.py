"""Align only the zero-science waiting dispatcher with the already admitted dependency names."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    old=A/'continue_nonflag_RFF12876_after_actual_admission_20261007.py'
    new=A/'continue_nonflag_RFF12876_after_actual_admission_v2_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8')
    assert text.count('nonflag_RFF12876_full73_controls_main_publication_v1')==1
    text=text.replace('nonflag_RFF12876_full73_controls_main_publication_v1','nonflag_RFF12876_full37_controls_main_publication_v1')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    tree=ast.parse(text);jobs=ast.literal_eval(next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='jobs' for t in n.targets)))
    assert len(jobs)==6 and all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    admitted=A/'run_nonflag_RFF12876_admitted_comparison_v1_20261007.py'
    assert repr(jobs[0][0]) in admitted.read_text(encoding='utf8')
    assert not (A/'nonflag_RFF12876_official_comparison_v1_20261007').exists()
    old_folder=A/'service_owned_workflows_20261006/nonflag_RFF12876_continue_after_actual_admission'
    row=read(old_folder/'native_launch.json')
    preserved={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in
      ('neural16384_annual','dependency_queue_v12_local_cache','nonflag_RFF12876_round125_source_admission_v1','nonflag_reverse_Ridge40_round124_full_registration_v1')}
    assert all(owned(r) for r in preserved.values())
    pins={str(p):sha(p) for p in [Path(__file__),old,new,admitted,A/'start_nonflag_RFF12876_actual_admission_20261007.py']}
    out=A/'RFF128125_zero_science_controller_actual_handoff_20261007';assert not out.exists();out.mkdir()
    create(out/'frozen_before_handoff.json',{'input_sha256':pins,'preserved_scientific_and_queue_identities':preserved,
      'actual_full_controls_count':73,'inherited_admitted_service_name':jobs[0][0],'quality_scores_before_handoff':0})
    parent,worker,idle=suspended_idle(row,'    main (continue_nonflag_RFF12876_after_actual_admission_20261007.py:9)')
    retired=False
    try:
        assert not worker.children();create(out/'old_controller_exact_idle_before_and_after.json',idle)
        successor=start_service('nonflag_RFF12876_continue_after_actual_admission_v2',new.name,[],pins)
        assert all(owned(r) for r in preserved.values())
        worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired=True
        create(old_folder/'administrative_supersession_to_admitted_dependency_name_20261007.json',
          {'status':'administratively_retired_exact_idle_zero_science_controller_not_scientific_completion',
           'identity':row,'successor':successor,'scientific_workers_stopped':0,'new_quality_scores':0})
        create(out/'verification.json',{'status':'passed_actual_zero_science_waiting_dispatcher_aligned_with_unchanged_admitted_scientific_sources',
          'input_sha256':pins,'new_identity':successor,'preserved_scientific_and_queue_identities':preserved,
          'scientific_workers_stopped':0,'new_native_fits':0,'new_quality_scores':0})
    finally:
        if not retired:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':main()
