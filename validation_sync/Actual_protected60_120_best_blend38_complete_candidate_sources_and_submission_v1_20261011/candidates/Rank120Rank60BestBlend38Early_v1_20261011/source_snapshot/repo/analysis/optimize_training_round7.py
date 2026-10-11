"""Waves59–61: repair W5a's feature-selection ancestry and optimize causal outputs."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import time

for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name] = '8'
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'analysis'), str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round6 as previous
from optimize_training_round6 import HERE, YEARS, KEYS, BASE_POST, read, dump, sha, log

OUT = ROOT/'analysis/optimization_20261003_r7'
PREVIOUS = ROOT/'analysis/optimization_20261003_r6'
ARCHIVE = ROOT.parent/'赛题五_历史归档_20261001'
BACKUP = ROOT.parent/'赛题五_清理备份_20261001'
R4 = ARCHIVE/'experiments/revalidation_20260926/validation'
HISTORICAL_SCORE = 0.44740649979403346
WAVES = (59,60,61)
ENSEMBLES = {
    'five_fold_local': {'lgb':1.,'xgb':1.,'two':1.,'pruned':1.,'gru':1.},
    'four_fold_local': {'lgb':1.,'xgb':1.,'two':1.,'pruned':1.},
    'five_half_gru': {'lgb':1.,'xgb':1.,'two':1.,'pruned':1.,'gru':.5},
    'four_no_pruning': {'lgb':1.,'xgb':1.,'two':1.,'gru':1.},
}
MEMBERSHIP_WEIGHTS = (0.,.0125,.05)
FINE_DELTAS = (-.0125,-.00625,-.003125,0.,.003125,.00625,.0125)
BLOCK_WEIGHTS = (.005,.0125,.025,.05)
TOP_WEIGHTS = (0.,.125,.24,.5,.75,1.)
REST_WEIGHTS = (.20,.24,.28)
RETENTIONS = (.9835,.9845,.9855)
SHIFTS = (.075,.095,.115)


def member_paths(year):
    folder = ARCHIVE/'experiments'/('extended_audit_eval' if year<2022 else 'final_sweep_eval')
    return {'lgb':R4/f'predictions_baseline_{year}.parquet',
            'xgb':folder/f'T2f_xgboost_backbone_{year}.parquet',
            'two':folder/f'W2c_two_day_horizon_{year}.parquet',
            'old_pruned':folder/f'W2d_pruned_features_{year}.parquet',
            'pruned':R4/f'raw_fold_local_pruned_{year}.parquet',
            'gru':ARCHIVE/f'experiments/final_sweep_eval/gru_oof_{year}.parquet' if year<2022
                  else ARCHIVE/f'experiments/sequence_ensemble_eval/nn_raw_{year}.parquet'}


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():
        assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round6 import selected
    selected()
    if (OUT/'protocol.json').exists():
        verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round7.py',ROOT/'后续选模标准.md',
             ROOT/'active_release.json',ROOT/'evaluate.py',ROOT/'analysis/continue_optimization.py',
             ROOT/'analysis/optimize_training_round6.py',ROOT/'analysis/finalize_optimization.py',
             ROOT/'experiments/final_sweep_wave3.py',ROOT/'experiments/revalidate_fold_local.py',
             HERE/'combined_fold_frame.parquet',PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',
             PREVIOUS/'promote_baseline.npy',HERE/'connected_pred_peer67_slow16.npy',
             HERE/'orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy',
             HERE/'pp_a0_b0_top_only_w0.25_rl1_tcw1.npy',
             ARCHIVE/'experiments/final_sweep_eval/protocol_wave2.json',
             ARCHIVE/'experiments/final_sweep_eval/training_wave5.json',
             ARCHIVE/'experiments/sequence_ensemble_eval/training.json',R4/'summary.json']
    for year in YEARS:
        sources += list(member_paths(year).values()) + [R4/f'result_{year}.json',
                    R4/f'model_fold_local_pruned_{year}.txt',
                    BACKUP/f'experiments/final_sweep_eval/W5a_five_way_with_gru_{year}.parquet',
                    HERE/f'wave36_topk/raw/info_f0.175_{year}.json']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'same_validation':'2020–2024 expanding OOF; 1212 connected days; 5635800 rows',
         'historical_uncorrected_score':HISTORICAL_SCORE,
         'repair':'Replace globally selected W2d with saved fold-local-pruned OOF member. Original W5a and descendants are historical diagnostics until this dependency is repaired.',
         'ensembles':ENSEMBLES,'membership_weights':MEMBERSHIP_WEIGHTS,'fine_deltas':FINE_DELTAS,
         'block_weights':BLOCK_WEIGHTS,'block_definition':'Rank-normalize slow16 and corrected ensemble inside the unchanged daily promoted block, retain global rank blend outside it.',
         'top_order_weights':TOP_WEIGHTS,'rest_order_weights':REST_WEIGHTS,
         'retentions':RETENTIONS,'limit_shifts':SHIFTS,
         'initial_output':{'slow16_weight':.24,'top_slow_weight':.24,'retention':.9845,'limit_up_delta':.095},
         'selected_topk_recipe':read(PREVIOUS/'selection.json')['winner']['recipe'],
         'control':'Reconstruct original W5a raw and finished arrays exactly before substituting its member; verify old complete output bit-identical. Old output is never selectable.',
         'new_model_fitting':False,'test_labels_read':False,'test_future_prices_used_to_select':False,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'selection_rule':'Highest connected official composite among repaired schemes; no significance or annual-score gate.',
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round7 causal-repair and optimization protocol frozen')


def build():
    import numpy as np
    import polars as pl
    from src.scoring import Panel
    from experiments.final_sweep_wave3 import ensemble_raw
    from optimize_wave6 import make_prediction_param
    verify()
    if (OUT/'component_audit.json').exists():
        for path,digest in read(OUT/'component_audit.json')['output_sha256'].items():assert sha(path)==digest,path
        return
    ctx=previous.Context()
    finished={name:[] for name in ENSEMBLES}
    old_finished=[]
    proofs=[]
    for year in YEARS:
        frame=ctx.label_free.filter(pl.col('trade_date')//10000==year)
        panel=Panel.from_frame(frame)
        arrays={}
        paths=member_paths(year)
        for name,path in paths.items():
            raw=pl.read_parquet(path).sort('trade_date','ts_code')
            assert raw.select(KEYS).with_columns(pl.col('trade_date').cast(pl.Int32)).equals(frame.select(KEYS))
            col='gru_raw' if name=='gru' and year<2022 else 'pred_raw'
            arrays[name]=raw[col].to_numpy().astype(np.float64)
        metadata=read(R4/f'result_{year}.json')
        assert metadata['feature_selection']['uses_future_labels'] is False
        assert metadata['boundaries']['one_day_last']<metadata['boundaries']['one_day_cutoff_exclusive']<year*10000+101
        for name in ('xgboost','two_day','old_pruned'):
            key={'xgboost':'xgb','two_day':'two','old_pruned':'old_pruned'}[name]
            assert sha(paths[key])==metadata['cache_sources'][name]['sha256']
        assert sha(paths['pruned'])==metadata['artifacts_sha256'][paths['pruned'].name]
        assert sha(R4/f'model_fold_local_pruned_{year}.txt')==metadata['models']['fold_local_pruned']['model_sha256']
        old_weights=dict(ENSEMBLES['five_fold_local']);old_weights['old_pruned']=old_weights.pop('pruned')
        old_raw=ensemble_raw(panel,old_weights,arrays)
        reference=pl.read_parquet(BACKUP/f'experiments/final_sweep_eval/W5a_five_way_with_gru_{year}.parquet').sort('trade_date','ts_code')
        assert np.array_equal(old_raw,reference['pred_raw'].to_numpy()),f'Old ensemble raw reconstruction failed: {year}'
        settings=dict(BASE_POST,alpha=0,bonus=0)
        old_finished.append(make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',old_raw))),frame['aux_raw'].to_numpy(),**settings))
        for name,weights in ENSEMBLES.items():
            corrected=ensemble_raw(panel,weights,arrays)
            pred=make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',corrected))),frame['aux_raw'].to_numpy(),**settings)
            finished[name].append(pred)
        proofs.append({'year':year,'original_raw_bit_identical':True,
                       'fold_local_feature_selector':metadata['feature_selection']['selector_model'],
                       'selector_sha256':metadata['feature_selection']['selector_sha256'],
                       'pruned_model_sha256':metadata['models']['fold_local_pruned']['model_sha256'],
                       'training_boundaries':metadata['boundaries'],
                       'inherited_future_label_poisoning_checks':metadata['tests'],
                       'kept_features':metadata['feature_selection']['kept']})
        topk_meta=read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
        dump(OUT/f'raw/source_topk_{year}.json',{'year':year,'seed':2026,'training_meta':topk_meta,
             'fixed_checkpoints':(90,180),'training_performed':False},immutable=True)
        log(f'{year}: original W5a raw rebuilt exactly; corrected member ancestry verified')
    assert np.array_equal(np.concatenate(old_finished),ctx.w5a),'Original finished orderer reconstruction failed'
    original=read(PREVIOUS/'selection.json')['winner']
    old_output,_=ctx.predict(ctx.donor(np.load(PREVIOUS/'promote_baseline.npy'),original['membership_w5a_weight']),
                            original['slow16_weight'],original['retention'],original['limit_up_delta'])
    assert np.array_equal(old_output,np.load(PREVIOUS/'selected_validation.npy'))
    (OUT/'rankers').mkdir(exist_ok=True)
    outputs=[]
    for name,parts in finished.items():
        path=OUT/f'rankers/{name}.npy';np.save(path,np.concatenate(parts));outputs.append(path)
    np.save(OUT/'promote_baseline.npy',np.load(PREVIOUS/'promote_baseline.npy'));outputs.append(OUT/'promote_baseline.npy')
    dump(OUT/'component_audit.json',{'status':'passed','old_finished_and_complete_output_bit_identical':True,
         'fold_local_pruning_repair':proofs,'test_data_read':False,'new_model_training':False,
         'output_sha256':{str(p):sha(p) for p in outputs}},immutable=True)
    dump(ROOT/'results/validation_provenance_erratum_20261003.json',{
         'finding':'W5a historical OOF ensemble includes W2d features chosen from full-model gain importance, not per-fold selectors.',
         'direct_evidence':str(ARCHIVE/'experiments/final_sweep_eval/protocol_wave2.json'),
         'original_instruction':read(ARCHIVE/'experiments/final_sweep_eval/protocol_wave2.json')['pruned_features'],
         'affected':'W5a and any complete validation output that depends on its historical OOF column, including the earlier R1–R6 leaders.',
         'historical_best_uncorrected_validation':HISTORICAL_SCORE,
         'handling':'Retain all original scores and submissions as evidence; do not call them certified causal OOF results. Optimize the repaired fold-local pipeline separately.',
         'repair_audit':str(OUT/'component_audit.json'),'original_scores_overwritten':False,'test_labels_read':False},immutable=True)
    log('Original dependency controls passed; four corrected rankers ready')


class Context(previous.Context):
    def __init__(self):
        super().__init__()
        self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name,cols in [('测试集_X.csv',KEYS+['flag_limit_up']),('测试集_Y.csv',KEYS+['y_ret_1d'])]:
            if not (self.scoring/name).exists():self.frame.select(cols).write_csv(self.scoring/name,float_precision=17)
        self.install('five_fold_local')
        self.membership_mode='global'
        self.top_slow_weight=.24

    def install(self,name):
        import numpy as np
        from optimize_wave15 import daily_ranks
        self.ensemble_name=name
        self.w5a=np.load(OUT/f'rankers/{name}.npy')
        self.ranks={'w5a':daily_ranks(self.w5a,self.valid,self.dates),
                    'slow':daily_ranks(self.slow,self.valid,self.dates)}

    def donor(self,promote,rerank_weight=None):
        import numpy as np
        from optimize_wave15 import daily_ranks,weighted_rank_blend
        from optimize_wave18 import lift
        weight=self.rerank_weight if rerank_weight is None else rerank_weight
        if self.membership_mode=='global' or weight==0:return super().donor(promote,weight)
        from analysis.topset_hybrid_20261002.fold_validation import top_sets
        promoted=np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*self.tie_key,promote)
        mask,stats=top_sets(self.pdf,promoted)
        assert stats['boundary_tie_days']==0
        reranker=weighted_rank_blend([self.slow_finished,self.w5a],[1-weight,weight],self.ranks,self.valid,self.dates,('membership_slow','w5a'))
        usable=mask & self.valid & (self.slow_finished>-9) & (self.w5a>-9)
        local_slow=daily_ranks(self.slow_finished,usable,self.dates)
        local_w5a=daily_ranks(self.w5a,usable,self.dates)
        reranker[usable]=(1-weight)*local_slow[usable]+weight*local_w5a[usable]
        reranker=np.where(reranker>-9,reranker+1e-9*self.tie_key,reranker)
        return lift(promoted,reranker,self.pdf)[0]

    def predict(self,donor,weight,retention,delta=0.):
        import numpy as np
        from optimize_wave15 import weighted_rank_blend
        from optimize_wave13 import build_ab
        def ordering(w):
            blended=weighted_rank_blend([self.w5a,self.slow],[1-w,w],self.ranks,self.valid,self.dates,('w5a','slow'))
            return np.where(blended>-9,blended+1e-9*self.tie_key,blended)+1e-9*self.tie_key
        a=ordering(self.top_slow_weight)
        b=a if self.top_slow_weight==weight else ordering(weight)
        pred,stats=build_ab(donor,a,b,self.dates,self.flags,self.codes,self.n_codes,retention)
        pred[self.flags==1]+=delta
        return pred,stats


def evaluate(ctx,ensemble,member,mode='global',top=.24,rest=.24,retention=.9845,shift=.095):
    if ctx.ensemble_name!=ensemble:ctx.install(ensemble)
    ctx.membership_mode=mode;ctx.rerank_weight=member;ctx.top_slow_weight=top
    recipe=read(PREVIOUS/'selection.json')['winner']['recipe']
    donor=ctx.donor(ctx.finished('baseline',recipe),member)
    pred,stats=ctx.predict(donor,rest,retention,shift)
    started=time.monotonic();metrics=ctx.score(pred)
    log(f'{ensemble} membership={member:g}/{mode} top/rest={top:g}/{rest:g} m={retention:g} shift={shift:g}: {metrics["final_score"]:.9f}; {time.monotonic()-started:.1f}s scoring')
    return {'donor':'baseline','recipe':recipe,'ensemble_name':ensemble,'fold_local_pruning_repaired':True,
            'membership_w5a_weight':member,'membership_mode':mode,'top_slow_weight':top,'slow16_weight':rest,
            'retention':retention,'limit_up_delta':shift,'connected_final_score':metrics['final_score'],
            'metrics':metrics,'construction':stats}


def coarse():
    verify();build();ctx=Context();path=OUT/'wave59_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    for name in ENSEMBLES:
        for weight in MEMBERSHIP_WEIGHTS:
            key=f'{name}_membership{weight:g}'
            if key not in result['results']:
                result['results'][key]=evaluate(ctx,name,weight);dump(path,result)
    result['status']='complete';dump(path,result)


def fine():
    verify();prior=read(OUT/'wave59_results.json');assert prior['status']=='complete'
    best=max(prior['results'].values(),key=lambda r:r['connected_final_score'])
    weights=sorted({max(0.,min(1.,best['membership_w5a_weight']+d)) for d in FINE_DELTAS})
    dump(OUT/'fine_protocol.json',{'winner_before_refinement':best,'global_weights':weights,'block_weights':BLOCK_WEIGHTS},immutable=True)
    ctx=Context();path=OUT/'wave60_results.json';result=read(path) if path.exists() else {'status':'running','results':{}}
    for mode,values in [('global',weights),('block',BLOCK_WEIGHTS)]:
        for weight in values:
            key=f'{mode}_membership{weight:g}'
            if key not in result['results']:
                result['results'][key]=evaluate(ctx,best['ensemble_name'],weight,mode);dump(path,result)
    result['status']='complete';dump(path,result)


def refinement():
    verify();items=[]
    for wave in (59,60):
        previous_rows=read(OUT/f'wave{wave}_results.json');assert previous_rows['status']=='complete'
        items+=list(previous_rows['results'].values())
    best=max(items,key=lambda r:r['connected_final_score'])
    dump(OUT/'role_protocol.json',{'winner_before_roles':best,'top_weights':TOP_WEIGHTS,'rest_weights':REST_WEIGHTS,
         'retentions':RETENTIONS,'shifts':SHIFTS},immutable=True)
    ctx=Context();path=OUT/'wave61_results.json';result=read(path) if path.exists() else {'status':'running','results':{}}
    def record(key,top=.24,rest=.24,retention=.9845,shift=.095):
        if key not in result['results']:
            result['results'][key]=evaluate(ctx,best['ensemble_name'],best['membership_w5a_weight'],best['membership_mode'],top,rest,retention,shift)
            dump(path,result)
    for top in TOP_WEIGHTS:record(f'top_order{top:g}',top=top)
    roles=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for rest in REST_WEIGHTS:record(f'rest_order{rest:g}',top=roles['top_slow_weight'],rest=rest)
    roles=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for retention in RETENTIONS:record(f'retention{retention:g}',top=roles['top_slow_weight'],rest=roles['slow16_weight'],retention=retention)
    roles=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for shift in SHIFTS:record(f'limit_shift{shift:g}',top=roles['top_slow_weight'],rest=roles['slow16_weight'],retention=roles['retention'],shift=shift)
    result['status']='complete';dump(path,result)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','coarse','fine','refinement','all'))
    stage=parser.parse_args().stage
    for name in (('freeze','build','coarse','fine','refinement') if stage=='all' else (stage,)):globals()[name]()


if __name__=='__main__':main()
