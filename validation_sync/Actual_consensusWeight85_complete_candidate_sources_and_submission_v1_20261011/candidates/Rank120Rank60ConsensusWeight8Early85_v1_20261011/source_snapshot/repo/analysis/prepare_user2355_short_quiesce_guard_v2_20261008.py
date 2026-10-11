"""Keep the explicit2355 stop while allowing completed science to publish until2353."""
from pathlib import Path
import ast
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save


def main():
    original=A/'user_requested_stop2355_v1_20261008.py'
    source=original.read_text(encoding='utf8')
    before='timedelta(seconds=.25 if fixture else 600)'
    after='timedelta(seconds=.25 if fixture else 120)'
    assert source.count(before)==1
    corrected=source.replace(before,after)
    assert ast.dump(ast.parse(source),include_attributes=False)==ast.dump(ast.parse(corrected.replace(after,before)),include_attributes=False)
    module=save('user_requested_stop2355_v2_20261008.py',corrected)
    products=[module]
    for suffix in ('','_preheld'):
        path=A/('verify_user_requested_stop2355'+suffix+'_v1_20261008.py')
        code=path.read_text(encoding='utf8')
        code=code.replace('current2355','late_quiesce2355').replace('user_requested_stop2355_v1_20261008.py','user_requested_stop2355_v2_20261008.py')
        code=code.replace('_v1_20261008','_v2_20261008')
        products.append(save('verify_user_requested_stop2355'+suffix+'_v2_20261008.py',code))
    original_activation=A/'activate_actual_user_stop2355_v2_20261008.py'
    code=original_activation.read_text(encoding='utf8')
    code=code.replace('from scheduled_user_pause_20261007 import identity,exact','from scheduled_user_pause_20261007 import identity,exact,write')
    code=code.replace('current2355','late_quiesce2355').replace('user_requested_stop2355_v1_20261008.py','user_requested_stop2355_v2_20261008.py')
    code=code.replace('user_requested_stop2355_until_manual_continue_20261008','user_requested_stop2355_until_manual_continue_v2_20261008')
    code=code.replace('2026-10-08T23:45:00+08:00','2026-10-08T23:53:00+08:00')
    code=code.replace('actual_user_stop2355_wait_manual_continue_v2_20261008','actual_user_stop2355_wait_manual_continue_v3_20261008')
    code=code.replace("create(A/'current_user_runtime_control_20261008.json'","write(A/'current_user_runtime_control_20261008.json'")
    marker=" print({'actual_guard_worker'"
    assert code.count(marker)==1
    retire=""" old_folder=A/'user_requested_stop2355_until_manual_continue_20261008'
 old_state=read(old_folder/'guardian_status.json');assert old_state['suspended_entries']==0
 old=read(A/'service_owned_workflows_20261006/actual_user_stop2355_wait_manual_continue_v2_20261008/native_launch.json')
 assert owned(old) and state['stop_at_local']==old_state['stop_at_local']
 from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
 parent,worker,idle=suspended_idle(old,'    run (user_requested_stop2355_v1_20261008.py:')
 assert not worker.children() and owned(row)
 worker.terminate();worker.wait(timeout=10);parent.terminate();parent.wait(timeout=10)
 create(folder/'old_guard_retired_after_new_live_verified.json',{'status':'retired_only_old_idle_stop_guard_after_live_same_deadline_replacement','old_launch':old,'idle_stack':idle,'new_guard':row,'old_suspended_entries':0,'current_scientific_workers_stopped':0,'stop_at_local_preserved':'2026-10-08T23:55:00+08:00','quiet_publisher_quiesce_at_local':'2026-10-08T23:53:00+08:00'})
"""
    code=code.replace(marker,retire+marker)
    products.append(save('activate_actual_user_stop2355_v3_20261008.py',code))
    create(A/'user2355_short_quiesce_guard_preparation_v2_20261008.json',{
        'status':'prepared_fresh_guard_same2355_stop_with_only_quiet_publisher_freeze_changed2353',
        'input_sha256':{str(path):sha(path) for path in [Path(__file__),original,original_activation,*products]},
        'only_guard_change_is600_to120_seconds_before_stop_AST_exact_after_reversal':True,
        'actual_deadline': '2026-10-08T23:55:00+08:00','old_guard_not_retired_until_new_two_tests_and_live_guard_verified':True,
        'current_scientific_workers_stopped':0,'new_native_fits':0,'new_quality_scores':0})
    print({'prepared_new_guard':module.name,'quiet_publisher_freeze':'23:53','actual_stop':'23:55'},flush=True)


if __name__=='__main__':main()
