"""Admit a single CPU2 full-bank worker only after the real200k probe passes."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    folder=A/'service_owned_workflows_20261006/nonflag_HuberIRLS64_actual200k_controls_v1_20261008'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    pointer=read(A/'actual_nonflag_HuberIRLS64_actual200k_location_v1_20261008.json')
    proof_path=Path(pointer['output'])/'verification.json';proof=read(proof_path)
    assert sha(proof_path)==pointer['verification_sha256'] and proof['actual_probe_native_fits']==2 and proof['actual_official_scores']==0
    paths=[Path(__file__),A/'train_nonflag_HuberIRLS64_bank10_v1_20261008.py',A/'nonflag_HuberIRLS64_bank10_plan_v1_20261008.json',
        A/'nonflag_HuberIRLS64_streamed_v1_20261008.py',A/'nonflag_HuberIRLS64_own_window_v1_20261008.py',proof_path]
    pins={str(p):sha(p) for p in paths}
    row=start('nonflag_HuberIRLS64_actual_bank10_v1_20261008','train_nonflag_HuberIRLS64_bank10_v1_20261008.py',[],pins)
    create(A/'actual_nonflag_HuberIRLS64_bank10_hidden_launch_v1_20261008.json',{
        'status':'started_actual10_own_mature_CPU2_HuberIRLS64_fits_after_actual200k_controls','identity':row,
        'input_sha256':pins,'actual_official_scores':0,'future_X_and_Y_read':False,'original_GPU_worker_unchanged':True})


if __name__=='__main__':main()
