"""Recompute every active layer so later refinement can change earlier weights."""
from copy import deepcopy
from pathlib import Path
import numpy as np
from optimize_training_round18 import Context as HybridContext,ROOT,YEARS,BASE_POST,read
from optimize_training_round25 import Context as FinalOutputContext
from optimize_training_round29 import Context as LinearOutputContext
from optimize_wave15 import daily_ranks
from optimize_wave13 import build_ab
ROLES=('membership','top','rest')
ORIGINAL=ROOT/'analysis/optimization_20261003_r18'


def empty_roles():return {role:{'model':'none','weight':0.} for role in ROLES}


class Context(HybridContext):
    replay_folder=ROOT/'analysis/complete_scheme_replay_20261003'

    def configure(self,cfg):
        super().configure(cfg)
        n=len(self.dates)
        # Older role loaders retain full-fold caches; inference may be a date prefix.
        for name in ('w5a','top_values','top_ranks','membership_values','membership_ranks'):
            if hasattr(self,name):setattr(self,name,getattr(self,name)[:n])
        self.ranks={name:values[:n] for name,values in self.ranks.items()}
        self.standalone=deepcopy(cfg.get('standalone'))
        self.secondary_augmentation=deepcopy(cfg.get('secondary_augmentation',empty_roles()))
        self.final_augmentation=deepcopy(cfg.get('final_augmentation',empty_roles()))
        self.final_limit_delta=cfg.get('final_limit_delta',0.)
        self.linear_augmentation=deepcopy(cfg.get('linear_augmentation',empty_roles()))
        self.linear_limit_delta=cfg.get('linear_limit_delta',0.)
        if not hasattr(self,'_final_cache'):self._final_cache={}
        if not hasattr(self,'_regime_cache'):self._regime_cache={}

    def score(self,pred):
        from score_calibrated_candidates_20261003 import score
        return score(self,pred)

    def finished(self,name,recipe=None):
        import polars as pl
        from optimize_wave6 import make_prediction_param
        from src.scoring import Panel
        assert name=='baseline'
        if not self.standalone:
            if recipe is not None:assert recipe==read(ORIGINAL/'selection.json')['winner']['recipe']
            return np.load(ORIGINAL/'promote_baseline.npy',mmap_mode='r')[:len(self.dates)]
        frame=self.label_free.head(len(self.dates))
        raw=np.load(self.replay_folder/f'raw/{self.standalone["model"]}.npy',mmap_mode='r')[:len(frame)]
        return make_prediction_param(Panel.from_frame(frame.with_columns(pl.Series('pred_raw',raw))),
                                     frame['aux_raw'].to_numpy(),**self.standalone['postprocessing'])

    def augment(self,base,role):
        for specs in (self.diverse_augmentation,self.secondary_augmentation):
            spec=specs[role];weight=spec['weight']
            if weight==0:continue
            assert 0<weight<=1
            name=spec['model'];n=len(self.dates)
            if name not in self._diverse_cache or len(self._diverse_cache[name][1])<n:
                values=np.load(self.replay_folder/f'rankers/{name}.npy',mmap_mode='r')[:n]
                self._diverse_cache[name]=(values,daily_ranks(values,self.valid,self.dates))
            other=self._diverse_cache[name][1][:n]
            if spec.get('blend','rank')=='rank':
                current=daily_ranks(base,self.valid,self.dates);valid=(other>-9)&(current>-9)
                out=np.full(n,-10.);out[valid]=(1-weight)*current[valid]+weight*other[valid]
                base=np.where(out>-9,out+1e-9*self.tie_key,out)+1e-9*self.tie_key
            else:
                assert spec['blend']=='score';valid=(other>-9)&(base>-9)
                out=np.full(n,-10.);out[valid]=(1-weight)*base[valid]+weight*other[valid]+weight*1e-9*self.tie_key[valid]
                base=out
        return base

    def donor(self,promote,rerank_weight=None):
        return promote if self.standalone else super().donor(promote,rerank_weight)

    def signal(self,name):
        n=len(self.dates)
        if name not in self._final_cache or len(self._final_cache[name])<n:
            values=np.load(self.replay_folder/f'raw/{name}.npy',mmap_mode='r')[:n]
            self._final_cache[name]=daily_ranks(values,self.valid,self.dates)
        return self._final_cache[name][:n]

    def weights_for(self,spec):
        if not spec.get('regime'):return spec['weight']
        import build_market_regime_bank_20261003 as regime
        name=spec['regime'];assert name in regime.NAMES
        if name not in self._regime_cache or len(self._regime_cache[name])<len(self.dates):
            self._regime_cache[name]=np.load(regime.OUT/f'{name}.npy',mmap_mode='r')[:len(self.dates)]
        maximum=max(spec['low'],spec['high']);assert maximum>0
        state=self._regime_cache[name][:len(self.dates)]
        return (spec['low']+(spec['high']-spec['low'])*state)*(spec['weight']/maximum)

    def predict(self,donor,weight,retention,delta=0.):
        if self.standalone:
            ordered=np.where(donor>-9,donor+1e-9*self.tie_key,donor)
            base,original=build_ab(ordered,ordered,ordered,self.dates,self.flags,self.codes,self.n_codes,retention)
            base[self.flags==1]+=delta
        else:base,original=super().predict(donor,weight,retention,delta)
        final,final_stats=FinalOutputContext.finish_output(self,base,retention,delta)
        linear,linear_stats=LinearOutputContext.finish_output(self,final,retention,delta+self.final_limit_delta)
        return linear,{'foundation':original,'final_augmentation':final_stats,'linear_augmentation':linear_stats}


def prefix_controls(ctx,cfg,counts=(80,260,975)):
    from copy import copy
    from optimize_training_round28 import prefix_controls as inherited_controls
    proof=inherited_controls(ctx,cfg,counts)
    ctx.configure(cfg);promote=ctx.finished('baseline')
    full,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    dates=np.unique(ctx.dates);cold=[]
    for count in counts:
        last=int(dates[count-1]);n=int(np.searchsorted(ctx.dates,last,side='right'));prefix=copy(ctx)
        for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):
            setattr(prefix,name,getattr(ctx,name)[:n])
        prefix.frame=ctx.frame.head(n);prefix.label_free=ctx.label_free.head(n);prefix.pdf=ctx.pdf.iloc[:n]
        prefix.ranks={key:values[:n] for key,values in ctx.ranks.items()}
        prefix._diverse_cache={};prefix._final_cache={};prefix._regime_cache={}
        prefix.configure(cfg);fresh=prefix.finished('baseline')
        result,_=prefix.predict(prefix.donor(fresh),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        assert np.array_equal(full[:n],result),(last,cfg.get('standalone'))
        cold.append({'days':count,'through_date':last,'new_model_signal_and_regime_caches_empty':True,'bit_identical':True})
    return {**proof,'cold_prefix_controls':cold}
