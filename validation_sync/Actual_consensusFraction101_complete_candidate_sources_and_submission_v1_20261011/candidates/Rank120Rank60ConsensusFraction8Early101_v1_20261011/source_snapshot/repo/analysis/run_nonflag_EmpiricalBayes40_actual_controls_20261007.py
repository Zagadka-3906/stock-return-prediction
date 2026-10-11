"""Run real3 Bayesian native hooks and37 full plus111 cold CDF controls."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]

def main():
    from run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_20261007 import main as hooks
    from verify_nonflag_residual_EmpiricalBayes37_transform_20261007 import main as transforms
    hooks();transforms()
    from run_dependency_queue_v3_20261006 import read,sha,create
    paths=[A/'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007/verification.json',
      A/'nonflag_residual_EmpiricalBayes37_transform_preflight_20261007/verification.json']
    assert len(read(paths[0])['records'])==3
    assert read(paths[1])['actual_full_cases']==37 and read(paths[1])['actual_cold_cases']==111
    create(A/'nonflag_EmpiricalBayes40_actual_native_and_transform_controls_20261007.json',{
      'status':'passed_actual3_native_hooks37_full_and111_cold_controls',
      'input_sha256':{str(p):sha(p) for p in paths},'actual_native_hooks':3,'actual_full_cases':37,
      'actual_cold_cases':111,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
