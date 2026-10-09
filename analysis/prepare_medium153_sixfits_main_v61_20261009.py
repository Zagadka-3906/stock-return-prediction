"""Upload complete six annual model metadata and new parent ABI; no quality qualification claim."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    old=A/'publish_medium153_controls_main_v60_20261009.py';new=A/'publish_medium153_sixfits_main_v61_20261009.py'
    s=old.read_text(encoding='utf8').replace('medium153_controls_main_v60','medium153_sixfits_main_v61').replace('medium153_controls_v60','medium153_sixfits_v61').replace('medium153_controls_safe_publication_v60','medium153_sixfits_safe_publication_v61')
    needle=" if (bank/'protocol.json').exists():sources.append(bank/'protocol.json')";assert s.count(needle)==1
    extra=""" closed('actual_BF16_medium2048_seed09_e64_bank6_v1_20261009')
 assert read(bank/'verification.json')['actual_native_fits']==6
 assert len(read(bank/'verification.json')['actual_models'])==6
 sources.append(bank/'verification.json')
 for f,d in read(bank/'verification.json')['input_sha256'].items():
  assert sha(f)==d,f
  if Path(f).suffix in ('.py','.json','.md'):sources.append(Path(f))
 sources.extend(A/n for n in ('prepare_medium153_controls_main_v60_20261009.py','medium153_controls_main_v60_receipt_20261009.json',
  'BF16Medium153_complete_native_predictor_preparation_v1_20261009.json','BF16Medium153_core_draft_preparation_v1_20261009.json'))
 sources.extend(p for p in A.glob('*BF16Medium*20261009.py') if p.is_file())
 sources.extend(p for p in A.glob('*BF16Medium*20261009.json') if p.is_file())
"""
    s=s.replace(needle,extra+needle)
    s=s.replace('actual_medium153_synthetic73_prefix219_CPU10017_four_prefixes_and_annual_partial_records','actual_medium153_six_mature_annual_fits_and_native_reload_cold80_plus_synthetic_and_parent_ABI')
    s=s.replace("'actual153_synthetic_cases':73", "'actual_new_medium_annual_fits_completed':6,'actual_medium153_parent_ABI_routes':5,'actual153_core_drafts_admitted':False,'actual153_synthetic_cases':73")
    s=s.replace('同步153的73组合219前缀及独立CPU控制，真实六状态验证已排队','同步新神经网络六个成熟年度模型及153原方案接口检查，完整训练验证继续')
    compile(s,str(new),'exec')
    with new.open('x',encoding='utf8') as f:f.write(s)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('medium153_sixfits_main_publication_v61_20261009',new.name,[],{str(new):sha(new),str(Path(__file__)):sha(__file__)})
    create(A/'medium153_sixfits_main_hidden_launch_v61_20261009.json',row);print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()
