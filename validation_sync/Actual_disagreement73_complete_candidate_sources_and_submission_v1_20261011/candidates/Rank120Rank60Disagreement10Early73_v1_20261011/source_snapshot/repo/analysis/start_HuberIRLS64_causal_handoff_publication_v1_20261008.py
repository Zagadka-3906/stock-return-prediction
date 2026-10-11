"""Queue serialized publication of completed causal controls and the next goal checkpoint."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'publish_HuberIRLS64_causal_and_handoff_v1_20261008.py',A/'record_actual_optimization_handoff_v5_20261008.py']
    pins={str(p):sha(p) for p in paths}
    row=start('HuberIRLS64_causal_and_handoff_main_publication_v1_20261008','publish_HuberIRLS64_causal_and_handoff_v1_20261008.py',[],pins)
    create(A/'actual_HuberIRLS64_causal_handoff_publication_hidden_launch_v1_20261008.json',{
        'status':'started_actual_causal_and_handoff_main_publication_after_completed_historical_controls','identity':row,'input_sha256':pins,
        'actual_quality_scores':0,'goal_remains_active':True})


if __name__=='__main__':main()
