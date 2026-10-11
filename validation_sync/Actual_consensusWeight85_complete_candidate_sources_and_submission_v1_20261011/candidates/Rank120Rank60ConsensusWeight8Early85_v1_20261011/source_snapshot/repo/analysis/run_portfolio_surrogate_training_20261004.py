"""Serialize new mature-checkpoint fine tuning after completed wide-model QA."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    gates=[ROOT/'analysis/neural_width_bank_20261004/training_execution_scope.json',
        ROOT/'analysis/neural_width_future_models_qa_20261004/verification.json',
        ROOT/'analysis/neural_width_complete_scheme_preflight_20261004/verification.json',
        ROOT/'analysis/portfolio_bank_implementation_preflight_20261004/verification.json',
        ROOT/'analysis/portfolio_surrogate_complete_output_search_plan_20261004.json',
        ROOT/'analysis/portfolio_surrogate_resource_observations_20261004/protocol.json']
    while not all(path.exists() for path in gates):time.sleep(10)
    for path in gates[:-2]:assert read(path)['status']=='passed',path
    assert read(gates[-1])['status']=='sampling_started'
    import train_portfolio_surrogate_bank_20261004 as bank
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    from locked_read_hash_cache_20261004 import fresh_sha
    sources=[Path(__file__),ROOT/'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT/'analysis/locked_read_hash_cache_20261004.py',*gates,
        ROOT/'analysis/observe_portfolio_surrogate_resources_20261004.py',
        ROOT/'analysis/portfolio_surrogate_training_run_20261004.json']
    metadata={'script':str(Path(__file__).resolve()),'driver_source_sha256':fresh_sha(Path(__file__)),
        'delegate':'train_portfolio_surrogate_bank_20261004.all_oof',
        'actual_passed_bank_implementation_controls_required':True,
        'no_overlap_with_original_wide_bank_fulltraining_or_complete_scheme_QA':True,
        'new_mature_checkpoint_fine_tuning_training_algorithms_unchanged':True}
    scope=FrozenProvenanceExecutionScope(bank,sources,metadata,ROOT/'analysis').install();failure=None
    try:bank.all_oof()
    except BaseException as error:failure=f'{type(error).__name__}: {error}';raise
    finally:
        report=scope.close(failed=failure is not None)
        bank.OUT.mkdir(exist_ok=True)
        with (bank.OUT/'training_execution_scope.json').open('x',encoding='utf-8') as stream:
            json.dump({'status':'passed' if failure is None else 'failed','failure':failure,
                'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),**report,
                'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)

if __name__=='__main__':main()
