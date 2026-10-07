"""Start fresh local candidate/sealing/QA services after actual recovery admission."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    proof=A/'weighted_HGB340_round117_source_admission_v2_20261007.json'
    pins={str(proof):sha(proof),str(A/'resolve_sealed_scientific_protocol_20261007.py'):sha(A/'resolve_sealed_scientific_protocol_20261007.py')}
    pins.update(read(A/'weighted_HGB340_protocol_recovery_source_preparation_v4_20261007.json')['input_sha256'])
    jobs=[
      ('flagged_HGB_weighted_quarters340_selected_candidate_preparation_v4','prepare_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007.py'),
      ('flagged_HGB_weighted_quarters340_selected_candidate_sealing_v4','seal_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007.py'),
      ('weighted_HGB340_round117_full_registration_v2','run_weighted_HGB340_round117_full_registration_v2_20261007.py')]
    rows=[]
    for name,driver in jobs:
        rows.append(start_service(name,driver,[],pins))
    create(A/'weighted_HGB340_protocol_recovery_actual_hidden_launches_v4_20261007.json',{
      'status':'started_actual_three_consoleless_recovery_services', 'rows':rows,
      'original_failed_scopes_preserved':True,'new_quality_scores':0,'test_labels_read':False})
    print([(r['name'],r['owned_worker_pid']) for r in rows],flush=True)

if __name__=='__main__':main()
