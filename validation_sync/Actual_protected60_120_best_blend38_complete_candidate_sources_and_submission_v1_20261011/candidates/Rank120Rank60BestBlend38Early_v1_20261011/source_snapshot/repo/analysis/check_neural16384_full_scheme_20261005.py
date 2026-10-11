"""Causal checks of the actual selected vector and every new native model role."""
from copy import deepcopy
import importlib


def main(number):
    import numpy as np
    module = importlib.import_module(f'optimize_training_round{number}')
    module.verify()
    selected = module.read(module.OUT / 'selection.json')['winner']
    context = module.Context()
    context.configure(selected)
    predicted = context.predict(context.donor(context.finished('baseline')), 0., 0.)[0]
    assert np.array_equal(predicted, np.load(module.OUT / 'selected_validation.npy'))
    checks = [{'case': 'selected', **module.prefix_controls(context, selected)}]
    checks.append({'case': 'baseline', **module.prefix_controls(context, module.baseline())})
    for name in module.MODELS:
        for role in module.ROLES if number == 67 else ('standalone',):
            cfg = deepcopy(module.baseline())
            if number == 67:
                module.node(cfg)['specs'][role] = {'model': name, 'weight': .025}
            else:
                cfg = module.standalone_cfg(name)
            checks.append({'case': name + '_' + role, **module.prefix_controls(context, cfg, counts=(80, 260))})
    module.dump(module.OUT / 'neural16384_full_causal_checks.json', {
        'status': 'passed', 'checks': checks, 'selected_validation_bit_identical': True,
        'all1_new_model_checked': True, 'new_quality_scores': 0,
        'test_labels_read': False}, immutable=True)
