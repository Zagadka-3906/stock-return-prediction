"""Queue actual own-window causal controls without touching the running neural training."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'verify_HuberIRLS64_10_causal_inputs_v1_20261008.py',A/'nonflag_HuberIRLS64_own_window_v1_20261008.py']
    pins={str(p):sha(p) for p in paths}
    row=start('HuberIRLS64_10_causal_input_controls_v1_20261008','verify_HuberIRLS64_10_causal_inputs_v1_20261008.py',[],pins)
    create(A/'actual_HuberIRLS64_causal_inputs_hidden_launch_v1_20261008.json',{
        'status':'started_actual5_maturity10_later_label_poison10_saved_native_audits','identity':row,'input_sha256':pins,
        'future_test_X_and_Y_read':False,'actual_official_scores':0})


if __name__=='__main__':main()
