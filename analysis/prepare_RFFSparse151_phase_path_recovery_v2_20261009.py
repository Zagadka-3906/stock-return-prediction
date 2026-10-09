"""Correct151 dynamic phase output dates under a fresh publisher before any quality publication."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    original=A/'publish_RFFSparse59_evidence_v1_20261009.py';source=original.read_text(encoding='utf8')
    before="RFFSparse59_{phase}_github_v1_20261008";after="RFFSparse59_{phase}_github_v1_20261009"
    assert source.count(before)==1;source=source.replace(before,after)
    source=source.replace('RFFSparse59_{phase}_20261008','RFFSparse59_{phase}_20261009')
    publisher=save('publish_RFFSparse59_evidence_v2_20261009.py',source)
    original_verifier=A/'verify_RFFSparse59_prospective_routes_v1_20261009.py';source=original_verifier.read_text(encoding='utf8')
    source=source.replace('publish_RFFSparse59_evidence_v1_20261009.py','publish_RFFSparse59_evidence_v2_20261009.py').replace(before,after)
    verifier=save('verify_RFFSparse59_prospective_routes_v2_20261009.py',source)
    create(A/'RFFSparse151_phase_path_recovery_v2_20261009.json',{'status':'prepared_own151_dynamic_phase_directory_date_and_matching_prospective_verifier_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,publisher,original_verifier,verifier]},
        'actual_original_verifier_rejected_mismatch_before_quality':True,'numeric_prediction_and_scoring_math_unchanged':True,'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0})
if __name__=='__main__':main()
