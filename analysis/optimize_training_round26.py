"""Waves131–134: past-normalized current-market-state role fusion."""
from copy import deepcopy
import itertools
import os
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round25 as previous
import build_market_regime_bank_20261003 as regime
from optimize_training_round25 import HERE,YEARS,KEYS,BASE_POST,ARCHIVE,RANKERS,read,dump,sha,log,weights_from_name,trainer,MODELS,ROLES
OUT=ROOT/'analysis/optimization_20261003_r26'
PREVIOUS=ROOT/'analysis/optimization_20261003_r25'
FOUNDATION=ROOT/'analysis/optimization_20261003_r24'
WAVES=(131,132,133,134)
FIELDS=previous.FIELDS
NEW_MODELS=()
PATTERNS=((0.,.05),(0.,.1),(0.,.2),(.05,0.),(.1,0.),(.2,0.))
configuration,signature,best=previous.configuration,previous.signature,previous.best


def baseline():return previous.configuration(read(PREVIOUS/'selection.json')['winner'])
def expected():return read(PREVIOUS/'selection.json')['winner']['connected_final_score']


def proposals():
    if (OUT/'protocol.json').exists():return read(OUT/'protocol.json')['proposal_models_by_role']
    rows=read(PREVIOUS/'wave127_results.json')['results'];scores={role:{} for role in ROLES}
    for key,row in rows.items():
        for role in ROLES:
            if key.startswith(role+'_'):
                spec=row['final_augmentation'][role];name=spec['model']
                scores[role][name]=max(scores[role].get(name,float('-inf')),row['connected_final_score'])
    result={role:sorted(scores[role],key=lambda name:(-scores[role][name],name))[:4] for role in ROLES}
    assert all(len(names)==4 for names in result.values());return result


