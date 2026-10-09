"""Real completed-foundation checks of generic extra-role output construction."""
from copy import copy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round43 as m


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    from return_mapping import top_sets
    qa=ROOT/'analysis/final_roles_round43_preflight_v2';qa.mkdir(exist_ok=True);(qa/'raw').mkdir(exist_ok=True);m.OUT=qa
    frame=pl.read_parquet(ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet')
    last=frame['trade_date'].unique().sort()[99];frame=frame.filter(pl.col('trade_date')<=last)
    base=np.load(ROOT/'analysis/optimization_20261003_r17/selected_validation.npy')[:len(frame)]
    winner=m.read(ROOT/'analysis/optimization_20261003_r17/selection.json')['winner'];retention=winner['retention'];delta=winner['limit_up_delta']
    ctx=m.Context.__new__(m.Context);ctx.dates=frame['trade_date'].to_numpy();ctx.valid=frame['price_valid'].to_numpy()
    ctx.flags=frame['flag_limit_up'].to_numpy().astype(np.int64);ctx.codes,unique=pd.factorize(frame['ts_code'].to_pandas(),sort=True)
    ctx.codes=ctx.codes.astype(np.int64);ctx.n_codes=len(unique);ctx.tie_key=1-ctx.codes/max(ctx.n_codes-1,1)
    ctx.fourier_ridge_limit_delta=0.;ctx.fourier_ridge_augmentation={r:{'model':'none','weight':0.} for r in m.ROLES};ctx._final_cache={}
    identity,_=ctx.finish_output(base,retention,delta);assert np.array_equal(identity,base)
    initial=top_sets(frame.select('trade_date','flag_limit_up').to_pandas(),base);proofs=[]
    for name in m.MODELS:
        raw=pl.read_parquet(m.trainer.source_dir(name)/'raw_2020.parquet').head(len(frame))
        assert raw.select(m.KEYS).equals(frame.select(m.KEYS));np.save(qa/f'raw/{name}.npy',raw['pred_raw'].to_numpy())
        for role in m.ROLES:
            ctx.fourier_ridge_augmentation={r:{'model':name if r==role else 'none','weight':.075 if r==role else 0.} for r in m.ROLES}
            output,_=ctx.finish_output(base,retention,delta)
            if role!='membership':assert top_sets(frame.select('trade_date','flag_limit_up').to_pandas(),output)==initial
            prefix=copy(ctx);n=80*4650
            for key in ('dates','valid','flags','codes','tie_key'):setattr(prefix,key,getattr(ctx,key)[:n])
            prefix._final_cache={};replay,_=prefix.finish_output(base[:n],retention,delta);assert np.array_equal(output[:n],replay)
            proofs.append({'model':name,'role':role,'cold_prefix_bit_identical':True,'ordering_only_membership_unchanged':role!='membership'})
    m.dump(qa/'verification.json',{'status':'passed','controls':proofs,'zero_weight_bit_identical':True,
         'foundation_round_used_for_preflight':17,'days':100,'test_data_read':False,'new_official_scores':0,
         'optimizer_sha256':m.sha(ROOT/'analysis/optimize_training_round43.py'),'script_sha256':m.sha(Path(__file__))},immutable=True)
    m.log('All18 generic complete-output role preflight checks passed')


if __name__=='__main__':main()
