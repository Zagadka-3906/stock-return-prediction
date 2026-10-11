from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
from run_protected167_complete_family_v1_20261010 import junction
def dispatch(name,driver):
 assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(A/'rank60_two_seed_protected37_early_sources_admission_v2_20261011.json'):sha(A/'rank60_two_seed_protected37_early_sources_admission_v2_20261011.json')})
 create(A/(name+'_activation.json'),r);closed(name)
def main():
 closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')
 assert allowed();closed('recovery59_actual_rank60_two_seed_after183_protected37_screen_v1_20261011')
 jobs=[('actual_rank60_two_seed_protected37_early_normalization_v1_20261011', 'normalize_rank60_two_seed_protected37_early_v1_20261011.py'), ('actual_rank60_two_seed_protected37_early_selected_native14_v1_20261011', 'qualify_rank60_two_seed_protected37_early_selected_native14_v2_20261011.py'), ('Rank60TwoSeedProtected37Early_selected_candidate_preparation_v1_20261011', 'run_Rank60TwoSeedProtected37Early_selected_candidate_feature_cache_v2_20261011.py'), ('Rank60TwoSeedProtected37Early_selected_candidate_sealing_v1_20261011', 'seal_Rank60TwoSeedProtected37Early_selected_candidate_v2_20261011.py')];dispatch(*jobs[0]);pilot=read(Path(read(A/'actual_rank60_two_seed_protected37_early_normalized_location_v1_20261011.json')['output'])/'pilot37.json')
 best=pilot['best'];references=[]
 for p in sorted(A.glob('alternate_verified_*submission_delivery_v1_20261011.json')):
  v=read(p)
  if v.get('all_full_native_independent_reload_csv_and_cold80_checks_passed') and v.get('actual_main_commit'):
   references.append({'pointer':str(p),'sha256':sha(p),'S':v['official_TRAIN_internal_score']})
 assert references;incumbent=max(r['S'] for r in references);adopt=best['connected_final_score']>incumbent
 create(A/'rank60_two_seed_protected37_early_gain_decision_v1_20261011.json',{'status':'actual_all_source_TRAIN_scores_vs_current_completed_candidate_S_only','adopt':adopt,'best':best,'incumbent_S':incumbent,'references':references,'test_labels_read':False})
 if not adopt:
  print('All official records retained; selected S below completed candidate, no full inference.',flush=True);return
 storage=importlib.import_module('rank60_two_seed_protected37_early_storage_v1_20261011')
 for logical,physical in storage.OUTPUTS.items():
  assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
 for job in jobs[1:]:dispatch(*job)
 print('Actual gaining ensemble full37-model candidate sealed; main/delivery still required.',flush=True)
if __name__=='__main__':main()
