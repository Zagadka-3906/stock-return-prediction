"""Publish the actual complete55 training controls and preserve a explicitly provisional147 score snapshot."""
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    pointer=A/'actual_HuberSparse55_parent134_location_v1_20261008.json'
    proof=Path(read(pointer)['output'])/'verification.json'
    assert sha(proof)==read(pointer)['verification_sha256']
    value=read(proof)
    assert value['actual_full_cases_including_identity']==55 and value['actual_cold_cases_including_identity']==165
    assert len(value['records'])==55 and value['actual_stage_base_round']==134
    for row in value['records']:
        assert row['full_independent_Pandas_bits_exact'] and row['preserved2020_flag1_invalid_bits_exact']
        assert len(row['cold_controls'])==3
    partial=[]
    for path in sorted((A/'JointCrossHuberOrder185_official_comparison_v1_20261008').glob('case*_official.json')):
        try:row=read(path)
        except (ValueError,OSError):continue
        assert row['connected_final_score']==row['metrics']['final_score']
        capsule=Path(row['official_score_cache']['official_metrics_source'])
        assert sha(capsule)==row['official_metric_capsule_sha256'] and read(capsule)['metrics']==row['metrics']
        partial.append({'record':str(path),'record_sha256':sha(path),'case':row['case'],
            'connected_final_score':row['connected_final_score'],'expected_unique_native_models':row['expected_unique_native_models'],
            'configuration':row['configuration'],'metrics_capsule':str(capsule),'metrics_capsule_sha256':sha(capsule)})
    best=min(partial,key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    checkpoint=A/'actual_optimization_checkpoint_v44_20261008.json'
    create(checkpoint,{'status':'actual150_full55_and165_prefix_controls_passed_with_provisional147_scoring_in_progress',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual150_full_control_cases':55,'actual150_full_rows_per_case':5635800,
        'actual150_cold_controls':165,'actual150_native_historical54_final_calendar18_cold72_passed':True,
        'full150_control_sha256':sha(proof),'full150_control_output':str(proof.parent),
        'actual147_saved_official_case_records_at_snapshot':len(partial),'actual147_expected_cases':185,
        'actual147_provisional_best':best,'actual147_provisional_records':partial,
        'actual147_provisional_best_is_not_frozen_selected_scheme_and_not_qualified':True,
        'best_fully_qualified_delivery':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'actual150_59_quality_receiver_source_admission_and_duplicate_audit_not_prepared':True,
        'new_quality_scores_by_checkpoint':0,'actual150_official_scores':0,'actual150_future_inference':0,
        'test_labels_read':False,'global_feasible_direction_and_compute_boundary_proven':False,
        'user_stop_at_local':'2026-10-08T23:55:00+08:00','no_early_goal_pause':True})
    original=A/'publish_actual150_native72_and_frontier_main_v38_20261008.py'
    source=original.read_text(encoding='utf8')
    source=source.replace('actual147_scorer_guard_and_progress_main_publication_v37_20261008','actual150_native72_and_frontier_main_publication_v38_20261008')
    source=source.replace('actual150_native72_and_frontier_main_v38','actual150_full55_and_provisional147_main_v39')
    source=source.replace('actual150_native72_and_frontier_v38','actual150_full55_and_provisional147_v39')
    source=source.replace('datetime.datetime(2026,10,8,23,0)','datetime.datetime(2026,10,8,23,12)')
    source=source.replace("sources=[Path(__file__),","sources=[Path(__file__),A/'actual_optimization_checkpoint_v44_20261008.json',")
    marker="'actual_HuberSparse72_native_calendar_location_v1_20261008.json',"
    assert source.count(marker)==1
    source=source.replace(marker,"'actual_HuberSparse55_parent134_location_v1_20261008.json',"+marker)
    before="'actual150_full55_controls_have_own_live_status_and_are_not_claimed_completed':True"
    assert source.count(before)==1
    source=source.replace(before,"'actual150_full55_full5635800_and165_cold_controls_passed':True")
    marker="  for directory in ('shutdown_ready_stop_preflight_current2355_20261008'"
    assert source.count(marker)==1
    source=source.replace(marker,"  snapshot=read(A/'actual_optimization_checkpoint_v44_20261008.json')\n  for record in snapshot['actual147_provisional_records']:\n   assert sha(record['record'])==record['record_sha256'] and sha(record['metrics_capsule'])==record['metrics_capsule_sha256']\n   sources.extend([Path(record['record']),Path(record['metrics_capsule'])])\n"+marker)
    source=source.replace('同步150轮20年度状态、55合成165截断和72原生日历复现及当前进度','同步150轮55完整历史165截断复现及147轮评分中间记录')
    publisher=save('publish_actual150_full55_and_provisional147_main_v39_20261008.py',source)
    pins={str(path):sha(path) for path in (Path(__file__),original,publisher,pointer,proof,checkpoint)}
    launch=start('actual150_full55_and_provisional147_main_publication_v39_20261008',publisher.name,[],pins)
    create(A/'actual150_full55_and_provisional147_main_hidden_launch_v39_20261008.json',launch)
    print({'main39_worker':launch['owned_worker_pid'],'actual55_full_controls':55,'provisional147_records':len(partial)},flush=True)


if __name__=='__main__':main()
