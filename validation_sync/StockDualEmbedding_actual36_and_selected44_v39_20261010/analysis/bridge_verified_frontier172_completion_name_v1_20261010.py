"""Resolve a generated wait-name typo with actual full172 completion evidence only."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed()
    actual='Frontier133172_complete133_family_v2_20261010'
    closed(actual)
    source=A/'service_owned_workflows_20261006'/actual
    assert not owned(read(source/'native_launch.json')) and read(source/'service_execution.json')['status']=='passed'
    receipt=A/'github_validation_sync_main_20261005/round172_receipt.json'
    assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['scored_records']==133
    execution=A/'optimization_20261003_r172/full_registration_execution.json'
    assert read(execution)['status']=='passed'
    proof=A/'frontier172_actual_completion_name_bridge_verification_v1_20261010.json'
    create(proof,{'status':'passed_administrative_alias_of_actual_full172_completion_only','actual_service':actual,'compatibility_wait_name':'Frontier133172_complete36_family_v2_20261010','actual_complete_records':133,'does_not_claim_new36_validation_family':True,'new_native_fits':0,'new_quality_scores':0,'input_sha256':{str(p):sha(p) for p in [Path(__file__),source/'native_launch.json',source/'service_execution.json',receipt,execution]}})
if __name__=='__main__':main()
