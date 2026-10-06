"""Joint nonzero membership/retention search; each model keeps a positive refinement anchor."""
from copy import deepcopy
from itertools import product

WEIGHTS = (.0001, .005, .025)
RETENTIONS = (.984, .99, .995, .998)
FINAL_RETENTIONS = (.995, .998, .999)
DELTAS = (-.02, 0., .02)
WAVES = (378, 379, 380)
COUNTS = (73, 24, 54)


def initial_arms(ns):
    base = ns.baseline()
    arms = [('baseline', deepcopy(base))]
    for name, weight, retention in product(ns.MODELS, WEIGHTS, RETENTIONS):
        cfg = deepcopy(base)
        node = ns.node(cfg)
        for role in ns.ROLES:
            node['specs'][role] = {'model': 'none', 'weight': 0.}
        node['specs']['membership'] = {'model': name, 'weight': weight}
        node.update(retention=retention, additional_delta=0.)
        arms.append((f'{name}_m{weight:g}_r{retention:g}', cfg))
    assert len(arms) == COUNTS[0]
    return arms


def local_positive_anchor(ns, rows, name):
    candidates = [r for r in rows if ns.node(r)['specs']['membership']['model'] == name
                  and ns.node(r)['specs']['membership']['weight'] > 0]
    assert candidates
    anchor = ns.configuration(ns.best(candidates))
    assert ns.node(anchor)['specs']['membership']['weight'] > 0
    return anchor


def combination_arms(ns, first_rows, top_rest_specs):
    assert set(top_rest_specs) == {'top', 'rest'}
    arms = []
    for name in ns.MODELS:
        anchor = local_positive_anchor(ns, first_rows, name)
        for top, rest in product((False, True), repeat=2):
            cfg = deepcopy(anchor)
            for role, enabled in (('top', top), ('rest', rest)):
                if enabled:
                    ns.node(cfg)['specs'][role] = deepcopy(top_rest_specs[role])
            assert ns.node(cfg)['specs']['membership']['weight'] > 0
            arms.append((f'{name}_top{int(top)}_rest{int(rest)}', cfg))
    assert len(arms) == COUNTS[1]
    return arms


def final_arms(ns, rows):
    arms = []
    for name in ns.MODELS:
        anchor = local_positive_anchor(ns, rows, name)
        for retention, delta in product(FINAL_RETENTIONS, DELTAS):
            cfg = deepcopy(anchor)
            ns.node(cfg).update(retention=retention, additional_delta=delta)
            assert ns.node(cfg)['specs']['membership']['weight'] > 0
            arms.append((f'{name}_r{retention:g}_d{delta:g}', cfg))
    assert len(arms) == COUNTS[2]
    return arms
