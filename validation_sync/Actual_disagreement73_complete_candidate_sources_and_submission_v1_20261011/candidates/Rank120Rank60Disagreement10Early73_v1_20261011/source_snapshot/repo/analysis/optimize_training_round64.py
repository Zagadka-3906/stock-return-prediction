"""Waves266-268: agreement and diversity gates on effective model layers."""
from copy import deepcopy
from pathlib import Path
import itertools
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis'), str(ROOT / 'analysis/connected_validation_20261002')]
import optimize_training_round63 as previous
from optimize_training_round63 import HERE, YEARS, KEYS, BASE_POST, ARCHIVE, RANKERS, read, dump, sha, log, weights_from_name
from whole_scheme_replay_runtime_20261004 import ValidationContext, raw_sources, prefix_controls as runtime_controls
from whole_scheme_future_runtime_20261004 import graph_native_models
from agreement_gated_weights_20261005 import context_weight

OUT = ROOT / 'analysis/optimization_20261003_r64'
PREVIOUS = ROOT / 'analysis/optimization_20261003_r63'
GRAPH_FIELD = 'agreement_scheme_graph'
NUMBER = 64
WAVES = (266, 267, 268)
FIELDS = previous.FIELDS + (GRAPH_FIELD,)
MODELS = NEW_MODELS = ()
GATES = tuple({'mode': mode, 'width': width, 'strength': strength}
              for mode, width, strength in itertools.product(('agreement', 'diversity'), (.1, .25, .5), (.25, .5, 1.)))
future_native_sources = previous.future_native_sources
root_model_sources = previous.root_model_sources
state_mapping_path = previous.state_mapping_path


def baseline():
    cfg = previous.configuration(read(PREVIOUS / 'selection.json')['winner'])
    return {**cfg, GRAPH_FIELD: deepcopy(cfg[previous.GRAPH_FIELD])}


def expected():
    return read(PREVIOUS / 'selection.json')['winner']['connected_final_score']


def configuration(row):
    return {key: deepcopy(row[key]) for key in FIELDS}


def signature(row):
    return json.dumps(configuration(row), sort_keys=True, separators=(',', ':'))


def best(rows):
    def complexity(row):
        return sum(bool(spec.get('agreement_gate', {}).get('strength', 0.))
                   for layer in row[GRAPH_FIELD]['layers'] for spec in layer['specs'].values())
    return min(rows, key=lambda row: (-row['connected_final_score'], complexity(row), signature(row)))


def axes():
    return read(OUT / 'protocol.json')['gate_axes']


def graph_axes(graph):
    names = list(graph_native_models(graph))
    preferred = ('rank512_drop000_seed18_e64', 'rank512_drop000_lr0005_e64')
    references = [name for name in preferred if name in names] + sorted(name for name in names if name not in preferred)
    result = []
    for index, layer in enumerate(graph['layers']):
        for role, spec in layer['specs'].items():
            if spec['weight'] <= 0:
                continue
            reference = next((name for name in references if name != spec['model']), None)
            if reference is not None:
                result.append({'layer_index': index, 'round': layer['round'], 'role': role,
                               'model': spec['model'], 'reference_model': reference})
    return result


def with_gate(cfg, axis, gate):
    result = configuration(cfg)
    spec = result[GRAPH_FIELD]['layers'][axis['layer_index']]['specs'][axis['role']]
    assert spec['model'] == axis['model'] and spec['weight'] > 0
    if gate is None or gate['strength'] == 0:
        spec.pop('agreement_gate', None)
    else:
        spec['agreement_gate'] = {**deepcopy(gate), 'reference_model': axis['reference_model']}
    return result


class Context(ValidationContext):
    def __init__(self):
        scoring = OUT / 'scoring_validation_only'
        scoring.mkdir(exist_ok=True)
        for name in ('测试集_X.csv', '测试集_Y.csv'):
            if not (scoring / name).exists():
                os.link(PREVIOUS / 'scoring_validation_only' / name, scoring / name)
        super().__init__(baseline()[GRAPH_FIELD], scoring=scoring)

    def configure(self, cfg):
        super().configure({'whole_scheme_graph': cfg.get(GRAPH_FIELD, cfg.get('whole_scheme_graph'))})

    def weights_for(self, spec):
        return context_weight(self, spec, super().weights_for(spec))


def verify():
    protocol = read(OUT / 'protocol.json')
    for path, digest in protocol['input_sha256'].items():
        assert sha(path) == digest, path
    return protocol


