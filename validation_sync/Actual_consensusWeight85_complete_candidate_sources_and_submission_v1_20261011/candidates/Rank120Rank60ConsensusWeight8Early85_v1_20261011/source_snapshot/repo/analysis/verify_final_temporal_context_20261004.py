"""Check R49's compact context, unchanged official baseline and actual inference helper."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
OUT=ROOT/'analysis/final_temporal_context_preflight_20261004'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def dump(path,value):
    assert not path.exists();path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    import numpy as np
    import optimize_training_round49 as module
    from predict_temporal_round49 import predict
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    source=ROOT/'analysis/optimization_20261003_r25';record=read(source/'selection.json');cfg=deepcopy(record['winner'])
    for field in module.FIELDS:
        if field in cfg:continue
        if field.endswith('_augmentation'):cfg[field]={r:{'model':'none','weight':0.} for r in ('membership','top','rest')}
        elif field.endswith('_limit_delta'):cfg[field]=0.
        elif field=='standalone':cfg[field]=None
        elif field=='standalone_replacement':cfg[field]=False
        elif field=='temporal_postprocessing':cfg[field]=deepcopy(module.IDENTITY)
        else:raise AssertionError(field)
    inputs=[Path(__file__),ROOT/'analysis/optimize_training_round49.py',ROOT/'analysis/finalize_training_round49.py',
        ROOT/'analysis/predict_temporal_round49.py',ROOT/'analysis/verify_methods_round49.py',ROOT/'analysis/run_training_round49_pipeline.py',
        source/'selection.json',source/'selected_validation.npy',source/'future_return_mapping.json',
        ROOT/'analysis/final_output_temporal_preflight_20261004/verification.json',ROOT/'analysis/final_output_temporal_future_qa_20261004/verification.json',
        ROOT/'candidates/optimization_20261003_r25/verification.json']
    dump(OUT/'frozen_before_controls.json',{'status':'frozen_implementation_control','source_sha256':{str(p.resolve()):sha(p) for p in inputs},
        'known_complete_baseline_used_only_as_control':True,'new_model_selection':False,'test_labels_read':False,
        'frozen_at_local':datetime.now().isoformat(timespec='seconds')})
    module.OUT=OUT;module.PREVIOUS=source;module.baseline=lambda:deepcopy(cfg)
    ctx=module.Context();raw=ctx.finished('baseline');pred=ctx.predict(raw,0.,0.)[0]
    assert np.array_equal(pred,np.load(source/'selected_validation.npy'))
    metrics=ctx.score(pred);assert metrics==record['winner']['metrics']
    controls=[]
    for p in ({'alpha':.5,'mix':.25,'power':.5},{'alpha':.9,'mix':.1,'power':1.},{'alpha':.995,'mix':.025,'power':2.}):
        test={**deepcopy(cfg),'temporal_postprocessing':p};controls.append(module.prefix_controls(ctx,test))
    # The actual helper uses fixedR25 forecasts and mapping only as implementation controls.
    module.OUT=source;prototype=deepcopy(record)
    prototype['winner'].update(temporal_postprocessing={'alpha':.9,'mix':.1,'power':1.},connected_final_score=None)
    predict(prototype,candidate_path=OUT/'future_candidate')
    future=read(OUT/'future_candidate/verification.json')
    assert future['status']=='passed' and future['rows']==1599600 and future['validation_score'] is None
    dump(OUT/'verification.json',{'status':'passed','verified_at_local':datetime.now().isoformat(timespec='seconds'),
        'all_eight_known_baseline_official_metrics_bit_identical':True,'official_baseline_metrics':metrics,
        'known_baseline_official_cache_provenance':ctx.last_official_score_cache,'actual_compact_context_controls':controls,
        'actual_future_helper_1599600_rows_passed':True,'future_candidate_verification_sha256':sha(OUT/'future_candidate/verification.json'),
        'no_new_model_quality_score':True,'test_labels_read':False,'frozen_controls_sha256':sha(OUT/'frozen_before_controls.json')})
    print('R49 compact context, all8 known official baseline metrics andactual future helper passed.',flush=True)


if __name__=='__main__':main()
