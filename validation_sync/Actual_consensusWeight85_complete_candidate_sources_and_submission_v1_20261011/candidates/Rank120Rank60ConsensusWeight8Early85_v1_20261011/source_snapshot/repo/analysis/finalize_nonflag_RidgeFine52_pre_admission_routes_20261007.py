"""Correct inherited cardinalities and publication paths before any new fine-grid score."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_RidgeFine52_round128_mapping_20261007 import finalize

def main():
    assert not (A/'nonflag_RidgeFine52_official_comparison_v1_20261007').exists()
    oldprep=A/'nonflag_RidgeFine52_science_route_preparation_20261007.json'
    paths=[Path(p) for p in read(oldprep)['input_sha256']]
    for path in paths:
        if path.suffix!='.py' or ('RidgeFine' not in path.name) or path.name.startswith('prepare_nonflag_RidgeFine52_science'):continue
        text=finalize(path.read_text(encoding='utf8'))
        if path.name.startswith('publish_nonflag_RidgeFine52_evidence'):
            text=text.replace("A/'prepare_nonflag_RidgeFine52_admission_and_publication_20261007.py'",
                              "A/'finalize_nonflag_RidgeFine52_pre_admission_routes_20261007.py'")
            text=text.replace("A/'nonflag_RidgeFine52_unadmitted_plan_metadata_correction_20261007.json'",
                              "A/'nonflag_RidgeFine52_science_route_preparation_v2_20261007.json'")
            needle="        parent,worker,idle=suspended_idle(main7,"
            assert text.count(needle)==1
            insertion="        import psutil\n        from datetime import datetime\n        deadline=datetime.fromisoformat('2026-10-07T23:45:00+08:00').timestamp()\n        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (main7['pid'],main7['owned_worker_pid'])):\n            assert time.time()<deadline\n            time.sleep(10)\n"
            text=text.replace(needle,insertion+needle)
        compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
    paths += [Path(__file__),oldprep]
    create(A/'nonflag_RidgeFine52_science_route_preparation_v2_20261007.json',{
      'status':'compiled_corrected_fine52_cardinalities_and_complete128_paths_before_scores',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},
      'actual_official_scores_before_correction':0,'new_native_fits':0,'test_labels_read':False})

if __name__=='__main__':main()
