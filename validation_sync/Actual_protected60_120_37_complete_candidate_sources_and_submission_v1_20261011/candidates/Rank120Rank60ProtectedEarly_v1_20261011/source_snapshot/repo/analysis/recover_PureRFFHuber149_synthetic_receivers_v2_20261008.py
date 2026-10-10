"""Preserve unscored import failure; verify reduced physical-head forecast against zero-Ridge reference."""
from pathlib import Path
import sys,time,json,io,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 failed=A/'service_owned_workflows_20261006/PureRFFHuber124_actual_synthetic_controls_v1_20261008/service_execution.json';assert read(failed)['status']=='failed'
 originals=[];products=[]
 for stem in ('PureRFFHuber_ordered_CDF','PureRFFHuber_ordered_native_stage'):
  p=A/(stem+'_v1_20261008.py');originals.append(p);s=p.read_text(encoding='utf8').replace('HuberPureRFFMean_complete_parent_CDF_v1_20261008','HuberCrossFamilyFine_complete_parent_CDF_v1_20261008')
  s=s.replace('PureRFFHuber_ordered_CDF_v1_20261008','PureRFFHuber_ordered_CDF_v2_20261008')
  products.append(save(stem+'_v2_20261008.py',s))
 p=A/'verify_PureRFFHuber124_synthetic_controls_v1_20261008.py';originals.append(p);s=p.read_text(encoding='utf8')
 for before,after in [('PureRFFHuber_ordered_CDF_v1','PureRFFHuber_ordered_CDF_v2'),('PureRFFHuber124_synthetic_v1','PureRFFHuber124_synthetic_v2'),('actual_PureRFFHuber124_synthetic_location_v1','actual_PureRFFHuber124_synthetic_location_v2')]:s=s.replace(before,after)
 tokens=list(tokenize.generate_tokens(io.StringIO(s).readline));s=tokenize.untokenize([t._replace(string={'181':'124','543':'372','81':'54'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
 needle=" import PureRFFHuber_ordered_CDF_v2_20261008 as codec\n";assert s.count(needle)==1
 s=s.replace(needle,needle+" import CrossFamilyFine_complete_parent_CDF_v1_20261008 as zero_ridge_reference\n")
 s=s.replace('Path(codec.huber.__file__)]','Path(codec.huber.__file__),Path(zero_ridge_reference.__file__)]')
 needle="  if not any(case[n]['amplitude'] for n in ('cross','huber')):exact(value,base)\n";assert s.count(needle)==1
 s=s.replace(needle,needle+'''  reference_raw={**raw,'ridge_l001':rng.normal(size=len(base)),'ridge_l025':rng.normal(size=len(base))}
  reference=np.array(base,dtype=np.float64,copy=True)
  for stage in case['order']:
   cfg=case[stage]
   if not cfg['amplitude']:continue
   original=zero_ridge_reference if stage=='cross' else codec.huber
   residual=original.independent_mixture(reference_raw,4,cfg['share'])
   reference=original.pandas_oracle(reference,residual,dates,flags,valid,cfg['amplitude'])
  exact(value,reference)
''')
 s=s.replace("'historical_full_rows_or_native_saved_model_replays_not_claimed_by_synthetic_controls':True", "'actual_zero_Ridge_reference_full_forecast_bits_equal_for_all124_cases':True,'historical_full_rows_or_native_saved_model_replays_not_claimed_by_synthetic_controls':True")
 products.append(save('verify_PureRFFHuber124_synthetic_controls_v2_20261008.py',s))
 meta=A/'PureRFFHuber149_synthetic_receiver_recovery_v2_20261008.json'
 create(meta,{'status':'prepared_actual_Huber_import_and124_count_and_reduced_RFF_forecast_reference_controls',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),failed,*originals,*products]},
  'all_original_failures_and_files_retained':True,'original149_grid_unchanged':True,'actual_native_or_full_historical_replay_not_claimed':True,'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p) for p in [Path(__file__),meta,*products,A/'PureRFFHuber128_round149_proposal_v1_20261008.json']}
 row=start('PureRFFHuber124_actual_synthetic_controls_v2_20261008',products[-1].name,[],pins)
 create(A/'PureRFFHuber149_synthetic_hidden_launch_v2_20261008.json',{'launch':row,'input_sha256':pins,'new_quality_scores':0});print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
