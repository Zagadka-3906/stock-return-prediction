"""Reconcile completed scores after a location-pointer collision; never rescore or replace failures."""
from pathlib import Path
import sys,time,argparse
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from run_protected162_complete_family_v1_20261010 import junction

def main(family):
    assert family in ('cumulative','official_top') and allowed()
    tag='high_impact_cumulative_screen_v2_20261010' if family=='cumulative' else 'protected_official_top_screen_v2_20261010'
    original_name='actual_'+tag;original=A/'service_owned_workflows_20261006'/original_name
    replacement=A/'service_owned_workflows_20261006'/('actual_'+tag+'_location_reconciliation_v1_20261010')
    while not (original/'service_execution.json').exists() or owned(read(original/'native_launch.json')):
        assert allowed();time.sleep(10)
    old=read(original/'service_execution.json')
    collision="FileExistsError: [Errno 17] File exists: '"+str(A/'actual_high_impact_cumulative_screen_location_v1_20261010.json')+"'"
    assert old['status']=='passed' or old['status']=='failed' and old['failure']==collision,old
    output=Path('E:/赛题五_本机临时')/tag;proof=read(output/'verification.json');count=97 if family=='cumulative' else 37
    assert len(proof['records'])==proof['new_quality_score_records']==count
    assert proof['actual_nonidentity_full_controls']==count-1 and proof['actual_nonidentity_prefix_controls']==3*(count-1)
    pins=dict(proof['input_sha256'])
    for p,d in pins.items():assert sha(p)==d,p
    for row in proof['records']:
        for path,digest in [(output/f"case{row['case']:03d}_controls.json",row['control_sha256']),(Path(row['official_score_cache']['official_metrics_source']),row['official_metric_capsule_sha256'])]:
            assert sha(path)==digest; pins[str(path)]=digest
        assert read(row['official_score_cache']['official_metrics_source'])['metrics']==row['metrics']
        path=output/f"case{row['case']:03d}_official.json";assert read(path)==row;pins[str(path)]=sha(path)
    assert proof['best']==max(proof['records'],key=lambda r:r['connected_final_score'])
    pointer=A/('actual_high_impact_cumulative_screen_location_v2_20261010.json' if family=='cumulative' else 'actual_protected_official_top_screen_location_v2_20261010.json')
    assert not pointer.exists();create(pointer,{'output':str(output),'verification_sha256':sha(output/'verification.json'),'reconciled_after_pointer_collision_only':True})
    archive=original.with_name(original_name+'_original_pointer_collision_evidence_v1_20261010')
    assert not archive.exists() and not owned(read(original/'native_launch.json'))
    original.rename(archive)
    assert archive.resolve().is_relative_to((A/'service_owned_workflows_20261006').resolve())
    junction(original,replacement)
    assert original.resolve()==replacement.resolve() and read(archive/'service_execution.json')==old
    create(A/(tag+'_location_reconciliation_v1_20261010.json'),{'status':'passed_rehashed_complete_official_scores_and_controls_with_original_pointer_collision_preserved','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'original_service_execution':old,'original_failure_evidence':str(archive),'actual_reconciliation_service':str(replacement),'canonical_service_compatibility_alias':str(original),'official_records':count,'full_controls':count-1,'prefix_controls':3*(count-1),'proper_output_pointer':str(pointer),'verification_sha256':sha(output/'verification.json'),'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('family',choices=['cumulative','official_top']);main(p.parse_args().family)
