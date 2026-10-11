"""Upload the actual all5 full independent forecasts and six-state native42/cold42 evidence."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'publish_medium153_sixfits_main_v61_20261009.py';new=A/'publish_medium153_native_main_v62_20261009.py'
    s=old.read_text(encoding='utf8').replace('medium153_sixfits_main_v61','medium153_native_main_v62').replace('medium153_sixfits_v61','medium153_native_v62').replace('medium153_sixfits_safe_publication_v61','medium153_native_safe_publication_v62')
    needle=" if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')";assert s.count(needle)==1
    addition=""" for n in ('BF16Medium153_independent_full5_GPU_controls_v1_20261009','BF16Medium153_actual_native42_calendar_v1_20261009'):closed(n)
 for pointer in ('actual_BF16Medium153_full5_independent_location_v1_20261009.json','actual_BF16Medium153_native42_calendar_location_v1_20261009.json'):
  p=A/pointer;out=Path(read(p)['output']);v=out/'verification.json';assert sha(v)==read(p)['verification_sha256']
  sources.extend([p,*out.glob('*.json')])
  proof=read(v)
  if 'actual_saved_states' in proof:
   assert (proof['actual_saved_states'],proof['actual_historical_cases'],proof['actual_calendar_cases'],proof['actual_cold_cases'])==(6,30,12,42)
   assert len(proof['records'])==42 and len(proof['prefit_rejections'])==7
  else:
   assert proof['rows_days_stocks']==[5635800,1212,4650] and len(proof['records'])==5
   assert all(r['full_original_native_reload_and_independent_bits_exact'] and len(r['cold_controls'])==2 for r in proof['records'])
  for f,d in proof['input_sha256'].items():
   assert sha(f)==d,f
   if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 sources.extend(A/n for n in ('prepare_medium153_sixfits_main_v61_20261009.py','medium153_sixfits_main_v61_receipt_20261009.json',
  'prepare_medium153_native_main_v62_20261009.py'))
"""
    s=s.replace(needle,addition+needle)
    s=s.replace('actual_medium153_six_mature_annual_fits_and_native_reload_cold80_plus_synthetic_and_parent_ABI','actual_medium153_5635800_full5_independent_forecasts_10_cold_and_six_states42_native42_cold')
    s=s.replace("'actual_new_medium_annual_fits_completed':6", "'actual_medium153_full5_independent_rows':5635800,'actual_medium153_full5_independent_cold_controls':10,'actual_medium153_saved_states':6,'actual_medium153_native_cases':42,'actual_medium153_native_cold_cases':42,'actual_medium153_prefit_calendar_rejections':7,'actual_new_medium_annual_fits_completed':6")
    s=s.replace('同步新神经网络六个成熟年度模型及153原方案接口检查，完整训练验证继续','同步153全训练期5635800独立预测及六状态42原生42冷验证')
    compile(s,str(new),'exec')
    with new.open('x',encoding='utf8') as f:f.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('medium153_native_main_publication_v62_20261009',new.name,[],{str(new):sha(new),str(Path(__file__)):sha(__file__)})
    create(A/'medium153_native_main_hidden_launch_v62_20261009.json',row);print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
