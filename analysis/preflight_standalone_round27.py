"""Real-data smoke check of the new standalone branch before any R23 scoring."""
from copy import deepcopy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002'),str(ROOT)]
import optimize_training_round27 as m


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    import connected_scorer as cs
    qa=ROOT/'analysis/standalone_round27_preflight';qa.mkdir(exist_ok=True);(qa/'raw').mkdir(exist_ok=True)
    # A separate process-local namespace keeps prospective R23 inputs untouched.
    m.OUT=qa
    frame=cs.combined_frame();last=frame['trade_date'].unique().sort()[99];frame=frame.filter(pl.col('trade_date')<=last)
    assert len(frame['trade_date'].unique())==100
    class PureContext(m.Context):
        def configure(self,cfg):self.standalone=deepcopy(cfg['standalone']);self.standalone_replacement=True
    ctx=PureContext.__new__(PureContext);ctx.frame=frame;ctx.label_free=frame.with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    ctx.dates=frame['trade_date'].to_numpy();ctx.flags=frame['flag_limit_up'].to_numpy().astype(np.int64);ctx.valid=frame['price_valid'].to_numpy()
    ctx.codes,unique=pd.factorize(frame['ts_code'].to_pandas(),sort=True);ctx.codes=ctx.codes.astype(np.int64)
    ctx.n_codes=len(unique);ctx.tie_key=1-ctx.codes/max(ctx.n_codes-1,1);ctx.pdf=frame.select('trade_date','flag_limit_up').to_pandas()
    ctx.slow_finished=ctx.w5a=ctx.slow=np.zeros(len(frame));ctx.ranks={'slow':ctx.slow,'w5a':ctx.w5a}
    proofs=[]
    for name in ('pair_rank256_e32','pair_rank512_e32','pair_rank128_t005_e32','pair_rank128_t020_e32'):
        raw=pl.read_parquet(m.trainer.source_dir(name)/'raw_2020.parquet').head(len(frame))
        assert raw.select(m.KEYS).equals(frame.select(m.KEYS));np.save(qa/f'raw/{name}.npy',raw['pred_raw'].to_numpy())
        cfg={'standalone':{'model':name,'postprocessing':dict(m.BASE_POST,alpha=.9,weight=.25,bonus=.3)},
             'slow16_weight':0.,'retention':.984,'limit_up_delta':.075}
        proof=m.prefix_controls(ctx,cfg,counts=(20,80));proofs.append(proof);m.log(f'Standalone preflight passed: {name}')
    m.dump(qa/'verification.json',{'status':'passed','real_training_validation_rows':len(frame),'days':100,
         'controls':proofs,'test_data_read':False,'new_official_scores':0,'source_sha256':m.sha(Path(__file__)),
         'standalone_optimizer_sha256':m.sha(ROOT/'analysis/optimize_training_round27.py')},immutable=True)


if __name__=='__main__':main()
