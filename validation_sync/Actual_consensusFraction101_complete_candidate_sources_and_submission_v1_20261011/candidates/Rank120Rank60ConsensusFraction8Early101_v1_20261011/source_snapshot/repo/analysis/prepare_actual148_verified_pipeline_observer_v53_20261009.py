from pathlib import Path
import sys,re
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
old=A/'monitor_actual_chronological_optimization_progress_v52_20261009.py';new=A/'monitor_actual_chronological_optimization_progress_v53_20261009.py'
names={
 'AdaptiveJointCrossHuber242_round148_full_registration_v2_20261009':'AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009',
 'PureRFFHuber80_native_historical_calendar_controls_v4_20261009':'PureRFFHuber80_native_historical_calendar_controls_v6_20261009',
 'PureRFFHuber124_actual_full_historical_controls_v4_20261009':'PureRFFHuber124_actual_full_historical_controls_v5_20261009',
 'Pure149_prior_complete_forecast_duplicate_audit_v3_20261009':'Pure149_prior_complete_forecast_duplicate_audit_v4_20261009',
 'PureRFFHuber149_complete_chronological_dispatch_v7_20261009':'PureRFFHuber149_complete_chronological_dispatch_v11_20261009',
 'PureRFFHuber20_year2023_native_supplement_v1_20261009':'PureRFFHuber20_year2023_native_supplement_v2_20261009',
 'PureRFFHuber25_all5_annual_native_coverage_v1_20261009':'PureRFFHuber25_all5_annual_native_coverage_v2_20261009',
 'SparseAfter14860_native_historical_calendar_controls_v1_20261009':'SparseAfter14860_native_historical_calendar_controls_v2_20261009',
 'SparseAfter14825_full_historical_controls_v1_20261009':'SparseAfter14825_full_historical_controls_v2_20261009',
 'actual149_all5_and152_historical_main_publication_v52_20261009':'actual149_all5_and152_historical_main_publication_v55_20261009',
 'optimization_live_progress_v52_20261009':'optimization_live_progress_v53_20261009'}
s=old.read_text(encoding='utf8');pattern=re.compile('|'.join(re.escape(k) for k in sorted(names,key=len,reverse=True)));s=pattern.sub(lambda m:names[m[0]],s)
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
create(A/'actual148_verified_pipeline_observer_preparation_v53_20261009.json',{'status':'prepared_current_actual_passed148_and_recovered149152_bindings','input_sha256':{str(p):sha(p) for p in (old,new,Path(__file__))},'new_scoring':0})
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('actual_chronological_optimization_progress_observer_v53_20261009',new.name,[],{str(new):sha(new)})
create(A/'actual148_verified_pipeline_observer_hidden_launch_v53_20261009.json',row)
print(row['owned_worker_pid'])
