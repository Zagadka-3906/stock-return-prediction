"""Actual frozen-model inference for explicit whole-scheme recipe graphs."""
from copy import deepcopy
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
from whole_scheme_replay_runtime_20261004 import ValidationContext,CompactContext,slice_context
from replay_complete_scheme_20261003 import Context as ReplayContext

FORMAL=ROOT/'deliveries/connected_topk0175_20261003'
KEYS=['ts_code','trade_date']


def graph_native_models(graph):
    root=graph['root'];cfg=root['configuration'];owners={}
    if cfg.get('standalone'):owners[cfg['standalone']['model']]=root['round']
    if root['kind']=='complete_r30':
        groups=('diverse_augmentation','secondary_augmentation','final_augmentation','linear_augmentation')
        for group in groups:
            if cfg.get('standalone') and group in groups[:2]:continue
            for spec in cfg[group].values():
                if spec['weight']>0:owners.setdefault(spec['model'],root['round'])
    for layer in graph['layers']:
        for spec in layer['specs'].values():
            if spec['weight']>0:owners.setdefault(spec['model'],layer['round'])
    return owners


def candidate_models(candidate):
    import json
    return json.loads((Path(candidate)/'verification.json').read_text(encoding='utf-8'))['models']


def resolve_native_sources(graph,candidate_overrides=None):
    overrides=candidate_overrides or {};result={}
    for name,number in graph_native_models(graph).items():
        candidate=Path(overrides.get(number,ROOT/f'candidates/optimization_20261003_r{number}'))
        matches=[info for key,info in candidate_models(candidate).items()
                 if key.endswith('_'+name) and Path(info['path']).suffix=='.joblib']
        assert matches,(name,number,candidate)
        assert len({info['sha256'] for info in matches})==1,(name,number)
        result[name]=deepcopy(matches[0])
    return result


class FutureContext(ValidationContext):
    def configure(self,configuration):
        graph=deepcopy(configuration['whole_scheme_graph'])
        assert graph['root']['kind']==self._whole_graph['root']['kind']
        self._whole_graph=graph
        cfg=graph['root']['configuration']
        if graph['root']['kind']=='complete_r30':
            for field in ('diverse_augmentation','secondary_augmentation','final_augmentation',
                          'linear_augmentation','final_limit_delta','linear_limit_delta','standalone'):
                setattr(self._whole_base,field,deepcopy(cfg[field]))

    def root_context(self):
        n=len(self.dates)
        if n==len(self._whole_base.dates):return self._whole_base
        base=slice_context(self._whole_base,n,cold=False)
        base._diverse_cache={name:(values[:n],ranks[:n]) for name,(values,ranks) in self._whole_base._diverse_cache.items()}
        base._final_cache={name:values[:n] for name,values in self._whole_base._final_cache.items()}
        base._regime_cache={name:values[:n] for name,values in self._whole_base._regime_cache.items()}
        return base

    def finished(self,name,recipe=None):
        assert name=='baseline'
        return self._whole_promote[:len(self.dates)]

    def signal(self,name):
        return self._whole_signal_cache[name][:len(self.dates)]

    def weights_for(self,spec):
        if not spec.get('regime'):return spec['weight']
        values=self._whole_regime_cache[spec['regime']][:len(self.dates)]
        return (spec['low']+(spec['high']-spec['low'])*values)*(spec['weight']/max(spec['low'],spec['high']))


