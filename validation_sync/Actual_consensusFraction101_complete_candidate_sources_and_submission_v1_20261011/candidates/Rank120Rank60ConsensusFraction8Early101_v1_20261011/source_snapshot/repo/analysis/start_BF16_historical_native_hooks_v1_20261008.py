"""Dispatch only lazy historical hooks; full future candidate inference remains selected and frozen first."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'verify_BF16_complete_parent_native_hook3_v1_20261008.py',
           A/'BF16_complete_parent_native_stage_v1_20261008.py',
           A/'predict_BF16_complete_parent_rank_scheme_v1_20261008.py',
           A/'neural_BF16_independent_forward_v1_20261008.py',
           A/'BF16_complete_parent_rank_CDF_v1_20261008.py']
    pins={str(p):sha(p) for p in paths}
    row=start('BF16_complete_parent_actual_historical_native_hook3_v1_20261008',paths[1].name,[],pins)
    create(A/'actual_BF16_complete_parent_historical_native_hook3_hidden_launch_v1_20261008.json',{
        'status':'started_lazily_gated_actual3_historical_BF16_native_decoder_CDF_and_day_prefix_hooks',
        'identity':row,'input_sha256':pins,'actual_future_candidate_inference_not_yet_executed':True,
        'new_quality_scores':0,'test_labels_read':False})
    print('Historical3 native hooks queued after full GPU oracle and37/111 controls; no future inference yet.',flush=True)


if __name__=='__main__':main()