def freeze():
    if (OUT / 'protocol.json').exists():
        verify()
        return
    from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence
    assert complete_round_evidence(63) is not None
    proof = ROOT / 'analysis/agreement_gate_preflight_v2_20261005/verification.json'
    assert read(proof)['status'] == 'passed_actual_mature_oof_gate_controls'
    OUT.mkdir(exist_ok=True)
    graph = baseline()[GRAPH_FIELD]
    actual_axes = graph_axes(graph)
    assert actual_axes, 'No effective late model layers available for the declared gate experiment'
    sources = [Path(__file__), ROOT / 'analysis/agreement_gated_weights_20261005.py', proof,
               ROOT / 'analysis/finalize_training_round64.py', ROOT / 'analysis/predict_agreement_scheme_20261005.py',
               ROOT / 'analysis/run_training_round64_pipeline.py', ROOT / 'analysis/check_agreement_scheme_20261005.py',
               ROOT / 'analysis/parallel_candidate_scoring_four_20261004.py',
               ROOT / 'analysis/whole_scheme_replay_runtime_20261004.py',
               ROOT / 'analysis/whole_scheme_future_runtime_20261004.py',
               ROOT / 'analysis/publish_training_round.py', ROOT / 'analysis/nystrom_future_codec_adapter_20261005.py',
               ROOT / '后续选模标准.md', ROOT / 'active_release.json', state_mapping_path(),
               PREVIOUS / 'selection.json', PREVIOUS / 'protocol.json', PREVIOUS / 'selected_validation.npy',
               PREVIOUS / 'provenance_scope_execution.json', ROOT / 'results/optimization_20261003_r63.json',
               ROOT / 'candidates/optimization_20261003_r63/verification.json',
               ROOT / 'candidates/optimization_20261003_r63/manifest.json']
    sources += [Path(path) for path in read(PREVIOUS / 'protocol.json')['input_sha256']]
    for paths in raw_sources(graph).values():
        sources.extend(paths)
    native, roots = future_native_sources(graph), root_model_sources(graph)
    sources += [Path(info['path']) for info in {**native, **roots}.values()]
    k = len(actual_axes)
    dump(OUT / 'protocol.json', {
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'baseline_score': expected(),
        'starting_configuration': baseline(), 'gate_axes': actual_axes, 'gate_grid': GATES,
        'expected_scored_records': (1 + 18*k) + (2 + k) + (1 + 6*k),
        'records_per_wave': {'266': 1 + 18*k, '267': 2 + k, '268': 1 + 6*k},
        'waves': WAVES, 'new_model_training': False, 'new_fold_models_trained': 0,
        'same_validation': '5635800 rows;1212 continuous days;2020-2024 expanding mature-label OOF',
        'method': 'Per-record same-day model rank disagreement attenuates effective late layer weights, favoring agreement or diversity.',
        'reference_selection': 'Prefer effective accepted seed18/lower-learning-rate models, otherwise lexical effective native model; never a target, label or missing-label mask.',
        'reference_models_remain_effective_in_every_candidate': True,
        'fixed_model_names_weights_retention_and_temporal_parameters': True,
        'future_native_model_sources': native, 'future_root_model_sources': roots,
        'current_parameter_authority': GRAPH_FIELD, 'parallel_candidate_execution': {'workers': 4, 'ordered_commits': True},
        'all_validation_years_previously_viewed': True, 'selection_bias_uncorrected': True,
        'test_labels_read': False, 'test_future_prices_used_to_select': False,
        'input_sha256': {str(p.resolve()): sha(p) for p in dict.fromkeys(sources)}}, immutable=True)


def prefix_controls(ctx, cfg, counts=(80, 260, 975)):
    return runtime_controls(ctx, cfg[GRAPH_FIELD], counts)


