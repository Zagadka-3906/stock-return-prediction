"""Actual predecessor graph schema and both synthetic-ordering generator branches."""
from pathlib import Path
from copy import deepcopy
import hashlib
import importlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/streaming_rank_classifier_search_generator_preflight_20261005'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, data):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    OUT.mkdir(exist_ok=True)
    selection = ROOT / 'analysis/optimization_20261003_r61/selection.json'
    reference = json.loads(selection.read_text(encoding='utf-8'))['winner']
    reference_graph = deepcopy(reference['nystrom_ridge_role_scheme_graph'])
    sources = [Path(__file__), selection, ROOT / 'analysis/streaming_rank_classifier_official_search_plan_20261005.json']
    sources += [p for p in (ROOT / 'analysis').glob('*memory_efficient*20261005.py')]
    sources += [ROOT / 'analysis' / f'{prefix}{n}{suffix}.py' for n in (79, 80)
                for prefix, suffix in (('optimize_training_round', ''), ('finalize_training_round', ''), ('run_training_round', '_pipeline'))]
    bindings = {str(path): sha(path) for path in sources}
    for path in sources:
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    create(OUT / 'frozen_before_generator_controls.json', {'status': 'frozen_before_controls',
        'source_sha256': bindings, 'actual_reference_round': 61,
        'ordering_values_are_synthetic_not_official_quality': True, 'new_quality_scores': 0,
        'test_labels_read': False})
    results = []
    for number, pure_wins in ((79, False), (80, False), (80, True)):
        ns = importlib.import_module(f'optimize_training_round{number}')
        seed = deepcopy(reference)
        from streaming_rank_classifier_scheme_runtime_20261005 import append_role_layer
        graph = append_role_layer(reference_graph) if number == 80 else reference_graph
        for field in ns.previous.FIELDS:
            if field.endswith('scheme_graph') and field not in seed:
                seed[field] = deepcopy(graph)
            assert field in seed, field
        seed[ns.previous.GRAPH_FIELD] = deepcopy(graph)
        predecessor = {'winner': seed}
        memory, counts, protocols = {}, {}, {}
        base_read, base_out = ns.read, ns.OUT
        ns.OUT = OUT / f'round{number}_purewins{int(pure_wins)}'

        def read(path):
            path = Path(path)
            if path == ns.PREVIOUS / 'selection.json':
                return deepcopy(predecessor)
            if path.name in memory:
                return deepcopy(memory[path.name])
            return base_read(path)

        def execute(wave, arms, finish=True):
            name = f'wave{wave}_results.json'
            payload = memory.setdefault(name, {'status': 'running', 'results': {}})
            for key, cfg in arms:
                assert ns.previous.configuration(cfg) == ns.previous.configuration(ns.baseline())
                g = ns.graph(cfg)
                if number == 79:
                    active = any(spec['weight'] > 0 for spec in ns.node(cfg)['specs'].values())
                    value = .4 if active else .9
                    assert g['root'] == reference_graph['root']
                    assert g['layers'][:-1] == reference_graph['layers']
                else:
                    pure = ns.pure(cfg)
                    value = .95 if pure and pure_wins else .4 if pure else .9
                    if pure:
                        assert not g['layers'] and g['root']['configuration']['standalone']['model'] in ns.MODELS
                assert key not in payload['results'], key
                payload['results'][key] = {**ns.configuration(cfg), 'connected_final_score': value}
                counts[wave] = counts.get(wave, 0) + 1
            if finish:
                payload['status'] = 'complete'
            return deepcopy(payload)

        ns.read = read
        ns.verify = lambda: None
        ns.build = lambda: None
        ns.dump = lambda path, data, **kwargs: protocols.setdefault(str(path), {'keys': list(data), 'synthetic_ordering_only': True})
        ns.execute = execute
        try:
            ns.independent()
            if number == 79:
                ns.combinations()
                ns.refine_weights()
            else:
                ns.model_refinement()
            ns.refinement()
            expected = [49, 8, 18, 25] if number == 79 else [25, 56, 17]
            assert [counts[wave] for wave in ns.WAVES] == expected
            assert sum(counts.values()) == (88 if number == 79 else 80)
            results.append({'round': number, 'synthetic_pure_wins': pure_wins,
                'generated_records': sum(counts.values()), 'counts_per_wave': counts,
                'previous_flat_configs_preserved': True, 'actual_reference_root_and_layers_preserved_for_role_additions': True})
        finally:
            ns.read, ns.OUT = base_read, base_out
    for path, expected in bindings.items():
        assert sha(path) == expected, path
    create(OUT / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'source_sha256': bindings, 'controls': results, 'actual_reference_round': 61,
        'actual_R78_and_R79_full_predecessor_checks_required_before_quality': True,
        'synthetic_ordering_only_not_actual_official_scores': True,
        'complete_output_and_future_checks_pending': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed_source_and_generator_controls', 'controls': results}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
