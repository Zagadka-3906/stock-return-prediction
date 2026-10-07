"""Refresh actual prospective checks with final byte hashes and start a hidden dependency queue."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    assert not (A/'nonflag_RidgeFine52_official_comparison_v1_20261007').exists()
    old=A/'verify_nonflag_RidgeFine52_prospective_routes_20261007.py'
    new=A/'verify_nonflag_RidgeFine52_prospective_routes_v2_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8').replace('nonflag_RidgeFine52_prospective_routes_20261007.json',
                                            'nonflag_RidgeFine52_prospective_routes_v2_20261007.json')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    for name in ('verify_nonflag_RidgeFine52_round128_sources_v1_20261007.py','publish_nonflag_RidgeFine52_evidence_v1_20261007.py'):
        path=A/name;text=path.read_text(encoding='utf8').replace('nonflag_RidgeFine52_prospective_routes_20261007.json',
                                                             'nonflag_RidgeFine52_prospective_routes_v2_20261007.json')
        compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
    import verify_nonflag_RidgeFine52_prospective_routes_v2_20261007 as prospective
    prospective.main()
    previous=A/'nonflag_RidgeFine52_science_route_preparation_v2_20261007.json'
    sources=[Path(p) for p in read(previous)['input_sha256']]
    sources += [Path(__file__),previous,new,A/'nonflag_RidgeFine52_prospective_routes_v2_20261007.json',
      A/'queue_nonflag_RidgeFine52_after_actual127_20261007.py',A/'nonflag_RidgeFine49_actual_controls_hidden_launch_20261007.json']
    pins={str(p):sha(p) for p in sources}
    preparation=A/'nonflag_RidgeFine52_science_route_preparation_v3_20261007.json'
    create(preparation,{'status':'passed_final_pre_score_fine52_complete_sources_and_actual24_prototypes12_graph_controls',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'new_native_fits':0,'new_quality_scores':0,
      'full49_cold147_actual_checks_in_progress_not_preclaimed':True,'actual127_closure_required':True,'test_labels_read':False})
    pins[str(preparation)]=sha(preparation)
    row=start('nonflag_RidgeFine52_actual128_after127_queue','queue_nonflag_RidgeFine52_after_actual127_20261007.py',[],pins)
    create(A/'nonflag_RidgeFine52_dependency_queue_actual_hidden_launch_20261007.json',{
      'status':'started_hidden_dependency_queue_for_actual128_after127','identity':row,'input_sha256':pins,
      'actual_quality_scores_by_queue_launch':0,'test_labels_read':False})
    print({'status':'started_hidden_fine52_queue','worker':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
