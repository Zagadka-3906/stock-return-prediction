"""Retire only the exact idle, empty, unscored incorrect future route helper."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

def main():
    out=A/'full_universe_HGB44_bad_route_idle_supersession_20261007';assert not out.exists();out.mkdir()
    folder=A/'service_owned_workflows_20261006/full_universe_HGB44_official_comparison'
    row=read(folder/'native_launch.json')
    old_output=A/'full_universe_HGB44_official_comparison_20261007'
    assert old_output.is_dir() and not list(old_output.iterdir())
    control=read(A/'full_universe_HGB44_route_correction_v2_20261007.json')
    assert sha(Path(control['original_source']))==control['original_sha256']
    assert sha(Path(control['corrected_source']))==control['corrected_sha256']
    preserved={name:read(A/'service_owned_workflows_20261006'/name/'native_launch.json') for name in ['neural16384_annual','dependency_queue_v12_local_cache','cpu_full_universe_HGB_native_bank24']}
    state=read(A/'service_owned_dependency_queue_v4_20261006/state.json');preserved['round90']=state['activated_jobs']['round90']
    assert all(owned(r) for r in preserved.values())
    parent,worker,idle=suspended_idle(row,'    main (run_full_universe_HGB44_official_comparison_20261007.py:34)')
    retired=False
    try:
        assert not worker.children() and not list(old_output.iterdir())
        worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired=True
        assert not owned(row) and all(owned(r) for r in preserved.values())
        proof={'status':'administratively_retired_exact_idle_incorrect_unstarted_score_route_not_scientific_completion','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'identity':row,'idle_before_and_after':idle,'original_output_directory_remains_empty':True,'original_source_sha256_unchanged':sha(Path(control['original_source'])),'corrected_source_sha256':sha(Path(control['corrected_source'])),'preserved_actual_workers':preserved,'scientific_workers_stopped_suspended_or_restarted':0,'original_helper_new_fits':0,'original_helper_new_official_scores':0,'test_labels_read':False}
        create(folder/'administrative_supersession_for_full_universe_HGB44_v2_20261007.json',proof);create(out/'verification.json',proof)
    finally:
        if not retired:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':main()
