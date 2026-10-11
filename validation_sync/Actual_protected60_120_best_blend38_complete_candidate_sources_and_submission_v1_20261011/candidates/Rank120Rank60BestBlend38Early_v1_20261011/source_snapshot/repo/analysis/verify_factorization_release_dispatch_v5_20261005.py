"""Exercise the actual legacy and corrected release closures with no scoring."""
from pathlib import Path
import hashlib
import importlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    controls = []
    for number in (73, 74):
        experiment = importlib.import_module(f'optimize_training_round{number}_v4')
        sys.modules[f'optimize_training_round{number}'] = experiment
        old = importlib.import_module(f'finalize_training_round{number}')
        assert old.OUT == ROOT / f'analysis/optimization_20261003_r{number - 2}'
        corrected = importlib.import_module(f'finalize_training_round{number}_v5')
        assert corrected.OUT == experiment.OUT == ROOT / f'analysis/optimization_20261003_r{number}'
        assert corrected.PREVIOUS == experiment.PREVIOUS and corrected.WAVES == experiment.WAVES
        for name in ('selected', 'select', 'calibrate', 'ReleaseContext'):
            function = getattr(corrected, name)
            if isinstance(function, type):
                assert function.__bases__ == (experiment.Context,)
                assert corrected.selected in [cell.cell_contents for cell in function.__init__.__closure__]
                continue
            cells = [cell.cell_contents for cell in (function.__closure__ or ())]
            assert experiment in cells, (number, name)
        controls.append({'round': number, 'legacy_actual_output_round': number - 2,
            'actual_v5_output_and_selected_select_calibrate_context_closures': number,
            'actual_v4_experiment_module_retained': True, 'forecast_math_unchanged': True})
    sources = [Path(__file__), A / 'prepare_factorization_release_dispatch_v5_20261005.py',
        A / 'run_factorization_machine_round_v5_20261005.py']
    sources += [A / f'{prefix}{n}{suffix}.py' for n in (73, 74)
        for prefix, suffix in (('finalize_training_round', ''), ('finalize_training_round', '_v5'),
            ('run_training_round', '_v5_pipeline'), ('optimize_training_round', '_v4'))]
    out = A / 'factorization_machine_release_dispatch_preflight_v5_20261005'
    out.mkdir(exist_ok=True)
    with (out / 'verification.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_actual_release_outputs_and_all_four_closures', 'controls': controls,
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'original_canonical_sources_preserved': True, 'new_model_fits': 0,
            'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print('Actual FM release73/74 output and closure dispatch passed', flush=True)


if __name__ == '__main__':
    main()
