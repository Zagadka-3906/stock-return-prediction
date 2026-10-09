"""Copy the effective explicit-parent sources and use the established native codec."""
from pathlib import Path
import shutil


def source_names(number):
    return ('ready_fm_reference_search_engine_20261005.py',
        'explicit_parent_release_engine_v2_20261005.py',
        'parallel_candidate_scoring_one_20261005.py',
        'run_ready_fm_reference_round_20261005.py',
        'publish_explicit_parent_training_round_v2_20261005.py',
        'check_ready_fm_reference_scheme_20261005.py',
        'predict_ready_fm_reference_scheme_20261005.py',
        f'optimize_training_round{number}_v2.py',f'finalize_training_round{number}_v2.py',
        f'run_training_round{number}_v2_pipeline.py',
        'optimize_training_round81_v2.py','optimize_training_round82_v2.py',
        'linear_leaf_reference66_search_engine_v2_20261005.py',
        *(() if number==83 else ('optimize_training_round83_v2.py','finalize_training_round83_v2.py')))


def copy_sources(ns,candidate):
    candidate=Path(candidate)
    assert not (candidate/'manifest.json').exists(),'A sealed candidate must not be edited.'
    candidate.mkdir(parents=True,exist_ok=True)
    for name in source_names(ns.NUMBER):
        shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)
        if name.startswith(('optimize_training_round','finalize_training_round')) and name.endswith('_v2.py'):
            shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name.replace('_v2.py','.py'))


def predict(ns,record,candidate_path=None,mapping_path=None):
    from predict_factorization_machine_scheme_codec_v2_20261005 import predict as original
    candidate=Path(candidate_path) if candidate_path is not None else ns.ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    copy_sources(ns,candidate)
    original(ns,record,candidate_path=candidate,mapping_path=mapping_path)
    copy_sources(ns,candidate)
