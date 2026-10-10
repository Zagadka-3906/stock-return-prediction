from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    fixed=A/'stock_rank60_fixed_case17_decay_none_recovery_v2_20261011.json'
    controls=[A/'shared_live_ranking_report_actual180_controls_v1_20261011.json',A/'shared_live_ranking_report_scope_controls_v1_20261011.json']
    assert read(controls[0])['status']=='passed_actual180_native_bytes_typed_graph_and_private_reader_controls'
    assert read(controls[1])['status']=='passed_actual_installed_scope_small_E_fixture_bindings_and_restoration'
    for p in [fixed,*controls]:
        for source,d in read(p)['input_sha256'].items():assert sha(source)==d,source
    score=Path('E:/赛题五_本机临时/StockRank60EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011/case017_official.json')
    row=read(score);assert row['connected_final_score']==0.4514355480841008
    services=[]
    for name in ['actual186_registered_QA_main_resume39_v1_20261011','actual_stock_rank60_fixed_leading_case17_native14_v2_20261011','actual_shared_report_controls_and_fixed60_case17_main_v2_20261011']:
        f=A/'service_owned_workflows_20261006'/name;identity=read(f/'native_launch.json')
        services.append({'name':name,'identity':identity,'actual_owned_live':owned(identity),
          'terminal':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None})
    qa=A/'lossless_ranking_display_qa_v97_20261010/round186/verification.json'
    assert read(qa)['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    paths=[Path(__file__),fixed,*controls,score,qa]
    create(A/'actual_rank60_gain_reader_controls_and_early_native_handoff_v233_20261011.json',
      {'status':'actual_new_scored_gain_two_reader_controls_and_full186_browser_QA_passed_early_native_v2_live',
       'at_local':datetime.now().astimezone().isoformat(),'deadline':'2026-10-11T13:00:00+08:00',
       'input_sha256':{str(p):sha(p) for p in paths},'services':services,
       'progress_snapshot':read(A/'optimization_live_progress_v121_20261011.json'),
       'fixed_case17_S':row['connected_final_score'],'gain_over_delivered183':row['score_gain_over_qualified_parent'],
       'fixed_case_configuration':row['configuration'],'candidate_future_full_graph_not_yet_qualified':True,
       'new_native14_checks_reuse_six_actual_saved_states':True,
       'prototype_v1_failed_missing_decay_preserved_v2_explicit_none':True,
       'completed_reader_controls_main_publication_queued_with_actual_fixed_case_native14':True,
       'reader_runtime_not_yet_adopted_existing_frozen_jobs_not_modified':True,
       'next':['finish actual186 main and bridge40; preserve actual current identities',
        'inspect actual direct33 winner after completion; leading fixed17 probes do not establish search winner',
        'finish mixed49 and H120 sixth year/full5/native42/direct33',
        'only adopt report reader in newly admitted exact-version scope, preserving all original QA',
        'complete best actual full candidate and full ranking/main before replacing delivered183'],
       'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    print({'actual_handoff233_saved':True},flush=True)

if __name__=='__main__':main()
