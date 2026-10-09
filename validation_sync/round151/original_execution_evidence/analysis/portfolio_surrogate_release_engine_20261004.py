"""Freeze complete additive schemes andreuse verified causal return calibration."""
from pathlib import Path
import importlib
import time


def install(number,namespace):
    experiment=importlib.import_module(f'optimize_training_round{number}')
    ROOT=experiment.ROOT
    def selected():
        experiment.verify();record=experiment.read(experiment.OUT/'selection.json')
        for path,digest in record['frozen_sha256'].items():assert experiment.sha(ROOT/path)==digest,path
        return record
    class ReleaseContext(experiment.Context):
        def __init__(self,winner=None):super().__init__();self.configure(winner or selected()['winner'])
    def select():
        import numpy as np
        experiment.verify()
        if (experiment.OUT/'selection.json').exists():selected();return
        rows=[]
        for wave in experiment.WAVES:
            payload=experiment.read(experiment.OUT/f'wave{wave}_results.json');assert payload['status']=='complete'
            rows.extend(dict(wave=wave,arm=key,**row) for key,row in payload['results'].items())
        assert len(rows)==experiment.read(experiment.OUT/'protocol.json')['expected_scored_records']
        winner=experiment.best(rows);assert winner['connected_final_score']>=experiment.expected()
        ctx=ReleaseContext(winner);promote=ctx.finished('baseline');pred,_=ctx.predict(ctx.donor(promote),0.,0.)
        assert ctx.score(pred)==winner['metrics']
        np.save(experiment.OUT/'selected_validation.npy',pred);np.save(experiment.OUT/'promote_baseline.npy',promote)
        sources=[Path(__file__),ROOT/f'analysis/finalize_training_round{number}.py',experiment.OUT/'protocol.json',
            experiment.OUT/'component_audit.json',*[experiment.OUT/f'wave{wave}_results.json' for wave in experiment.WAVES],
            *experiment.OUT.glob('*_protocol.json'),experiment.OUT/'selected_validation.npy',experiment.OUT/'promote_baseline.npy',
            experiment.PREVIOUS/'selection.json',ROOT/'active_release.json',
            ROOT/'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
            ROOT/f'candidates/optimization_20261003_r{number-1}/verification.json']
        sources += [Path(row['official_score_cache']['official_metrics_source']) for row in rows]
        experiment.dump(experiment.OUT/'selection.json',{'status':'frozen_before_test_prediction',
            'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'winner':winner,
            'ranking':sorted(rows,key=lambda row:(-row['connected_final_score'],row['wave'],row['arm'])),
            'scored_records':len(rows),'baseline_score':experiment.expected(),'score_gain':winner['connected_final_score']-experiment.expected(),
            'current_parameter_authority':experiment.GRAPH_FIELD,'flat_predecessor_configurations_are_history_only':True,
            'pruned_member_excluded':True,'fold_local_pruning_repaired':True,'test_labels_read':False,
            'selection_rule':'Highest actual complete official connected score; exact ties prefer fewer active model branches',
            'frozen_sha256':{p.relative_to(ROOT).as_posix():experiment.sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    def calibrate():
        import finalize_training_round7 as shared
        shared.OUT=experiment.OUT;shared.selected=selected;shared.ReleaseContext=ReleaseContext;shared.verify=experiment.verify;shared.calibrate()
    def predict():
        assert experiment.read(experiment.OUT/'causal_validation.json')['status']==experiment.read(experiment.OUT/'calibrated_csv_official.json')['status']=='passed'
        from predict_portfolio_surrogate_scheme_20261004 import predict as infer
        infer(experiment,selected())
    namespace.update(ROOT=ROOT,OUT=experiment.OUT,PREVIOUS=experiment.PREVIOUS,WAVES=experiment.WAVES,
        read=experiment.read,dump=experiment.dump,sha=experiment.sha,verify=experiment.verify,
        ReleaseContext=ReleaseContext,selected=selected,select=select,calibrate=calibrate,predict=predict)
