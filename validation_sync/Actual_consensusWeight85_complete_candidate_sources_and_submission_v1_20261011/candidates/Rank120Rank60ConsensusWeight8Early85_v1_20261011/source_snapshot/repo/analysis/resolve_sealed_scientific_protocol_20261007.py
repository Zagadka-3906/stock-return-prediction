"""Resolve a scientific protocol through sealed registration aliases before inference."""
from pathlib import Path
from copy import deepcopy
from run_dependency_queue_v3_20261006 import read, sha

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def resolve(candidate, release, graph, runtime):
    candidate, release = Path(candidate), Path(release)
    selection = read(candidate / 'selection.json')
    protocol_path = release / 'protocol.json'
    protocol = read(protocol_path)
    evidence = [protocol_path]
    if not {'future_native_model_sources', 'future_root_model_sources'} <= protocol.keys():
        alias_path = candidate / 'registry_alias_verification.json'
        alias = read(alias_path)
        original = Path(alias['source_candidate'])
        manifest_path = original / 'manifest.json'
        assert sha(manifest_path) == alias['source_manifest_sha256']
        original_selection = original / 'selection.json'
        assert Path(selection['original_frozen_selection_source']) == original_selection
        assert sha(original_selection) == selection['original_frozen_selection_sha256']
        assert read(original / 'verification.json')['whole_scheme_graph'] == read(candidate / 'verification.json')['whole_scheme_graph']
        matches = []
        for ready_path in A.glob('*/selected_candidate_ready_for_registration.json'):
            ready = read(ready_path)
            if ready.get('source_candidate') == str(original):
                scientific_release = Path(ready.get('original_source_release', ready['source_release']))
                path = scientific_release / 'protocol.json'
                if path.is_file() and {'future_native_model_sources', 'future_root_model_sources'} <= read(path).keys():
                    matches.append((path, ready_path))
        assert matches, original
        protocol_path, ready_path = sorted(matches, key=lambda pair: str(pair[0]))[0]
        protocol = read(protocol_path)
        evidence += [alias_path, manifest_path, original_selection, ready_path, protocol_path]
        assert read(manifest_path)['files']['selection.json']['sha256'] == sha(original_selection)
    native = runtime.future_native_sources(graph)
    roots = runtime.root_model_sources(graph)
    for field, actual in [('future_native_model_sources', native), ('future_root_model_sources', roots)]:
        for name, info in actual.items():
            assert info['sha256'] == protocol[field][name]['sha256'], (field, name)
            assert sha(info['path']) == info['sha256'], (field, name)
    pins = {str(path): sha(path) for path in evidence}
    return deepcopy(protocol), pins, {
        'status': 'passed_sealed_scientific_protocol_core_sources_before_future_features',
        'scientific_protocol_source': str(protocol_path), 'input_sha256': pins,
        'actual_core_native_sources': len(native), 'actual_root_sources': len(roots),
        'new_native_fits': 0, 'test_labels_read': False,
    }
