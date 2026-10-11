from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'publish_neural_medium_restart_main_v58_20261009.py';new=A/'publish_actual_entry_and_partial_neural_main_v59_20261009.py'
s=old.read_text(encoding='utf8').replace('neural_medium_restart_main_v58','actual_entry_and_partial_neural_main_v59').replace('neural_medium_restart_v58','actual_entry_and_partial_neural_v59')
s=s.replace('neural_medium_restart_safe_publication_v58','actual_entry_and_partial_neural_safe_publication_v59')
needle=" if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')";assert needle in s
extra=""" if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')
 for info in sorted(bank.glob('*/info.json')):
  row=read(info);assert row['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
  assert sha(info.parent/'model.joblib')==row['model_sha256']
  assert row['training_meta']['last_label_end']<=row['training_meta']['cutoff_exclusive']
  if int(row['year'])<2025:
   assert sha(info.parent/'raw.parquet')==row['prediction_sha256']
   assert row['actual_full_annual_reload_prediction_bits_exact'] and row['actual_cold80_prefix_bits_exact']
  sources.extend([info,info.parent/'frozen_training_inputs.json'])
 sources.extend(A/n for n in ('SparseAfter148152_static_entry_consistency_v1_20261009.json',
  'verify_SparseAfter148152_static_entry_consistency_v1_20261009.py','monitor_actual_chronological_optimization_progress_v55_20261009.py',
  'prepare_actual_neural_and_quality_progress_v55_20261009.py','actual_neural_and_quality_progress_hidden_launch_v55_20261009.json',
  'latest_actual_optimization_progress_pointer_v55_20261009.json'))
"""
s=s.replace(needle,extra)
s=s.replace("'同步BF16中型2048新种子64轮方案及实际重启和重载逐位验证，年度训练进行中'","'同步152的88接口核对及新中型神经网络已完成年度训练证据，剩余年度继续运行'")
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('actual_entry_and_partial_neural_main_publication_v59_20261009',new.name,[],{str(new):sha(new),str(Path(__file__)):sha(__file__)})
create(A/'actual_entry_and_partial_neural_main_hidden_launch_v59_20261009.json',row);print(row['owned_worker_pid'])
