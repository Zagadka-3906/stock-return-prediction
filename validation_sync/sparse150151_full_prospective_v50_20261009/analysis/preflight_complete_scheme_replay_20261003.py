"""Real-data compatibility and cold-prefix controls for complete-layer recomputation."""
from pathlib import Path
import sys
import time
from copy import deepcopy,copy
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import polars as pl
from finalize_training_round18 import ReleaseContext,selected
import replay_complete_scheme_20261003 as replay
import linear_model_sources_20261003 as models
from optimize_training_round28 import sha,dump
from replay_complete_scheme_20261003 import prefix_controls


def main():
    qa=ROOT/'analysis/complete_scheme_replay_preflight_20261003';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    for folder in ('raw','rankers'):(qa/folder).mkdir(exist_ok=True)
    winner=selected()['winner'];ctx=ReleaseContext(winner)
    original_promote=ctx.finished('baseline')
    frozen=np.load(replay.ORIGINAL/'selected_validation.npy')
    original,_=ctx.predict(ctx.donor(original_promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(original,frozen)
    for name,(values,ranks) in ctx._diverse_cache.items():np.save(qa/f'rankers/{name}.npy',values)
    cfg={**deepcopy(winner),'standalone':None,'secondary_augmentation':replay.empty_roles(),
         'final_augmentation':replay.empty_roles(),'final_limit_delta':0.,
         'linear_augmentation':replay.empty_roles(),'linear_limit_delta':0.}
    ctx.__class__=replay.Context;ctx.replay_folder=qa;ctx._diverse_cache={};ctx.configure(cfg)
    rebuilt,_=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    assert np.array_equal(rebuilt,frozen)
    # Preserve the frozen old configuration; this diagnostic emits no scores.
    baseline_proof=prefix_controls(ctx,cfg)
    dates=np.unique(ctx.dates);n=int(np.searchsorted(ctx.dates,dates[99],side='right'))
    small=copy(ctx)
    for name in ('dates','flags','valid','codes','tie_key','slow_finished','w5a','slow'):
        setattr(small,name,getattr(ctx,name)[:n])
    small.frame=ctx.frame.head(n);small.label_free=ctx.label_free.head(n);small.pdf=ctx.pdf.iloc[:n]
    small.ranks={key:values[:n] for key,values in ctx.ranks.items()}
    small._diverse_cache={};small._final_cache={};small._regime_cache={}
    names=('rank512_e32','rank_ridge_l01','pair_rank128_e32')
    for name in names:
        raw=pl.read_parquet(models.source_dir(name)/'raw_2020.parquet').head(n)
        assert raw.select(['ts_code','trade_date']).equals(small.frame.select(['ts_code','trade_date']))
        np.save(qa/f'raw/{name}.npy',raw['pred_raw'].to_numpy())
    proofs=[]
    for role in replay.ROLES:
        proposal=deepcopy(cfg)
        proposal['final_augmentation'][role]={'model':'rank512_e32','weight':.075,
             'regime':'abs_return','low':0.,'high':.075}
        proposal['linear_augmentation'][role]={'model':'rank_ridge_l01','weight':.025}
        proofs.append(prefix_controls(small,proposal,counts=(20,80)))
    for name in ('rank_ridge_l01','pair_rank128_e32'):
        proposal=deepcopy(cfg);proposal['standalone']={'model':name,'postprocessing':dict(replay.BASE_POST,alpha=.9,weight=.25,bonus=.3)}
        proposal['diverse_augmentation']=replay.empty_roles()
        proposal['final_augmentation']['top']={'model':'rank512_e32','weight':.075}
        proposal['linear_augmentation']['membership']={'model':'rank_ridge_l01','weight':.025}
        proofs.append(prefix_controls(small,proposal,counts=(20,80)))
    dump(qa/'verification.json',{'status':'passed','full_validation_rows':len(frozen),
         'all_active_R18_layers_recomputed_bit_identically':True,
         'baseline_controls':baseline_proof,'mixed_hybrid_standalone_and_regime_controls':proofs,
         'new_official_scores':0,'test_data_read':False,
         'source_sha256':{str(path.resolve()):sha(path) for path in (Path(__file__),Path(replay.__file__),
              replay.ORIGINAL/'selected_validation.npy',replay.ORIGINAL/'selection.json')},
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Complete-layer replay, poisoned labels and cold-prefix controls passed.',flush=True)


if __name__=='__main__':main()
