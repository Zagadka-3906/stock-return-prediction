"""Waves56-58: rerank the membership donor with a label-free model consensus."""
from __future__ import annotations

import argparse
import itertools
import os
from pathlib import Path
import sys
import time

for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[_name] = '8'
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round5 as previous
from optimize_training_round5 import HERE, YEARS, KEYS, BASE_POST, read, dump, sha, log, source_raw, source_model

OUT = ROOT/'analysis/optimization_20261003_r6'
PREVIOUS = ROOT/'analysis/optimization_20261003_r5'
EXPECTED = 0.4473425202487328
WAVES = (56,57,58)
CONFIGS = ((2026,90),(2026,180))
RERANK_WEIGHTS = (0.0,0.025,0.05,0.10,0.20,0.35,0.50,0.75,1.0)
FINE_DELTAS = (-0.025,-0.0125,0.0,0.0125,0.025)
SLOW_WEIGHTS = (0.23,0.24,0.25)
RETENTION = (0.984,0.9845,0.985)
LIMIT_SHIFTS = (0.09,0.095,0.10)


def verify():
    protocol = read(OUT/'protocol.json')
    for name,digest in protocol['input_sha256'].items():
        assert sha(ROOT/name)==digest,name
    return protocol


def freeze():
    from finalize_training_round5_v2 import selected
    selected()
    if (OUT/'protocol.json').exists():
        verify()
        return
    sources = [Path(__file__),ROOT/'analysis/finalize_training_round6.py',
               *[ROOT/'analysis'/name for name in ('optimize_training_round5.py','finalize_training_round5_v2.py',
                   'optimize_training_round4.py','optimize_training_round3.py','continue_optimization.py','finalize_optimization.py')],
               ROOT/'后续选模标准.md',ROOT/'evaluate.py',ROOT/'run.py',ROOT/'experiments/r6_topk.py',
               ROOT/'src/scoring.py',ROOT/'src/postprocessing.py',
               *[HERE/name for name in ('connected_scorer.py','optimize_wave31.py','optimize_wave6.py','optimize_wave13.py',
                    'optimize_wave15.py','optimize_wave18.py','return_mapping.py')],
               ROOT/'data/features.parquet',ROOT/'data/raw/训练集.csv',ROOT/'data/feature_manifest.json',
               PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
               ROOT/'active_release.json',HERE/'combined_fold_frame.parquet',HERE/'connected_pred_peer67_slow16.npy',
               HERE/'orderer_a0b0_W5a_five_way_with_gru__final_sweep_eval.npy',HERE/'pp_a0_b0_top_only_w0.25_rl1_tcw1.npy']
    sources += [p for seed,rounds in CONFIGS for year in YEARS
                for p in (source_raw(seed,rounds,year),source_raw(seed,rounds,year).with_suffix('.json'))]
    sources += [source_model(2026,year) for year in YEARS]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'baseline_score':EXPECTED,'same_validation':'2020-2024 expanding OOF;1212 connected days;5635800 rows',
         'fixed_recipe':read(PREVIOUS/'selection.json')['winner']['recipe'],
         'membership_rerank_weights':RERANK_WEIGHTS,'fine_weight_deltas':FINE_DELTAS,'fine_boundary_clamp':(0,1),
         'membership_rerank_definition':'Within the unchanged promoted Top10% block, blend daily ranks of finished slow16 with W5a alpha0/bonus0; W5a weight is the searched value. Use shared valid subset and the established code tie-break. At weight0 preserve the original donor exactly.',
         'initial_output':{'slow16_weight':0.24,'retention':0.9845,'limit_up_delta':0.095},
         'output_grid':{'slow_weights':SLOW_WEIGHTS,'retention':RETENTION,'limit_up_deltas':LIMIT_SHIFTS},
         'expected_scored_records':26,'new_fold_training_required':False,
         'baseline_control':'full prediction and written-CSV score reproduce round5 winner',
         'selection_rule':'highest official connected composite among compliant complete schemes; exact ties prefer fewer models and simpler reranking',
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'test_labels_read':False,'test_future_prices_used_to_select':False,
         'input_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round6 consensus-reranking protocol frozen')


