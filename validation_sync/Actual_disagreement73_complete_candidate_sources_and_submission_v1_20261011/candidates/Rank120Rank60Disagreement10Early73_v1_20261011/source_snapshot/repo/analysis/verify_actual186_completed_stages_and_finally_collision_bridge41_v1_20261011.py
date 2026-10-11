"""Prove the real186 completion after fresh QA/main resume; never rewrite failed helpers."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed()
 source=A/'service_owned_workflows_20261006/actual186_registered_QA_main_resume39_v1_20261011'
 from run_dependency_queue_v3_20261006 import owned
 assert not owned(read(source/'native_launch.json'))
 failure=read(source/'service_execution.json')
 assert failure['status']=='failed' and 'FileExistsError' in failure['failure'] and 'actual_hidden_registration_children.json' in failure['failure']
 assert read(A/'lossless_ranking_display_qa_v97_20261010/round186/verification.json')['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'

 release=A/'optimization_20261003_r186';candidate=ROOT/'candidates/optimization_20261003_r186'
 receiptpath=A/'github_validation_sync_main_20261005/round186_receipt.json';receipt=read(receiptpath)
 terminal=read(release/'full_registration_execution.json');assert terminal['status']=='passed' and terminal['existing_official_scores_registered']==48
 assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main' and receipt['scored_records']==48 and receipt['connected_records']==17402
 selection=read(release/'selection.json');metrics=read(release/'calibrated_csv_official.json')['metrics'];assert selection['winner']['metrics']==metrics and receipt['official_score']==metrics['final_score']
 ready=read(A/'StockRank20Seed10Embedding186_selected_release_v1_20261010/inference_ready.json');assert not ready['new_inference_claimed'] and ready['selected_configuration']['anchor_round']==185
 report=read(candidate/'verification.json');assert report['status']=='passed' and not report['test_labels_read']
 assert (report['rows'],report['days'],report['codes'])==(1599600,344,4650)
 assert report['cold80_day_prefix_bit_identical'] and report['model_reload_bit_identical'] and report['csv_replay_byte_identical']
 assert sha(candidate/'submission.csv')==report['csv_sha256']==sha(Path(ready['source_candidate'])/'submission.csv')
 models=report['models'];assert len(models)==len({r['sha256'] for r in models.values()})==35
 for row in models.values():assert sha(row['path'])==row['sha256'],row['path']
 for row in selection['ranking']:
  cache=row['official_score_cache'];p=Path(cache['official_metrics_source']);key=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)
  frozen=selection['frozen_sha256'] if p.is_relative_to(ROOT) else selection['frozen_external_input_sha256'];assert sha(p)==frozen[key] and read(p)['metrics']==row['metrics']
 assert allowed()
 from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
 update()
 create(A/'actual186_completed_stages_and_finally_collision_bridge41_v1_20261011.json',{'status':'passed_actual186_48_QA97_main_and_registered_candidate_anchor183_rehashed','input_sha256':{str(p):sha(p) for p in [Path(__file__),receiptpath,release/'full_registration_execution.json',release/'selection.json',release/'calibrated_csv_official.json',candidate/'verification.json',candidate/'submission.csv']},'actual_receipt':receipt,'actual_rehashed_physical_models':35,'actual_rows_days_stocks':[1599600,344,4650],'actual48_capsules_checked':48,'new_scientific_scores':0,'new_inference_claimed':False,'old_failed_helpers_preserved':True,'test_labels_read':False})
 print({'actual186_complete_parent_verified':True,'main_commit':receipt['commit'],'new_fits_or_scores':0},flush=True)
if __name__=='__main__':main()
