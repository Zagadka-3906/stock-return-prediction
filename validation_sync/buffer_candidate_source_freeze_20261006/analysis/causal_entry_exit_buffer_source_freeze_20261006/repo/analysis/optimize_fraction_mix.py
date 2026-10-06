"""Wave43: compare adjacent training-fraction mixtures using existing causal OOF models."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
from continue_optimization import OUT,HERE,YEARS,KEYS,Context,EXPECTED,read,dump,sha,log,verify_protocol


def main():
    import numpy as np
    import polars as pl
    from optimize_wave15 import daily_ranks
    verify_protocol()
    protocol_path = OUT/'fraction_mix_protocol.json'
    sources = [Path(__file__)] + [HERE/f'wave31_topk/raw/topk_seed2026_f{frac:.2f}_{year}.parquet'
               for frac in (0.15,0.20,0.25) for year in YEARS]
    if protocol_path.exists():
        for path,digest in read(protocol_path)['input_sha256'].items():
            assert sha(ROOT/path) == digest
    else:
        dump(protocol_path,{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
             'selection_rule':'highest connected2020-2024 official composite; no test labels',
             'partner_fractions':[0.15,0.20,0.25],'partner_weights':[0.125,0.25,0.5],
             'base_fraction':0.175,'slow16_weight':0.25,'retention':0.985,
             'hypothesis':'Adjacent Top-K objective widths can supply complementary membership signals after new-seed mixtures failed.',
             'input_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in sources}},immutable=True)
    ctx = Context()
    base = daily_ranks(ctx.promote('seed2026'),ctx.valid,ctx.dates)
    result_path = OUT/'wave43_results.json'
    result = read(result_path) if result_path.exists() else {'status':'running','results':{}}
    for frac in (0.15,0.20,0.25):
        raw_parts = []
        for year in YEARS:
            frame = ctx.frame.filter(pl.col('trade_date')//10000 == year)
            raw = pl.read_parquet(HERE/f'wave31_topk/raw/topk_seed2026_f{frac:.2f}_{year}.parquet')
            assert raw.select(KEYS).equals(frame.select(KEYS))
            meta = read(HERE/f'wave31_topk/raw/info_f{frac:.2f}_{year}.json')['training_meta']
            assert meta == read(HERE/f'wave36_topk/raw/info_f0.175_{year}.json')['training_meta']
            raw_parts.append(raw['pred_raw'].to_numpy().astype(np.float64))
        finished = ctx.finish(raw_parts)
        partner = daily_ranks(finished,ctx.valid,ctx.dates)
        for weight in (0.125,0.25,0.5):
            name = f'frac0175_{frac:.3f}_w{weight:.3f}'
            if name in result['results']:
                continue
            promote = (1-weight)*base+weight*partner
            promote[~ctx.valid] = -10.0
            np.save(OUT/f'promote_{name}.npy',promote)
            pred,stats = ctx.predict(ctx.donor(promote),0.25,0.985)
            metrics = ctx.score(pred)
            result['results'][name] = {'donor':name,'fraction_components':[
                {'seed':2026,'fraction':0.175,'weight':1-weight},{'seed':2026,'fraction':frac,'weight':weight}],
                'slow16_weight':0.25,'retention':0.985,'limit_up_delta':0.0,
                'connected_final_score':metrics['final_score'],'metrics':metrics,'construction':stats}
            dump(result_path,result)
            log(f'wave43 {name}: {metrics["final_score"]:.9f}, delta={metrics["final_score"]-EXPECTED:+.9f}')
    result['status'] = 'complete'
    dump(result_path,result)


if __name__ == '__main__':
    main()
