"""Verify all five complete original GOSS annual windows against existing disk buffers."""
from pathlib import Path
import gc
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'gradient_sampling_all_annual_cache_controls_20261006'


def main():
    import numpy as np
    import gradient_sampling_exact_memmap_20261006 as core
    import mature_training_memmap_20261006 as mapped
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
    assert not OUT.exists()
    initial = A / 'gradient_sampling_exact_memmap_preflight_20261006/verification.json'
    assert read(initial)['status'] == 'passed_all6_native_GOSS_parameters_and_full_original_preprocessing_and_full2020_equivalence'
    cfg = next(iter(core.CONFIGS.values()))
    assert all(c['clip_z'] == cfg['clip_z'] and c['chunk_rows'] == cfg['chunk_rows'] for c in core.CONFIGS.values())
    artifacts = {year: A / f'quantile_tree_memmap_complete_bank_20261006/exact_training_artifact_{year}.json'
                 for year in range(2020, 2025)}
    pins = [Path(__file__), Path(core.__file__), Path(core.original.__file__), Path(mapped.__file__), initial,
        A / 'locked_read_hash_cache_20261004.py', A / 'linear_leaf_actual_resource_sampler_20261005.py',
        A / 'train_diverse_backbones_20261003.py', core.engine.FEATURE_FILE, core.engine.MANIFEST,
        ROOT / '后续选模标准.md', *artifacts.values()]
    for year, path in artifacts.items():
        value = read(path)
        artifact = value['artifact']
        assert artifact['year'] == year and artifact['shape'][1] == 63
        pins += [Path(artifact['raw_path']), Path(value['standardization']['path'])]
        pins += [Path(row['path']) for row in artifact['targets'].values()]
        pins += [A / f'linear_bank_20261003/{label}_ridge_l01/info_{year}.json'
                 for label in ('rank', 'return')]
    bindings = {str(p.resolve()): sha(p) for p in dict.fromkeys(pins)}
    OUT.mkdir()
    create(OUT / 'protocol.json', {'status': 'frozen_before_all5_full_annual_GOSS_preprocessing_controls',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': bindings,
        'configurations': core.CONFIGS, 'years': list(artifacts),
        'all_original_mature_rows_and63_features_required': True,
        'original_full_column_mean_std_and_all_standardized_bytes_required': True,
        'shared_training_buffers_read_only_and_not_rewritten': True,
        'actual_annual_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    sampler = ResourceSampler(OUT)
    sampler.start()
    checks, failure = [], None
    try:
        with LockedReadHashCache(bindings) as cache:
            for year, path in artifacts.items():
                value = read(path)
                artifact, clean = value['artifact'], value['standardization']
                rows, features = artifact['shape']
                sampler.context = {'stage': 'all_original_full_annual_GOSS_mean_std_and_standardized_bytes',
                                   'year': year, 'rows': rows}
                assert cache.sha(artifact['raw_path']) == artifact['training_meta_without_target']['training_matrix_sha256']
                raw = np.memmap(artifact['raw_path'], mode='r', dtype=np.float32, shape=(rows, features))
                mean, scale = core.original.preprocessing(raw)
                assert np.array_equal(mean.view(np.uint64), np.asarray(value['mean'], dtype=np.float64).view(np.uint64))
                assert np.array_equal(scale.view(np.uint64), np.asarray(value['scale'], dtype=np.float64).view(np.uint64))
                digest = hashlib.sha256()
                for offset in range(0, rows, cfg['chunk_rows']):
                    block = core.original.standardize(raw[offset:offset + cfg['chunk_rows']], mean, scale, cfg)
                    digest.update(memoryview(block).cast('B'))
                actual = digest.hexdigest()
                assert actual == clean['sha256'] == cache.sha(clean['path'])
                raw._mmap.close()
                del raw, block
                for label, target in (('rank', 'y_rank'), ('return', 'y_ret_1d')):
                    reference = read(A / f'linear_bank_20261003/{label}_ridge_l01/info_{year}.json')['training_meta']
                    info = artifact['targets'][target]
                    assert cache.sha(info['path']) == info['sha256']
                    metadata = dict(artifact['training_meta_without_target'], training_target_sha256=info['sha256'])
                    assert metadata == reference
                    assert metadata['last'] < metadata['cutoff_exclusive'] and metadata['last_label_end'] <= metadata['cutoff_exclusive']
                    assert metadata['features'] == core.engine.feature_names()
                    y = np.memmap(info['path'], mode='r', dtype=info['dtype'], shape=(rows,))
                    assert np.isfinite(y).all()
                    y._mmap.close()
                    del y
                check = {'year': year, 'full_actual_training_shape': [rows, features],
                    'artifact_record_path': str(path.resolve()), 'artifact_record_sha256': cache.sha(path),
                    'original_complete_mean_scale_bit_identical': True,
                    'entire_original_standardized_matrix_sha256': actual,
                    'both_full_targets_and_training_matrix_keys_and_maturity_match_original_references': True,
                    'all6_configurations_share_original_exact_preprocessing': True,
                    'shared_buffers_only_read_and_no_native_fit_performed': True}
                create(OUT / f'full{year}_verification.json', {'status': 'passed', **check})
                checks.append(check)
                print(json.dumps({'stage': 'passed_original_full_annual_GOSS_cache', 'year': year, 'rows': rows}), flush=True)
                del mean, scale
                gc.collect()
            cache.reverify()
        assert len(checks) == 5
        create(OUT / 'verification.json', {'status': 'passed_all5_full_original_GOSS_annual_preprocessing_targets_and_maturity',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'checks': checks, 'input_sha256': bindings,
            'actual_native_fits': 0, 'new_cache_files_written': 0, 'actual_annual_fits': 0,
            'original30_annual_and6_final_and262_quality_records_still_required': True,
            'new_quality_scores': 0, 'test_labels_read': False, 'physical_resource_boundary_established': False})
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        create(OUT / 'failure.json', {'status': 'failed_preserved_all_annual_GOSS_cache_controls', 'error': failure,
                                   'actual_completed_years': [c['year'] for c in checks]})
        raise
    finally:
        create(OUT / 'resource_summary.json', {'status': 'passed' if failure is None else 'failed',
            'failure': failure, **sampler.finish()})


if __name__ == '__main__':
    main()
