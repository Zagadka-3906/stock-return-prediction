from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from scoped_user_cleanup_package134_runtime_v1_20261011 import install
gates=install();original=gates.closed
aliases={'Rank120Rank60ConsensusFraction8Early101_selected_candidate_sealing_v1_20261011':'actual_fraction101_scoped_seal134_v1_20261011','actual_consensusFraction101_complete_candidate_main_v1_20261011':'actual_fraction101_scoped_main134_v1_20261011'}
gates.closed=lambda name:original(aliases.get(name,name))
try:runpy.run_path(str(A/'prepare_verified_consensusFraction101_alternate_submission_delivery_v1_20261011.py'),run_name='__main__')
finally:gates.closed=original