def provenance():
    verify()
    for seed,rounds in CONFIGS:
        for year in YEARS:
            path=source_raw(seed,rounds,year)
            info=read(path.with_suffix('.json'))
            original=read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
            model=source_model(seed,year)
            assert info['training_meta']==original and info['model_reload_bit_identical']
            assert sha(path)==info['prediction_sha256'] and sha(model)==info['model_sha256']
            dump(OUT/f'raw/source_seed{seed}_r{rounds}_{year}.json',
                 {'year':year,'seed':seed,'checkpoint':rounds,'training_meta':original,
                  'source_prediction':str(path),'source_model':str(model),
                  'prediction_sha256':sha(path),'model_sha256':sha(model),
                  'same_training_keys_and_labels':True,'inherited_model_reload_bit_identical':True},immutable=True)
    log('10 source arrays and5 fold models verified; no new training')


class Context(previous.Context):
    rerank_weight=0.0

    def __init__(self):
        super().__init__()
        self.scoring=OUT/'scoring_validation_only'
        self.scoring.mkdir(exist_ok=True)
        for name,cols in [('测试集_X.csv',KEYS+['flag_limit_up']),('测试集_Y.csv',KEYS+['y_ret_1d'])]:
            if not (self.scoring/name).exists():
                self.frame.select(cols).write_csv(self.scoring/name,float_precision=17)

    def finished(self,name,recipe=None):
        import numpy as np
        assert name=='baseline'
        path=OUT/'promote_baseline.npy'
        if not path.exists():
            assert recipe==read(PREVIOUS/'selection.json')['winner']['recipe']
            np.save(path,np.load(PREVIOUS/'promote_baseline.npy'))
        return np.load(path)

    def donor(self,promote,rerank_weight=None):
        import numpy as np
        from optimize_wave15 import weighted_rank_blend
        from optimize_wave18 import lift
        weight=self.rerank_weight if rerank_weight is None else rerank_weight
        assert 0<=weight<=1
        if weight==0:return super().donor(promote)
        reranker=weighted_rank_blend([self.slow_finished,self.w5a],[1-weight,weight],
                    self.ranks,self.valid,self.dates,('membership_slow','w5a'))
        reranker=np.where(reranker>-9,reranker+1e-9*self.tie_key,reranker)
        promote=np.where(np.isfinite(promote)&(promote>-9),promote+1e-9*self.tie_key,promote)
        return lift(promote,reranker,self.pdf)[0]


def score_record(ctx,recipe,rerank_weight,weight=0.24,retention=0.9845,delta=0.095):
    donor=ctx.donor(ctx.finished('baseline',recipe),rerank_weight)
    pred,stats=ctx.predict(donor,weight,retention,delta)
    metrics=ctx.score(pred)
    log(f'membershipW5a={rerank_weight:g} orderSlow={weight:g} retain={retention:g} shift={delta:g}: '
        f'{metrics["final_score"]:.9f}, gain={metrics["final_score"]-EXPECTED:+.9f}')
    return {'donor':'baseline','recipe':recipe,'membership_w5a_weight':rerank_weight,
            'slow16_weight':weight,'retention':retention,'limit_up_delta':delta,
            'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}


def prefix_controls(ctx,promote):
    import numpy as np
    proofs=[]
    for weight in (0.0,0.20,1.0):
        full,_=ctx.predict(ctx.donor(promote,weight),0.24,0.9845,0.095)
        for count in (80,260):
            last=np.unique(ctx.dates)[count-1]
            n=int(np.searchsorted(ctx.dates,last,side='right'))
            prefix=Context.__new__(Context)
            for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):
                setattr(prefix,name,getattr(ctx,name)[:n])
            prefix.n_codes=ctx.n_codes
            prefix.pdf=ctx.pdf.iloc[:n]
            prefix.ranks={key:value[:n] for key,value in ctx.ranks.items()}
            pred,_=prefix.predict(prefix.donor(promote[:n],weight),0.24,0.9845,0.095)
            assert np.array_equal(pred,full[:n]),(weight,last)
            proofs.append({'membership_w5a_weight':weight,'days':count,'through_date':int(last),'bit_identical':True})
    dump(OUT/'consensus_prefix_controls.json',{'status':'passed','test_data_read':False,'label_free_prediction_controls':proofs},immutable=True)
    log('Six prefix controls passed, including nonzero and pureW5a membership reranking')