def build_context(graph,inputs,test,model_sources,root_models,state_mappings,reload_controls=True):
    import polars as pl
    import lightgbm as lgb
    from src.scoring import Panel
    from experiments.final_sweep_wave3 import ensemble_raw
    from optimize_training_round7 import ENSEMBLES
    from optimize_training_round30 import BASE_POST,HERE,ARCHIVE,weights_from_name
    from optimize_wave6 import make_prediction_param
    from optimize_wave15 import daily_ranks
    from run import to_matrix
    import fourier_tuning_model_sources_20261004 as trainer
    import build_market_regime_bank_20261003 as regime
    from verify_role_layer_replay_20261004 import sha
    assert test.select(KEYS).equals(inputs.select(KEYS))
    assert 'y_ret_1d' not in inputs.columns and 'y_rank' not in inputs.columns
    features=list(test.columns[2:]);vx=to_matrix(test,features)
    frame=inputs.with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    compact=CompactContext(frame);dates=compact.dates;valid=compact.valid
    cfg=graph['root']['configuration']
    raw_new={};model_checks=[]
    for name,info in model_sources.items():
        source=Path(info['path']);assert sha(source)==info['sha256']
        training=info['training_info']['training_meta']
        assert training['last']<training['cutoff_exclusive'] and training['last_label_end']<=training['cutoff_exclusive']
        assert training['features']==features
        raw=trainer.predict_arrays(trainer.load_bundle(source),vx,dates=dates,valid=valid)
        assert len(raw)==len(inputs) and np.isfinite(raw).all()
        if reload_controls:
            replay=trainer.predict_arrays(trainer.load_bundle(source),vx,dates=dates,valid=valid)
            assert np.array_equal(raw,replay),name
        raw[~valid]=-1e6;raw_new[name]=raw
        model_checks.append({'name':name,'sha256':info['sha256'],'reload_exact':reload_controls})
    panel=Panel.from_frame(frame)
    aux=inputs['aux_raw'].to_numpy()
    def process(raw,settings):
        return make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw))),aux,**settings)
    states=regime.future_values(state_mappings,test.select(KEYS+['RET1','RVOL20']).with_columns(inputs['price_valid'])) if state_mappings else {}
    if graph['root']['kind']=='standalone':
        base=compact
        promote=process(raw_new[cfg['standalone']['model']],cfg['standalone']['postprocessing'])
    else:
        assert graph['root']['kind']=='complete_r30'
        base=ReplayContext.__new__(ReplayContext);base.__dict__.update(compact.__dict__)
        paths={'lgb':ARCHIVE/'releases/pooled_rms25/backbone_raw.parquet',
               'xgb':ARCHIVE/'releases/ensemble4/T2f_xgboost_test_raw.parquet',
               'two':ARCHIVE/'releases/ensemble4/W2c_two_day_test_raw.parquet',
               'pruned':ARCHIVE/'releases/ensemble4/W2d_pruned_test_raw.parquet',
               'gru':HERE/'w5a_test/gru_raw_test.npy'}
        members={}
        for name,path in paths.items():
            if path.suffix=='.npy':values=np.load(path,mmap_mode='r')[:len(inputs)].astype(np.float64)
            else:
                member=pl.read_parquet(path).sort('trade_date','ts_code').head(len(inputs))
                assert member.select(KEYS).equals(inputs.select(KEYS))
                values=member['pred_raw'].to_numpy().astype(np.float64)
            members[name]=values
        assert np.array_equal(ensemble_raw(panel,ENSEMBLES['five_fold_local'],members),inputs['w5a_raw'].to_numpy())
        for key in ('ensemble_name','top_ensemble_name','membership_ensemble_name'):assert 'pruned' not in cfg[key]
        base.ensemble_name=base.rest_ensemble_name=cfg['ensemble_name'];base.top_ensemble_name=cfg['top_ensemble_name']
        for key in ('membership_mode','top_slow_weight','add_priority_weight','drop_priority_weight',
                    'priority_signal','membership_signal','membership_ensemble_name','membership_slow_weight',
                    'membership_power','membership_memory'):
            setattr(base,key,cfg[key])
        base.rerank_weight=cfg['membership_w5a_weight'];base.rest_slow_weight=cfg['slow16_weight']
        base.slow_finished=inputs['rank_score'].to_numpy()
        base.w5a=process(ensemble_raw(panel,weights_from_name(cfg['ensemble_name']),members),dict(BASE_POST,alpha=0,bonus=0))
        split=cfg['top_ensemble_name']!=cfg['ensemble_name']
        base.top_values=base.w5a if not split else process(ensemble_raw(panel,weights_from_name(cfg['top_ensemble_name']),members),dict(BASE_POST,alpha=0,bonus=0))
        base.membership_values=base.top_values if cfg['membership_ensemble_name']==cfg['top_ensemble_name'] else (base.w5a if cfg['membership_ensemble_name']==cfg['ensemble_name'] else process(ensemble_raw(panel,weights_from_name(cfg['membership_ensemble_name']),members),dict(BASE_POST,alpha=0,bonus=0)))
        base.slow=process(inputs['pred_raw'].to_numpy(),dict(BASE_POST,alpha=0,bonus=0))
        base.ranks={'w5a':daily_ranks(base.w5a,valid,dates),'slow':daily_ranks(base.slow,valid,dates)}
        base.top_ranks=base.ranks['w5a'] if not split else daily_ranks(base.top_values,valid,dates)
        base.membership_ranks=daily_ranks(base.membership_values,valid,dates)
        base._diverse_cache={name:(values,daily_ranks(values,valid,dates))
            for name,raw in raw_new.items() for values in (process(raw,dict(BASE_POST,alpha=0,bonus=0)),)}
        base._final_cache={name:daily_ranks(raw,valid,dates) for name,raw in raw_new.items()}
        base._regime_cache=states
        for field in ('diverse_augmentation','secondary_augmentation','final_augmentation',
                      'linear_augmentation','final_limit_delta','linear_limit_delta','standalone'):
            setattr(base,field,deepcopy(cfg[field]))
        if cfg['standalone']:
            promote=process(raw_new[cfg['standalone']['model']],cfg['standalone']['postprocessing'])
        else:
            mixed=np.zeros(len(inputs))
            for component in cfg['recipe']['components']:
                name=f'seed{component["seed"]}_f{component["fraction"]:.3f}_r{component["rounds"]}'
                info=root_models[name];source=Path(info['path']);assert sha(source)==info['sha256']
                text=source.read_text(encoding='utf-8')
                raw=lgb.Booster(model_str=text).predict(vx,num_threads=8);raw[~valid]=-1e6
                if reload_controls:
                    replay=lgb.Booster(model_str=text).predict(vx,num_threads=8);replay[~valid]=-1e6
                    assert np.array_equal(raw,replay)
                mixed+=component['weight']*daily_ranks(raw,valid,dates)
                model_checks.append({'name':name,'sha256':info['sha256'],'reload_exact':reload_controls})
            mixed[~valid]=-10.
            promote=process(mixed,cfg['recipe']['postprocessing'])
    context=FutureContext.__new__(FutureContext);context.__dict__.update(base.__dict__)
    context._whole_graph=deepcopy(graph);context._whole_base=base;context._whole_promote=promote
    context._whole_signal_cache={name:daily_ranks(raw,valid,dates) for name,raw in raw_new.items()}
    context._whole_regime_cache=states;context._whole_paths={}
    context.configure({'whole_scheme_graph':graph})
    return context,model_checks


def copy_models(native_sources,root_sources,destination):
    from verify_role_layer_replay_20261004 import sha
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    copied={}
    for key,info in {**root_sources,**{'whole_'+name:value for name,value in native_sources.items()}}.items():
        source=Path(info['path']);assert sha(source)==info['sha256']
        target=destination/source.name
        if target.exists():assert sha(target)==info['sha256'],target
        else:shutil.copyfile(source,target)
        assert sha(target)==info['sha256']
        copied[key]={**deepcopy(info),'path':str(target),'whole_graph_source':str(source)}
    return copied
