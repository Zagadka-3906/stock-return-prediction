"""Generate identical146 mathematics with actual admission2 and declared three-head registry."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_HuberCrossFamilyFine125_round146_sources_v2_20261008 as original
from recover_HuberCrossFamilyFine146_actual_admission_paths_v3_20261008 import MAP,adapt
NAMES=original.NAMES
def source_paths():
 out=[A/MAP.get(p.relative_to(A).as_posix(),p.relative_to(A).as_posix()) for p in original.source_paths()]
 out += [Path(__file__),Path(original.__file__),A/'recover_HuberCrossFamilyFine146_actual_admission_paths_v3_20261008.py',A/'HuberCrossFamilyFine146_actual_admission_paths_recovery_v3_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 outputs={n:adapt(s) for n,s in original.generate(parent).items()}
 for n,s in outputs.items():compile(s,str(A/n),'exec')
 return outputs
def main():
    ready_path=A/'HuberCrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual125_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'HuberCrossFamilyFine125_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==125 and pilot['best']==ready['best']
    admission=A/'HuberCrossFamilyFine125_round146_source_admission_v2_20261008.json';proof=read(admission)
    assert proof['status']=='passed_actual15_heads121_fixed_base_CDF363cold30hooks_and32_prospective146_sources'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    assert set(generated)==set(expected)
    for n,s in generated.items():assert not (A/n).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[n],n
    for n,s in generated.items():(A/n).write_text(s,encoding='utf8',newline='\n')
    create(A/'HuberCrossFamilyFine125_round146_source_preparation_v1_20261008.json',{'status':'passed_actual125_sealed_candidate_and_admitted_full146_QA57_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':146,'scored_records':125,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