class Context(previous.Context):
    def __init__(self):
        super().__init__();self.scoring=OUT/'scoring_validation_only';self.scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(PREVIOUS/'scoring_validation_only'/name,self.scoring/name)
        self.configure(baseline())

    def configure(self,cfg):
        super().configure(cfg)
        if not hasattr(self,'_regime_cache'):self._regime_cache={}

    def weights_for(self,spec):
        import numpy as np
        name=spec.get('regime')
        if not name:return super().weights_for(spec)
        assert name in regime.NAMES;maximum=max(spec['low'],spec['high']);assert maximum>0
        if name not in self._regime_cache or len(self._regime_cache[name])<len(self.dates):
            self._regime_cache[name]=np.load(regime.OUT/f'{name}.npy',mmap_mode='r')[:len(self.dates)]
        values=self._regime_cache[name][:len(self.dates)]
        return (spec['low']+(spec['high']-spec['low'])*values)*(spec['weight']/maximum)


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    from finalize_training_round25 import selected
    selected();regime.verify();assert read(regime.OUT/'oof_audit.json')['status']=='passed'
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/finalize_training_round26.py',ROOT/'analysis/verify_methods_round26.py',
             ROOT/'analysis/run_training_round26_pipeline.py',ROOT/'analysis/predict_final_roles_round26.py',
             ROOT/'analysis/preflight_market_regimes_round26.py',ROOT/'analysis/market_regimes_round26_preflight/verification.json',
             Path(regime.__file__),regime.OUT/'protocol.json',regime.OUT/'oof_audit.json',
             PREVIOUS/'selection.json',PREVIOUS/'protocol.json',PREVIOUS/'component_audit.json',
             PREVIOUS/'final_role_causal_checks.json',PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',
             ROOT/'candidates/optimization_20261003_r25/verification.json',ROOT/'active_release.json']
    sources += [ROOT/'analysis/official_validation_csv_parse_cache_20261003.py',
                ROOT/'analysis/validation_parse_cache_qa_20261003/verification.json',
                ROOT/'analysis/verify_validation_parse_cache_20261003.py',
                ROOT/'analysis/validation_parse_cache_full_oof_qa_20261003/verification.json',
                ROOT/'analysis/verify_prospective_score_wrappers_20261003.py',
                ROOT/'analysis/prospective_score_wrappers_qa_20261003/verification.json']
    sources += [ROOT/'analysis/cross_round_official_score_reuse_20261003.py',
                ROOT/'analysis/verify_cross_round_official_reuse_20261003.py',
                ROOT/'analysis/cross_round_official_reuse_qa_20261003/verification.json',
                ROOT/'analysis/verify_mapped_cross_round_reuse_20261003.py',
                ROOT/'analysis/mapped_cross_round_reuse_qa_20261003/verification.json']
    sources += [ROOT/'analysis/parallel_candidate_scoring_20261004.py',
                ROOT/'analysis/parallel_scoring_qa_context_20261004.py',
                ROOT/'analysis/verify_parallel_candidate_scoring_20261004.py',
                ROOT/'analysis/parallel_candidate_scoring_qa_20261004/verification.json']
    sources += [ROOT/'analysis/parallel_candidate_scoring_four_20261004.py',
                ROOT/'analysis/parallel_scoring_four_qa_context_20261004.py',
                ROOT/'analysis/verify_parallel_candidate_scoring_four_20261004.py',
                ROOT/'analysis/parallel_candidate_scoring_four_qa_20261004/verification.json',
                ROOT/'analysis/verify_official_parallel_capacity_20261004.py',
                ROOT/'analysis/official_parallel_capacity_qa_20261004/verification.json',
                ROOT/'analysis/prospective_parallel_four_adoption_20261004/verification.json']
    sources.extend(Path(p) for p in read(PREVIOUS/'protocol.json')['input_sha256'])
    sources.extend(Path(p) for p in read(regime.OUT/'oof_audit.json')['output_sha256'])
    sources.extend(PREVIOUS/f'raw/{name}.npy' for name in MODELS)
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'baseline_score':expected(),
         'starting_configuration':baseline(),'same_validation':'2020–2024 expanding OOF;1212 continuous days;5635800 rows',
         'proposal_models_by_role':proposals(),'proposal_rule':'Four highest independent complete-output signal scores per role from completed R25; no test-period data.',
         'wave131':{'roles':ROLES,'regimes':regime.NAMES,'low_high_patterns':PATTERNS,'models_per_role':4,'baseline_records':1},
         'wave132':{'baseline_rising_falling_role_combinations':27},
         'wave133':{'maximum_weight_scale_refinement':'zero,half,anchor,double,anchor+0.0125,anchor+0.025','clip':(0.,.8)},
         'wave134':{'additional_limit_shift':(-.04,-.02,0.,.02,.04)},
         'parallel_candidate_execution':{'workers':4,'commit_order':'declared arm order','adaptive_stage_barriers_preserved':True,'private_actual_csv_and_official_capsules':True},
         'expected_scored_records':267,'new_model_training':False,'new_fold_models_trained':0,
         'complete_output_foundation_round':24,'method':'Replace independently selected static final-role weights with weights interpolated from current-day price/volume regimes normalized using past training dates. Scale refinement preserves the declared low/high shape.',
         'selection_rule':'highest official connected composite; exact ties prefer fewer extra models/roles and smaller extra shift',
         'test_labels_read':False,'test_future_prices_used_to_select':False,'pruned_member_excluded':True,
         'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    log('Round26 past-only market-regime fusion protocol frozen')


