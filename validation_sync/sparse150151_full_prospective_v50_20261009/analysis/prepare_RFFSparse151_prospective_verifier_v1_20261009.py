"""Prepare151 route verifier with its own59/QA62 contracts and six actual mixture groups."""
from pathlib import Path
import re,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    original=A/'verify_HuberSparse59_prospective_routes_v1_20261009.py';source=original.read_text(encoding='utf8')
    source=source.replace("ns['collect'](145,56,125)","ns['collect'](150,61,59)")
    mapping={
        'prepare_HuberSparse59_round150_sources_v2_20261009':'prepare_RFFSparse59_round151_sources_v1_20261009',
        'HuberSparse150_storage_v1_20261008':'RFFSparse151_storage_v2_20261009',
        'HuberSparse_complete_parent_CDF_v1_20261008':'RFFSparse_complete_parent_CDF_v3_20261009',
        'run_HuberSparse59_official_comparison_v2_20261009':'run_RFFSparse59_official_comparison_v3_20261009',
        'prepare_HuberSparse59_selected_candidate_v2_20261009':'prepare_RFFSparse59_selected_candidate_v3_20261009',
        'publish_HuberSparse59_evidence_v1_20261009':'publish_RFFSparse59_evidence_v1_20261009'}
    for before,after in mapping.items():source=source.replace(before,after)
    source=source.replace('HuberSparse','RFFSparse').replace('RFFSparse150','RFFSparse151').replace('round150','round151').replace('prospective150','prospective151')
    source=source.replace('[146,147,148,149]','[147,148,149,150]').replace('(150,61,59)','(151,62,59)').replace('(150, 61, 59)','(151, 62, 59)').replace('[150,61,59]','[151,62,59]')
    source=source.replace("namespace['snapshot'](150)","namespace['snapshot'](151)").replace('QA61','QA62')
    source=re.sub(r'(RFFSparse[A-Za-z0-9_/-]*?)_v1_20261008',r'\1_v1_20261009',source)
    source=source.replace('register_RFFSparse59_round151_artifacts_20261008','register_RFFSparse59_round151_artifacts_20261009').replace('publish_RFFSparse59_round151_full_validation_20261008','publish_RFFSparse59_round151_full_validation_20261009')
    source=source.replace('before any official125 score.','before any official59 score.')
    destination=save('verify_RFFSparse59_prospective_routes_v1_20261009.py',source)
    create(A/'RFFSparse151_prospective_verifier_preparation_v1_20261009.json',{'status':'prepared151_prospective_verifier_before_execution',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),original,destination)},'new_quality_scores':0,'new_future_inference':0})
if __name__=='__main__':main()
