"""Exercise Fourier-tuning portable full-model and both complete future branches without scores."""
from copy import deepcopy
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]


def main():
    gate=ROOT/'analysis/fourier_tuning_bank_20261004/oof_audit.json'
    while not gate.exists():time.sleep(10)
    import numpy as np
    import polars as pl
    import fourier_tuning_model_sources_20261004 as models
    import optimize_training_round47 as role_module
    import optimize_training_round48 as pure_module
    from predict_final_roles_round47 import predict as role_predict
    from predict_standalone_round48 import predict as pure_predict
    from run import FEATURE_FILE,feature_names,to_matrix
    models.verify();assert models.read(gate)['status']=='passed'
    name='rank_fourier_tuning_c512_mass128';models.train_one(name,2025)
    full=models.read(models.source_dir(name)/'info_2025.json')
    assert full['fulltraining_only_test_prediction_not_generated']
    assert full['training_meta']['last_label_end']<=full['training_meta']['cutoff_exclusive']
    qa=ROOT/'analysis/fourier_tuning_future_pipelines_qa_20261004';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    source=ROOT/'analysis/optimization_20261003_r24';name='rank_fourier_tuning_c512_mass128'
    original=models.read(source/'selection.json');role=deepcopy(original);pure=deepcopy(original)
    role['winner'].update(fourier_tuning_augmentation={
        'membership':{'model':name,'weight':.025},'top':{'model':name,'weight':.075},
        'rest':{'model':name,'weight':.15}},fourier_tuning_limit_delta=.02,connected_final_score=None)
    pure['winner'].update(standalone={'model':name,'postprocessing':dict(pure_module.BASE_POST,alpha=.9,weight=.25,bonus=.3)},
                         standalone_replacement=True,connected_final_score=None)
    inputs=[Path(__file__),ROOT/'analysis/predict_final_roles_round47.py',ROOT/'analysis/predict_standalone_round48.py',
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
    # Reload the copied self-contained raw-feature Fourier model.
    copied=qa/'standalone_candidate'/f'model_standalone_{name}.joblib'
    bundle=models.load_bundle(copied)
    assert bundle['kind']=='ridge_fourier' and len(bundle['mean'])==63 and len(bundle['coefficients'])==575
    features=feature_names()
    frame=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(['ts_code','trade_date']+features+['price_valid']).sort('trade_date','ts_code').collect()
    last=int(frame['trade_date'].unique().sort()[79]);prefix=frame.filter(pl.col('trade_date')<=last)
    dates=prefix['trade_date'].to_numpy();valid=prefix['price_valid'].to_numpy();x=to_matrix(prefix,features)
    embedded=models.predict_arrays(bundle,x,dates=dates,valid=valid)
    original_pred=models.predict_arrays(models.load_bundle(models.model_path(name,2025)),x,dates=dates,valid=valid)
    assert np.array_equal(embedded,original_pred)
    checks={}
    for branch in ('role_candidate','standalone_candidate'):
        result=models.read(qa/branch/'verification.json')
        assert result['status']=='passed' and result['rows']==1599600 and result['validation_score'] is None
        for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','csv_ranks_unchanged'):
            assert result[key]
        checks[branch]={'verification_sha256':models.sha(qa/branch/'verification.json'),
                       'csv_sha256':models.sha(qa/branch/'submission.csv'),'rows':result['rows']}
    models.dump(qa/'verification.json',{'status':'passed','branches':checks,
         'portable_raw_feature_bundle_replay_bit_identical':True,'basis_columns':575,'raw_features':63,
         'complete_first_80_future_days_prefix_rows':len(prefix),'new_model_scores':0,'test_labels_read':False,
         'past_mapping_used_for_implementation_control_only':True,
         'diagnostic_freeze_sha256':models.sha(qa/'diagnostic_frozen_before_inference.json'),
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Both Fourier-tuning future pipelines and portable575-column bundle passed; no test scores generated',flush=True)


if __name__=='__main__':main()
