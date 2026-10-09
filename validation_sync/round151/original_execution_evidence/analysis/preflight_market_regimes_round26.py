"""Use a completed real foundation to check all current-state weight shapes."""
from copy import copy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round26 as m


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    from return_mapping import top_sets
    qa=ROOT/'analysis/market_regimes_round26_preflight';qa.mkdir(exist_ok=True)
    frame=pl.read_parquet(ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet').head(100*4650)
    base=np.load(ROOT/'analysis/optimization_20261003_r17/selected_validation.npy')[:len(frame)]
    original=m.read(ROOT/'analysis/optimization_20261003_r17/selection.json')['winner']
    ctx=m.Context.__new__(m.Context);ctx.dates=frame['trade_date'].to_numpy();ctx.valid=frame['price_valid'].to_numpy();ctx.flags=frame['flag_limit_up'].to_numpy().astype(np.int64)
    ctx.codes,unique=pd.factorize(frame['ts_code'].to_pandas(),sort=True);ctx.codes=ctx.codes.astype(np.int64);ctx.n_codes=len(unique);ctx.tie_key=1-ctx.codes/max(ctx.n_codes-1,1)
    from optimize_wave15 import daily_ranks
    raw=pl.read_parquet(m.trainer.source_dir('pair_rank256_e32')/'raw_2020.parquet').head(len(frame))['pred_raw'].to_numpy()
    ranks=daily_ranks(raw,ctx.valid,ctx.dates);ctx._final_cache={'pair_rank256_e32':ranks};ctx._regime_cache={};ctx.final_limit_delta=0.
    initial=top_sets(frame.select('trade_date','flag_limit_up').to_pandas(),base);proofs=[]
    for role in m.ROLES:
        for state in m.regime.NAMES:
            for low,high in ((0.,.1),(.1,0.)):
                ctx.final_augmentation={r:({'model':'pair_rank256_e32','weight':.1,'regime':state,'low':low,'high':high} if r==role else {'model':'none','weight':0.}) for r in m.ROLES}
                output,_=ctx.finish_output(base,original['retention'],original['limit_up_delta'])
                if role!='membership':assert top_sets(frame.select('trade_date','flag_limit_up').to_pandas(),output)==initial
                prefix=copy(ctx);n=80*4650
                for key in ('dates','valid','flags','codes','tie_key'):setattr(prefix,key,getattr(ctx,key)[:n])
                prefix._final_cache={'pair_rank256_e32':ranks[:n]};prefix._regime_cache={}
                replay,_=prefix.finish_output(base[:n],original['retention'],original['limit_up_delta']);assert np.array_equal(output[:n],replay)
                proofs.append({'role':role,'regime':state,'low':low,'high':high,'cold_market_state_prefix_bit_identical':True})
    m.dump(qa/'verification.json',{'status':'passed','controls':proofs,'test_data_read':False,'new_official_scores':0,
         'optimizer_sha256':m.sha(ROOT/'analysis/optimize_training_round26.py'),'script_sha256':m.sha(Path(__file__))},immutable=True)
    m.log('All18 rising/falling market-state preflight controls passed')


if __name__=='__main__':main()
