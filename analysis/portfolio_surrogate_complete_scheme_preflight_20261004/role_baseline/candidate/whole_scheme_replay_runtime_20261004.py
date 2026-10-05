"""Recompute an explicit selected root and all surviving downstream layers."""
from copy import copy,deepcopy
from pathlib import Path
import os
import sys
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[variable]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
from role_layer_replay_20261004 import replay_layers
from final_output_temporal_postprocessing_20261004 import transform as temporal_transform

META_ARRAYS=('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow',
             'top_values','top_ranks','membership_values','membership_ranks')


def slice_context(context,n,cold=False):
    prefix=copy(context)
    for name in META_ARRAYS:
        if hasattr(context,name):setattr(prefix,name,getattr(context,name)[:n])
    for name in ('frame','label_free'):
        if hasattr(context,name):setattr(prefix,name,getattr(context,name).head(n))
    if hasattr(context,'pdf'):prefix.pdf=context.pdf.iloc[:n]
    if hasattr(context,'ranks'):prefix.ranks={key:values[:n] for key,values in context.ranks.items()}
    if cold:
        for name in ('_diverse_cache','_final_cache','_regime_cache','_whole_signal_cache','_whole_regime_cache'):
            setattr(prefix,name,{})
    return prefix


def raw_sources(graph):
    sources={}
    def add(name,number):
        path=ROOT/f'analysis/optimization_20261003_r{number}/raw/{name}.npy'
        sources.setdefault(name,[])
        if path not in sources[name]:sources[name].append(path)
    root=graph['root']
    if root['kind']=='standalone':add(root['configuration']['standalone']['model'],root['round'])
    for layer in graph['layers']:
        for spec in layer['specs'].values():
            if spec['weight']>0:add(spec['model'],layer['round'])
    return sources


class CompactContext:
    def __init__(self,frame):
        import pandas as pd
        import polars as pl
        self.frame=frame
        self.label_free=frame.with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
        self.dates=frame['trade_date'].to_numpy()
        self.flags=frame['flag_limit_up'].to_numpy().astype(np.int64)
        self.valid=frame['price_valid'].to_numpy()
        self.codes,symbols=pd.factorize(frame['ts_code'].to_numpy(),sort=True)
        self.codes=self.codes.astype(np.int64);self.n_codes=len(symbols)
        self.tie_key=1.-self.codes/max(self.n_codes-1,1)
        self.pdf=frame.select('trade_date','flag_limit_up').to_pandas()
        self.slow_finished=self.w5a=self.slow=np.zeros(len(frame));self.ranks={}


