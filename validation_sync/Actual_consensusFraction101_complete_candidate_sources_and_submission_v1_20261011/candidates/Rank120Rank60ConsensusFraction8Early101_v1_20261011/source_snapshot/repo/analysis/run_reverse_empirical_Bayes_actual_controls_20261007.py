"""Actually run the signed native3 and full37/111 controls, never score or adopt a candidate."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from run_nonflag_residual_ReverseBayes64_hook3_after_bank_20261007 import main as native
    from verify_nonflag_residual_ReverseBayes37_transform_20261007 import main as full
    native();full()
    n=A/'nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007/verification.json';f=A/'nonflag_residual_ReverseBayes37_transform_preflight_20261007/verification.json'
    assert len(read(n)['records'])==3 and len(read(f)['controls'])==37 and read(f)['actual_cold_cases']==111
    create(A/'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json',{
      'status':'passed_actual_signed_native3_full37_independent_CDF_and111_cold_controls','residual_sign':-1,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),n,f]},'new_native_fits':0,'new_quality_scores':0,
      'official_scores_and_complete_frozen_future_candidate_and_QA_not_yet_executed':True,'test_labels_read':False})

if __name__=='__main__':main()
