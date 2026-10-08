"""Queue the two completed-control main publications without opening windows."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'publish_nonflag_HuberIRLS64_controls_v1_20261008.py',
        A/'actual_nonflag_HuberIRLS64_small_location_v2_20261008.json',A/'actual_nonflag_HuberIRLS64_actual200k_location_v1_20261008.json',
        A/'actual_nonflag_HuberIRLS64_bank10_hidden_launch_v1_20261008.json']
    pins={str(p):sha(p) for p in paths}
    row=start('nonflag_HuberIRLS64_controls_main_publication_v1_20261008','publish_nonflag_HuberIRLS64_controls_v1_20261008.py',[],pins)
    create(A/'actual_nonflag_HuberIRLS64_controls_publication_hidden_launch_v1_20261008.json',{
        'status':'started_main_publication_of_actual_probe_then_completed_bank','identity':row,'input_sha256':pins,'actual_official_scores':0})


if __name__=='__main__':main()
