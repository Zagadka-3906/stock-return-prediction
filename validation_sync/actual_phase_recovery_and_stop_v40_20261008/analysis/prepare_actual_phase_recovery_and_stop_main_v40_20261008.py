"""Publish the failed147 publisher, real recovery, pending phase regression and verified unchanged2355 stop."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    original=A/'publish_actual150_full55_and_provisional147_main_v39_20261008.py'
    source=original.read_text(encoding='utf8')
    source=source.replace('actual150_native72_and_frontier_main_publication_v38_20261008','actual150_full55_and_provisional147_main_publication_v39_20261008')
    source=source.replace('actual150_full55_and_provisional147_main_v39','actual_phase_recovery_and_stop_main_v40')
    source=source.replace('actual150_full55_and_provisional147_v39','actual_phase_recovery_and_stop_v40')
    source=source.replace('datetime.datetime(2026,10,8,23,12)','datetime.datetime(2026,10,8,23,19)')
    marker="sources=[Path(__file__),"
    assert source.count(marker)==1
    source=source.replace(marker,"sources=[Path(__file__),A/'actual_optimization_checkpoint_v45_20261008.json',A/'Joint147_publisher_phase_scratch_recovery_v7_20261008.json',A/'pending148_149_phase_isolation_preparation_v1_20261008.json',A/'HuberSparse_complete_native_predictor_preparation_v1_20261008.json',A/'predict_HuberSparse_complete_parent_scheme_v1_20261008.py',A/'prepare_HuberSparse_complete_native_predictor_v1_20261008.py',")
    marker="'actual_HuberSparse55_parent134_location_v1_20261008.json',"
    assert source.count(marker)==1
    source=source.replace(marker,"'actual_isolated_publisher_phase_preflight_v1_20261008.json',"+marker)
    source=source.replace("'user_requested_stop2355_until_manual_continue_20261008'):","'user_requested_stop2355_until_manual_continue_20261008','shutdown_ready_stop_preflight_late_quiesce2355_20261008','shutdown_ready_stop_preflight_late_quiesce2355_preheld_20261008','user_requested_stop2355_until_manual_continue_v2_20261008'):")
    marker="  storage=Path(read(A/'Git_publisher_E_relocation_location_v10_20261008.json')"
    assert source.count(marker)==1
    source=source.replace(marker,"  for failed_name in ('JointCrossHuberOrder185_scores_main_publication_v1_20261008','JointCrossHuber147_complete_chronological_dispatch_v4_20261008'):\n   failed_folder=A/'service_owned_workflows_20261006'/failed_name\n   sources.extend(failed_folder.glob('*.json'));sources.extend(failed_folder.glob('*.log'))\n"+marker)
    source=source.replace("'actual_user2355_stop_schedule_live_not_paused_early':True,","'actual_user2355_stop_schedule_live_not_paused_early':True,'actual147_failed_scores_publisher_preserved_and_retry2_live':True,'actual147_original_live185_scoring_worker_not_restarted':True,'pending148_149_same_parent_two_phase_hidden_git_regression_passed':True,'actual_user2355_guard_replacement_passed_both_deadline_probes_and_verified_live_before_retiring_old_guard':True,'quiet_publisher_quiesce_at_local':'2026-10-08T23:53:00+08:00',")
    source=source.replace('同步150轮55完整历史165截断复现及147轮评分中间记录','同步147轮失败发布恢复、148及149轮阶段目录回归、2355停工守护验证')
    driver=save('publish_actual_phase_recovery_and_stop_main_v40_20261008.py',source)
    pins={str(path):sha(path) for path in (Path(__file__),original,driver,A/'actual_optimization_checkpoint_v45_20261008.json')}
    launch=start('actual_phase_recovery_and_stop_main_publication_v40_20261008',driver.name,[],pins)
    create(A/'actual_phase_recovery_and_stop_main_hidden_launch_v40_20261008.json',launch)
    print({'main40_worker':launch['owned_worker_pid']},flush=True)


if __name__=='__main__':main()
