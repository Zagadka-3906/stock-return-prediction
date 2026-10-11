"""Wait for an actual resource observer, declare driver provenance, fit frozen widths."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]

def main():
    observation=ROOT/'analysis/neural_width_resource_observations_20261004/protocol.json'
    while not observation.exists():time.sleep(1)
    proof=json.loads(observation.read_text(encoding='utf-8-sig'))
    assert proof['status']=='sampling_started'
    import train_neural_width_bank_20261004 as bank
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    from locked_read_hash_cache_20261004 import fresh_sha
    sources=[Path(__file__),ROOT/'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT/'analysis/locked_read_hash_cache_20261004.py',observation,
        ROOT/'analysis/observe_neural_width_resources_20261004.py',
        ROOT/'analysis/neural_width_training_run_20261004.json']
    metadata={'script':str(Path(__file__).resolve()),'driver_source_sha256':fresh_sha(Path(__file__)),
        'delegate':'train_neural_width_bank_20261004.all_oof',
        'original_training_algorithms_andconfigurations_unchanged':True}
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
