"""Freeze independent membership and TopK recipe, then replay calibrated test-X inference."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round30 as experiment
from optimize_training_round30 import OUT,PREVIOUS,expected,WAVES,RANKERS,FIELDS,MODELS,NEW_MODELS,best,Context,HERE,ARCHIVE,KEYS,BASE_POST,read,dump,sha,log,verify
import finalize_training_round7 as shared
EXPECTED=expected()
CANDIDATE=ROOT/'candidates/optimization_20261003_r30'
FORMAL=ROOT/'deliveries/connected_topk0175_20261003'


def selected():
    verify();record=read(OUT/'selection.json')
    for name,digest in record['frozen_sha256'].items():assert sha(ROOT/name)==digest,name
    return record


def select():
    import numpy as np
    verify()
    if (OUT/'selection.json').exists():selected();return
    rows=[]
    for wave in WAVES:
        payload=read(OUT/f'wave{wave}_results.json');assert payload['status']=='complete'
        rows.extend(dict(wave=wave,arm=name,**row) for name,row in payload['results'].items())
    winner=best(rows)
    rows.sort(key=lambda r:(-r['connected_final_score'],r['wave'],r['arm']));assert winner['connected_final_score']>=EXPECTED
    ctx=ReleaseContext(winner);promote=ctx.finished('baseline',winner['recipe'])
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    metrics=ctx.score(pred);assert abs(metrics['final_score']-winner['connected_final_score'])<1e-12
    np.save(OUT/'selected_validation.npy',pred);np.save(OUT/'promote_baseline.npy',promote)
    paths=[Path(__file__),OUT/'protocol.json',OUT/'component_audit.json',
           *[OUT/f'wave{wave}_results.json' for wave in WAVES],
           *sorted(OUT.glob('coordinate_*_protocol.json')),*sorted(OUT.glob('output_*_protocol.json')),
           OUT/'selected_validation.npy',OUT/'promote_baseline.npy',PREVIOUS/'selection.json',
           ROOT/'active_release.json',FORMAL/'generation_inputs.parquet',
           ROOT/'candidates/optimization_20261003_r29/verification.json']
    paths.extend(Path(row['official_score_cache']['official_metrics_source']) for row in rows if 'official_score_cache' in row)
    dump(OUT/'selection.json',{'status':'frozen_before_test_prediction','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'winner':winner,'ranking':rows,'scored_records':len(rows),'baseline_score':EXPECTED,
         'score_gain':winner['connected_final_score']-EXPECTED,'pruned_member_excluded':True,
         'fold_local_pruning_repaired':True,'test_labels_read':False,
         'selection_rule':'highest official connected composite; exact ties prefer fewer model families and role ensembles',
         'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(paths)}},immutable=True)
    log(f'Round30 selected {winner["arm"]}: {metrics["final_score"]:.9f}, gain={winner["connected_final_score"]-EXPECTED:+.9f}')


class ReleaseContext(Context):
    def __init__(self,winner=None):
        super().__init__();winner=winner or selected()['winner']
        self.configure(winner);self.recipe=winner['recipe']
    def promote(self,name):return self.finished(name,self.recipe)


def calibrate():
    shared.OUT=OUT;shared.selected=selected;shared.ReleaseContext=ReleaseContext;shared.verify=verify
    shared.calibrate()


def predict():
    record=selected()
    assert read(OUT/'causal_validation.json')['status']==read(OUT/'calibrated_csv_official.json')['status']=='passed'
    if (CANDIDATE/'verification.json').exists():assert sha(CANDIDATE/'submission.csv')==read(CANDIDATE/'verification.json')['csv_sha256'];return
    from predict_complete_scheme_round30 import predict as generate
    generate(record)


def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('select','calibrate','predict'))
    globals()[parser.parse_args().stage]()


if __name__=='__main__':main()
