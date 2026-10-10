"""Record actual current handles and staged performance controls without adoption claims."""
from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    names=['actual186_registered_QA_main_resume39_v1_20261011',
      'actual_stock_rank120_embedding_small512_bank6_v1_20261011',
      'actual_shared_live_ranking_report180_reader_controls_v1_20261011',
      'actual_shared_live_ranking_report_scope_controls_v1_20261011',
      'actual_stock_rank120_direct_embedding35_after200_normalization_queue_v7_20261011',
      'StockRank120DirectEmbedding35_selected_native14_v7_20261011',
      'StockRank120DirectEmbedding201_complete35_family_v7_20261011']
    rows=[]
    for name in names:
        f=A/'service_owned_workflows_20261006'/name
        identity=read(f/'native_launch.json')
        rows.append({'name':name,'actual_verified_owned_live':owned(identity),
          'identity':identity,'terminal':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None})
    sources=[Path(__file__),A/'shared_live_ranking_report_runtime_v1_20261011.py',
      A/'verify_shared_live_ranking_report_actual180_v1_20261011.py',
      A/'verify_shared_live_ranking_report_scope_controls_v1_20261011.py',
      A/'stock_rank120_direct201_complete35_sources_admission_v7_20261011.json']
    progress=read(A/'optimization_live_progress_v121_20261011.json')
    create(A/'actual_shared_live_report_controls_and_scientific_progress_handoff_v232_20261011.json',
      {'status':'actual_new_reader_controls_staged_existing_scientific_jobs_kept_live',
       'at_local':datetime.now().astimezone().isoformat(),'stop_at_local':'2026-10-11T13:00:00+08:00',
       'input_sha256':{str(p):sha(p) for p in sources},'actual_services':rows,
       'progress_snapshot':progress,'prior_turn_classification':'verified_wait_actual_owned_model_and_score_handles',
       'this_turn_progress':'created_scoped_live_report_reader_and_launched_real_full180_byte_and_scope_controls',
       'scientific_workers_stopped_or_restarted':0,
       'report_reader_not_yet_adopted':True,
       'required_before_adoption':['actual_shared_live_ranking_report180_reader_controls_v1_20261011 terminal passed',
          'actual_shared_live_ranking_report_scope_controls_v1_20261011 terminal passed',
          'verify exact upcoming codec/version routing and pins; immutable existing drivers must not be edited',
          'preserve original full codec/native SHA/browser45sec assertions for actual adopted round'],
       'model_or_score_or_delivery_completion_not_claimed_by_this_handoff':True,
       'next_actions':['finish actual186 browser QA and main; do not restart live644',
          'finish pure60 and mixed20/60 official scans and all H120 annuals/native/33 scores',
          'extend observer range to include already queued201 when safely replacing observer',
          'publish every completed validation on main; qualify best new candidate before delivery'],
       'global_goal_or_resource_exhaustion_claimed':False,'test_labels_read':False})
    print({'handoff232_saved':True,'actual_live_services':sum(r['actual_verified_owned_live'] for r in rows)},flush=True)

if __name__=='__main__':main()
