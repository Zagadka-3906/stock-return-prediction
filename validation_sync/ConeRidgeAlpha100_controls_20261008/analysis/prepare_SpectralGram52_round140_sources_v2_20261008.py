"""Fresh2 identifiers for the same52-case registry and QA51 mathematics."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_SpectralGram52_round140_sources_v1_20261008 as original
from prepare_SpectralGram140_truthful_metadata_receivers_v2_20261008 import remap
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
def source_paths():
    paths=[A/remap(p.relative_to(A).as_posix()) for p in original.source_paths()]
    paths += [p for p in original.source_paths() if p.is_file()]
    paths += [Path(__file__),A/'prepare_SpectralGram140_truthful_metadata_receivers_v2_20261008.py',
        A/'SpectralGram140_truthful_metadata_receiver_preparation_v2_20261008.json',A/'verify_SpectralGram52_prospective_routes_v3_20261008.py']
    return list(dict.fromkeys(paths))
def generate(parent):return {name:remap(text) for name,text in original.generate(parent).items()}
def main():
    ready_path=A/'SpectralGram52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual52_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'SpectralGram52_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==52 and pilot['best']==ready['best']
    proof_path=A/'SpectralGram52_round140_source_admission_v2_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual20_heads49_current_CDF147cold24hooks_and24_prospective140_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'SpectralGram52_round140_source_preparation_v2_20261008.json',{
        'status':'passed_actual52_sealed_candidate_and_admitted_full140_QA51_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':140,'scored_records':52,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