class ValidationContext:
    def __init__(self,graph,scoring=None,paths=None):
        import polars as pl
        self._whole_graph=deepcopy(graph)
        if graph['root']['kind']=='complete_r30':
            from replay_complete_scheme_20261003 import Context as RootContext
            base=RootContext();base.configure(graph['root']['configuration'])
        else:
            assert graph['root']['kind']=='standalone'
            frame=pl.read_parquet(ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet',
                columns=['ts_code','trade_date','price_valid','flag_limit_up','aux_raw','y_ret_1d'])
            base=CompactContext(frame)
        self._whole_base=base
        self._whole_paths=deepcopy(paths) if paths is not None else {name:values[0] for name,values in raw_sources(graph).items()}
        self._whole_signal_cache={};self._whole_regime_cache={}
        for name in META_ARRAYS+('n_codes','frame','label_free','pdf','ranks'):
            if hasattr(base,name):setattr(self,name,getattr(base,name))
        if scoring is not None:self.scoring=Path(scoring)
        self.configure({'whole_scheme_graph':graph})

    def configure(self,configuration):
        graph=deepcopy(configuration['whole_scheme_graph'])
        assert graph['root']['kind']==self._whole_graph['root']['kind']
        assert graph['root']['round']==self._whole_graph['root']['round']
        self._whole_graph=graph
        if graph['root']['kind']=='complete_r30':
            self._whole_base.configure(graph['root']['configuration'])

    def root_context(self):
        n=len(self.dates)
        base=self._whole_base
        if n!=len(base.dates):base=slice_context(base,n,cold=True)
        if self._whole_graph['root']['kind']=='complete_r30':
            base.configure(self._whole_graph['root']['configuration'])
        return base

    def finished(self,name,recipe=None):
        assert name=='baseline'
        base=self.root_context()
        root=self._whole_graph['root'];cfg=root['configuration']
        if root['kind']=='complete_r30':return base.finished(name)
        import polars as pl
        from src.scoring import Panel
        from optimize_wave6 import make_prediction_param
        frame=self.label_free.head(len(self.dates))
        raw=np.load(self._whole_paths[cfg['standalone']['model']],mmap_mode='r')[:len(frame)]
        return make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw))),
                                     frame['aux_raw'].to_numpy(),**cfg['standalone']['postprocessing'])

    def promote(self,name):return self.finished(name)

    def donor(self,promote,rerank_weight=None):
        if self._whole_graph['root']['kind']=='standalone':return promote
        return self.root_context().donor(promote)

    def signal(self,name):
        from optimize_wave15 import daily_ranks
        n=len(self.dates)
        if name not in self._whole_signal_cache or len(self._whole_signal_cache[name])<n:
            raw=np.load(self._whole_paths[name],mmap_mode='r')[:n]
            assert len(raw)==n
            self._whole_signal_cache[name]=daily_ranks(raw,self.valid,self.dates)
        return self._whole_signal_cache[name][:n]

    def weights_for(self,spec):
        if not spec.get('regime'):return spec['weight']
        name=spec['regime'];n=len(self.dates)
        if name not in self._whole_regime_cache or len(self._whole_regime_cache[name])<n:
            self._whole_regime_cache[name]=np.load(ROOT/f'analysis/market_regime_bank_20261003/{name}.npy',mmap_mode='r')[:n]
        return (spec['low']+(spec['high']-spec['low'])*self._whole_regime_cache[name][:n])*(spec['weight']/max(spec['low'],spec['high']))

    def root_prediction(self,donor):
        root=self._whole_graph['root'];cfg=root['configuration']
        if root['kind']=='complete_r30':
            base=self.root_context()
            return base.predict(donor,cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        from optimize_wave13 import build_ab
        ordered=np.where(donor>-9,donor+1e-9*self.tie_key,donor)
        pred,stats=build_ab(ordered,ordered,ordered,self.dates,self.flags,self.codes,self.n_codes,cfg['retention'])
        pred[self.flags==1]+=cfg['limit_up_delta']
        return pred,stats

    def predict(self,donor,weight,retention,delta=0.):
        # Legacy calibration passes the last flat recipe parameters here.
        # The explicit graph is authoritative for each historical root/layer.
        base,root_stats=self.root_prediction(donor)
        pred,layer_stats=replay_layers(self,base,self._whole_graph['layers'])
        temporal=self._whole_graph['temporal_postprocessing']
        if temporal is not None:pred=temporal_transform(pred,self.dates,self.valid,self.codes,temporal)
        return pred,{'whole_selected_scheme_recomputed':True,'root_round':self._whole_graph['root']['round'],
                     'root':root_stats,'layers':layer_stats,'temporal_postprocessing':deepcopy(temporal)}

    def score(self,pred):
        from score_calibrated_candidates_20261003 import score
        return score(self,pred)


def prefix_controls(context,graph,counts=(80,260,975)):
    import polars as pl
    context.configure({'whole_scheme_graph':graph})
    pred,_=context.predict(context.donor(context.finished('baseline')),0.,0.)
    poisoned=copy(context)
    poisoned.frame=context.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    poisoned._whole_base=copy(context._whole_base)
    poisoned._whole_base.frame=context._whole_base.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
    assert np.array_equal(pred,poisoned.predict(poisoned.donor(poisoned.finished('baseline')),0.,0.)[0])
    dates=np.unique(context.dates);prefixes=[]
    for count in counts:
        n=int(np.searchsorted(context.dates,dates[count-1],side='right'))
        prefix=slice_context(context,n,cold=True)
        result,_=prefix.predict(prefix.donor(prefix.finished('baseline')),0.,0.)
        assert np.array_equal(pred[:n],result),(count,graph['root']['kind'])
        prefixes.append({'days':count,'root_and_late_signal_caches_cold':True,'bit_identical':True})
    return {'label_poisoning_bit_identical':True,'prefixes':prefixes,
            'root_round':graph['root']['round'],'layer_rounds':[node['round'] for node in graph['layers']]}
