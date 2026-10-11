"""Queue historical CDF and native-hook controls behind the actual10-model bank."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'verify_HuberIRLS64_49_parent134_historical_v1_20261008.py',
        A/'verify_HuberIRLS64_18_native_historical_hooks_v1_20261008.py',A/'HuberIRLS64_52_round137_plan_v1_20261008.json',
        A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',A/'HuberIRLS64_complete_parent_native_stage_v1_20261008.py',
        A/'predict_HuberIRLS64_complete_parent_scheme_v1_20261008.py']
    pins={str(p):sha(p) for p in paths};rows={}
    for name,driver in (('HuberIRLS64_49_parent134_historical_controls_v1_20261008','verify_HuberIRLS64_49_parent134_historical_v1_20261008.py'),
        ('HuberIRLS64_18_native_historical_hooks_v1_20261008','verify_HuberIRLS64_18_native_historical_hooks_v1_20261008.py')):
        rows[name]=start(name,driver,[],pins)
    create(A/'actual_HuberIRLS64_historical_controls_hidden_launches_v1_20261008.json',{
        'status':'started_actual49_full147cold_and18_native_historical_control_queue_after_bank10','launches':rows,
        'input_sha256':pins,'actual_quality_scores':0,'future_X_and_Y_read':False})


if __name__=='__main__':main()
