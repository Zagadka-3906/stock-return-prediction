"""Freeze R8, calibrate using past labels, replay saved-model test-X inference."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round8 as experiment
from optimize_training_round8 import OUT,PREVIOUS,EXPECTED,WAVES,Context,read,dump,sha,log,verify
import finalize_training_round7 as shared
CANDIDATE=ROOT/'candidates/optimization_20261003_r8'


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
    rows.sort(key=lambda r:(-r['connected_final_score'],len(r['ensemble_weights']),r['wave'],r['arm']))
    winner=rows[0];assert winner['connected_final_score']>=EXPECTED
    ctx=Context();ctx.install(winner['ensemble_name'])
    promote=ctx.finished('baseline',winner['recipe'])
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    metrics=ctx.score(pred);assert abs(metrics['final_score']-winner['connected_final_score'])<1e-12
    np.save(OUT/'selected_validation.npy',pred);np.save(OUT/'promote_baseline.npy',promote)
    paths=[Path(__file__),OUT/'protocol.json',OUT/'component_audit.json',OUT/'fine_protocol.json',OUT/'donor_protocol.json',
           *[OUT/f'wave{wave}_results.json' for wave in WAVES],OUT/'selected_validation.npy',OUT/'promote_baseline.npy',
           OUT/f'rankers/{winner["ensemble_name"]}.npy',PREVIOUS/'selection.json',ROOT/'active_release.json',
           ROOT/'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
           ROOT/'candidates/optimization_20261003_r7/verification.json']
    dump(OUT/'selection.json',{'status':'frozen_before_test_prediction','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'winner':winner,'ranking':rows,'scored_records':len(rows),'baseline_score':EXPECTED,
         'score_gain':winner['connected_final_score']-EXPECTED,'pruned_member_excluded':True,
         'fold_local_pruning_repaired':True,'test_labels_read':False,
         'selection_rule':'highest official connected composite; exact ties prefer fewer members',
         'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in paths}},immutable=True)
    log(f'Round8 selected {winner["arm"]}: {metrics["final_score"]:.9f}, gain={winner["connected_final_score"]-EXPECTED:+.9f}')


class ReleaseContext(Context):
    def __init__(self):
        super().__init__();self.install(selected()['winner']['ensemble_name'])
    def promote(self,name):return self.finished(name,selected()['winner']['recipe'])


def configure_shared():
    winner=selected()['winner']
    shared.OUT=OUT;shared.PREVIOUS=PREVIOUS;shared.CANDIDATE=CANDIDATE
    shared.experiment=experiment;shared.verify=verify;shared.selected=selected;shared.ReleaseContext=ReleaseContext
    shared.ENSEMBLES={'five_fold_local':experiment.previous.ENSEMBLES['five_fold_local'],
                      winner['ensemble_name']:winner['ensemble_weights']}
    shared.log=lambda message:log(message.replace('Round7','Round8'))


def calibrate():configure_shared();shared.calibrate()


def predict():configure_shared();shared.predict()


def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('select','calibrate','predict'))
    globals()[parser.parse_args().stage]()


if __name__=='__main__':main()
