"""Waves62–64: pruning-free member weights and TopK donor finishing."""
from __future__ import annotations
import argparse
from copy import deepcopy
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round7 as previous
from optimize_training_round7 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,read,dump,sha,log,member_paths
from optimize_training_round6 import source_raw,source_model
OUT=ROOT/'analysis/optimization_20261003_r8'
PREVIOUS=ROOT/'analysis/optimization_20261003_r7'
EXPECTED=0.4477441201313571
WAVES=(62,63,64)
MEMBERS=('lgb','xgb','two','gru')
MULTIPLIERS=(0.,.5,1.5,2.)
FINE_DELTAS=(-.25,.25)
EARLY_WEIGHTS=(.15,.20,.25,.30,.35)
ALPHAS=(.875,.90,.925)
AUX_WEIGHTS=(.20,.25,.30)
SHIFTS=(.095,.115,.135,.155)


def weights_name(weights):
    return '_'.join(f'{m}{weights.get(m,0):g}' for m in MEMBERS)


def weights_from_name(name):
    return {m:float(token[len(m):]) for m,token in zip(MEMBERS,name.split('_')) if float(token[len(m):])>0}


BASE_WEIGHTS=dict.fromkeys(MEMBERS,1.)
BASE_NAME=weights_name(BASE_WEIGHTS)
ENSEMBLES={BASE_NAME:BASE_WEIGHTS}
for member in MEMBERS:
    for multiplier in MULTIPLIERS:
        weights=dict(BASE_WEIGHTS);weights[member]=multiplier
        ENSEMBLES[weights_name(weights)]={m:w for m,w in weights.items() if w>0}


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round7 import selected
    selected()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round8.py',ROOT/'后续选模标准.md',
             ROOT/'evaluate.py',ROOT/'active_release.json',ROOT/'analysis/finalize_training_round7.py',
             ROOT/'analysis/optimize_training_round7.py',ROOT/'analysis/finalize_optimization.py',
             ROOT/'experiments/final_sweep_wave3.py',HERE/'optimize_wave6.py',HERE/'optimize_wave15.py',
             PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
             PREVIOUS/'component_audit.json',PREVIOUS/'rankers/four_no_pruning.npy',
             HERE/'combined_fold_frame.parquet',ROOT/'candidates/optimization_20261003_r7/verification.json']
    for year in YEARS:
        sources += [member_paths(year)[m] for m in MEMBERS]
        sources += [source_model(2026,year),HERE/f'wave36_topk/raw/info_f0.175_{year}.json']
        for rounds in (90,180):sources += [source_raw(2026,rounds,year),source_raw(2026,rounds,year).with_suffix('.json')]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':EXPECTED,'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'coarse_ensembles':ENSEMBLES,'fine_member_deltas':FINE_DELTAS,'fine_weights_clamped_at_zero':True,
         'donor_early90_weights':EARLY_WEIGHTS,'donor_alphas':ALPHAS,'donor_auxiliary_weights':AUX_WEIGHTS,
         'limit_up_shifts':SHIFTS,'starting_winner':read(PREVIOUS/'selection.json')['winner'],
         'new_training':False,'pruned_member_excluded_from_all_candidates':True,
         'selection_rule':'highest official connected composite among complete compliant outputs',
         'adaptive_rule':'coarse winner; fixed one-coordinate weight deltas around it; then sequential donor axes and shift',
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round8 search protocol frozen')


