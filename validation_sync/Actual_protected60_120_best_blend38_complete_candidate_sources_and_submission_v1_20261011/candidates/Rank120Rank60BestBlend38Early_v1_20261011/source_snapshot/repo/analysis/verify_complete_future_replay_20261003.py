"""Freeze a compatibility diagnostic, then reproduce the already selected R18 candidate."""
from pathlib import Path
import sys
import time
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import optimize_training_round30 as prospective
from replay_complete_scheme_20261003 import empty_roles
from predict_complete_scheme_round30 import predict


def main():
    qa=ROOT/'analysis/complete_scheme_future_replay_qa_20261003';qa.mkdir(exist_ok=True)
    target=qa/'verification.json';assert not target.exists()
    source=ROOT/'analysis/optimization_20261003_r18'
    record=prospective.read(source/'selection.json');record=deepcopy(record)
    record['winner'].update(standalone=None,standalone_replacement=False,
         secondary_augmentation=empty_roles(),final_augmentation=empty_roles(),final_limit_delta=0.,
         linear_augmentation=empty_roles(),linear_limit_delta=0.)
    # This is solely an implementation control using the earlier training-selected recipe.
    prospective.dump(qa/'diagnostic_frozen_before_inference.json',{'status':'frozen_implementation_control',
         'winner':record['winner'],'original_selection_sha256':prospective.sha(source/'selection.json'),
         'test_labels_read':False,'new_model_selection':False,
         'source_sha256':{str(path.resolve()):prospective.sha(path) for path in (
             Path(__file__),ROOT/'analysis/predict_complete_scheme_round30.py',
             ROOT/'analysis/replay_complete_scheme_20261003.py',ROOT/'analysis/optimize_training_round30.py')},
         'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    prospective.OUT=source;prospective.PREVIOUS=source
    predict(record,candidate_path=qa/'candidate')
    original=ROOT/'candidates/optimization_20261003_r18'
    assert np.array_equal(np.load(qa/'candidate/rank_prediction.npy'),np.load(original/'rank_prediction.npy'))
    assert prospective.sha(qa/'candidate/submission.csv')==prospective.sha(original/'submission.csv')
    verification=prospective.read(qa/'candidate/verification.json')
    prospective.dump(target,{'status':'passed','all1599600_future_rows_rank_bit_identical':True,
         'actual_one_day_return_csv_byte_identical':True,'old_selected_validation_recipe_only':True,
         'frozen_before_inference_sha256':prospective.sha(qa/'diagnostic_frozen_before_inference.json'),
         'prediction_verification_sha256':prospective.sha(qa/'candidate/verification.json'),
         'frozen_original_candidate_sha256':prospective.sha(original/'verification.json'),
         'new_model_scores':0,'test_labels_read':False,
         'test_X_used_only_to_verify_prediction_implementation':True,
         'formal_delivery_pointer_unchanged':verification['old_delivery_pointer_unchanged'],
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Full frozen future inference and emitted CSV reproduced byte-identically.',flush=True)


if __name__=='__main__':main()
