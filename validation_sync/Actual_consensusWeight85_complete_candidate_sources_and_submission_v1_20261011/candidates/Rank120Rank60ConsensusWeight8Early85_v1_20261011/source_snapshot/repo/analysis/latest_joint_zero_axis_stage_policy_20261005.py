"""Preserve two nonempty coordinate stages when the selected root has no weights."""
from pathlib import Path
from latest_graph_joint_axes_20261005 import active_axes, expected_records


def actual_records(graph):
    return expected_records(graph) + (2 if not active_axes(graph) else 0)


def install(module):
    old_count = module.expected_records
    old_coordinate = module.coordinate_pass
    old_dump = module.dump

    def coordinate(wave, earlier, order):
        order = list(order)
        if order:
            return old_coordinate(wave, earlier, order)
        module.verify()
        winner = module.prior_best(earlier)
        return module.execute(wave, [('unchanged_no_active_weight_axes', module.configuration(winner))])

    def dump(path, value, *args, **kwargs):
        if Path(path).resolve() == (module.OUT / 'protocol.json').resolve():
            value = dict(value)
            value['records_formula'] = '1+6*A+max(1,6*A)+max(1,6*A)+5*R+20; A=actual active weights; R=actual membership retention axes'
            value['zero_active_weight_coordinate_stages'] = {'records_each': 1,
                'unchanged_baseline_control_only': True, 'not_new_model_fits': True}
        return old_dump(path, value, *args, **kwargs)

    module.expected_records = actual_records
    module.coordinate_pass = coordinate
    module.dump = dump

    def restore():
        module.expected_records = old_count
        module.coordinate_pass = old_coordinate
        module.dump = old_dump

    return restore
