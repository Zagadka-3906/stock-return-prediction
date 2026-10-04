"""Resume the failed standalone branch with prospectively frozen constant fixes."""
from copy import deepcopy
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]


def main():
    import numpy as np
    import polars as pl
    import expanded_stacking_model_sources_20261004 as models
    import optimize_training_round40 as pure_module
    from run_future_inference_recovered_pipeline_20261004 import install
    from run import FEATURE_FILE,feature_names,to_matrix
    models.verify();qa=ROOT/'analysis/expanded_stacking_future_pipelines_qa_20261004'
    assert not (qa/'verification.json').exists()
    frozen=models.read(qa/'diagnostic_frozen_before_inference.json')
    for path,digest in frozen['source_sha256'].items():assert models.sha(path)==digest,path
    assert models.read(qa/'role_candidate/verification.json')['status']=='passed'
    prepared=ROOT/'analysis/future_inference_recovery_sources_20261004.json'
    sources=[Path(__file__),ROOT/'analysis/run_future_inference_recovered_pipeline_20261004.py',prepared]
    # Prove the replacement is restricted to these two generated constants.
    import re
    records=models.read(prepared)['sources']
    for path,item in records.items():
        assert models.sha(path)==item['corrected_sha256'] and models.sha(item['original'])==item['original_sha256']
        text=Path(item['original']).read_text(encoding='utf-8')
        text=re.sub(r'connected_topk0\d+_20261003','connected_topk0175_20261003',text)
        text=re.sub(r'len\(parsed\)==\d+','len(parsed)==1599600',text)
        assert text==Path(path).read_text(encoding='utf-8'),path
        sources.extend([Path(path),Path(item['original'])])
    protocol=qa/'standalone_inference_recovery_protocol.json'
    models.dump(protocol,{'status':'frozen_before_recovered_future_inference',
        'original_diagnostic_freeze_sha256':models.sha(qa/'diagnostic_frozen_before_inference.json'),
        'role_candidate_reused_sha256':models.sha(qa/'role_candidate/verification.json'),
        'changes_restricted_to_delivery_path_and_row_assertion':True,'new_model_scores':0,'test_labels_read':False,
        'source_sha256':{str(p.resolve()):models.sha(p) for p in sources},
        'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    source=ROOT/'analysis/optimization_20261003_r24';pure=deepcopy(models.read(source/'selection.json'))
    pure['winner']=deepcopy(frozen['standalone_configuration']);pure_module.OUT=source
    helper=install('predict_standalone_round',40);helper.predict(pure,candidate_path=qa/'standalone_candidate')
    name=frozen['model'];alias=models.read(ROOT/'analysis/expanded_stacking_fulltraining_warmup_20261004.json')['paired_uniform_model']
    bundle=models.load_bundle(qa/'standalone_candidate'/f'model_standalone_{name}.joblib')
    assert len(bundle['member_bundles'])==55;del bundle['member_model_paths']
    features=feature_names()
    frame=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(['ts_code','trade_date']+features+['price_valid']).sort('trade_date','ts_code').collect()
    last=int(frame['trade_date'].unique().sort()[79]);prefix=frame.filter(pl.col('trade_date')<=last)
    x=to_matrix(prefix,features);dates=prefix['trade_date'].to_numpy();valid=prefix['price_valid'].to_numpy()
    original=models.predict_arrays(models.load_bundle(models.model_path(name,2025)),x,dates=dates,valid=valid)
    assert np.array_equal(original,models.predict_arrays(bundle,x,dates=dates,valid=valid))
    assert np.array_equal(original,models.predict_arrays(models.load_bundle(models.model_path(alias,2025)),x,dates=dates,valid=valid))
    checks={}
    for branch in ('role_candidate','standalone_candidate'):
        result=models.read(qa/branch/'verification.json')
        assert result['status']=='passed' and result['rows']==1599600 and result['validation_score'] is None
        for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','csv_ranks_unchanged'):assert result[key]
        checks[branch]={'verification_sha256':models.sha(qa/branch/'verification.json'),'csv_sha256':models.sha(qa/branch/'submission.csv'),'rows':result['rows']}
    proof={'status':'passed','branches':checks,'portable_bundle_without_child_paths_replay_bit_identical':True,
        'paired_full_training_inference_bit_identical':True,'embedded_children':55,'complete_first_80_future_days_prefix_rows':len(prefix),
        'new_model_scores':0,'test_labels_read':False,'past_mapping_used_for_implementation_control_only':True,
        'diagnostic_freeze_sha256':models.sha(qa/'diagnostic_frozen_before_inference.json'),
        'recovery_protocol_sha256':models.sha(protocol),'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
    models.dump(qa/'verification.json',proof,immutable=True)
    destination=ROOT/'analysis/future_inference_recovery_20261004';destination.mkdir(exist_ok=True)
    models.dump(destination/'verification.json',{'status':'passed','prospective_rounds':[36,38,40],
        'changes_restricted_to_delivery_path_and_row_assertion':True,'forecast_scoring_and_selection_algorithms_unchanged':True,
        'complete_standalone_and_role1599600_row_replay_passed':True,'new_model_scores':0,'test_labels_read':False,
        'source_sha256':{str(p.resolve()):models.sha(p) for p in [*sources,qa/'verification.json',protocol]},
        'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Recovered55-child role/standalone future QA passed; future-only constant repairs ready for36/38/40.',flush=True)


if __name__=='__main__':main()