def build():
    import numpy as np
    verify()
    if (OUT / 'component_audit.json').exists():
        return
    ctx, cfg = Context(), baseline()
    pred = ctx.predict(ctx.donor(ctx.finished('baseline')), 0., 0.)[0]
    assert np.array_equal(pred, np.load(PREVIOUS / 'selected_validation.npy'))
    assert ctx.score(pred) == read(PREVIOUS / 'selection.json')['winner']['metrics']
    controls = [{'case': 'baseline', **prefix_controls(ctx, cfg)}]
    from predict_agreement_scheme_20261005 import predict
    cases = [('baseline', cfg)]
    for mode in ('agreement', 'diversity'):
        changed = with_gate(cfg, axes()[0], {'mode': mode, 'width': .25, 'strength': .5})
        controls.append({'case': mode, **prefix_controls(ctx, changed, counts=(80, 260))})
        cases.append((mode, changed))
    future = {}
    for label, case in cases:
        record = {'winner': {**case, 'connected_final_score': None},
                  'frozen_sha256': {'active_release.json': sha(ROOT / 'active_release.json')}}
        destination = OUT / f'{label}_future_control'
        predict(record, candidate_path=destination, mapping_path=PREVIOUS / 'future_return_mapping.json')
        future[label] = sha(destination / 'verification.json')
        if label == 'baseline':
            assert sha(destination / 'submission.csv') == sha(ROOT / 'candidates/optimization_20261003_r63/submission.csv')
    dump(OUT / 'component_audit.json', {'status': 'passed', 'latest_selected_R63_validation_bit_identical': True,
        'all_eight_official_baseline_metrics_exact': True, 'actual_full1599600_row_future_cases': future,
        'controls': controls, 'new_quality_scores': 0, 'new_model_fits': 0, 'test_labels_read': False}, immutable=True)


def evaluate(ctx, cfg):
    assert previous.configuration(cfg) == previous.configuration(baseline())
    ctx.configure(cfg)
    pred, stats = ctx.predict(ctx.donor(ctx.finished('baseline')), 0., 0.)
    metrics = ctx.score(pred)
    foundation = read(PREVIOUS / 'selection.json')['winner']
    log(f"Round64 agreement-gated complete graph:{metrics['final_score']:.9f}")
    return {**configuration(cfg), 'donor': 'baseline',
            **{key: deepcopy(foundation[key]) for key in ('ensemble_weights', 'top_ensemble_weights', 'membership_ensemble_weights', 'role_ensembles_split')},
            'fold_local_pruning_repaired': True, 'pruned_member_excluded': True,
            'connected_final_score': metrics['final_score'], 'metrics': metrics, 'construction': stats,
            'official_score_cache': deepcopy(ctx.last_official_score_cache),
            'causal_return_mapping': deepcopy(ctx.last_candidate_return_mapping)}


def execute(wave, arms):
    from parallel_candidate_scoring_four_20261004 import evaluate_many
    path = OUT / f'wave{wave}_results.json'
    assert not path.exists()
    dump(OUT / f'wave{wave}_protocol.json', {'status': 'frozen_before_candidate_scores',
        'arms': arms, 'test_labels_read': False}, immutable=True)
    payload = {'status': 'running', 'results': {}}
    for key, row in evaluate_many(__name__, arms.items(), OUT):
        payload['results'][key] = row
        dump(path, payload)
    payload['status'] = 'complete'
    dump(path, payload)


def prior_best(waves):
    return best([row for wave in waves for row in read(OUT / f'wave{wave}_results.json')['results'].values()])


def independent():
    cfg = baseline()
    arms = {'baseline': cfg}
    for index, axis in enumerate(axes()):
        for j, gate in enumerate(GATES):
            arms[f'axis{index}_gate{j}'] = with_gate(cfg, axis, gate)
    execute(266, arms)


def combinations():
    rows = read(OUT / 'wave266_results.json')['results']
    anchor = baseline()
    combined = configuration(anchor)
    arms = {'baseline': anchor}
    for index, axis in enumerate(axes()):
        local = best([rows['baseline'], *[row for key, row in rows.items() if key.startswith(f'axis{index}_gate')]])
        spec = local[GRAPH_FIELD]['layers'][axis['layer_index']]['specs'][axis['role']]
        combined = with_gate(combined, axis, spec.get('agreement_gate'))
        arms[f'forward{index}'] = deepcopy(combined)
    arms['best_independent'] = configuration(prior_best((266,)))
    execute(267, arms)


def refinement():
    anchor = configuration(prior_best((266, 267)))
    arms = {'best_before_strength_refinement': anchor}
    for index, axis in enumerate(axes()):
        spec = anchor[GRAPH_FIELD]['layers'][axis['layer_index']]['specs'][axis['role']]
        gate = spec.get('agreement_gate', {'mode': 'agreement', 'width': .25, 'strength': .5})
        for strength in (0., .125, .25, .5, .75, 1.):
            arms[f'axis{index}_strength{strength}'] = with_gate(anchor, axis, {**gate, 'strength': strength})
    execute(268, arms)
