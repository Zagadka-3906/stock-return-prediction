"""Check real frozen roots and all10 new native sources without scoring labels."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    import optimize_training_round66_v2 as module
    import optimize_training_round50 as roots
    from standalone_root_source_adapter_20261005 import resolve
    out = ROOT / 'analysis/standalone_root_source_adapter_preflight_20261005'
    out.mkdir(exist_ok=True)
    sources = [Path(__file__), ROOT / 'analysis/standalone_root_source_adapter_20261005.py',
        Path(roots.__file__), ROOT / 'analysis/optimization_20261003_r66/protocol.json',
        ROOT / 'analysis/optimization_20261003_r66/provenance_scope_execution.json',
        ROOT / 'analysis/optimization_20261003_r65/selection.json',
        ROOT / 'analysis/nystrom_tuning_future_qa_20261005/verification.json']
    bindings = {str(path): sha(path) for path in sources}
    with (out / 'frozen_before_controls.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'frozen_before_source_resolution_controls', 'input_sha256': bindings,
                   'actual_fullfuture_replay_under_repaired_execution_still_required': True,
                   'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    base = module.graph(module.baseline())
    previous = roots.root_model_sources(base)
    assert previous and resolve(base, roots.root_model_sources) == previous
    for info in previous.values():
        assert sha(info['path']) == info['sha256']
    checks = []
    for name in module.MODELS:
        graph = module.graph(module.standalone_cfg(name))
        assert graph['root']['round'] == 66 and graph['root']['kind'] == 'standalone' and not graph['layers']
        try:
            roots.root_model_sources(graph)
        except FileNotFoundError as error:
            assert 'optimization_20261003_r66' in str(error)
        else:
            raise AssertionError('Expected the original premature candidate dependency.')
        assert resolve(graph, roots.root_model_sources) == {}
        native = module.future_native_sources(graph)
        assert set(native) == {name}
        info = native[name]
        assert sha(info['path']) == info['sha256']
        training = info['training_info']['training_meta']
        assert training['last'] < training['cutoff_exclusive']
        assert training['last_label_end'] <= training['cutoff_exclusive']
        checks.append({'model': name, 'root_models': 0, 'actual_native_sources': 1,
                       'native_model_sha256': info['sha256'],
                       'original_premature_candidate_dependency_reproduced': True,
                       'candidate_self_dependency_removed_without_changing_native_model': True})
    for source, expected in bindings.items():
        assert sha(source) == expected, source
    with (out / 'verification.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_source_resolution_only', 'source_sha256': bindings,
                   'checks': checks, 'actual_R65_root_source_dictionary_unchanged': True,
                   'all10_R66_standalone_models_resolve_actual_frozen_native_bytes': True,
                   'full_scheme_replay_official_scoring_and_repaired_execution_pending': True,
                   'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print('Passed actual R65 source parity and all10 R66 standalone native-source controls.', flush=True)


if __name__ == '__main__':
    main()
