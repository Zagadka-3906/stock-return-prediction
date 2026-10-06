"""Waves65–67: independent Top/rest ensembles, ordering weights, and retention."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round8 as previous
from optimize_training_round8 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,read,dump,sha,log,weights_from_name
OUT=ROOT/'analysis/optimization_20261003_r9'
PREVIOUS=ROOT/'analysis/optimization_20261003_r8'
EXPECTED=0.4486144884288789
WAVES=(65,66,67)
BASE_NAME='lgb1_xgb1_two0.75_gru2'
ROLE_NAMES=(BASE_NAME,'lgb1_xgb1_two1_gru1','lgb1_xgb1_two1_gru2',
            'lgb1_xgb1_two0_gru1','lgb0_xgb1_two1_gru1','lgb1_xgb0_two1_gru1','lgb1_xgb1_two1_gru2.25')
TOP_SLOW_WEIGHTS=(.125,.24,.375)
REST_SLOW_WEIGHTS=(.125,.20,.275)
RETENTIONS=(.9835,.984,.9845,.985,.9855)
SHIFTS=(.055,.075,.095,.115,.135)


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round8 import selected
    selected()
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round9.py',ROOT/'后续选模标准.md',ROOT/'evaluate.py',
             ROOT/'active_release.json',ROOT/'analysis/optimize_training_round8.py',ROOT/'analysis/optimize_training_round7.py',
             ROOT/'analysis/finalize_training_round8.py',ROOT/'analysis/finalize_training_round7.py',
             ROOT/'analysis/finalize_optimization.py',HERE/'optimize_wave13.py',HERE/'optimize_wave15.py',
             HERE/'combined_fold_frame.parquet',PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',
             PREVIOUS/'promote_baseline.npy',PREVIOUS/'component_audit.json',
             ROOT/'candidates/optimization_20261003_r8/verification.json']
    sources += [PREVIOUS/f'rankers/{name}.npy' for name in ROLE_NAMES]
    sources += [PREVIOUS/f'raw/source_topk_{year}.json' for year in YEARS]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':EXPECTED,'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'role_ensembles':{name:weights_from_name(name) for name in ROLE_NAMES},
         'role_search':'Vary Top ensemble with baseline rest; freeze highest-scoring Top; then vary rest.',
         'ordering_grid':{'top_slow_weights':TOP_SLOW_WEIGHTS,'rest_slow_weights':REST_SLOW_WEIGHTS},
         'retentions':RETENTIONS,'shifts':SHIFTS,'starting_winner':read(PREVIOUS/'selection.json')['winner'],
         'fixed_membership':'Use the exact R8 TopK promoted signal and slow16 membership donor, with zero ensemble membership mixture.',
         'expected_scored_records':33,'new_model_training':False,'pruned_member_excluded':True,
         'selection_rule':'highest official connected composite; exact ties prefer a shared ensemble between roles',
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round9 role-separation protocol frozen')


class Context(previous.Context):
    def __init__(self):
        super().__init__()
        self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self._role_cache={}
        self.roles(BASE_NAME,BASE_NAME)

    def roles(self,top,rest):
        import numpy as np
        from optimize_wave15 import daily_ranks
        for name in dict.fromkeys((top,rest)):
            if name not in self._role_cache:
                values=np.load(PREVIOUS/f'rankers/{name}.npy')
                self._role_cache[name]=(values,daily_ranks(values,self.valid,self.dates))
        self.ensemble_name=self.rest_ensemble_name=rest;self.top_ensemble_name=top
        self.w5a,rank_rest=self._role_cache[rest]
        self.top_values,self.top_ranks=self._role_cache[top]
        self.ranks={'w5a':rank_rest,'slow':self.ranks['slow']}

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline'
        if recipe is not None:assert recipe==read(PREVIOUS/'selection.json')['winner']['recipe']
        return np.load(PREVIOUS/'promote_baseline.npy')

    def predict(self,donor,weight,retention,delta=0.):
        import numpy as np
        from optimize_wave15 import weighted_rank_blend
        from optimize_wave13 import build_ab
        n=len(self.dates)
        # A copied prefix context retains the immutable full role arrays; consume only its dates.
        top=self.top_values[:n];top_ranks=self.top_ranks[:n]
        def ordering(values,ranks,w):
            blend=weighted_rank_blend([values,self.slow],[1-w,w],ranks,self.valid,self.dates,('w5a','slow'))
            return np.where(blend>-9,blend+1e-9*self.tie_key,blend)+1e-9*self.tie_key
        a=ordering(top,{'w5a':top_ranks,'slow':self.ranks['slow']},self.top_slow_weight)
        if self.top_ensemble_name==self.ensemble_name and self.top_slow_weight==weight:b=a
        else:b=ordering(self.w5a,self.ranks,weight)
        pred,stats=build_ab(donor,a,b,self.dates,self.flags,self.codes,self.n_codes,retention)
        pred[self.flags==1]+=delta
        return pred,stats


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();winner=read(PREVIOUS/'selection.json')['winner']
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    for year in YEARS:dump(OUT/f'raw/source_topk_{year}.json',read(PREVIOUS/f'raw/source_topk_{year}.json'),immutable=True)
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_prediction_bit_identical':True,
         'source_rankers':{name:sha(PREVIOUS/f'rankers/{name}.npy') for name in ROLE_NAMES},
         'test_data_read':False,'new_model_training':False,'pruned_member_excluded':True},immutable=True)
    log('Round9 shared-role baseline rebuilt bit identically')


def evaluate(ctx,top,rest,top_weight=.24,rest_weight=.20,retention=.9845,shift=.095):
    ctx.roles(top,rest);ctx.top_slow_weight=top_weight
    pred,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),rest_weight,retention,shift)
    metrics=ctx.score(pred)
    log(f'Round9 Top={top} rest={rest} slow={top_weight:g}/{rest_weight:g} retain={retention:g} shift={shift:g}: {metrics["final_score"]:.9f}')
    return {'donor':'baseline','recipe':read(PREVIOUS/'selection.json')['winner']['recipe'],
            'ensemble_name':rest,'ensemble_weights':weights_from_name(rest),
            'top_ensemble_name':top,'top_ensemble_weights':weights_from_name(top),
            'role_ensembles_split':top!=rest,'fold_local_pruning_repaired':True,'pruned_member_excluded':True,
            'membership_w5a_weight':0.,'membership_mode':'global','top_slow_weight':top_weight,
            'slow16_weight':rest_weight,'retention':retention,'limit_up_delta':shift,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def roles():
    verify();build();ctx=Context();path=OUT/'wave65_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    for top in ROLE_NAMES:
        key=f'top_{top}'
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,top,BASE_NAME);dump(path,result)
            if top==BASE_NAME:assert abs(result['results'][key]['connected_final_score']-EXPECTED)<1e-12
    best=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    dump(OUT/'rest_role_protocol.json',{'winner_before_rest':best,'rest_names':ROLE_NAMES},immutable=True)
    for rest in ROLE_NAMES:
        key=f'rest_{rest}'
        if key not in result['results']:result['results'][key]=evaluate(ctx,best['top_ensemble_name'],rest);dump(path,result)
    result['status']='complete';dump(path,result)


def ordering():
    import itertools
    verify();prior=read(OUT/'wave65_results.json');assert prior['status']=='complete'
    best=max(prior['results'].values(),key=lambda r:r['connected_final_score'])
    dump(OUT/'ordering_protocol.json',{'winner_before_ordering':best,'top_weights':TOP_SLOW_WEIGHTS,
         'rest_weights':REST_SLOW_WEIGHTS},immutable=True)
    ctx=Context();path=OUT/'wave66_results.json';result=read(path) if path.exists() else {'status':'running','results':{}}
    for top,rest in itertools.product(TOP_SLOW_WEIGHTS,REST_SLOW_WEIGHTS):
        key=f'top{top:g}_rest{rest:g}'
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,best['top_ensemble_name'],best['ensemble_name'],top,rest);dump(path,result)
    result['status']='complete';dump(path,result)


def refinement():
    verify();rows=[]
    for wave in (65,66):
        result=read(OUT/f'wave{wave}_results.json');assert result['status']=='complete';rows+=list(result['results'].values())
    best=max(rows,key=lambda r:r['connected_final_score'])
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':best,'retentions':RETENTIONS,'shifts':SHIFTS},immutable=True)
    ctx=Context();path=OUT/'wave67_results.json';result=read(path) if path.exists() else {'status':'running','results':{}}
    for retention in RETENTIONS:
        key=f'retention{retention:g}'
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,best['top_ensemble_name'],best['ensemble_name'],best['top_slow_weight'],best['slow16_weight'],retention);dump(path,result)
    best=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for shift in SHIFTS:
        key=f'limit_shift{shift:g}'
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,best['top_ensemble_name'],best['ensemble_name'],best['top_slow_weight'],best['slow16_weight'],best['retention'],shift);dump(path,result)
    result['status']='complete';dump(path,result)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','roles','ordering','refinement','all'))
    stage=parser.parse_args().stage
    for name in (('freeze','build','roles','ordering','refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
