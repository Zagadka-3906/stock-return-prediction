"""Finish frozen meta/child full fits without reading test feature rows or labels."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main():
    gates=[ROOT/'analysis/oof_stacking_bank_20261004/oof_audit.json',
           ROOT/'analysis/current_day_input_loading_qa_20261004/verification.json']
    while not all(p.exists() for p in gates):time.sleep(10)
    import stacking_model_sources_20261004 as models
    models.verify()
    name=next(iter(models.NEW_CONFIGS));info=models.train_one(name,2025)
    models.dump(ROOT/'analysis/stacking_fulltraining_warmup_20261004.json',
        {'status':'passed','model':name,'fulltraining_info':info,'fulltraining_only_test_prediction_not_generated':True,
         'test_data_read':False,'script_sha256':models.sha(Path(__file__))},immutable=True)
    print('One frozen stacking full fit warmed; all45 child models fitted before any test inference',flush=True)


if __name__=='__main__':main()
