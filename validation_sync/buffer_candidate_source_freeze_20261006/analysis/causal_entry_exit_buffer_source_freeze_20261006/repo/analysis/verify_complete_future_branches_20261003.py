"""Freeze and exercise standalone, macro and linear inference without test scoring."""
from pathlib import Path
import sys
import time
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import optimize_training_round30 as m
from replay_complete_scheme_20261003 import empty_roles
from predict_complete_scheme_round30 import predict


def main():
    qa=ROOT/'analysis/complete_scheme_future_branches_qa_20261003';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    source=ROOT/'analysis/optimization_20261003_r18'
    record=deepcopy(m.read(source/'selection.json'));winner=record['winner']
    winner.update(standalone={'model':'rank512_e32','postprocessing':dict(m.BASE_POST,alpha=.9,weight=.25,bonus=.3)},
         standalone_replacement=True,diverse_augmentation=empty_roles(),secondary_augmentation=empty_roles(),
         final_augmentation=empty_roles(),final_limit_delta=.02,linear_augmentation=empty_roles(),linear_limit_delta=-.01)
    winner['final_augmentation']['top']={'model':'pair_rank128_e32','weight':.075,'regime':'abs_return','low':0.,'high':.075}
    winner['linear_augmentation']['membership']={'model':'rank_ridge_l01','weight':.025}
    m.dump(qa/'diagnostic_frozen_before_inference.json',{'status':'frozen_branch_implementation_control',
         'configuration':m.configuration(winner),'original_selection_sha256':m.sha(source/'selection.json'),
         'new_model_selection':False,'official_scores_generated':0,'test_labels_read':False,
         'past_return_mapping_used_as_fixed_monotone_implementation_control_only':True,
         'source_sha256':{str(path.resolve()):m.sha(path) for path in (Path(__file__),
              ROOT/'analysis/predict_complete_scheme_round30.py',ROOT/'analysis/replay_complete_scheme_20261003.py')},
         'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    m.OUT=source;m.PREVIOUS=source
    predict(record,candidate_path=qa/'candidate')
    verification=m.read(qa/'candidate/verification.json');rank=np.load(qa/'candidate/rank_prediction.npy')
    assert len(rank)==1599600 and np.isfinite(rank).all()
    assert verification['model_reload_bit_identical'] and verification['pipeline_replay_bit_identical']
    assert verification['csv_ranks_unchanged'] and verification['csv_replay_byte_identical']
    m.dump(qa/'verification.json',{'status':'passed','full_future_rows':len(rank),
         'standalone_macro_and_linear_branches_active_together':True,
         'return_mapping_for_implementation_control_not_a_selected_model':True,
         'all_prediction_and_csv_replay_checks_passed':True,
         'diagnostic_freeze_sha256':m.sha(qa/'diagnostic_frozen_before_inference.json'),
         'candidate_verification_sha256':m.sha(qa/'candidate/verification.json'),
         'new_annual_oof_fits':0,'new_model_scores':0,'test_labels_read':False,
         'formal_delivery_pointer_unchanged':verification['old_delivery_pointer_unchanged'],
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Standalone, market-state and linear future branches replayed successfully.',flush=True)


if __name__=='__main__':main()