def prefix_controls(ctx,cfg,counts=(80,260,975)):
    from copy import copy
    import numpy as np
    proof=previous.prefix_controls(ctx,cfg,counts);promote=ctx.finished('baseline')
    pred,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);dates=np.unique(ctx.dates);extra=[]
    for count in counts:
        last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.pdf=ctx.pdf.iloc[:n];prefix.ranks={k:v[:n] for k,v in ctx.ranks.items()};prefix._final_cache={};prefix._regime_cache={}
        replay,_=prefix.predict(prefix.donor(promote[:n]),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta']);assert np.array_equal(pred[:n],replay)
        extra.append({'days':count,'through_date':last,'both_market_state_and_signal_caches_cold':True,'bit_identical':True})
    return {**proof,'cold_market_regime_cache_controls':extra}


def build():
    import numpy as np
    verify()
    if (OUT/'component_audit.json').exists():return
    ctx=Context();base=baseline();promote=ctx.finished('baseline')
    pred,_=ctx.predict(ctx.donor(promote),base['slow16_weight'],base['retention'],base['limit_up_delta']);assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    controls=[]
    for role,name in ((role,names[0]) for role,names in proposals().items()):
        for state,(low,high) in itertools.product(regime.NAMES,((0.,.1),(.1,0.))):
            cfg=deepcopy(base);cfg['final_augmentation'][role]={'model':name,'weight':max(low,high),'regime':state,'low':low,'high':high}
            controls.append(prefix_controls(ctx,cfg,counts=(80,260)))
    dump(OUT/'component_audit.json',{'status':'passed','baseline_complete_output_bit_identical':True,
         'active_method_prefix_and_poisoning_controls':controls,'models_trained':0,'test_data_read':False,
         'regime_audit_sha256':sha(regime.OUT/'oof_audit.json')},immutable=True)
    log('Round26 rising/falling regime controls and exact baseline passed')


def evaluate(ctx,cfg):return previous.evaluate(ctx,cfg)


def execute(wave,arms,ctx=None,finish=True):
    from parallel_candidate_scoring_four_20261004 import evaluate_many
    path=OUT/f'wave{wave}_results.json';payload=read(path) if path.exists() else {'status':'running','results':{}}
    missing=[];seen=set(payload['results'])
    for key,cfg in arms:
        if key not in seen:missing.append((key,cfg));seen.add(key)
    configurations=dict(missing)
    for key,row in evaluate_many('optimize_training_round26',missing,OUT):
        payload['results'][key]=row;dump(path,payload)
        if signature(configurations[key])==signature(baseline()):assert abs(row['connected_final_score']-expected())<1e-12
    if finish:payload['status']='complete';dump(path,payload)
    return payload


def prior_best(waves):return best([r for w in waves for r in read(OUT/f'wave{w}_results.json')['results'].values()])


def independent():
    verify();build();base=baseline();arms=[('baseline',base)]
    for role,state,(low,high) in itertools.product(ROLES,regime.NAMES,PATTERNS):
        for name in proposals()[role]:
            cfg=deepcopy(base);cfg['final_augmentation'][role]={'model':name,'weight':max(low,high),'regime':state,'low':low,'high':high}
            arms.append((f'{role}_{state}_{name}_lo{low:g}_hi{high:g}',cfg))
    execute(131,arms)


def combinations():
    verify();base=baseline();rows=read(OUT/'wave131_results.json')['results'];winners={}
    for role in ROLES:
        winners[role]={direction:best(row for key,row in rows.items() if key.startswith(role+'_') and
            ((row['final_augmentation'][role]['high']>row['final_augmentation'][role]['low'])==(direction=='rising')))
            for direction in ('rising','falling')}
    dump(OUT/'combination_protocol.json',{'independent_role_winners':winners},immutable=True)
    arms=[]
    for choices in itertools.product(('baseline','rising','falling'),repeat=3):
        cfg=deepcopy(base)
        for role,choice in zip(ROLES,choices):
            if choice!='baseline':cfg['final_augmentation'][role]=deepcopy(winners[role][choice]['final_augmentation'][role])
        arms.append(('choices_'+'_'.join(choices),cfg))
    execute(132,arms)


def refine_weights():
    verify();winner=prior_best((131,132));base=configuration(winner);ctx=Context()
    role_winners=read(OUT/'combination_protocol.json')['independent_role_winners']
    dump(OUT/'weight_refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    for role in ROLES:
        spec=deepcopy(base['final_augmentation'][role])
        if spec['weight']==0:spec=deepcopy(best(role_winners[role].values())['final_augmentation'][role])
        anchor=base['final_augmentation'][role]['weight']
        values=[0.,max(0.,anchor*.5),anchor,min(.8,anchor*2),min(.8,anchor+.0125),min(.8,anchor+.025)]
        dump(OUT/f'weight_refinement_{role}_protocol.json',{'anchor':base,'spec':spec,'maximum_weights':values},immutable=True)
        arms=[]
        for index,weight in enumerate(values):
            cfg=deepcopy(base);cfg['final_augmentation'][role]={**spec,'model':spec['model'] if weight>0 else 'none','weight':weight}
            arms.append((f'{role}_{index}_max{weight:g}',cfg))
        payload=execute(133,arms,ctx,False);winner=best([winner]+list(payload['results'].values()));base=configuration(winner)
    execute(133,[],ctx)


def refinement():
    verify();winner=prior_best((131,132,133));base=configuration(winner)
    dump(OUT/'refinement_protocol.json',{'winner_before_refinement':winner},immutable=True)
    execute(134,[(f'extra_shift{value:g}',dict(base,final_limit_delta=value)) for value in (-.04,-.02,0.,.02,.04)])


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','build','independent','combinations','refine_weights','refinement'))
    globals()[parser.parse_args().stage]()
