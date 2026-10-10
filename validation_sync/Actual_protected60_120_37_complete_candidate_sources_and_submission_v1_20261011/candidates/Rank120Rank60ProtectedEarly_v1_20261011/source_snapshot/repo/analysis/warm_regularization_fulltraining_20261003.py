"""Fit frozen raw architectures on mature supplied training data; never infer test rows."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_neural_regularization_bank_20261003 as bank


def main():
    bank.verify();assert bank.read(bank.OUT/'oof_audit.json')['status']=='passed'
    target=bank.OUT/'fulltraining_cache_audit.json'
    if target.exists():
        for path,digest in bank.read(target)['output_sha256'].items():assert bank.sha(path)==digest,path
        return
    info={name:bank.train_one(name,2025) for name in bank.CONFIGS}
    assert all(row['fulltraining_only_test_prediction_not_generated'] and not row['test_data_read'] for row in info.values())
    paths=[bank.OUT/name/f'{kind}_2025.{suffix}' for name in bank.CONFIGS
           for kind,suffix in (('model','joblib'),('info','json'))]
    bank.dump(target,{'status':'passed','raw_architectures_frozen_before_fit':True,
         'complete_output_scheme_still_requires_validation_selection_and_freeze':True,
         'fulltraining_models':4,'new_annual_oof_fits':0,'new_model_scores':0,
         'test_X_inference_generated':False,'test_labels_read':False,
         'output_sha256':{str(path.resolve()):bank.sha(path) for path in paths},
         'script_sha256':bank.sha(Path(__file__)),
         'completed_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Four frozen raw architectures fitted; no test inference or scores generated.',flush=True)


if __name__=='__main__':main()
