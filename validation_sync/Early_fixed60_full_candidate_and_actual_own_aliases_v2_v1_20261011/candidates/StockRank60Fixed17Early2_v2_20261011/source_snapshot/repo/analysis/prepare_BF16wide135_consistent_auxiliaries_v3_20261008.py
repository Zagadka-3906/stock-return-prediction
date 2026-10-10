"""Prepare current3 observer, main publication and reversible completed-CSV archival for the fully consistent dispatch."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    pub_source=A/'publish_actual_BF16wide135_receiver_preflight_v2_20261008.py';pub=pub_source.read_text(encoding='utf8')
    for stem in ('BF16wide135_complete_pipeline_dispatch','BF16wide40_prospective_routes','BF16wide135_receiver_preparation',
        'BF16wide135_complete_dependency_plan','BF16wide135_complete_hidden_launches','actual_BF16wide135_complete_pipeline_dispatch',
        'prepare_BF16wide40_round135_sources','record_BF16wide135_receiver_preparation','actual_BF16wide135_receiver_preflight_main',
        'monitor_BF16wide135_progress'):
        pub=pub.replace(stem+'_v2_20261008',stem+'_v3_20261008')
    pub=pub.replace('validation_sync/actual_BF16wide135_receiver_preflight_v2_20261008','validation_sync/actual_BF16wide135_receiver_preflight_v3_20261008')
    before='    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}'
    after="""    sources += [A/'actual_BF16wide135_complete_dependency_recovery_v5_20261008.json',A/'recover_BF16wide135_complete_dependency_references_v5_20261008.py',
        A/'verify_BF16wide40_prospective_routes_v4_20261008.py',A/'archive_BF16wide135_completed_scoring_CSV_v3_20261008.py',
        A/'prepare_BF16wide135_consistent_auxiliaries_v3_20261008.py',
        *[A/'service_owned_workflows_20261006'/name/file for name in ('BF16wide135_complete_pipeline_dispatch_v2_20261008',
            'BF16wide40_selected_candidate_sealing_v2_20261008','actual_BF16wide135_live_progress_monitor_v2_20261008')
            for file in ('native_launch.json','service_execution.json','stderr.log')]]
    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}"""
    assert pub.count(before)==1;pub=pub.replace(before,after)
    monitor_source=A/'monitor_BF16wide135_progress_v2_20261008.py';monitor=monitor_source.read_text(encoding='utf8')
    monitor=monitor.replace('BF16wide135_complete_hidden_launches_v2_20261008','BF16wide135_complete_hidden_launches_v3_20261008')
    monitor=monitor.replace('actual_BF16wide135_progress_v2_20261008','actual_BF16wide135_progress_v3_20261008')
    archive_source=A/'archive_BF16wide135_completed_scoring_CSV_v2_20261008.py';archive=archive_source.read_text(encoding='utf8')
    for stem in ('BF16wide40_official_comparison','BF16wide40_selected_candidate_preparation'):
        archive=archive.replace(stem+'_v2_20261008',stem+'_v3_20261008')
    archive=archive.replace('scoring_CSV_archive_v2_20261008','scoring_CSV_archive_v3_20261008')
    files={A/'publish_actual_BF16wide135_receiver_preflight_v3_20261008.py':pub,
        A/'monitor_BF16wide135_progress_v3_20261008.py':monitor,A/'archive_BF16wide135_completed_scoring_CSV_v3_20261008.py':archive}
    for p,text in files.items():assert not p.exists();compile(text,str(p),'exec')
    for p,text in files.items():p.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual_BF16wide135_consistent_auxiliary_preparation_v3_20261008.json',{'status':'prepared_current3_progress_main_publication_and_closed_CSV_archival',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),pub_source,monitor_source,archive_source,*files]},'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
