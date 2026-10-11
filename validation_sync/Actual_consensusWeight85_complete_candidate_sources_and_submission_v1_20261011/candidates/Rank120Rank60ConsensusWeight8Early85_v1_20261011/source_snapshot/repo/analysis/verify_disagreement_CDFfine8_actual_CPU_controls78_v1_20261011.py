"""Actual independent CDF controls for all six new allocation configurations."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
import numpy as np
import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec
import rank120_rank60_disagreement_raw_signal_v1_20261011 as mixing
rng=np.random.default_rng(2026101176);n=2000;dates=np.repeat(np.arange(20200101,20200121),100)
parent=rng.normal(size=n).astype('float64');a=rng.normal(size=n);b=rng.normal(size=n);valid=rng.random(n)>.12;flags=rng.random(n)<.1
a[~valid]=b[~valid]=-1e6
rows=[]
for k in (-.5,.5):
 raw=mixing.combine(a,b,k)
 assert np.array_equal(raw.view('u8'),mixing.scalar_oracle(a,b,k).view('u8'))
 for w in (.0005,.002,.008):
  value=codec.transform(parent,raw,dates,flags,valid,'nonflag_valid',w,1.)
  independent=codec.pandas_oracle(parent,raw,dates,flags,valid,'nonflag_valid',w,1.)
  assert np.array_equal(value.view('u8'),independent.view('u8'))
  mask=codec.selected(flags,valid,'nonflag_valid');assert np.array_equal(value[~mask].view('u8'),parent[~mask].view('u8'))
  prefixes=[]
  for count in (100,700,1500):
   x=codec.transform(parent[:count],raw[:count],dates[:count],flags[:count],valid[:count],'nonflag_valid',w,1.)
   y=codec.pandas_oracle(parent[:count],raw[:count],dates[:count],flags[:count],valid[:count],'nonflag_valid',w,1.)
   assert np.array_equal(x.view('u8'),value[:count].view('u8')) and np.array_equal(x.view('u8'),y.view('u8'));prefixes.append(count)
  poisoned=raw.copy();poisoned[1500:]*=-999.;future=codec.transform(parent,poisoned,dates,flags,valid,'nonflag_valid',w,1.)
  assert np.array_equal(future[:1500].view('u8'),value[:1500].view('u8'))
  rows.append({'disagreement_penalty':k,'weight':w,'full_independent_Pandas_bits_exact':True,'prefix_rows':prefixes,'future_suffix_poison_does_not_change_prior_predictions':True,'unselected_parent_bits_preserved':True})
create(A/'actual_disagreement_CDFfine8_six_cases_CPU_controls78_v1_20261011.json',{'status':'passed_actual6_full_Pandas18_prefix6_future_suffix_controls_no_labels','input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(codec.__file__),Path(mixing.__file__),A/'rank120_rank60_disagreement_CDFfine8_predeclared_sources77_v1_20261011.json']},'records':rows,'synthetic_rows':n,'actual_TRAIN_scores_and_native_GPU_qualification_not_yet_claimed':True,'future_X_read':False,'test_labels_read':False})
print({'actual_full_CPU_Pandas':6,'actual_prefix_CPU':18,'actual_future_suffix_controls':6,'actual_TRAIN_gain_not_claimed':True},flush=True)
