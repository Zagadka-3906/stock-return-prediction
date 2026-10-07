"""Fresh actual130 receivers require recovered128 closure, while retaining V1-V3 evidence."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    names={
      'verify_nonflag_EmpiricalBayes40_round130_sources_v3_20261007.py':'verify_nonflag_EmpiricalBayes40_round130_sources_v4_20261007.py',
      'run_nonflag_EmpiricalBayes40_official_comparison_v3_20261007.py':'run_nonflag_EmpiricalBayes40_official_comparison_v4_20261007.py',
      'run_nonflag_EmpiricalBayes40_admitted_comparison_v3_20261007.py':'run_nonflag_EmpiricalBayes40_admitted_comparison_v4_20261007.py',
      'prepare_nonflag_EmpiricalBayes40_selected_candidate_v3_20261007.py':'prepare_nonflag_EmpiricalBayes40_selected_candidate_v4_20261007.py',
      'publish_nonflag_EmpiricalBayes40_evidence_v3_20261007.py':'publish_nonflag_EmpiricalBayes40_evidence_v4_20261007.py',
      'queue_nonflag_EmpiricalBayes130_after_actual129_v3_20261007.py':'queue_nonflag_EmpiricalBayes130_after_actual129_v4_20261007.py'}
    sources=[Path(__file__)]
    for old,new in names.items():
        text=(A/old).read_text(encoding='utf8').replace('nonflag_RidgeFine52_round128_full_registration_v1','nonflag_RidgeFine52_round128_full_registration_v2')
        if old.startswith('run_nonflag_EmpiricalBayes40_admitted'):
            text=text.replace('run_nonflag_EmpiricalBayes40_official_comparison_v3_20261007','run_nonflag_EmpiricalBayes40_official_comparison_v4_20261007')
            text=text.replace("closed('nonflag_EmpiricalBayes40_round130_source_admission_v1')","closed('nonflag_EmpiricalBayes40_round130_source_admission_v4')")
        if old.startswith('verify_'):
            needle='    for p in sources:';assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'nonflag_EmpiricalBayes130_parent128_gate_recovery_v4_20261007.json',A/'recover_nonflag_EmpiricalBayes130_parent128_gate_v4_20261007.py',"+','.join('A/'+repr(p) for p in names.values())+"]\n"+needle)
        if old.startswith('publish_'):
            needle="    if phase=='scores':\n        for row in proof['records']:";assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'nonflag_EmpiricalBayes130_parent128_gate_recovery_v4_20261007.json',A/'recover_nonflag_EmpiricalBayes130_parent128_gate_v4_20261007.py',"+','.join('A/'+repr(p) for p in names.values())+"]\n"+needle)
        if old.startswith('queue_'):
            text=text.replace("    closed('nonflag_RFF128StreamMid76_round129_full_registration_v1')", "    closed('nonflag_RFF128StreamMid76_round129_full_registration_v1')\n    old=A/'service_owned_workflows_20261006/nonflag_EmpiricalBayes40_actual130_after129_dependency_queue_v3'\n    while owned(read(old/'native_launch.json')):time.sleep(10)\n    assert read(old/'service_execution.json')['status']=='failed', 'V3 failure must remain actual, not silently overwritten'")
            for before,after in names.items():text=text.replace(repr(before),repr(after))
            text=text.replace("name='nonflag_EmpiricalBayes40_round130_source_admission_v1'","name='nonflag_EmpiricalBayes40_round130_source_admission_v4'")
            text=text.replace('nonflag_EmpiricalBayes40_actual_admission_hidden_launch_v3_20261007.json','nonflag_EmpiricalBayes40_actual_admission_hidden_launch_v4_20261007.json').replace('nonflag_EmpiricalBayes40_actual6_complete_pipeline_launches_v3_20261007.json','nonflag_EmpiricalBayes40_actual6_complete_pipeline_launches_v4_20261007.json')
            needle='    for p,d in pins.items():assert sha(p)==d,p';assert text.count(needle)==2
            text=text.replace(needle,"    actual_recovery=A/'nonflag_EmpiricalBayes130_parent128_gate_recovery_v4_20261007.json'\n    pins.update({**read(actual_recovery)['input_sha256'],str(actual_recovery):sha(actual_recovery)})\n"+needle,1)
        compile(text,str(A/new),'exec');assert not (A/new).exists();(A/new).write_text(text,encoding='utf8',newline='\n');sources.extend([A/old,A/new])
    create(A/'nonflag_EmpiricalBayes130_parent128_gate_recovery_v4_20261007.json',{
      'status':'compiled_actual130_fresh_receivers_for_recovered128_closure_and_preserved_original_admission_failure','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in sources},'gate_before':'nonflag_RidgeFine52_round128_full_registration_v1','gate_after':'nonflag_RidgeFine52_round128_full_registration_v2',
      'original_frozen_bank_and_official40_math_and_generator_unchanged':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
