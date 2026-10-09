"""Queue complete73/219 historical evidence publication after real controls and149 main closeout."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'publish_medium153_native_main_v62_20261009.py';new=A/'publish_medium153_fulltraining_main_v63_20261009.py'
    s=old.read_text(encoding='utf8').replace('medium153_native_main_v62','medium153_fulltraining_main_v63').replace('medium153_native_v62','medium153_fulltraining_v63').replace('medium153_native_safe_publication_v62','medium153_fulltraining_safe_publication_v63')
    needle=" jobs=['AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009',";assert s.count(needle)==1
    s=s.replace(needle," closed('PureRFFHuber128_round149_full_registration_v1_20261008')\n closed('BF16Medium153_actual_full73_training_v1_20261009')\n"+needle)
    needle=" if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')";assert s.count(needle)==1
    addition=""" p=A/'actual_BF16Medium153_full73_training_location_v1_20261009.json';out=Path(read(p)['output']);v=out/'verification.json'
 assert sha(v)==read(p)['verification_sha256'];complete=read(v)
 assert (complete['actual_parent_round'],complete['actual_full_cases'],complete['actual_cold_cases'])==(148,73,219)
 assert len(complete['controls'])==73 and all(len(r['controls'])==3 and r['full_independent_Pandas_bits_exact'] for r in complete['controls'])
 sources.extend([p,*out.glob('*.json')])
 for f,d in complete['input_sha256'].items():
  assert sha(f)==d,f
  if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 sources.extend(A/n for n in ('prepare_medium153_native_main_v62_20261009.py','medium153_native_main_v62_receipt_20261009.json',
  'prepare_medium153_fulltraining_main_v63_20261009.py','prepare_BF16Medium78_round153_sources_v1_20261009.py'))
"""
    s=s.replace(needle,addition+needle)
    s=s.replace('actual_medium153_5635800_full5_independent_forecasts_10_cold_and_six_states42_native42_cold','actual_medium153_six_states_native42_full73_training_and219_prefixes_before_quality')
    s=s.replace("'actual153_complete_six_state_native_and_full_training_controls_not_yet_claimed':True", "'actual153_complete_six_state_native_and_full_training_controls_passed':True,'actual153_full_training_cases':73,'actual153_full_training_cold_cases':219")
    s=s.replace('同步153全训练期5635800独立预测及六状态42原生42冷验证','同步153完整训练73组合及219前缀验证，正式质量准入待完成')
    compile(s,str(new),'exec')
    with new.open('x',encoding='utf8') as f:f.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('medium153_fulltraining_main_publication_v63_20261009',new.name,[],{str(new):sha(new),str(Path(__file__)):sha(__file__)})
    create(A/'medium153_fulltraining_main_hidden_launch_v63_20261009.json',row);print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
