"""Queue the next local comparison behind real full123 qualification."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_reverse_Ridge124_route_mapping_20261007 import convert
def main():
    pairs=['start_nonflag_reverse_RFF40_actual_admission_20261007.py','continue_nonflag_reverse_RFF40_after_actual_admission_20261007.py']
    generated=[]
    for name in pairs:
        old=A/name;new=A/convert(name);assert not new.exists()
        text=convert(old.read_text(encoding='utf8'));compile(text,str(new),'exec')
        new.write_text(text,encoding='utf8',newline='\n');generated.append(new)
    paths=[Path(__file__),*generated,A/'nonflag_reverse_Ridge124_route_mapping_20261007.py',
      A/'nonflag_reverse_Ridge40_prospective_routes_v1_20261007.json',
      A/'nonflag_reverse_Ridge_actual_native_and_transform_controls_20261007.json']
    assert read(paths[-2])['status']=='passed_actual24_prospective_sources_and12_graph_controls'
    assert read(paths[-1])['actual_full_cases']==37 and read(paths[-1])['actual_cold_cases']==111
    pins={str(p):sha(p) for p in paths}
    create(A/'nonflag_reverse_Ridge40_launch_routes_source_preparation_20261007.json',
      {'status':'compiled_fresh_local124_launch_after_actual_controls_and_full123_admission',
       'input_sha256':pins,'actual_quality_scores':0,'test_labels_read':False})
    from start_nonflag_reverse_Ridge40_actual_admission_20261007 import main as admit
    admit()
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_reverse_Ridge40_continue_after_actual_admission',generated[1].name,[],pins)
    create(A/'nonflag_reverse_Ridge40_continuation_hidden_launch_20261007.json',row)
    print({'status':'queued_actual124_admission_and_guarded_local_continuation','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
