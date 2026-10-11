"""Recheck unchanged, architecture-independent H60 fixture bits; no new fit claim."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('StockRank60Embedding_actual_mature_fixture_CPU_v1_20261011')
 import numpy as np
 import stock_rank60medium_embedding_medium2048_BF16_native_v1_20261011 as native
 pointer=A/'actual_stock_rank60_embedding_mature_fixture_location_v1_20261011.json'
 f=Path(read(pointer)['output']);proof=read(f/'verification.json')
 assert sha(f/'verification.json')==read(pointer)['verification_sha256']
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 prior=proof['configuration'];cfg=native.CONFIG
 assert {k:v for k,v in cfg.items() if k not in ('hidden','recipe')}=={k:v for k,v in prior.items() if k not in ('hidden','recipe')}
 x=np.load(f/'past_features121.npy');y=np.load(f/'past_rank60_targets.npy')
 assert x.shape==(49153,121) and y.shape==(49153,)
 assert native.array_sha(x)==proof['feature121_sha256']
 assert native.array_sha(y)==proof['raw_rank60_target_sha256']
 assert proof['last_label_end']<proof['cutoff_exclusive']==20191231
 assert proof['numeric120_full_supplied_peer_Pandas_bits_exact'] and proof['actual_future_label_poisoning_same_keys_and_targets']
 create(A/'stock_rank60medium_embedding_reused_maturity_fixture_actual_controls_v1_20261011.json',{
  'status':'passed_actual_rehashed_same_H60_mature_fixture_arrays_and_capacity_independent_configuration',
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),pointer,f/'verification.json',f/'past_features121.npy',f/'past_rank60_targets.npy',Path(native.__file__)]},
  'source_actual_CPU_controls':str(f/'verification.json'),'actual_array_checks':2,'new_fits':0,'new_scores':0,'test_labels_read':False})
 print('Actual unchanged mature H60 fixture hashes verified for the new capacity.',flush=True)
if __name__=='__main__':main()
