"""Correct a source-only prospective path before admitting or scoring round125."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    failed=A/'nonflag_RFF12876_prospective_routes_v1_20261007.json';proof=read(failed)
    assert proof['status']=='failed_actual_prospective_route_audit' and len(proof['issues'])==3
    assert all(Path(i['missing_unclassified_source']).name=='verify_nonflag_residual_RFF12837_transform_20261007.py' for i in proof['issues'])
    assert not (A/'nonflag_RFF12876_official_comparison_v1_20261007').exists()
    assert not (A/'nonflag_RFF12876_round125_source_admission_v1_20261007.json').exists()
    mapping=A/'nonflag_RFF128125_route_mapping_20261007.py'
    saved=A/'RFF128125_unadmitted_mapping_before_path_correction_20261007.py';assert not saved.exists()
    saved.write_bytes(mapping.read_bytes())
    text=mapping.read_text(encoding='utf8');needle='    m={\n';assert text.count(needle)==1
    text=text.replace(needle,needle+"      'verify_nonflag_residual_RFFRidge37_transform_20261007':'verify_nonflag_residual_RFF12873_transform_20261007',\n")
    compile(text,str(mapping),'exec');mapping.write_text(text,encoding='utf8',newline='\n')
    old=A/'verify_nonflag_RFF12876_prospective_routes_v1_20261007.py';new=A/'verify_nonflag_RFF12876_prospective_routes_v2_20261007.py';assert not new.exists()
    text=old.read_text(encoding='utf8').replace('nonflag_RFF12876_prospective_routes_v1_20261007.json','nonflag_RFF12876_prospective_routes_v2_20261007.json')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
    create(A/'RFF128125_zero_score_transform_path_correction_20261007.json',
      {'status':'corrected_unadmitted_73_case_driver_path_before_any125_official_score',
       'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
       'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,saved,mapping,old,new]},
       'failed_prospective_graph_controls_passed':24,'new_native_fits_by_correction':0,'new_quality_scores_by_correction':0})
    import verify_nonflag_RFF12876_prospective_routes_v2_20261007 as verifier
    verifier.main()
    corrected=A/'nonflag_RFF12876_prospective_routes_v2_20261007.json';assert read(corrected)['status']=='passed_actual24_prospective_sources_and24_graph_controls'
    original=read(A/'nonflag_RFF12876_science_route_preparation_20261007.json')
    pins={p:sha(p) for p in original['input_sha256']}
    pins.update({str(p):sha(p) for p in [Path(__file__),mapping,saved,new,corrected,A/'RFF128125_zero_score_transform_path_correction_20261007.json']})
    create(A/'nonflag_RFF12876_science_route_preparation_v2_20261007.json',
      {'status':'compiled_and_actual_prospective24_sources24_graphs_passed_before125_admission',
       'input_sha256':pins,'original_failed_prospective_record':str(failed),'actual_official_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
