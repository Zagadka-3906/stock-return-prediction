"""Waves211–213: causal temporal processing after the entire selected output."""
from copy import copy,deepcopy
from pathlib import Path
import itertools
import json
import os
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round48 as previous
from optimize_training_round48 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name
from final_output_temporal_postprocessing_20261004 import transform
OUT=ROOT/'analysis/optimization_20261003_r49'
PREVIOUS=ROOT/'analysis/optimization_20261003_r48'
FOUNDATION=PREVIOUS
WAVES=(211,212,213)
FIELDS=previous.FIELDS+('temporal_postprocessing',)
MODELS=NEW_MODELS=()
IDENTITY={'alpha':1.,'mix':0.,'power':1.}
ALPHAS=(.5,.75,.9,.95,.98,.995)
POWERS=(.5,1.,2.)
MIXES=(.025,.1,.25,1.)


def baseline():return {**previous.configuration(read(PREVIOUS/'selection.json')['winner']),'temporal_postprocessing':deepcopy(IDENTITY)}
def expected():return read(PREVIOUS/'selection.json')['winner']['connected_final_score']
def configuration(row):return {key:deepcopy(row[key]) for key in FIELDS}
def signature(row):return json.dumps(configuration(row),sort_keys=True,separators=(',',':'))
def active(cfg):
    p=cfg['temporal_postprocessing'];return p['mix']>0. and (p['alpha']!=1. or p['power']!=1.)
def best(rows):
    return min(rows,key=lambda r:(-r['connected_final_score'],active(r),r['temporal_postprocessing']['mix'],abs(r['temporal_postprocessing']['power']-1.),signature(r)))


class Context:
    def __init__(self):
        import numpy as np
        import pandas as pd
        import polars as pl
        self.frame=pl.read_parquet(ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet',
            columns=KEYS+['price_valid','flag_limit_up','y_ret_1d'])
        assert len(self.frame)==5635800 and self.frame['trade_date'].n_unique()==1212
        self.label_free=self.frame.with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
        self.dates=self.frame['trade_date'].to_numpy();self.flags=self.frame['flag_limit_up'].to_numpy().astype(np.int64)
        self.valid=self.frame['price_valid'].to_numpy();self.codes,symbols=pd.factorize(self.frame['ts_code'].to_numpy(),sort=True)
        self.codes=self.codes.astype(np.int64);self.n_codes=len(symbols);self.tie_key=np.zeros(len(self.frame))
        self.pdf=self.frame.select('trade_date','flag_limit_up').to_pandas()
        self.raw=np.load(PREVIOUS/'selected_validation.npy',mmap_mode='r')
        self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        # These unused aliases support the existing calibration prefix inspector.
        self.slow_finished=self.w5a=self.slow=self.raw;self.ranks={};self.configure(baseline())
    def configure(self,cfg):self.cfg=configuration(cfg)
    def finished(self,name,recipe=None):
        assert name=='baseline';return self.raw[:len(self.dates)]
    def promote(self,name):return self.finished(name)
    def donor(self,promote):return promote
    def predict(self,promote,weight,retention,delta=0.):
        pred=transform(promote,self.dates,self.valid,self.codes,self.cfg['temporal_postprocessing'])
        return pred,{'foundation_complete_output_reused':True,'foundation_round':48,'temporal_postprocessing':deepcopy(self.cfg['temporal_postprocessing'])}
    def score(self,pred):
        from score_calibrated_candidates_20261003 import score
        return score(self,pred)


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round48 import selected
    selected()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round49.py',ROOT/'analysis/predict_temporal_round49.py',
        ROOT/'analysis/verify_methods_round49.py',ROOT/'analysis/run_training_round49_pipeline.py',
        ROOT/'analysis/final_output_temporal_postprocessing_20261004.py',ROOT/'analysis/verify_final_output_temporal_postprocessing_20261004.py',
        ROOT/'analysis/final_output_temporal_preflight_20261004/verification.json',
        ROOT/'analysis/verify_final_output_temporal_future_20261004.py',ROOT/'analysis/final_output_temporal_future_qa_20261004/verification.json',
        ROOT/'analysis/verify_final_temporal_context_20261004.py',ROOT/'analysis/final_temporal_context_preflight_20261004/verification.json',
        ROOT/'analysis/score_calibrated_candidates_20261003.py',ROOT/'analysis/finalize_optimization.py',
        ROOT/'analysis/identical_official_score_cache_20261003.py',ROOT/'analysis/cross_round_official_score_reuse_20261003.py',
        ROOT/'analysis/official_validation_csv_parse_cache_20261003.py',ROOT/'analysis/parallel_candidate_scoring_four_20261004.py',
        ROOT/'analysis/parallel_candidate_scoring_four_qa_20261004/verification.json',ROOT/'analysis/official_parallel_capacity_qa_20261004/verification.json',
        ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet',ROOT/'后续选模标准.md',ROOT/'active_release.json',
        PREVIOUS/'protocol.json',PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',PREVIOUS/'standalone_causal_checks.json',
        ROOT/'candidates/optimization_20261003_r48/verification.json',ROOT/'candidates/optimization_20261003_r48/manifest.json']
    sources.extend(Path(p) for p in read(PREVIOUS/'protocol.json')['input_sha256'])
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'baseline_score':expected(),
        'starting_configuration':baseline(),'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
        'wave211':{'baseline':1,'alpha':ALPHAS,'power':POWERS,'mix':MIXES,'records':73},
        'wave212':{'alpha_offsets':(-.025,-.005,0.,.005,.025),'mix_values':'zero,half,anchor,double clipped[0,1]','records':20,
            'identity_refinement_anchor':{'alpha':.995,'mix':.025,'power':1.}},
        'wave213':{'powers':POWERS,'records':3},'expected_scored_records':96,
        'method':'Current price-valid complete-output ranks, optional power and per-symbol causalEMA; blend current withupdated past state. Missing-price rows preserve the frozen forecast; no labels enter the transform. States continue over all annual boundaries.',
        'foundation_parameters_fixed':True,'new_model_training':False,'new_fold_models_trained':0,
        'parallel_candidate_execution':{'workers':4,'commit_order':'declared arm order','adaptive_stage_barriers_preserved':True},
        'official_candidate_scoring':'Each full output gets its own mature past-OOF return mapping and actual CSV official score.',
        'selection_rule':'highest official connected composite; exact ties prefer identity thenlower blend andpower complexity',
        'test_labels_read':False,'test_future_prices_used_to_select':False,'all_validation_years_previously_viewed':True,
        'selection_bias_uncorrected':True,'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)


