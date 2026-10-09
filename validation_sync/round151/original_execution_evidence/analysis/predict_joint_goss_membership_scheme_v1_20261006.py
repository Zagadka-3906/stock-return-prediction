"""Copy round97 and all effective parent codecs before and after shared prediction."""
from pathlib import Path
import shutil
from predict_ready_goss_reference_scheme_v2_20261006 import source_names as previous_sources

def source_names(number):
    assert number == 97
    return tuple(dict.fromkeys((*previous_sources(96),
        'joint_goss_membership_retention_grid_v2_20261006.py',
        'joint_goss_membership_search_engine_v1_20261006.py',
        'joint_goss_membership_release_engine_v1_20261006.py',
        'run_joint_goss_membership_round_v1_20261006.py',
        'check_joint_goss_membership_scheme_v1_20261006.py',
        'predict_joint_goss_membership_scheme_v1_20261006.py',
        'optimize_training_round97_v1.py','finalize_training_round97_v1.py',
        'run_training_round97_v1_pipeline.py')))

def copy_sources(ns,candidate):
    candidate=Path(candidate)
    assert not (candidate/'manifest.json').exists(),'A sealed candidate must not be edited.'
    candidate.mkdir(parents=True,exist_ok=True)
    for name in source_names(ns.NUMBER):
        shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)
        for suffix in ('_v1.py','_v2.py','_v3.py'):
            if name.startswith(('optimize_training_round','finalize_training_round')) and name.endswith(suffix):
                shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name[:-len(suffix)]+'.py')

def predict(ns,record,candidate_path=None,mapping_path=None):
    from predict_gradient_sampling_scheme_codec_20261005 import predict as original
    candidate=Path(candidate_path) if candidate_path is not None else ns.ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    copy_sources(ns,candidate)
    original(ns,record,candidate_path=candidate,mapping_path=mapping_path)
    copy_sources(ns,candidate)
