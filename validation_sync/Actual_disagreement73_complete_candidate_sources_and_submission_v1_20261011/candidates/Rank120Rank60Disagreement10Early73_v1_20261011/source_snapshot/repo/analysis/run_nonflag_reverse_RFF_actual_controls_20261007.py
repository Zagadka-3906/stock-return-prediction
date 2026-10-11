"""Run both real control suites; no future qualification or official scores are claimed."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
def main():
    from run_nonflag_reverse_RFF_hook3_after_bank_20261007 import main as hooks
    from verify_nonflag_reverse_RFF37_transform_20261007 import main as transforms
    hooks();transforms()
    from run_dependency_queue_v3_20261006 import create,read,sha
    paths=[A/'nonflag_reverse_RFF_native_hook3_preflight_20261007/verification.json',
        A/'nonflag_reverse_RFF37_transform_preflight_20261007/verification.json']
    assert len(read(paths[0])['records'])==3
    assert read(paths[1])['actual_full_cases']==37 and read(paths[1])['actual_cold_cases']==111
    create(A/'nonflag_reverse_RFF_actual_native_and_transform_controls_20261007.json',
        {'status':'passed_actual3_native_hooks37_full_CDF_and111_cold_controls',
         'input_sha256':{str(p):sha(p) for p in paths},'actual_native_hooks':3,'actual_full_cases':37,'actual_cold_cases':111,
         'actual_official_scores':0,'round123_full_future_recipe_not_yet_admitted':True,'test_labels_read':False})
if __name__=='__main__':main()
