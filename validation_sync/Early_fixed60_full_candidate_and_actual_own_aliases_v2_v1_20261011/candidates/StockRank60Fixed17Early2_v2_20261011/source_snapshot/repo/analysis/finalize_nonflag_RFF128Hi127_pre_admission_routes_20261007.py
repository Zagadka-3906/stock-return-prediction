"""Freeze corrected complete routes before any stronger-L2 official comparison."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    assert not (A/'nonflag_RFF128Hi76_official_comparison_v1_20261007').exists()
    assert not (A/'nonflag_RFF128Hi76_round127_source_admission_v1_20261007.json').exists()
    old=A/'verify_nonflag_RFF128Hi76_prospective_routes_v1_20261007.py'
    new=A/'verify_nonflag_RFF128Hi76_prospective_routes_v2_20261007.py'
    assert not new.exists()
    text=old.read_text(encoding='utf8').replace('nonflag_RFF128Hi76_prospective_routes_v1_20261007.json',
                                            'nonflag_RFF128Hi76_prospective_routes_v2_20261007.json')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    import verify_nonflag_RFF128Hi76_prospective_routes_v2_20261007 as prospective
    prospective.main()
    oldprep=A/'nonflag_RFF128Hi76_science_route_preparation_v1_20261007.json'
    paths=[Path(p) for p in read(oldprep)['input_sha256']]
    paths += [Path(__file__),oldprep,new,A/'nonflag_RFF128Hi76_prospective_routes_v2_20261007.json',
              A/'start_nonflag_RFF128Hi127_complete_pipeline_20261007.py']
    create(A/'nonflag_RFF128Hi76_science_route_preparation_v2_20261007.json',{
        'status':'passed_corrected_pre_score_complete127_routes_and_actual24_graph_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},
        'prior_compiled_routes_record':str(oldprep),'official_comparisons_before_correction':0,
        'native_hook_provider_status_matches_actual_Hi_proof':True,
        'RAM_dispatch_gate_has_actual4_uncached_full_scoring_evidence':True,
        'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
