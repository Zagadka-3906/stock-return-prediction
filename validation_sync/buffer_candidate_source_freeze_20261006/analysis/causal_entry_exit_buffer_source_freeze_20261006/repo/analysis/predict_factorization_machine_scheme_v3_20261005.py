from pathlib import Path
import shutil
from predict_factorization_machine_scheme_20261005 import predict as original

def predict(ns,record,candidate_path=None,mapping_path=None):
    candidate=Path(candidate_path) if candidate_path is not None else ns.ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    candidate.mkdir(parents=True,exist_ok=True)
    for name in ('factorization_machine_search_engine_v3_20261005.py','predict_factorization_machine_scheme_v3_20261005.py',f'optimize_training_round{ns.NUMBER}_v3.py'):
        shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)
    original(ns,record,candidate_path=candidate,mapping_path=mapping_path)
