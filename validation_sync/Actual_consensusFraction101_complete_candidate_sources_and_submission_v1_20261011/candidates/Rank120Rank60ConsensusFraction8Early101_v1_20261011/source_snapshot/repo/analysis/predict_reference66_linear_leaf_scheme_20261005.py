"""Copy the effective explicit-parent sources and use the established native codec."""
from pathlib import Path
import shutil


def source_names(number):
    return ('linear_leaf_reference66_search_engine_20261005.py',
        'explicit_parent_release_engine_20261005.py',
        'parallel_candidate_scoring_one_20261005.py',
        'run_reference66_linear_leaf_round_20261005.py',
        'publish_explicit_parent_training_round_20261005.py',
        'check_reference66_linear_leaf_scheme_20261005.py',
        'predict_reference66_linear_leaf_scheme_20261005.py',
        f'optimize_training_round{number}.py',f'finalize_training_round{number}.py',
        f'run_training_round{number}_pipeline.py',
        *(() if number==81 else ('optimize_training_round81.py','finalize_training_round81.py')))


def copy_sources(ns,candidate):
    candidate=Path(candidate)
    assert not (candidate/'manifest.json').exists(),'A sealed candidate must not be edited.'
    candidate.mkdir(parents=True,exist_ok=True)
    for name in source_names(ns.NUMBER):
        shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)


def predict(ns,record,candidate_path=None,mapping_path=None):
    from predict_linear_leaf_scheme_20261005 import predict as original
    candidate=Path(candidate_path) if candidate_path is not None else ns.ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    copy_sources(ns,candidate)
    original(ns,record,candidate_path=candidate,mapping_path=mapping_path)
    copy_sources(ns,candidate)
