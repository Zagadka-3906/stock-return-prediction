"""Expose the actual new ensemble controls and publish completed72-native evidence."""
from pathlib import Path
import ast
import importlib.util
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle


def main():
    pointer=A/'actual_HuberSparse72_native_calendar_location_v1_20261008.json'
    proof=Path(read(pointer)['output'])/'verification.json'
    assert sha(proof)==read(pointer)['verification_sha256']
    verification=read(proof)
    assert verification['actual_historical_cases']==54 and verification['actual_calendar_cases']==18
    original=A/'monitor_actual_chronological_optimization_progress_v42_20261008.py'
    source=original.read_text(encoding='utf8').replace('progress_v42_20261008','progress_v43_20261008')
    marker="    write(A/'optimization_live_progress_v43_20261008.json'"
    assert source.count(marker)==1
    source=source.replace(marker,"""    sparse150=Path('E:/赛题五_本机临时/HuberSparse55_parent134_historical_v1_20261008')
    state['huber_sparse150_frontier']={'expected_quality_cases':59,'existing_annual_states':20,
        'synthetic55_and_metadata20_passed':True,
        'native72':status('HuberSparse72_native_historical_calendar_controls_v1_20261008'),
        'full55':status('HuberSparse55_full_historical_controls_v1_20261008'),
        'actual_full_control_records':len(list(sparse150.glob('case*.json'))),
        'expected_full_control_records':55,'actual_official_scores':0,'actual_future_inference':0,
        'complete_quality_receivers_not_yet_prepared':True,'duplicate_audit_still_required':True,
        'historical_controls_do_not_use_futureX_or_labels':True,'full_control_start_memory_threshold_GiB':12,
        'new_native_fits':0,'new_unadopted_candidates_not_claimed_qualified':True}
"""+marker)
    marker="    write(A/'optimization_live_progress_v43_20261008.md',text)"
    assert source.count(marker)==1
    source=source.replace(marker,"    text+=f\"\\n第150轮Huber与稀疏残差混合：复用20个年度状态，55合成/165截断已通过；72项真实原生、重载、解码与日历控制{state['huber_sparse150_frontier']['native72']['status']}，完整历史控制{state['huber_sparse150_frontier']['actual_full_control_records']}/55；59项正式评分接收流程与历史预测去重仍需准备。尚无该轮质量分或测试推理。\\n\"\n"+marker)
    driver=save('monitor_actual_chronological_optimization_progress_v43_20261008.py',source)
    spec=importlib.util.spec_from_file_location('actual_sparse_frontier43',driver)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    actual=module.snapshot()
    assert actual['huber_sparse150_frontier']['native72']['status']=='passed'
    assert actual['pipeline']['146']['full_registration']['status']=='passed'
    pins={str(path):sha(path) for path in (Path(__file__),original,driver,pointer,proof)}
    launch=start('actual_chronological_optimization_progress_observer_v43_20261008',driver.name,[],pins)
    old=read(A/'service_owned_workflows_20261006/actual_chronological_optimization_progress_observer_v42_20261008/native_launch.json')
    tree=ast.parse(original.read_text(encoding='utf8'))
    lines=[node.lineno for node in ast.walk(tree) if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and node.value.func.attr=='sleep' and len(node.value.args)==1 and isinstance(node.value.args[0],ast.Constant) and node.value.args[0].value==45]
    assert len(lines)==1
    parent,worker,idle=suspended_idle(old,f'    main ({original.name}:{lines[0]})')
    try:
        assert owned(launch) and not worker.children()
        worker.terminate();worker.wait(timeout=10)
        parent.terminate();parent.wait(timeout=10)
    finally:
        for process in (parent,worker):
            if process.is_running():process.resume()
    create(A/'latest_actual_optimization_progress_pointer_v43_20261008.json',{
        'json':str(A/'optimization_live_progress_v43_20261008.json'),
        'markdown':str(A/'optimization_live_progress_v43_20261008.md'),'launch':launch,'new_quality_scores':0})
    create(A/'actual_old_progress42_retired_after43_v1_20261008.json',{
        'status':'retired_only_proved_idle_old_observer','launch':old,'idle_stack':idle,
        'new_observer':launch,'scientific_workers_stopped':0})
    checkpoint=A/'actual_optimization_checkpoint_v43_20261008.json'
    create(checkpoint,{'status':'actual147_185_scoring_and_new150_training_only72_passed55_controls_running',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'best_fully_qualified':actual['best_fully_qualified'],
        'actual147':actual['pipeline']['147'],'actual150':actual['huber_sparse150_frontier'],
        'actual148':actual['adaptive148_frontier'],'actual149':actual['pure149_frontier'],
        'latest_verified_delivery':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
        'new150_native72_proof_sha256':sha(proof),'new150_native72_output':str(proof.parent),
        'stop_schedule':actual['actual_user_runtime_control'],'guardian':actual['actual_user2355_stop_guardian'],
        'new_quality_scores_by_checkpoint':0,'test_labels_read':False,'global_boundary_proven':False})
    base=A/'publish_actual147_scorer_guard_and_progress_main_v37_20261008.py'
    publication=base.read_text(encoding='utf8')
    publication=publication.replace('actual14780_149_preflight_and2355_main_publication_v36_20261008','actual147_scorer_guard_and_progress_main_publication_v37_20261008')
    publication=publication.replace('actual147_scorer_guard_and_progress_main_v37','actual150_native72_and_frontier_main_v38')
    publication=publication.replace('actual147_scorer_guard_and_progress_v37','actual150_native72_and_frontier_v38')
    publication=publication.replace('datetime.datetime(2026,10,8,22,44)','datetime.datetime(2026,10,8,23,0)')
    publication=publication.replace("sources=[Path(__file__),","sources=[Path(__file__),A/'actual_optimization_checkpoint_v43_20261008.json',")
    marker="'actual_JointCrossHuber35_existing_native_location_v1_20261008.json','actual_JointCrossHuber181_synthetic_location_v1_20261008.json'"
    assert publication.count(marker)==1
    publication=publication.replace(marker,"'actual_HuberSparse72_native_calendar_location_v1_20261008.json',"+marker)
    marker="'actual147_80_native_controls_completed':True,"
    assert publication.count(marker)==1
    publication=publication.replace(marker,marker+"'actual150_existing20_state_metadata_and55_synthetic165_prefix_passed':True,'actual150_native_historical54_calendar18_cold72_prefit_rejections18_passed':True,'actual150_full55_controls_have_own_live_status_and_are_not_claimed_completed':True,'actual150_quality_receivers_duplicate_audit_and_future_inference_not_completed':True,'actual150_official_scores':0,")
    publication=publication.replace('同步147轮评分前依赖修正、真实进度及观察器失败恢复记录','同步150轮20年度状态、55合成165截断和72原生日历复现及当前进度')
    publisher=save('publish_actual150_native72_and_frontier_main_v38_20261008.py',publication)
    launch=start('actual150_native72_and_frontier_main_publication_v38_20261008',publisher.name,[],{
        str(p):sha(p) for p in (Path(__file__),base,publisher,checkpoint,pointer,proof)})
    create(A/'actual150_native72_and_frontier_main_hidden_launch_v38_20261008.json',launch)
    print({'status':'new150_frontier43_observer_running_and_native72_main38_started','main_worker':launch['owned_worker_pid']},flush=True)


if __name__=='__main__':main()
