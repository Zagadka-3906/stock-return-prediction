"""Publish truthful medium153 proposal/synthetic/actual CPU controls and current annual records."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'publish_actual_entry_and_partial_neural_main_v59_20261009.py';new=A/'publish_medium153_controls_main_v60_20261009.py'
    s=old.read_text(encoding='utf8').replace('actual_entry_and_partial_neural_main_v59','medium153_controls_main_v60').replace('actual_entry_and_partial_neural_v59','medium153_controls_v60').replace('actual_entry_and_partial_neural_safe_publication_v59','medium153_controls_safe_publication_v60')
    needle=' for p in A.glob(\'*round148*20261009.py\'):sources.append(p)';assert s.count(needle)==1
    addition=""" closed('PureRFFHuber128_scores_main_publication_v1_20261008')
 closed('BF16Medium153_independent_small_CPU_v1_20261009')
 small=Path('E:/赛题五_本机临时/BF16Medium153_independent_small_CPU_v1_20261009/verification.json')
 actualsmall=read(small);assert len(actualsmall['controls'])==4
 sources.extend([small,*small.parent.glob('*.json'),Path(__file__)])
 for f,d in actualsmall['input_sha256'].items():
  assert sha(f)==d,f
  if Path(f).suffix in ('.py','.json'):sources.append(Path(f))
 for pattern in ('*BF16Medium153*20261009.py','*BF16Medium153*20261009.json','BF16Medium78*20261009.json','*actual_medium153*20261009.py','*actual_medium153*20261009.json'):
  sources.extend(p for p in A.glob(pattern) if p.is_file())
 sources.extend(A/n for n in ('monitor_actual_chronological_optimization_progress_v56_20261009.py',
  'latest_actual_optimization_progress_pointer_v56_20261009.json','neural_BF16_medium2048_seed09_independent_forward_v1_20261009.py'))
 for n in ('BF16Medium153_independent_small_CPU_v1_20261009','BF16Medium153_independent_full5_GPU_controls_v1_20261009',
  'BF16Medium153_actual_full73_training_v1_20261009','BF16Medium153_actual_native42_calendar_v1_20261009'):
  f=A/'service_owned_workflows_20261006'/n
  sources.extend(f/p for p in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
  if (f/'service_execution.json').exists():sources.extend(f/p for p in ('service_execution.json','stdout.log','stderr.log'))
 synth=read(A/'BF16Medium78_synthetic73_cold219_v1_20261009.json')
 assert (synth['actual_cases'],synth['actual_cold_cases'])==(73,219)
 for f,d in synth['input_sha256'].items():
  assert sha(f)==d,f
  if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
"""
    s=s.replace(needle,addition+needle)
    s=s.replace("'actual149_all25_annual_native100_cold100_and152_native60_full25_cold75_historical_controls'","'actual_medium153_synthetic73_prefix219_CPU10017_four_prefixes_and_annual_partial_records'")
    s=s.replace("'new_native_fits':0,'test_labels_read':False,'primary_workspace_dirty_index_preserved':True", "'actual153_synthetic_cases':73,'actual153_synthetic_cold_cases':219,'actual153_small_CPU_rows':10017,'actual153_small_CPU_prefixes':4,'actual153_complete_six_state_native_and_full_training_controls_not_yet_claimed':True,'actual153_official_scores':0,'actual153_future_X_read':False,'new_native_fits_by_publication':0,'test_labels_read':False,'primary_workspace_dirty_index_preserved':True")
    s=s.replace('同步152的88接口核对及新中型神经网络已完成年度训练证据，剩余年度继续运行','同步153的73组合219前缀及独立CPU控制，真实六状态验证已排队')
    compile(s,str(new),'exec')
    with new.open('x',encoding='utf8') as f:f.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('medium153_controls_main_publication_v60_20261009',new.name,[],{str(new):sha(new),str(Path(__file__)):sha(__file__)})
    create(A/'medium153_controls_main_hidden_launch_v60_20261009.json',row);print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
