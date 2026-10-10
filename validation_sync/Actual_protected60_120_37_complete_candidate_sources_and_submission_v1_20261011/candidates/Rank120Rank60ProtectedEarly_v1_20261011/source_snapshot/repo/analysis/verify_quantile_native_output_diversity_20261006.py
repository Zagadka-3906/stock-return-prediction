"""Full saved OOF output diversity, without labels, quality scores or grid changes."""
from pathlib import Path
import gc
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_native_output_diversity_20261006'
YEARS = (2020, 2021)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import numpy as np
    import polars as pl
    import psutil
    import scipy.stats
    import lightgbm as lgb
    import joblib
    from run import FEATURE_FILE, MANIFEST
    from run_dependency_queue_v3_20261006 import owned
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    assert not OUT.exists()
    OUT.mkdir()
    new_bank = A / 'quantile_tree_memmap_complete_bank_20261006'
    configs = read(new_bank / 'protocol.json')['configurations']
    names = list(configs)
    folders = {name: new_bank / name for name in names}
    leaf = Path(read(A / 'linear_leaf_storage_20261005.json')['output_directory'])
    folders.update({name: leaf / name for name in ('rank_lgb_constant_r300', 'return_lgb_constant_r300')})
    folders.update({name: A / 'linear_bank_20261003' / name for name in ('rank_ridge_l01', 'return_ridge_l01')})
    create(OUT / 'prespecified_diagnostic_scope.json', {
        'status': 'frozen_two_complete_annual_output_diagnostic_before_execution',
        'years': YEARS, 'models': list(folders),
        'diagnostic': 'Per-day raw prediction Spearman and valid-price top10percent overlap, no labels loaded.',
        'raw_head_rule': 'Eligible price-valid rows, floor10percent; ties follow ts_code order. Descriptive output overlap only.',
        'not_an_official_score_or_extra_adoption_gate': True,
        'all20_annual_models_and198_official_scheme_scores_still_required': True,
        'original_full198_grid_and_parameters_unchanged': True, 'new_model_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False})
    while not all((folders[name] / f'info_{year}.json').exists() for name in names for year in YEARS):
        row = read(A / 'service_owned_workflows_20261006/quantile_tree_memmap_complete_workflow/native_launch.json')
        assert owned(row), 'Required annual native worker must actually remain live while waiting.'
        time.sleep(10)
    while psutil.virtual_memory().available < 2 * 2**30:
        time.sleep(10)
    sources = [Path(__file__), FEATURE_FILE, MANIFEST, ROOT / 'run.py', ROOT / '后续选模标准.md',
        A / 'linear_leaf_storage_20261005.json', A / 'locked_read_hash_cache_20261004.py',
        A / 'linear_leaf_actual_resource_sampler_20261005.py', new_bank / 'protocol.json']
    for name, folder in folders.items():
        for year in YEARS:
            info = read(folder / f'info_{year}.json')
            assert info['status'] == 'passed'
            assert sha(folder / f'raw_{year}.parquet') == info['prediction_sha256']
            reference = 'rank_ridge_l01' if info['configuration']['target'] == 'y_rank' else 'return_ridge_l01'
            assert info['training_meta'] == read(A / f'linear_bank_20261003/{reference}/info_{year}.json')['training_meta']
            sources += [folder / f'info_{year}.json', folder / f'raw_{year}.parquet']
            if name in configs:
                model = folder / f'model_{year}.joblib'
                assert sha(model) == info['model_sha256'] and info['actual_native_boosting_iterations'] == 300
                bundle = joblib.load(model)
                booster = lgb.Booster(model_str=bundle['model_string'])
                assert booster.current_iteration() == booster.num_trees() == 300
                assert bundle['config'] == configs[name]
                sources.append(model)
                del bundle, booster
    bindings = {str(p.resolve()): sha(p) for p in dict.fromkeys(sources)}
    create(OUT / 'frozen_before_actual_full_vectors.json', {'input_sha256': bindings,
        'new_model_fits': 0, 'new_quality_scores': 0, 'labels_loaded': False})
    resource, failure, years = ResourceSampler(OUT), None, []
    resource.start()
    try:
        with LockedReadHashCache(bindings) as cache:
            for year in YEARS:
                expected = pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select('ts_code', 'trade_date', 'price_valid').sort('trade_date', 'ts_code').collect()
                arrays, digests = {}, {}
                for name, folder in folders.items():
                    frame = pl.read_parquet(folder / f'raw_{year}.parquet')
                    assert frame.select('ts_code', 'trade_date').equals(expected.select('ts_code', 'trade_date'))
                    pred = frame['pred_raw'].to_numpy()
                    assert np.isfinite(pred).all()
                    arrays[name] = pred
                    digests[name] = hashlib.sha256(memoryview(np.ascontiguousarray(pred)).cast('B')).hexdigest()
                dates, valid = expected['trade_date'].to_numpy(), expected['price_valid'].to_numpy()
                starts = np.r_[0, np.flatnonzero(np.diff(dates)) + 1, len(dates)]
                summaries = {(left, right): {'correlations': [], 'overlaps': [], 'valid_rows': 0}
                             for i, left in enumerate(folders) for right in list(folders)[i + 1:]}
                for start, end in zip(starts[:-1], starts[1:]):
                    keep = np.flatnonzero(valid[start:end])
                    assert len(keep) >= 10
                    ranks, heads = {}, {}
                    k = int(len(keep) * .1)
                    for name, values in arrays.items():
                        current = values[start:end][keep]
                        ranked = scipy.stats.rankdata(current, method='average')
                        ranked -= ranked.mean()
                        norm = np.linalg.norm(ranked)
                        ranks[name] = ranked / norm if norm else None
                        head = np.zeros(len(keep), dtype=bool)
                        head[np.argsort(-current, kind='stable')[:k]] = True
                        heads[name] = head
                    for (left, right), summary in summaries.items():
                        if ranks[left] is not None and ranks[right] is not None:
                            summary['correlations'].append(float(np.dot(ranks[left], ranks[right])))
                        summary['overlaps'].append(float(np.count_nonzero(heads[left] & heads[right]) / k))
                        summary['valid_rows'] += len(keep)
                pairs = []
                for (left, right), summary in summaries.items():
                    corr, overlap = summary['correlations'], summary['overlaps']
                    pairs.append({'left': left, 'right': right,
                        'all_full_annual_saved_prediction_bytes_identical': digests[left] == digests[right],
                        'daily_spearman_mean': float(np.mean(corr)) if corr else None,
                        'daily_spearman_days': len(corr), 'daily_valid_price_raw_head10percent_overlap_mean': float(np.mean(overlap)),
                        'diagnostic_days': len(overlap), 'eligible_valid_price_rows': summary['valid_rows']})
                year_proof = {'year': year, 'full_saved_prediction_rows': len(expected),
                    'complete_annual_days': len(starts) - 1, 'codes': expected['ts_code'].n_unique(),
                    'all_saved_keys_bit_identical': True, 'raw_array_sha256': digests, 'pairs': pairs}
                create(OUT / f'diagnostic_{year}.json', year_proof)
                years.append(year_proof)
                print(json.dumps({'status': 'passed_actual_full_annual_output_diagnostic', 'year': year,
                                  'rows': len(expected), 'models': len(folders)}), flush=True)
                del expected, arrays, dates, valid, frame, pred, summaries
                gc.collect()
            cache.reverify()
        create(OUT / 'verification.json', {'status': 'passed_actual_two_complete_annual_native_output_diversity_checks',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': bindings,
            'years': list(YEARS), 'models': list(folders), 'total_rows_each_model': sum(y['full_saved_prediction_rows'] for y in years),
            'actual_new_native_models_checked': 8, 'actual_new_model_fits': 0,
            'new_quality_scores': 0, 'labels_loaded': False, 'test_labels_read': False,
            'full20_annual_closure_and198_official_quality_and_adoption_still_pending': True,
            'diagnostics_do_not_change_any_required_grid_or_adoption_gate': True,
            'global_resource_boundary_established': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        create(OUT / 'failure.json', {'status': 'failed_preserved_actual_diagnostics', 'error': failure})
        raise
    finally:
        create(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed', 'failure': failure,
                                              **resource.finish()})


if __name__ == '__main__':
    main()
