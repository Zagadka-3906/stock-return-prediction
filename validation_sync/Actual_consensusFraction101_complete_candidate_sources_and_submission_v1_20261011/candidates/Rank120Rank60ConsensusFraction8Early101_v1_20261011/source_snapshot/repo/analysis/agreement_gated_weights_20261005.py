"""Causal per-record attenuation from two same-day model percentile ranks."""
import numpy as np


def gated_weight(base_weight, signal, reference, gate):
    if gate is None:
        return base_weight
    assert gate['mode'] in ('agreement', 'diversity')
    width, strength = gate['width'], gate['strength']
    assert width > 0 and 0 <= strength <= 1
    signal = np.asarray(signal, dtype=np.float64)
    reference = np.asarray(reference, dtype=np.float64)
    assert signal.shape == reference.shape
    if strength == 0:
        return base_weight
    valid = (signal > -9) & (reference > -9)
    disagreement = np.minimum(np.abs(signal - reference) / width, 1.)
    factor = 1. - strength * (disagreement if gate['mode'] == 'agreement' else 1. - disagreement)
    factor = np.where(valid, factor, 1.)
    result = np.asarray(base_weight) * factor
    assert np.isfinite(result).all() and np.all(result >= 0) and np.all(result <= 1)
    return result


def context_weight(context, spec, base_weight):
    gate = spec.get('agreement_gate')
    if gate is None or gate['strength'] == 0:
        return base_weight
    return gated_weight(base_weight, context.signal(spec['model']), context.signal(gate['reference_model']), gate)
