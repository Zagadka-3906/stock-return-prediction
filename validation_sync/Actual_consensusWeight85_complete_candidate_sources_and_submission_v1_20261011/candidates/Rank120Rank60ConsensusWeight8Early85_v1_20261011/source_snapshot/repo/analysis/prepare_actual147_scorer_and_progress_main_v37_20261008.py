"""Preserve the actual pre-score recovery and operational failure evidence on main."""
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save


def main():
    progress=A/'optimization_live_progress_v42_20261008.json'
    actual=read(progress)
    checkpoint=A/'actual_optimization_checkpoint_v42_20261008.json'
    create(checkpoint,{'status':'actual_training_controls_running_until_user2355_stop',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'best_fully_qualified':actual['best_fully_qualified'],
        'actual147':actual['joint147_frontier'],'actual148':actual['adaptive148_frontier'],
        'actual149':actual['pure149_frontier'],'latest_fully_verified_delivery':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'latest_main':read(A/'actual14780_149_preflight_and2355_main_v36_receipt_20261008.json'),
        'stop_schedule':actual['actual_user_runtime_control'],'stop_guard':actual['actual_user2355_stop_guardian'],
        'pre_score_scorer_recovery':read(A/'Joint147_actual_scorer_upstream_recovery_v6_20261008.json'),
        'progress_recovery':read(A/'actual_progress146_and147_receiver_binding_v42_20261008.json'),
        'source_snapshots':{str(p):sha(p) for p in (progress,Path(__file__))},
        'new_quality_scores_by_checkpoint':0,'optimization_exhaustion_proven':False})
    original=A/'publish_actual14780_149_preflight_and2355_main_v36_20261008.py'
    source=original.read_text(encoding='utf8')
    source=source.replace('actual146_recovery_and14925_main_publication_v35_20261008','actual14780_149_preflight_and2355_main_publication_v36_20261008')
    source=source.replace('actual14780_149_preflight_and2355_main_v36','actual147_scorer_guard_and_progress_main_v37')
    source=source.replace('actual14780_149_preflight_and2355_stop_v36','actual147_scorer_guard_and_progress_v37')
    source=source.replace('datetime.datetime(2026,10,8,22,35)','datetime.datetime(2026,10,8,22,44)')
    marker="sources=[Path(__file__),"
    assert source.count(marker)==1
    source=source.replace(marker,"sources=[Path(__file__),A/'actual_optimization_checkpoint_v42_20261008.json',A/'Joint147_actual_scorer_upstream_recovery_v6_20261008.json',A/'actual_progress41_idle_line_failure_v1_20261008.json',A/'actual_progress146_and147_receiver_binding_v42_20261008.json',")
    source=source.replace('同步147轮80项原生复现、149轮32条程序与992图检查及今晚2355停工安排','同步147轮评分前依赖修正、真实进度及观察器失败恢复记录')
    marker="'actual147_80_native_controls_completed':True,"
    assert source.count(marker)==1
    source=source.replace(marker,marker+"'actual147_scorer_upstream_corrected_before_any185_score':True,'all_scorer_numeric_calculations_and_case_grid_preserved':True,'progress146_successful_recovery_service_binding_corrected':True,'progress_idle_line_failure_preserved_and_two_old_observers_retired':True,")
    driver=save('publish_actual147_scorer_guard_and_progress_main_v37_20261008.py',source)
    metadata=A/'actual147_scorer_guard_and_progress_main_preparation_v37_20261008.json'
    pins={str(p):sha(p) for p in (Path(__file__),original,driver,checkpoint,A/'Joint147_actual_scorer_upstream_recovery_v6_20261008.json')}
    create(metadata,{'status':'prepared_actual_pre_score_identity_and_progress_recovery_publication','input_sha256':pins,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launch=start('actual147_scorer_guard_and_progress_main_publication_v37_20261008',driver.name,[],{**pins,str(metadata):sha(metadata)})
    create(A/'actual147_scorer_guard_and_progress_main_hidden_launch_v37_20261008.json',launch)
    print({'started_actual_main37':launch['owned_worker_pid']},flush=True)


if __name__=='__main__':main()
