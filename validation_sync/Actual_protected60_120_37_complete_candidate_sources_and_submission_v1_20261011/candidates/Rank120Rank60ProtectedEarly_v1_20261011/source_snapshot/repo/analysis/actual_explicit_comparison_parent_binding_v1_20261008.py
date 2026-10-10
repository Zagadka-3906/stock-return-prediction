"""Bind report-only PREVIOUS to the already frozen comparison parent; never alter sources or forecasts."""
from pathlib import Path
import importlib,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
def bind(number,proof_path):
 from run_dependency_queue_v3_20261006 import read,sha,create
 module=importlib.import_module(f'optimize_training_round{number}')
 folder=A/f'optimization_20261003_r{number}';protocol=read(folder/'protocol.json');selection=read(folder/'selection.json')
 parent=protocol['explicit_parent_round'];assert module.PREVIOUS_NUMBER==parent==selection['explicit_comparison_parent_round']
 target=A/f'optimization_20261003_r{parent}';baseline=read(target/'selection.json')['winner']['metrics']
 assert baseline['final_score']==selection['baseline_score']
 winner=selection['winner']['metrics'];expected=.4*(winner['ic_mean']-baseline['ic_mean'])+.3*(winner['annual_excess']-baseline['annual_excess'])-.3*(winner['mean_turnover']-baseline['mean_turnover'])
 assert abs(expected-selection['score_gain'])<1e-12
 source=Path(module.__file__);digest=sha(source);previous=module.PREVIOUS
 create(proof_path,{'status':'bound_report_only_previous_path_to_original_frozen_explicit_comparison_parent_without_source_or_prediction_changes',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':number,'actual_comparison_parent':parent,'original_module_PREVIOUS_path':str(previous),
  'actual_report_previous_path':str(target),'original_module_source_sha256':digest,'selection_sha256':sha(folder/'selection.json'),
  'original_frozen_prediction_sha256':sha(folder/'selected_validation.npy'),'official_contribution_sum':expected,'original_frozen_gain':selection['score_gain'],
  'original_source_files_and_freeze_and_all_scores_unchanged':True,'new_quality_scores':0,'new_inference':0,'test_labels_read':False})
 module.PREVIOUS=target
 assert sha(source)==digest
 return module
