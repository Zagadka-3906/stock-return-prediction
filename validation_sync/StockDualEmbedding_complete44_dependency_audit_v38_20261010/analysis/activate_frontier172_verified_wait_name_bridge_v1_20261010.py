"""Attach a truthful completion bridge without editing pinned scientific drivers."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    old=A/'normalize_completed_stock_embedding36_after172_v1_20261010.py'
    assert old.read_text(encoding='utf8').count("closed('Frontier133172_complete36_family_v2_20261010')")==1
    name='Frontier133172_complete36_family_v2_20261010';assert not (A/'service_owned_workflows_20261006'/name).exists()
    actual=A/'service_owned_workflows_20261006/Frontier133172_complete133_family_v2_20261010/native_launch.json'
    assert owned(read(actual)) or read(actual.parent/'service_execution.json')['status']=='passed'
    driver=A/'bridge_verified_frontier172_completion_name_v1_20261010.py'
    pins={str(p):sha(p) for p in [Path(__file__),driver,old]}
    row=start_service(name,driver.name,[],pins)
    create(A/'frontier172_verified_wait_name_bridge_activation_v1_20261010.json',{'status':'actual_alias_waiting_for_verified_full172_only','actual_launch':row,'input_sha256':pins,'actual_dependency':'Frontier133172_complete133_family_v2_20261010','new_native_fits':0,'new_quality_scores':0,'scientific_sources_changed':False})
    print({'dependency_typo_bridge':'waiting_actual_complete133_record_172','new_scores':0},flush=True)
if __name__=='__main__':main()
