"""Real matched512 instrumentation replay and full16384 architecture/control audit."""
from pathlib import Path
import ast
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/neural16384_full_preflight_20261005'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import numpy as np
    import polars as pl
    import torch
    import train_neural16384_full_bank_20261005 as bank
    from neural16384_actual_resource_recorder_20261005 import ActualResourceRecorder
    OUT.mkdir(exist_ok=True)
    sources = [Path(__file__), Path(bank.__file__), bank.SOURCE, bank.STORAGE,
        ROOT / 'analysis/run_neural16384_full_bank_20261005.py',
        ROOT / 'analysis/neural16384_actual_resource_recorder_20261005.py',
        ROOT / 'analysis/prepare_neural16384_full_20261005.py',
        ROOT / 'analysis/neural_width_frontier_20261004/verification.json',
        ROOT / 'analysis/neural_regularization_bank_20261003/protocol.json',
        *[bank.BASELINE / f'info_{year}.json' for year in bank.YEARS]]
    bindings = {str(path): sha(path) for path in sources}
    create(OUT / 'frozen_before_actual_instrumentation_controls.json', {
        'status': 'frozen_before_actual_controls', 'source_sha256': bindings,
        'actual5124096_row1_epoch_control_is_not_a_new_annual_fit': True,
        'full16384_complete_training_and_scores_pending': True, 'test_labels_read': False})
    for path in sources:
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'))
    cfg = next(iter(bank.CONFIGS.values()))
    reference = bank.read(bank.BASELINE / 'info_2020.json')['configuration']
    assert {k: v for k, v in cfg.items() if k != 'hidden'} == {k: v for k, v in reference.items() if k != 'hidden'}
    assert cfg['epochs'] == 32 and cfg['hidden'] == [16384, 8192, 4096]
    expected_rows = {}
    for year in bank.YEARS:
        info = bank.read(bank.BASELINE / f'info_{year}.json')
        assert info['status'] == 'passed' and info['configuration'] == reference
        assert sha(bank.BASELINE / f'model_{year}.joblib') == info['model_sha256']
        meta = info['training_meta']
        assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
        expected_rows[year] = meta['rows']
    with torch.device('meta'):
        network = bank.engine.network(len(bank.engine.feature_names()), cfg)
    parameters = sum(value.numel() for value in network.parameters())
    frontier = bank.read(ROOT / 'analysis/neural_width_frontier_20261004/verification.json')
    actual = next(row for row in frontier['execution_controls'] if row['width'] == 16384)
    assert actual['status'] == 'completed' and actual['child_result']['status'] == 'one_step_completed'
    assert actual['child_result']['parameter_count'] == parameters == 168894465
    lazy = pl.scan_parquet(bank.engine.FEATURE_FILE)
    past = bank.engine.training_frame(lazy, bank.engine.fold_cutoff(2020), reference).select(
        bank.engine.KEYS + bank.engine.feature_names() + ['y_rank']).sort('trade_date', 'ts_code').head(4096).collect()
    x = bank.engine.to_matrix(past, bank.engine.feature_names())
    y = past['y_rank'].to_numpy()
    pilot = dict(reference, epochs=1)
    untouched = bank.engine.fit_arrays(x, y, pilot)
    recorder = ActualResourceRecorder(OUT)
    recorder.context = {'stage': 'instrumentation_equivalence_only', 'model': 'actual512_matched_control', 'rows': 4096, 'epochs': 1}
    recorder.start()
    try:
        wrapped = recorder.measured_fit(bank.engine.fit_arrays)(x, y, pilot)
    finally:
        resources = recorder.finish()
    assert resources['observer_errors'] == []
    assert np.array_equal(untouched['mean'], wrapped['mean'])
    assert np.array_equal(untouched['scale'], wrapped['scale'])
    assert untouched['training_losses'] == wrapped['training_losses']
    assert all(torch.equal(untouched['state'][k], wrapped['state'][k]) for k in untouched['state'])
    a = bank.engine.predict_arrays(untouched, x[:512])
    b = bank.engine.predict_arrays(wrapped, x[:512])
    assert np.array_equal(a, b)
    for source, digest in bindings.items():
        assert sha(source) == digest
    create(OUT / 'verification.json', {'status': 'passed_actual_matched_instrumentation_and_architecture_controls',
        'source_sha256': bindings, 'full16384_parameter_count': parameters,
        'all_nonwidth_parameters_match_actual512_no_dropout32epoch_control': True,
        'all_five_actual_reference_model_hashes_and_maturity_verified': True,
        'actual_matched_past4096_row_control_states_preprocessing_losses_and_predictions_bit_identical': True,
        'resource_instrumentation_changes_no_original_fit_math': True, 'actual_resources': resources,
        'planned_full_annual_rows': expected_rows, 'planned_full_annual_fits': 5,
        'actual_full16384_annual_fits': 0, 'new_quality_scores': 0,
        'fulltraining_future_and_complete_scheme_scores_still_pending': True, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_actual_matched_instrumentation_and_architecture_controls',
        'parameters': parameters, 'full16384_annual_fits': 0}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
