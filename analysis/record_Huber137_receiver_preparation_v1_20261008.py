"""Record the complete prospective52 receiver set before executing any quality or future inference."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    from Huber137_storage_v1_20261008 import OUTPUTS,empty
    paths=[Path(__file__),A/'prepare_Huber137_complete_receivers_v1_20261008.py',A/'prepare_Huber52_round137_sources_v1_20261008.py',
        A/'run_Huber52_official_comparison_v1_20261008.py',A/'prepare_Huber52_selected_candidate_v1_20261008.py',
        A/'seal_Huber52_selected_candidate_v1_20261008.py',A/'run_Huber52_round137_full_registration_v1_20261008.py',
        A/'publish_Huber52_evidence_v1_20261008.py',A/'verify_Huber52_round137_sources_v1_20261008.py',
        A/'verify_Huber52_prospective_routes_v1_20261008.py',A/'queue_Huber137_complete_pipeline_v1_20261008.py',
        A/'Huber137_receiver_drafts_v1_20261008.json',A/'Huber52_round137_receiver_contract_v1_20261008.json',
        A/'Huber137_D_scoring_scope_v1_20261008.json',A/'Huber137_storage_v1_20261008.py']
    for path in paths:
        assert path.is_file(),path
        if path.suffix=='.py':compile(path.read_text(encoding='utf8'),str(path),'exec')
    for path in OUTPUTS:empty(path)
    create(A/'Huber137_receiver_preparation_v1_20261008.json',{'status':'prepared_complete52_scientific_and_registry_sources_before_quality',
        'input_sha256':{str(path):sha(path) for path in paths},'exact_empty_outputs':{str(path):str(target) for path,target in OUTPUTS.items()},
        'new_quality_scores':0,'actual_future_X_calls':0,'native10_bank_unchanged':True,'full24_prospective_checks_still_required':True})


if __name__=='__main__':main()
