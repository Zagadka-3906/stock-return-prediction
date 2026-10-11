"""Infer the latest jointly changed graph using the existing verified model loader."""
from pathlib import Path
import shutil


def predict(record, candidate_path=None, mapping_path=None):
    import optimize_training_round63 as experiment
    from predict_nystrom_ridge_scheme_20261004 import predict as original
    candidate = Path(candidate_path) if candidate_path is not None else experiment.ROOT / 'candidates/optimization_20261003_r63'
    candidate.mkdir(parents=True, exist_ok=True)
    for name in ('latest_graph_joint_axes_20261005.py', 'optimize_training_round63.py',
                 'finalize_training_round63.py', 'check_latest_joint_scheme_20261005.py',
                 'predict_latest_joint_scheme_20261005.py'):
        shutil.copyfile(experiment.ROOT / 'analysis' / name, candidate / name)
    original(experiment, record, candidate_path=candidate, mapping_path=mapping_path)
