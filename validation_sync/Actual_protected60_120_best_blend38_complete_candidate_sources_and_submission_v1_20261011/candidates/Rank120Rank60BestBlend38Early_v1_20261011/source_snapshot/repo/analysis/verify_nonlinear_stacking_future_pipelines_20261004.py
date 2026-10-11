"""Exercise portable full-model and both complete future branches, without scores."""
from copy import deepcopy
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]


def main():
    gate=ROOT/'analysis/nonlinear_stacking_fulltraining_warmup_20261004.json'
    while not gate.exists():time.sleep(10)
    import numpy as np
    import polars as pl
    import nonlinear_stacking_model_sources_20261004 as models
    import optimize_training_round45 as role_module
    import optimize_training_round46 as pure_module
    from predict_final_roles_round45 import predict as role_predict
    from predict_standalone_round46 import predict as pure_predict
    from run import FEATURE_FILE,feature_names,to_matrix
    models.verify();assert models.read(gate)['status']=='passed'
    qa=ROOT/'analysis/nonlinear_stacking_future_pipelines_qa_20261004';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    source=ROOT/'analysis/optimization_20261003_r24';name=next(iter(models.NEW_CONFIGS))
    original=models.read(source/'selection.json');role=deepcopy(original);pure=deepcopy(original)
    role['winner'].update(nonlinear_stacking_augmentation={
        'membership':{'model':name,'weight':.025},'top':{'model':name,'weight':.075},
        'rest':{'model':name,'weight':.15}},nonlinear_stacking_limit_delta=.02,connected_final_score=None)
    pure['winner'].update(standalone={'model':name,'postprocessing':dict(pure_module.BASE_POST,alpha=.9,weight=.25,bonus=.3)},
                         standalone_replacement=True,connected_final_score=None)
    inputs=[Path(__file__),ROOT/'analysis/predict_final_roles_round45.py',ROOT/'analysis/predict_standalone_round46.py',
            Path(models.__file__),ROOT/'analysis/causal_model_loading_20261004.py',
            models.bank.OUT/'protocol.json',models.model_path(name,2025),
            models.source_dir(name)/'info_2025.json',source/'selection.json',source/'future_return_mapping.json',
            ROOT/'candidates/optimization_20261003_r24/verification.json']
    models.dump(qa/'diagnostic_frozen_before_inference.json',{'status':'frozen_implementation_control',
         'role_configuration':role['winner'],'standalone_configuration':pure['winner'],'model':name,
         'new_model_selection':False,'official_scores_generated':0,'test_labels_read':False,
         'past_mapping_used_as_fixed_monotone_implementation_control_only':True,
         'source_sha256':{str(p.resolve()):models.sha(p) for p in inputs},
         'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    role_module.OUT=source;role_module.FOUNDATION=source;pure_module.OUT=source
    role_predict(role,candidate_path=qa/'role_candidate')
    pure_predict(pure,candidate_path=qa/'standalone_candidate')
    # Paired first-year policies reuse identical full-training coefficients and child bundles.
    alias=models.read(gate)['paired_uniform_model']
    paired=models.train_one(alias,2025);assert paired['new_model_fits']==0
    # Load the copied, embedded bundle directly; no annual child path is available to it.
    copied=qa/'standalone_candidate'/f'model_standalone_{name}.joblib'
    bundle=models.load_bundle(copied)
    assert len(bundle['member_bundles'])==67
    del bundle['member_model_paths']
    features=feature_names()
    frame=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(['ts_code','trade_date']+features+['price_valid']).sort('trade_date','ts_code').collect()
    last=int(frame['trade_date'].unique().sort()[79]);prefix=frame.filter(pl.col('trade_date')<=last)
    dates=prefix['trade_date'].to_numpy();valid=prefix['price_valid'].to_numpy();x=to_matrix(prefix,features)
    embedded=models.predict_arrays(bundle,x,dates=dates,valid=valid)
    original_pred=models.predict_arrays(models.load_bundle(models.model_path(name,2025)),x,dates=dates,valid=valid)
    assert np.array_equal(embedded,original_pred)
    alias_pred=models.predict_arrays(models.load_bundle(models.model_path(alias,2025)),x,dates=dates,valid=valid)
    assert np.array_equal(original_pred,alias_pred)
    checks={}
    for branch in ('role_candidate','standalone_candidate'):
        result=models.read(qa/branch/'verification.json')
        assert result['status']=='passed' and result['rows']==1599600 and result['validation_score'] is None
        for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','csv_ranks_unchanged'):
            assert result[key]
        checks[branch]={'verification_sha256':models.sha(qa/branch/'verification.json'),
                       'csv_sha256':models.sha(qa/branch/'submission.csv'),'rows':result['rows']}
    models.dump(qa/'verification.json',{'status':'passed','branches':checks,
         'portable_bundle_without_child_paths_replay_bit_identical':True,'paired_full_training_inference_bit_identical':True,'embedded_children':67,
         'complete_first_80_future_days_prefix_rows':len(prefix),'new_model_scores':0,'test_labels_read':False,
         'past_mapping_used_for_implementation_control_only':True,
         'diagnostic_freeze_sha256':models.sha(qa/'diagnostic_frozen_before_inference.json'),
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Both stacking future pipelines and portable67-child bundle passed; no test scores generated',flush=True)


if __name__=='__main__':main()
