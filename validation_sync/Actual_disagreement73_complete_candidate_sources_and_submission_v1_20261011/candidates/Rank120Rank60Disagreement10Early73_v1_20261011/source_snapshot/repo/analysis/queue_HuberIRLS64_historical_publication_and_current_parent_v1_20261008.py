"""Publish actual preliminary controls, then admit the current parent only after136 qualifies."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    paths=[Path(__file__),A/'publish_HuberIRLS64_historical_controls_v1_20261008.py',
        A/'verify_HuberIRLS64_49_current_parent_v1_20261008.py',A/'HuberIRLS64_52_round137_plan_v1_20261008.json']
    pins={str(p):sha(p) for p in paths};rows={}
    for name,driver in (('HuberIRLS64_historical_controls_main_publication_v1_20261008','publish_HuberIRLS64_historical_controls_v1_20261008.py'),
        ('HuberIRLS64_49_current_parent_controls_v1_20261008','verify_HuberIRLS64_49_current_parent_v1_20261008.py')):
        rows[name]=start(name,driver,[],pins)
    create(A/'actual_HuberIRLS64_historical_publication_and_current_parent_hidden_launch_v1_20261008.json',{
        'status':'started_preliminary_controls_main_and_ordered137_current_parent_controls','launches':rows,
        'input_sha256':pins,'actual_quality_scores':0,'full52_official_queue_not_yet_admitted':True})


if __name__=='__main__':main()