class Context(previous.Context):
    def __init__(self):
        super().__init__()
        self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.install(BASE_NAME)
        self.membership_mode='global';self.rerank_weight=0.;self.top_slow_weight=.24

    def install(self,name):
        if name in previous.ENSEMBLES:return super().install(name)
        import numpy as np
        from optimize_wave15 import daily_ranks
        self.ensemble_name=name
        path=OUT/f'rankers/{name}.npy'
        self.w5a=np.load(path)
        self.ranks={'w5a':daily_ranks(self.w5a,self.valid,self.dates),'slow':daily_ranks(self.slow,self.valid,self.dates)}

    def finished(self,name,recipe=None):
        import hashlib
        import json
        import numpy as np
        import polars as pl
        from optimize_wave15 import daily_ranks
        from optimize_wave6 import make_prediction_param
        from src.scoring import Panel
        assert name=='baseline'
        recipe=recipe or read(PREVIOUS/'selection.json')['winner']['recipe']
        key=hashlib.sha256(json.dumps(recipe,sort_keys=True).encode()).hexdigest()[:20]
        path=OUT/f'promote/{key}.npy'
        if path.exists():return np.load(path)
        parts=[]
        for year in YEARS:
            frame=self.label_free.filter(pl.col('trade_date')//10000==year)
            valid=frame['price_valid'].to_numpy();dates=frame['trade_date'].to_numpy()
            raws=[]
            for component in recipe['components']:
                cached=pl.read_parquet(source_raw(component['seed'],component['rounds'],year))
                assert cached.select(KEYS).equals(frame.select(KEYS))
                raws.append((component['weight'],cached['pred_raw'].to_numpy()))
            mixed=sum(w*daily_ranks(raw,valid,dates) for w,raw in raws);mixed[~valid]=-10.
            parts.append(make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',mixed))),
                         frame['aux_raw'].to_numpy(),**recipe['postprocessing']))
        path.parent.mkdir(exist_ok=True);np.save(path,np.concatenate(parts));return np.load(path)


def build_rankers(configs):
    import numpy as np
    import polars as pl
    from experiments.final_sweep_wave3 import ensemble_raw
    from optimize_wave6 import make_prediction_param
    from src.scoring import Panel
    verify();ctx=previous.Context()
    (OUT/'rankers').mkdir(exist_ok=True)
    pending={n:[] for n in configs if not (OUT/f'rankers/{n}.npy').exists()}
    for year in YEARS:
        frame=ctx.label_free.filter(pl.col('trade_date')//10000==year);panel=Panel.from_frame(frame)
        arrays={}
        for member in MEMBERS:
            raw=pl.read_parquet(member_paths(year)[member]).sort('trade_date','ts_code')
            assert raw.select(KEYS).with_columns(pl.col('trade_date').cast(pl.Int32)).equals(frame.select(KEYS))
            col='gru_raw' if member=='gru' and year<2022 else 'pred_raw'
            arrays[member]=raw[col].to_numpy().astype(np.float64)
        for name in pending:
            weights=configs[name];assert 'pruned' not in weights and all(w>0 for w in weights.values())
            raw=ensemble_raw(panel,weights,arrays)
            pending[name].append(make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw))),
                                 frame['aux_raw'].to_numpy(),**dict(BASE_POST,alpha=0,bonus=0)))
        log(f'Round8: {year} member-weight rankers built ({len(pending)} variants)')
    for name,parts in pending.items():np.save(OUT/f'rankers/{name}.npy',np.concatenate(parts))


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():
        for path,digest in read(OUT/'component_audit.json')['output_sha256'].items():assert sha(path)==digest,path
        return
    build_rankers(ENSEMBLES);ctx=Context();winner=read(PREVIOUS/'selection.json')['winner']
    assert np.array_equal(ctx.w5a,np.load(PREVIOUS/'rankers/four_no_pruning.npy'))
    promote=ctx.finished('baseline',winner['recipe']);assert np.array_equal(promote,np.load(PREVIOUS/'promote_baseline.npy'))
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    for year in YEARS:
        for rounds in (90,180):
            info=read(source_raw(2026,rounds,year).with_suffix('.json'))
            original=read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
            assert info['training_meta']==original and info['model_reload_bit_identical']
            assert sha(source_raw(2026,rounds,year))==info['prediction_sha256']
            assert sha(source_model(2026,year))==info['model_sha256']
        dump(OUT/f'raw/source_topk_{year}.json',{'year':year,'seed':2026,'training_meta':original,
             'training_performed':False,'fixed_checkpoints':(90,180)},immutable=True)
    files=[*sorted((OUT/'rankers').glob('*.npy')),*sorted((OUT/'promote').glob('*.npy'))]
    dump(OUT/'component_audit.json',{'status':'passed','baseline_ranker_bit_identical':True,
         'baseline_promote_bit_identical':True,'baseline_complete_prediction_bit_identical':True,
         'test_data_read':False,'new_model_training':False,'pruned_member_excluded':True,
         'output_sha256':{str(p):sha(p) for p in files}},immutable=True)
    log('Round8 baseline and source checkpoint controls passed')


