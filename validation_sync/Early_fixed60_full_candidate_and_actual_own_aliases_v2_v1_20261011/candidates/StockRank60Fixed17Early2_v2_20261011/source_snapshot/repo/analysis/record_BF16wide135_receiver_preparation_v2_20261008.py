"""Record prepared sources and exact empty E junctions before actual135 quality scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    from BF16wide135_storage_v1_20261008 import OUTPUTS,empty
    import prepare_BF16wide40_round135_sources_v2_20261008 as generator
    for path in OUTPUTS:empty(path)
    sources=[Path(__file__),A/'BF16wide135_storage_v1_20261008.py',
        A/'BF16wide40_round135_plan_v1_20261008.json',A/'prepare_BF16wide135_receivers_v1_20261008.py',
        A/'prepare_BF16wide40_round135_sources_v2_20261008.py',A/'run_BF16wide40_official_comparison_v2_20261008.py',
        A/'prepare_BF16wide40_selected_candidate_v2_20261008.py',A/'seal_BF16wide40_selected_candidate_v2_20261008.py',
        A/'run_BF16wide40_round135_full_registration_v2_20261008.py',A/'publish_BF16wide40_evidence_v2_20261008.py',
        A/'verify_BF16wide40_round135_sources_v2_20261008.py',A/'verify_BF16wide40_prospective_routes_v2_20261008.py',
        A/'queue_BF16wide135_complete_pipeline_v2_20261008.py']
    for p in sources:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    for parent in (112,133,134):
        generated=generator.generate(parent)
        assert len(generated)==8 and all(not (A/n).exists() for n in generated)
    create(A/'BF16wide135_receiver_preparation_v2_20261008.json',{'status':'prepared_fresh135_sources_and_exact_empty_E_outputs_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'empty_E_junctions':{str(p):str(p.resolve()) for p in OUTPUTS},'original_failed_or_frozen_sources_not_modified':True,
        'prospective24_semantic_controls_and_actual6_GPU_controls_still_required':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('Receiver preparation recorded: six exact empty E junctions and compiled135 sources.',flush=True)


if __name__=='__main__':main()
