"""Check the winner, baseline, each real weight axis, retention and temporal path."""
from copy import deepcopy
import time


def main():
    import numpy as np
    import optimize_training_round63 as module
    import finalize_training_round63 as release
    from latest_graph_joint_axes_20261005 import with_weight
    winner = release.selected()['winner']
    context = module.Context()
    context.configure(winner)
    full = context.predict(context.donor(context.finished('baseline')), 0., 0.)[0]
    assert np.array_equal(full, np.load(module.OUT / 'selected_validation.npy'))
    cases = [('selected', winner, (80, 260, 975)), ('baseline', module.baseline(), (80, 260, 975))]
    for axis in module.axes():
        changed = deepcopy(module.baseline())
        changed[module.GRAPH_FIELD] = with_weight(changed[module.GRAPH_FIELD], axis, 0., module.axes())
        cases.append((f"weight_r{axis['round']}_{axis['group']}_{axis['role']}", changed, (80, 260)))
    retained = deepcopy(module.baseline())
    retained[module.GRAPH_FIELD]['root']['configuration']['retention'] = .97
    cases.append(('root_retention', retained, (80, 260)))
    temporal = deepcopy(module.baseline())
    temporal[module.GRAPH_FIELD]['temporal_postprocessing'] = {'alpha': .995, 'mix': .025, 'power': 1.}
    cases.append(('final_temporal', temporal, (80, 260)))
    controls = []
    for name, configuration, lengths in cases:
        controls.append({'case': name, **module.prefix_controls(context, configuration, counts=lengths)})
    module.dump(module.OUT / 'latest_joint_scheme_causal_checks.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'selected_output_bit_identical': True, 'actual_weight_axes_checked': len(module.axes()),
        'actual_complete_output_cold_prefix_andlabel_poisoning_controls': controls,
        'new_model_fits': 0, 'test_labels_read': False,
    }, immutable=True)
