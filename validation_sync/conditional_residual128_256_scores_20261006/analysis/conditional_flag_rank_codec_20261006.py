"""Independent numerical-tree decoder for actual LightGBM flag specialists."""
import numpy as np


def clean_matrix(values):
    values = np.asarray(values, dtype=np.float32)
    return np.ascontiguousarray(np.where(np.isfinite(values), values, np.nan), dtype=np.float32)


def predict_dump(model, values):
    values = clean_matrix(values)
    assert model['objective'].split()[0] == 'regression'
    assert not model['average_output']
    output = np.zeros(len(values), dtype=np.float64)
    for tree in model['tree_info']:
        stack = [(tree['tree_structure'], np.arange(len(values)))]
        prediction = np.empty(len(values), dtype=np.float64)
        while stack:
            node, rows = stack.pop()
            if not len(rows):
                continue
            if 'leaf_value' in node:
                prediction[rows] = float(node['leaf_value'])
                continue
            assert node['decision_type'] == '<='
            column = values[rows, int(node['split_feature'])].astype(np.float64)
            missing_type = node['missing_type']
            if missing_type == 'None':
                column = np.where(np.isnan(column), 0., column)
                missing = np.zeros(len(rows), dtype=bool)
            elif missing_type == 'NaN':
                missing = np.isnan(column)
            else:
                assert missing_type == 'Zero'
                missing = np.isnan(column) | (column == 0.)
            left = column <= float(node['threshold'])
            left[missing] = bool(node['default_left'])
            stack.append((node['left_child'], rows[left]))
            stack.append((node['right_child'], rows[~left]))
        output += prediction
    assert np.isfinite(output).all()
    return output
