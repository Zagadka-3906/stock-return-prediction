"""Declare five comparison anchors and queue exact official scoring after actual156."""
from pathlib import Path
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    proposal=A/'BF16FlagAfter15217_train_only_proposal_v1_20261009.json'
    driver=A/'run_BF16FlagAfter15222_official_comparison_v1_20261009.py'
    control=A/'verify_BF16FlagAfter15217_full_training_v1_20261009.py'
    assert len(read(proposal)['new_cases'])==17
    ast.parse(driver.read_text(encoding='utf8'));ast.parse(control.read_text(encoding='utf8'))
    meta=A/'BF16FlagAfter15222_quality_preparation_v56_20261009.json'
    create(meta,{'status':'prepared_training_only22_after_actual156_and_full17_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'fixed_scientific_stage_base_round':152,
        'comparison_anchor_rounds':list(range(152,157)),'expected_quality_cases':22,
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),proposal,driver,control)},
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,
        'full_candidate_freeze_end_to_end_native_replays_and_registration_not_prepared_yet':True})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('BF16FlagAfter15222_official_comparison_v1_20261009',driver.name,[],{str(meta):sha(meta),str(driver):sha(driver)})
    create(A/'BF16FlagAfter15222_quality_launch_v56_20261009.json',{'launch':row,'official_scoring_not_claimed_started_before_gates':True})
    print({'queued_quality_cases':22,'owned_worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
