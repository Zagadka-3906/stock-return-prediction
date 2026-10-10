"""Preserve the frozen r7 run; repair only the original-control reduction order."""
from pathlib import Path
import argparse
import time

import optimize_training_round7 as original
from optimize_training_round7 import ROOT,OUT,read,dump,sha,log
import experiments.final_sweep_wave3 as ensemble_module

_ensemble_raw=ensemble_module.ensemble_raw


def ensemble_raw_with_original_order(panel,members,cache_raws):
    if 'old_pruned' in members:
        names=('lgb','xgb','two','old_pruned','gru')
        assert set(members)==set(names)
        members={name:members[name] for name in names}
    return _ensemble_raw(panel,members,cache_raws)


def amendment():
    original.verify()
    path=OUT/'repair_amendment.json'
    if not path.exists():
        assert not (OUT/'wave59_results.json').exists() and not (OUT/'component_audit.json').exists()
        sources=[Path(__file__),ROOT/'analysis/optimize_training_round7.py',ROOT/'analysis/finalize_training_round7.py']
        dump(path,{'recorded_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
             'reason':'Original-control dict pop appended old_pruned after GRU, changing floating reduction order by at most2.22e-16; the bit-identity assertion fired before any scoring.',
             'correction':'Original-control order is lgb,xgb,two,old_pruned,gru, matching frozen W5a. Corrected candidate definitions and their reduction order are unchanged.',
             'prior_scored_records':0,'prior_protocol_preserved':True,'test_labels_read':False,
             'source_sha256':{str(p):sha(p) for p in sources}},immutable=True)
    for source,digest in read(path)['source_sha256'].items():assert sha(source)==digest,source
    ensemble_module.ensemble_raw=ensemble_raw_with_original_order


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('build','coarse','fine','refinement','all'))
    stage=parser.parse_args().stage
    amendment()
    for name in (('build','coarse','fine','refinement') if stage=='all' else (stage,)):getattr(original,name)()


if __name__=='__main__':main()
