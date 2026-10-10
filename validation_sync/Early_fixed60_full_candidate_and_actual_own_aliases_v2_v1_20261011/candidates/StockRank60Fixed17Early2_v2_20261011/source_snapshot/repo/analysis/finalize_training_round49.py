"""Freeze the final temporal scheme, calibrate past returns, then infer the candidate."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import optimize_training_round49 as experiment
from optimize_training_round49 import OUT,PREVIOUS,WAVES,Context,read,dump,sha,log,verify,best,expected


def selected():
    verify();record=read(OUT/'selection.json')
    for path,digest in record['frozen_sha256'].items():assert sha(ROOT/path)==digest,path
    return record


class ReleaseContext(Context):
    def __init__(self,winner=None):super().__init__();self.configure(winner or selected()['winner'])


def select():
    import numpy as np
    import time
    verify()
    if (OUT/'selection.json').exists():selected();return
    rows=[]
    for wave in WAVES:
        payload=read(OUT/f'wave{wave}_results.json');assert payload['status']=='complete'
        rows.extend(dict(wave=wave,arm=key,**row) for key,row in payload['results'].items())
    winner=best(rows);assert winner['connected_final_score']>=expected()
    ctx=ReleaseContext(winner);promote=ctx.finished('baseline');pred,_=ctx.predict(promote,0.,0.)
    metrics=ctx.score(pred);assert metrics==winner['metrics']
    np.save(OUT/'selected_validation.npy',pred);np.save(OUT/'promote_baseline.npy',promote)
    paths=[Path(__file__),OUT/'protocol.json',OUT/'component_audit.json',OUT/'refinement_protocol.json',OUT/'power_refinement_protocol.json',
        *[OUT/f'wave{w}_results.json' for w in WAVES],OUT/'selected_validation.npy',OUT/'promote_baseline.npy',
        PREVIOUS/'selection.json',ROOT/'active_release.json',ROOT/'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT/'candidates/optimization_20261003_r48/verification.json']
    paths.extend(Path(r['official_score_cache']['official_metrics_source']) for r in rows)
    dump(OUT/'selection.json',{'status':'frozen_before_test_prediction','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'winner':winner,'ranking':sorted(rows,key=lambda r:(-r['connected_final_score'],r['wave'],r['arm'])),
        'scored_records':len(rows),'baseline_score':expected(),'score_gain':winner['connected_final_score']-expected(),
        'pruned_member_excluded':True,'fold_local_pruning_repaired':True,'test_labels_read':False,
        'selection_rule':'highest official complete connected composite; exact ties prefer temporal identity',
        'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(paths)}},immutable=True)
    log(f'Round49 selected {winner["arm"]}: {winner["connected_final_score"]:.9f}')


def calibrate():
    import finalize_training_round7 as shared
    shared.OUT=OUT;shared.selected=selected;shared.ReleaseContext=ReleaseContext;shared.verify=verify;shared.calibrate()


def predict():
    assert read(OUT/'causal_validation.json')['status']==read(OUT/'calibrated_csv_official.json')['status']=='passed'
    from predict_temporal_round49 import predict as infer
    infer(selected())