def evaluate(ctx,name,weights,recipe=None,shift=.115):
    if ctx.ensemble_name!=name:ctx.install(name)
    recipe=recipe or read(PREVIOUS/'selection.json')['winner']['recipe']
    promote=ctx.finished('baseline',recipe)
    pred,stats=ctx.predict(ctx.donor(promote),.20,.9845,shift)
    metrics=ctx.score(pred)
    log(f'Round8 {name} early={recipe["components"][0]["weight"]:g} alpha={recipe["postprocessing"]["alpha"]:g} aux={recipe["postprocessing"]["weight"]:g} shift={shift:g}: {metrics["final_score"]:.9f}')
    return {'donor':'baseline','recipe':recipe,'ensemble_name':name,'ensemble_weights':weights,
            'fold_local_pruning_repaired':True,'pruned_member_excluded':True,
            'membership_w5a_weight':0.,'membership_mode':'global','top_slow_weight':.24,'slow16_weight':.20,
            'retention':.9845,'limit_up_delta':shift,'connected_final_score':metrics['final_score'],
            'metrics':metrics,'construction':stats}


def coarse():
    verify();build();ctx=Context();path=OUT/'wave62_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    for name,weights in ENSEMBLES.items():
        if name not in result['results']:
            result['results'][name]=evaluate(ctx,name,weights);dump(path,result)
            if name==BASE_NAME:assert abs(result['results'][name]['connected_final_score']-EXPECTED)<1e-12
    result['status']='complete';dump(path,result)


def fine():
    verify();prior=read(OUT/'wave62_results.json');assert prior['status']=='complete'
    best=max(prior['results'].values(),key=lambda r:r['connected_final_score'])
    configs={best['ensemble_name']:best['ensemble_weights']}
    for member in MEMBERS:
        for delta in FINE_DELTAS:
            w={m:best['ensemble_weights'].get(m,0.) for m in MEMBERS};w[member]=max(0,w[member]+delta)
            configs[weights_name(w)]={m:v for m,v in w.items() if v>0}
    dump(OUT/'fine_protocol.json',{'winner_before_fine':best,'ensembles':configs},immutable=True)
    build_rankers(configs);ctx=Context();path=OUT/'wave63_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    for name,weights in configs.items():
        if name not in result['results']:result['results'][name]=evaluate(ctx,name,weights);dump(path,result)
    result['status']='complete';dump(path,result)


def donor_refinement():
    verify();rows=[]
    for wave in (62,63):
        prior=read(OUT/f'wave{wave}_results.json');assert prior['status']=='complete';rows+=list(prior['results'].values())
    best=max(rows,key=lambda r:r['connected_final_score'])
    dump(OUT/'donor_protocol.json',{'winner_before_donor':best,'early_weights':EARLY_WEIGHTS,
         'alphas':ALPHAS,'auxiliary_weights':AUX_WEIGHTS,'shifts':SHIFTS},immutable=True)
    ctx=Context();path=OUT/'wave64_results.json';result=read(path) if path.exists() else {'status':'running','results':{}}
    def record(key,recipe,shift=.115):
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,best['ensemble_name'],best['ensemble_weights'],recipe,shift);dump(path,result)
    for value in EARLY_WEIGHTS:
        recipe=deepcopy(best['recipe']);recipe['components'][0]['weight']=value;recipe['components'][1]['weight']=1-value
        record(f'early90_weight{value:g}',recipe)
    choice=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for value in ALPHAS:
        recipe=deepcopy(choice['recipe']);recipe['postprocessing']['alpha']=value;record(f'alpha{value:g}',recipe)
    choice=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for value in AUX_WEIGHTS:
        recipe=deepcopy(choice['recipe']);recipe['postprocessing']['weight']=value;record(f'aux{value:g}',recipe)
    choice=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for value in SHIFTS:record(f'limit_shift{value:g}',choice['recipe'],value)
    result['status']='complete';dump(path,result)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','coarse','fine','donor_refinement','all'))
    stage=parser.parse_args().stage
    for name in (('freeze','build','coarse','fine','donor_refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
