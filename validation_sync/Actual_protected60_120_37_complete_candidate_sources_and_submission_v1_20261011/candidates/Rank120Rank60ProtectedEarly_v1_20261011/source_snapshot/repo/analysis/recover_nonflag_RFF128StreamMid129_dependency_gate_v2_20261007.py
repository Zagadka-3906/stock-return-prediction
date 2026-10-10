"""Use actual recovered128 closure in fresh129 receivers; mathematical recipes are identical."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    gate_before='nonflag_RidgeFine52_round128_full_registration_v1';gate_after='nonflag_RidgeFine52_round128_full_registration_v2'
    names={
      'run_nonflag_RFF128StreamMid76_official_comparison_v1_20261007.py':'run_nonflag_RFF128StreamMid76_official_comparison_v2_20261007.py',
      'run_nonflag_RFF128StreamMid76_admitted_comparison_v1_20261007.py':'run_nonflag_RFF128StreamMid76_admitted_comparison_v2_20261007.py',
      'publish_nonflag_RFF128StreamMid76_evidence_v1_20261007.py':'publish_nonflag_RFF128StreamMid76_evidence_v2_20261007.py',
      'prepare_nonflag_RFF128StreamMid76_selected_candidate_v1_20261007.py':'prepare_nonflag_RFF128StreamMid76_selected_candidate_v2_20261007.py',
      'run_nonflag_RFF128StreamMid76_round129_full_registration_v1_20261007.py':'run_nonflag_RFF128StreamMid76_round129_full_registration_v2_20261007.py',
      'verify_nonflag_RFF128StreamMid76_round129_sources_v1_20261007.py':'verify_nonflag_RFF128StreamMid76_round129_sources_v2_20261007.py',
      'queue_nonflag_RFF128StreamMid129_after_actual128_20261007.py':'queue_nonflag_RFF128StreamMid129_after_actual128_v2_20261007.py'}
    sources=[Path(__file__)];actual_names={k:v for k,v in names.items()}
    for old,new in names.items():
        text=(A/old).read_text(encoding='utf8').replace(gate_before,gate_after)
        if old.startswith('run_nonflag_RFF128StreamMid76_admitted'):
            text=text.replace('run_nonflag_RFF128StreamMid76_official_comparison_v1_20261007','run_nonflag_RFF128StreamMid76_official_comparison_v2_20261007')
        if old.startswith('verify_'):
            needle='    for p in sources:';assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'nonflag_RFF128StreamMid129_dependency_gate_recovery_v2_20261007.json',A/'recover_nonflag_RFF128StreamMid129_dependency_gate_v2_20261007.py',"+','.join("A/"+repr(x) for x in names.values())+"]\n"+needle)
        if old.startswith('publish_'):
            needle="    if phase=='scores':\n        for row in proof['records']:";assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'nonflag_RFF128StreamMid129_dependency_gate_recovery_v2_20261007.json',A/'recover_nonflag_RFF128StreamMid129_dependency_gate_v2_20261007.py',"+','.join("A/"+repr(x) for x in names.values())+"]\n"+needle)
        if old.startswith('queue_'):
            for before,after in names.items():text=text.replace(repr(before),repr(after))
            needle="    for p,d in pins.items():assert sha(p)==d,p";assert text.count(needle)==2
            text=text.replace(needle,"    recovery=A/'nonflag_RFF128StreamMid129_dependency_gate_recovery_v2_20261007.json'\n    pins.update({**read(recovery)['input_sha256'],str(recovery):sha(recovery)})\n"+needle,1)
        compile(text,str(A/new),'exec');assert not (A/new).exists();(A/new).write_text(text,encoding='utf8',newline='\n');sources.extend([A/old,A/new])
    oldqueue=A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue'
    assert read(oldqueue/'service_execution.json')['status']=='failed'
    create(A/'nonflag_RFF128StreamMid129_dependency_gate_recovery_v2_20261007.json',{
      'status':'compiled_fresh129_execution_receivers_for_actual_recovered128_closure','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [*sources,*oldqueue.glob('*.json'),*oldqueue.glob('*.log')]},
      'gate_before':gate_before,'gate_after':gate_after,'official_numerics_and_bank_and_original_frozen_generator_unchanged':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
