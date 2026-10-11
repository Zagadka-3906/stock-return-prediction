"""Audit actual reference graph and generator counts, then queue R64 lazily."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/agreement_gate_round64_source_preflight_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    sources = [ROOT / 'analysis' / name for name in (
        Path(__file__).name, 'agreement_gated_weights_20261005.py', 'optimize_training_round64.py',
        'predict_agreement_scheme_20261005.py', 'finalize_training_round64.py',
        'check_agreement_scheme_20261005.py', 'run_training_round64_pipeline.py')]
    reference = ROOT / 'analysis/optimization_20261003_r61/protocol.json'
    proof = ROOT / 'analysis/agreement_gate_preflight_v2_20261005/verification.json'
    assert read(proof)['status'] == 'passed_actual_mature_oof_gate_controls'
    sources += [reference, proof]
    bindings = {str(path): sha(path) for path in sources}
    create(OUT / 'frozen_before_reference_graph_controls.json', {
        'status': 'frozen_before_source_and_generator_controls', 'at_local': datetime.now().isoformat(),
        'input_sha256': bindings, 'actual_reference': str(reference),
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    import optimize_training_round64 as module
    cfg = deepcopy(read(reference)['starting_configuration'])
    graph = deepcopy(cfg['nystrom_ridge_role_scheme_graph'])
    cfg['nystrom_ridge_standalone_scheme_graph'] = deepcopy(graph)
    cfg['latest_joint_scheme_graph'] = deepcopy(graph)
    cfg[module.GRAPH_FIELD] = deepcopy(graph)
    actual_axes = module.graph_axes(graph)
    assert actual_axes
    original_baseline, original_axes, original_read, original_execute = module.baseline, module.axes, module.read, module.execute
    generated, wave_rows = {}, {}
    reference_score = read(reference)['baseline_score']

    def execute(wave, arms):
        assert len(arms) == len(set(arms))
        generated[str(wave)] = len(arms)
        rows = {}
        for key, value in arms.items():
            assert module.previous.configuration(value) == module.previous.configuration(cfg)
            g = value[module.GRAPH_FIELD]
            assert g['root'] == graph['root'] and g['temporal_postprocessing'] == graph['temporal_postprocessing']
            for old, new in zip(graph['layers'], g['layers']):
                assert len(old['specs']) == len(new['specs'])
                for role, spec in new['specs'].items():
                    retained = {k: v for k, v in spec.items() if k != 'agreement_gate'}
                    assert retained == old['specs'][role]
                    gate = spec.get('agreement_gate')
                    if gate:
                        assert gate['reference_model'] in module.graph_native_models(g)
                        assert gate['reference_model'] != spec['model']
                        assert 0 < gate['strength'] <= 1 and gate['width'] > 0
            # Synthetic ordering exercises baseline/no-gain combination paths only.
            # These values are not written as model scores or sent to the official scorer.
            count = sum('agreement_gate' in spec for layer in g['layers'] for spec in layer['specs'].values())
            rows[key] = {**value, 'connected_final_score': reference_score - count}
        wave_rows[wave] = {'results': rows}

    module.baseline = lambda: deepcopy(cfg)
    module.axes = lambda: deepcopy(actual_axes)
    module.execute = execute
    module.read = lambda path: wave_rows[int(Path(path).stem[4:].split('_')[0])] if Path(path).name.startswith('wave') else original_read(path)
    try:
        module.independent()
        module.combinations()
        module.refinement()
    finally:
        module.baseline, module.axes, module.read, module.execute = original_baseline, original_axes, original_read, original_execute
    k = len(actual_axes)
    expected = {'266': 1 + 18*k, '267': 2 + k, '268': 1 + 6*k}
    assert generated == expected
    for source, digest in bindings.items():
        assert sha(source) == digest, source
    control = {'status': 'passed_actual_reference_graph_and_synthetic_generator_checks',
        'at_local': datetime.now().isoformat(), 'input_sha256': bindings,
        'actual_reference_gate_axes': actual_axes, 'conditional_reference_records_per_wave': expected,
        'conditional_reference_scored_records': sum(expected.values()),
        'actual_r63_axes_and_counts_must_be_frozen_after_qualified_predecessor': True,
        'source_control_preserves_root_model_names_weights_retention_temporal_and_flat_predecessor': True,
        'both_nonzero_gate_modes_actual_oof_prefix_proof': str(proof),
        'generator_ordering_values_are_synthetic_andnot_quality_scores': True,
        'actual_complete_output_replay_future_controls_and_official_scores_still_required': True,
        'all_runtime_bindings_restored': True, 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'verification.json', control)
    registry = ROOT / 'analysis/resumed_rounds_nystrom_locked_20261004.json'
    records = read(registry)
    assert not any(row['round'] == 64 for row in records)
    wrapper = ROOT / 'analysis/run_training_round64_pipeline.py'
    stdout = ROOT / 'analysis/run_logs/round64_agreement_gate_20261005.stdout.log'
    stderr = ROOT / 'analysis/run_logs/round64_agreement_gate_20261005.stderr.log'
    env = os.environ.copy()
    scratch = ROOT / 'tmp/round64_20261005'
    scratch.mkdir(parents=True, exist_ok=True)
    for name in ('TMP', 'TEMP', 'TMPDIR'):
        env[name] = str(scratch)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        env[name] = '8'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(wrapper)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    new = {'round': 64, 'pid': process.pid, 'script': 'analysis/run_training_round64_pipeline.py', 'script_args': [],
           'stdout': str(stdout), 'stderr': str(stderr), 'launched_at_local': datetime.now().isoformat(),
           'status': 'waiting_for_full_qualified_round63', 'source_preflight': str(OUT / 'verification.json'),
           'actual_quality_records_at_launch': 0, 'new_model_fits': 0, 'test_labels_read': False,
           'conditional_reference_scored_records': sum(expected.values())}
    records.append(new)
    create(ROOT / 'analysis/agreement_gate_round64_run_20261005.json', {
        **new, 'input_sha256': {**bindings, str(OUT / 'verification.json'): sha(OUT / 'verification.json')}})
    # The currently running scientific scope does not bind this mutable registry.
    assert not any('resumed_rounds' in path for path in read(reference)['input_sha256'])
    temporary = registry.with_suffix('.agreement.tmp')
    temporary.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(registry)
    create(OUT / 'queue_adoption.json', {'status': 'launched_waiting_actual_qualified_predecessor',
        'at_local': datetime.now().isoformat(), 'round': 64, 'owned_root_pid': process.pid,
        'all_new_temporary_paths_on_D': True, 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': control['status'], 'reference_gate_axes': k,
        'conditional_reference_records': sum(expected.values()), 'round64_owned_root_pid': process.pid}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