def rerank():
    import numpy as np
    verify()
    ctx=Context()
    recipe=read(PREVIOUS/'selection.json')['winner']['recipe']
    promote=ctx.finished('baseline',recipe)
    prefix_controls(ctx,promote)
    pred,_=ctx.predict(ctx.donor(promote,0),0.24,0.9845,0.095)
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    path=OUT/'wave56_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    for weight in RERANK_WEIGHTS:
        name=f'membership_w5a{weight:g}'
        if name in result['results']:continue
        result['results'][name]=score_record(ctx,recipe,weight)
        if weight==0:assert abs(result['results'][name]['connected_final_score']-EXPECTED)<1e-12
        dump(path,result)
    result.update(status='complete',baseline_bit_identical=True)
    dump(path,result)


def fine():
    verify()
    coarse=read(OUT/'wave56_results.json')
    assert coarse['status']=='complete'
    best=max(coarse['results'].values(),key=lambda r:r['connected_final_score'])
    dump(OUT/'fine_rerank_protocol.json',{'winner_before_refinement':best,'weight_deltas':FINE_DELTAS},immutable=True)
    ctx=Context()
    path=OUT/'wave57_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    for delta in FINE_DELTAS:
        name=f'fine_delta{delta:+g}'
        if name in result['results']:continue
        weight=min(1,max(0,best['membership_w5a_weight']+delta))
        result['results'][name]=score_record(ctx,best['recipe'],weight)
        dump(path,result)
    result['status']='complete'
    dump(path,result)


def refine():
    verify()
    items=[]
    for wave in (56,57):
        records=read(OUT/f'wave{wave}_results.json')
        assert records['status']=='complete'
        items+=list(records['results'].values())
    best=max(items,key=lambda r:r['connected_final_score'])
    dump(OUT/'refinement_protocol.json',{'winner_before_output':best,'slow_weights':SLOW_WEIGHTS,
         'retention':RETENTION,'limit_up_deltas':LIMIT_SHIFTS},immutable=True)
    ctx=Context()
    path=OUT/'wave58_results.json'
    result=read(path) if path.exists() else {'status':'running','results':{}}
    for weight,retention in itertools.product(SLOW_WEIGHTS,RETENTION):
        name=f'order_w{weight:g}_m{retention:g}'
        if name in result['results']:continue
        result['results'][name]=score_record(ctx,best['recipe'],best['membership_w5a_weight'],weight,retention)
        dump(path,result)
    refined=max(result['results'].values(),key=lambda r:r['connected_final_score'])
    for delta in LIMIT_SHIFTS:
        name=f'limit_shift{delta:g}'
        if name in result['results']:continue
        result['results'][name]=score_record(ctx,best['recipe'],best['membership_w5a_weight'],
                            refined['slow16_weight'],refined['retention'],delta)
        dump(path,result)
    result['status']='complete'
    dump(path,result)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=('freeze','provenance','rerank','fine','refine','all'))
    stage=parser.parse_args().stage
    for name in (('freeze','provenance','rerank','fine','refine') if stage=='all' else (stage,)):
        globals()[name]()

if __name__=='__main__':main()
