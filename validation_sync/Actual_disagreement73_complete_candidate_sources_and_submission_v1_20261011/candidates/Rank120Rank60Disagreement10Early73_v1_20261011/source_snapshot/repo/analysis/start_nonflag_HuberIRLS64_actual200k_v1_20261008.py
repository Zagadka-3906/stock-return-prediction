"""Launch the CPU2 actual-window probe without a console or any GPU change."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'verify_nonflag_HuberIRLS64_actual200k_v1_20261008.py',
        A/'nonflag_HuberIRLS64_own_window_v1_20261008.py',A/'nonflag_HuberIRLS64_streamed_v1_20261008.py',
        A/'actual_nonflag_HuberIRLS64_small_location_v2_20261008.json']
    pins={str(p):sha(p) for p in paths}
    row=start('nonflag_HuberIRLS64_actual200k_controls_v1_20261008','verify_nonflag_HuberIRLS64_actual200k_v1_20261008.py',[],pins)
    create(A/'actual_nonflag_HuberIRLS64_actual200k_hidden_launch_v1_20261008.json',{
        'status':'started_actual_CPU2_own_mature200003row_HuberIRLS64_probe','identity':row,'input_sha256':pins,
        'actual_official_scores':0,'future_X_and_Y_read':False})


if __name__=='__main__':main()
