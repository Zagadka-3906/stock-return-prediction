"""Start an ordered main-only publication after the existing134 writer completes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'publish_actual_BF16_independent_rank_controls_v1_20261008.py',
           A/'BF16_rank_CDF_synthetic_preflight_v1_20261008/verification.json',
           A/'BF16_independent_small_CPU_preflight_v1_20261008/verification.json']
    pins={str(p):sha(p) for p in paths}
    row=start('actual_BF16_independent_rank_controls_main_publication_v1_20261008',paths[1].name,[],pins)
    create(A/'actual_BF16_independent_rank_controls_main_hidden_launch_v1_20261008.json',{
        'status':'started_ordered_main_publication_of_completed_CPU_and_synthetic_controls_after_full134',
        'identity':row,'input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    print('Completed CPU and synthetic controls publication queued after actual134 main closure.',flush=True)


if __name__=='__main__':main()
