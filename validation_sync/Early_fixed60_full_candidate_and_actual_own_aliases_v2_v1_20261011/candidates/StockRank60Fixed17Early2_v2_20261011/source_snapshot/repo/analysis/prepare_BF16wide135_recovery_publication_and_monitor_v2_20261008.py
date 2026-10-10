"""Prepare a fresh live observer and main publication for corrected D-scoring receivers and preserved failures."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    source=A/'publish_actual_BF16wide135_receiver_preflight_v1_20261008.py';text=source.read_text(encoding='utf8')
    for stem in ('BF16wide135_complete_pipeline_dispatch','BF16wide40_prospective_routes','BF16wide135_receiver_preparation',
        'BF16wide135_complete_dependency_plan','BF16wide135_complete_hidden_launches',
        'actual_BF16wide135_complete_pipeline_dispatch','prepare_BF16wide40_round135_sources','record_BF16wide135_receiver_preparation'):
        text=text.replace(stem+'_v1_20261008',stem+'_v2_20261008')
    text=text.replace('actual_BF16wide135_receiver_preflight_main_v1_20261008','actual_BF16wide135_receiver_preflight_main_v2_20261008')
    text=text.replace('validation_sync/actual_BF16wide135_receiver_preflight_20261008','validation_sync/actual_BF16wide135_receiver_preflight_v2_20261008')
    before='    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}'
    after="""    sources += [A/'actual_BF16wide135_D_scoring_receiver_recovery_v4_20261008.json',
        A/'recover_BF16wide135_D_scoring_receivers_v2_20261008.py',A/'recover_BF16wide135_D_scoring_receivers_v3_20261008.py',
        A/'recover_BF16wide135_D_scoring_receivers_v4_20261008.py',A/'prepare_BF16wide135_inline_seal_waiter_guard_v3_20261008.py',
        A/'prepare_BF16wide135_inline_registration_guard_v4_20261008.py',A/'BF16wide135_inline_seal_waiter_guard_preparation_v3_20261008.json',
        A/'BF16wide135_inline_registration_guard_preparation_v4_20261008.json',A/'BF16wide135_scope_proof_prospective_preparation_v3_20261008.json',
        A/'prepare_BF16wide135_scope_proof_prospective_v3_20261008.py',A/'verify_BF16wide40_prospective_routes_v3_20261008.py',
        A/'verify_BF16wide135_D_scoring_scope_v2_20261008.py',A/'BF16wide135_D_scoring_scope_v2_20261008.json',
        A/'archive_BF16wide135_completed_scoring_CSV_v2_20261008.py',A/'monitor_BF16wide135_progress_v2_20261008.py',
        A/'prepare_BF16wide135_recovery_publication_and_monitor_v2_20261008.py']
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}"""
    assert text.count(before)==1;text=text.replace(before,after)
    text=text.replace('同步第135轮实际24项方案接收器检查与完整排队流程','同步第135轮实际D盘评分路径检查、24项新接收器与旧等待任务退役证据')
    monitor_source=A/'monitor_BF16wide135_progress_v1_20261008.py'
    monitor=monitor_source.read_text(encoding='utf8').replace('BF16wide135_complete_hidden_launches_v1_20261008','BF16wide135_complete_hidden_launches_v2_20261008')
    monitor=monitor.replace('actual_BF16wide135_progress_20261008','actual_BF16wide135_progress_v2_20261008')
    files={A/'publish_actual_BF16wide135_receiver_preflight_v2_20261008.py':text,A/'monitor_BF16wide135_progress_v2_20261008.py':monitor}
    for p,t in files.items():assert not p.exists();compile(t,str(p),'exec')
    for p,t in files.items():p.write_text(t,encoding='utf8',newline='\n')
    create(A/'actual_BF16wide135_recovery_publication_and_monitor_preparation_v2_20261008.json',{
        'status':'prepared_fresh_corrected_receiver_publication_and_observer','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,monitor_source,*files]},
        'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
