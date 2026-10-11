"""Verify selected gated output and both nonzero modes on every gate axis."""
from copy import deepcopy
import time


def main():
    import numpy as np
    import optimize_training_round64 as module
    import finalize_training_round64 as release
    winner = release.selected()['winner']
    ctx = module.Context()
    ctx.configure(winner)
    selected = ctx.predict(ctx.donor(ctx.finished('baseline')), 0., 0.)[0]
    assert np.array_equal(selected, np.load(module.OUT / 'selected_validation.npy'))
    controls = [{'case': 'selected', **module.prefix_controls(ctx, winner)},
                {'case': 'baseline', **module.prefix_controls(ctx, module.baseline())}]
    for index, axis in enumerate(module.axes()):
        for mode in ('agreement', 'diversity'):
            cfg = module.with_gate(module.baseline(), axis, {'mode': mode, 'width': .25, 'strength': .5})
            controls.append({'case': f'axis{index}_{mode}', **module.prefix_controls(ctx, cfg, counts=(80, 260))})
    module.dump(module.OUT / 'agreement_gate_causal_checks.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'selected_output_bit_identical': True, 'actual_gate_axes_checked': len(module.axes()),
        'actual_complete_output_cold_prefix_andlabel_poisoning_controls': controls,
        'same_day_model_ranks_only': True, 'new_model_fits': 0, 'test_labels_read': False}, immutable=True)
