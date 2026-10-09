"""Recover inference routing without changing frozen meta fits or OOF forecasts."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_oof_stacking_bank_20261004 as bank
import causal_model_loading_20261004 as loading


def main():
    bank.verify();loading.install(bank.members)
    sources=[Path(__file__),Path(loading.__file__),ROOT/'analysis/stacking_model_sources_20261004.py',
             bank.OUT/'protocol.json',bank.OUT/'feature_audit.json',
             ROOT/'analysis/oof_stacking_replay_diagnostic_20261004.json']
    protocol=bank.OUT/'input_routing_recovery_protocol.json'
    if protocol.exists():
        for path,digest in bank.read(protocol)['input_sha256'].items():assert bank.sha(path)==digest,path
    else:
        bank.dump(protocol,{'status':'frozen_before_replay_and_scoring','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
             'reason':'The later generic joblib loader bypassed the existing cross-sectional input marker for three child models. Their cached OOF predictions and the meta fits are correct; restore the required marker during model loading.',
             'meta_fit_or_cached_prediction_changed':False,'frozen_original_sources_changed':False,
             'test_data_read':False,'input_sha256':{str(p.resolve()):bank.sha(p) for p in sources}},immutable=True)
    bank.all_oof()


if __name__=='__main__':main()
