"""Execute the unchanged146 mathematical receiver with actual recovered145 completion and report metadata binding."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from prepare_actual146_after_recovered145_report_v4_20261008 import execute
if __name__=='__main__':execute('run_HuberCrossFamilyFine125_official_comparison_v2_20261008.py')