def prefix_controls(ctx,cfg,counts=(80,260,975)):
    import numpy as np
    import polars as pl
    ctx.configure(cfg);raw=ctx.finished('baseline');pred,_=ctx.predict(raw,0.,0.)
    poisoned=copy(ctx);poisoned.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    assert np.array_equal(pred,poisoned.predict(raw,0.,0.)[0])
    controls=[]
    for count in counts:
        last=int(np.unique(ctx.dates)[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
        for name in ('dates','flags','valid','codes'):setattr(prefix,name,getattr(ctx,name)[:n])
        assert np.array_equal(pred[:n],prefix.predict(raw[:n],0.,0.)[0])
        controls.append({'days':count,'through_date':last,'cold_prefix_bit_identical':True})
    return {'temporal_postprocessing':cfg['temporal_postprocessing'],'label_poisoning_bit_identical':True,'complete_day_prefixes':controls}


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();cfg=baseline();pred,_=ctx.predict(ctx.finished('baseline'),0.,0.)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    cases=[cfg]+[{**cfg,'temporal_postprocessing':p} for p in ({'alpha':.5,'mix':.25,'power':.5},{'alpha':.9,'mix':.1,'power':1.},{'alpha':.995,'mix':.025,'power':2.})]
    dump(OUT/'component_audit.json',{'status':'passed','complete_previous_output_recomputed_bit_identically':True,
        'controls':[prefix_controls(ctx,c) for c in cases],'models_trained':0,'test_data_read':False,'output_sha256':{}},immutable=True)


def evaluate(ctx,cfg):
    assert previous.configuration(cfg)==previous.configuration(baseline())
    ctx.configure(cfg);pred,stats=ctx.predict(ctx.finished('baseline'),0.,0.);metrics=ctx.score(pred)
    foundation=read(PREVIOUS/'selection.json')['winner'];log(f'Round49 temporal={cfg["temporal_postprocessing"]}: {metrics["final_score"]:.9f}')
    return {**configuration(cfg),'donor':'baseline',**{k:deepcopy(foundation[k]) for k in ('ensemble_weights','top_ensemble_weights','membership_ensemble_weights','role_ensembles_split')},
        'fold_local_pruning_repaired':True,'pruned_member_excluded':True,'connected_final_score':metrics['final_score'],
        'metrics':metrics,'construction':stats,'official_score_cache':deepcopy(ctx.last_official_score_cache),
        'causal_return_mapping':deepcopy(ctx.last_candidate_return_mapping)}


def execute(wave,arms):
    from parallel_candidate_scoring_four_20261004 import evaluate_many
    path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    missing=[(key,cfg) for key,cfg in arms if key not in payload['results']]
    for key,row in evaluate_many('optimize_training_round49',missing,OUT):payload['results'][key]=row;dump(path,payload)
    payload['status']='complete';dump(path,payload);return payload
def prior_best(waves):return best([r for w in waves for r in read(OUT/f'wave{w}_results.json')['results'].values()])
def independent():
    verify();build();base=baseline();arms=[('baseline',base)]
    for alpha,power,mix in itertools.product(ALPHAS,POWERS,MIXES):
        cfg=deepcopy(base);cfg['temporal_postprocessing']={'alpha':alpha,'power':power,'mix':mix};arms.append((f'a{alpha:g}_p{power:g}_m{mix:g}',cfg))
    execute(211,arms)
def refinement():
    winner=prior_best((211,));base=configuration(winner)
    anchor=base['temporal_postprocessing'] if active(base) else {'alpha':.995,'mix':.025,'power':1.}
    alphas=[min(1.,max(.001,anchor['alpha']+v)) for v in (-.025,-.005,0.,.005,.025)]
    mixes=[0.,anchor['mix']*.5,anchor['mix'],min(1.,anchor['mix']*2.)]
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner,'anchor':anchor,'alphas':alphas,'mixes':mixes},immutable=True)
    arms=[]
    for i,(alpha,mix) in enumerate(itertools.product(alphas,mixes)):
        cfg=deepcopy(base);cfg['temporal_postprocessing']={**anchor,'alpha':alpha,'mix':mix};arms.append((f'refine{i}_a{alpha:g}_m{mix:g}',cfg))
    execute(212,arms)
def power_refinement():
    winner=prior_best((211,212));base=configuration(winner)
    dump(OUT/'power_refinement_protocol.json',{'winner_before_refinement':winner,'powers':POWERS},immutable=True)
    arms=[]
    for power in POWERS:
        cfg=deepcopy(base);cfg['temporal_postprocessing']['power']=power;arms.append((f'power{power:g}',cfg))
    execute(213,arms)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('freeze','build','independent','refinement','power_refinement'));globals()[p.parse_args().stage]()
