"""Derive joint axes from actual graph branches, independent of cached old axes."""
from copy import deepcopy

ROLES = ('membership', 'top', 'rest')
EARLY_GROUPS = ('diverse_augmentation', 'secondary_augmentation',
                'final_augmentation', 'linear_augmentation')


def active_axes(graph):
    result = []
    root = graph['root']
    if root['kind'] == 'complete_r30':
        configuration = root['configuration']
        for group in EARLY_GROUPS:
            if configuration.get('standalone') and group in EARLY_GROUPS[:2]:
                continue
            for role in ROLES:
                spec = configuration[group][role]
                if spec['weight'] > 0:
                    result.append({'round': root['round'], 'group': group, 'role': role,
                                   'model': spec['model'], 'anchor': spec['weight']})
    else:
        assert root['kind'] == 'standalone'
    for layer in graph['layers']:
        for role in ROLES:
            spec = layer['specs'][role]
            if spec['weight'] > 0:
                result.append({'round': layer['round'], 'group': layer['group'], 'role': role,
                               'model': spec['model'], 'anchor': spec['weight']})
    keys = [(axis['round'], axis['group'], axis['role']) for axis in result]
    assert len(keys) == len(set(keys))
    assert all(axis['model'] != 'none' and 0 < axis['anchor'] <= .8 for axis in result)
    return result


def target(graph, axis):
    if axis['round'] == graph['root']['round']:
        return graph['root']['configuration'][axis['group']][axis['role']]
    layer = next(item for item in graph['layers'] if item['round'] == axis['round'])
    assert layer['group'] == axis['group']
    return layer['specs'][axis['role']]


def with_weight(graph, axis, weight, frozen_axes):
    assert 0 <= weight <= .8
    key = (axis['round'], axis['group'], axis['role'], axis['model'])
    assert key in {(a['round'], a['group'], a['role'], a['model']) for a in frozen_axes}
    result = deepcopy(graph)
    spec = target(result, axis)
    assert spec['model'] == axis['model']
    spec['weight'] = float(weight)
    return result


def retention_axes(graph):
    return [{'kind': 'root', 'round': graph['root']['round']}] + [
        {'kind': 'layer', 'round': layer['round']} for layer in graph['layers']
        if layer['specs']['membership']['weight'] > 0]


def expected_records(graph):
    return 1 + 18 * len(active_axes(graph)) + 5 * len(retention_axes(graph)) + 20


def weight_values(anchor):
    return (0., anchor * .5, anchor, min(.8, anchor * 2),
            min(.8, anchor + .0125), min(.8, anchor + .025))
