from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'publish_actual_prospective_and_delivery_main_v57_20261009.py';new=A/'publish_neural_medium_restart_main_v58_20261009.py'
s=old.read_text(encoding='utf8').replace('actual_prospective_and_delivery_main_v57','neural_medium_restart_main_v58').replace('actual_prospective_and_delivery_v57','neural_medium_restart_v58')
s=s.replace('actual_prospective_and_delivery_safe_publication_v57','neural_medium_restart_safe_publication_v58')
needle=" for p in A.glob('*round148*20261009.py'):sources.append(p)";assert needle in s
add=""" closed('actual_BF16_medium2048_seed09_restart_control_v1_20261009')
 neural_pointer=A/'actual_BF16_medium2048_seed09_restart_location_v1_20261009.json'
 neural_out=Path(read(neural_pointer)['output']);neural_proof=neural_out/'verification.json'
 assert sha(neural_proof)==read(neural_pointer)['verification_sha256']
 neural=read(neural_proof);assert len(neural['records'])==2
 assert all(r['all_training_losses_and_all_weight_bits_exact'] and r['preprocessing_and_native_prediction_bits_exact'] and r['actual_fixed8192_cold_prefix_bits_exact'] and r['changed_training_input_checkpoint_rejected'] for r in neural['records'])
 sources.extend([neural_pointer,neural_proof,A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json',A/'neural_BF16_medium2048_seed09_e64_hidden_launches_v1_20261009.json'])
 for p,d in read(A/'neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json')['input_sha256'].items():
  assert sha(p)==d,p
  if Path(p).suffix=='.py':sources.append(Path(p))
 for p,d in neural['input_sha256'].items():
  assert sha(p)==d,p
  if Path(p).suffix in ('.py','.json'):sources.append(Path(p))
 sources.extend(p for p in neural_out.rglob('*') if p.is_file() and p.suffix in ('.json','.log'))
 for n in ('actual_BF16_medium2048_seed09_restart_control_v1_20261009','actual_BF16_medium2048_seed09_e64_bank6_v1_20261009'):
  f=A/'service_owned_workflows_20261006'/n
  sources.extend(f/p for p in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
  if n.endswith('restart_control_v1_20261009'):sources.extend(f/p for p in ('service_execution.json','stdout.log','stderr.log'))
 bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_seed09_e64_bank6_v1_20261009')
 if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')
"""
s=s.replace(needle,add+needle)
needle="'actual148_delivered_submission_verified':True,";assert needle in s
s=s.replace(needle,"'actual148_delivered_submission_verified':True,'new_neural_medium_restart_controls_passed':True,'new_neural_annual_fits_not_yet_qualified':True,")
s=s.replace("'同步152完整32路径200方案图验证、150至152安全发布接收流程和148交付核验'","'同步BF16中型2048新种子64轮方案及实际重启和重载逐位验证，年度训练进行中'")
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('neural_medium_restart_main_publication_v58_20261009',new.name,[],{str(new):sha(new),str(Path(__file__)):sha(__file__)})
create(A/'neural_medium_restart_main_hidden_launch_v58_20261009.json',row);print(row['owned_worker_pid'])
