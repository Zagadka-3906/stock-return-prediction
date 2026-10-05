"""Explicit role layers for joint refinement of an entire selected scheme.

Each layer carries its own retention and accumulated limit shift.  A later
layer never substitutes a saved final forecast for a changed earlier layer.
Signals and market-state weights are provided by the causal caller.
"""
from copy import deepcopy
import numpy as np
from optimize_wave13 import build_ab
from optimize_wave15 import daily_ranks

ROLES = ('membership', 'top', 'rest')


def finish_layer(context, base, specs, retention, original_delta, additional_delta):
    assert set(specs) == set(ROLES)
    if not any(spec['weight'] > 0 for spec in specs.values()):
        pred = base.copy()
        if additional_delta:
            pred[context.flags == 1] += additional_delta
        return pred, {'extra_role_augmentation': False,
                      'additional_limit_shift': additional_delta}
    unshifted = base.copy()
    unshifted[context.flags == 1] -= original_delta
    ranks = daily_ranks(unshifted, context.valid, context.dates)

    def blend(role):
        spec = specs[role]
        if spec['weight'] == 0:
            return unshifted
        weight = context.weights_for(spec)
        other = context.signal(spec['model'])
        valid = (ranks > -9) & (other > -9)
        values = np.full(len(base), -10.)
        weighted = (1 - weight) * ranks + weight * other
        assert np.isfinite(weighted).all()
        assert np.all(np.asarray(weight) >= 0) and np.all(np.asarray(weight) <= 1)
        values[valid] = weighted[valid] + 1e-9 * context.tie_key[valid]
        return values

    donor, top, rest = (blend(role) for role in ROLES)
    second_retention = retention if specs['membership']['weight'] > 0 else 0.
    pred, stats = build_ab(donor, top, rest, context.dates, context.flags,
                           context.codes, context.n_codes, second_retention)
    pred[context.flags == 1] += original_delta
    if additional_delta:
        pred[context.flags == 1] += additional_delta
    return pred, {'extra_role_augmentation': True,
                  'second_retention': second_retention, 'construction': stats,
                  'additional_limit_shift': additional_delta}


def replay_layers(context, foundation, layers):
    pred = foundation
    records = []
    for layer in layers:
        pred, stats = finish_layer(context, pred, layer['specs'],
                                   layer['retention'], layer['original_delta'],
                                   layer['additional_delta'])
        records.append({'name': layer['name'], 'configuration': deepcopy(layer),
                        'construction': stats})
    return pred, records
