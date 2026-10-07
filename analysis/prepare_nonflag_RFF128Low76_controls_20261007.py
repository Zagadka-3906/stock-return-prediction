"""Prepare both signs for the weaker-L2 bank, reusing the validated generic128 native stage."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    mapping={
      'nonflag_residual_RFF128_native_stage_20261007':'nonflag_residual_RFF128_native_stage_20261007',
      'nonflag_residual_RFF128_codec_20261007':'nonflag_residual_RFF128_codec_20261007',
      'nonflag_CPU_RFF128_residual_CDF':'nonflag_CPU_RFF128_residual_CDF',
      'nonflag_residual_RFF128':'nonflag_residual_RFF128Low',
      'nonflag_RFF12876':'nonflag_RFF128Low76',
      'nonflag_RFF128_actual':'nonflag_RFF128Low_actual',
      'passed_actual6_historical603_nonflag_RFF128':'passed_actual6_historical603_nonflag_RFF128Low',
      'remove_nonflag_RFF128':'remove_nonflag_RFF128Low',
      'round125':'round126','QA36':'QA37'}
    pairs=[('run_nonflag_residual_RFF128_hook6_after_bank_20261007.py','run_nonflag_residual_RFF128Low_hook6_after_bank_20261007.py'),
      ('verify_nonflag_residual_RFF12873_transform_20261007.py','verify_nonflag_residual_RFF128Low73_transform_20261007.py'),
      ('run_nonflag_RFF128_actual_controls_20261007.py','run_nonflag_RFF128Low_actual_controls_20261007.py')]
    generated=[];originals=[]
    for before,after in pairs:
        old=A/before;originals.append(old);new=A/after;assert not new.exists()
        text=substitute(old.read_text(encoding='utf8'),mapping)
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');generated.append(new)
    plan=read(A/'nonflag_RFF12876_plan_20261007.json')
    heads=list(read(A/'nonflag_residual_RFF128Low10_plan_20261007.json')['configurations'])
    plan.update(status='frozen_RFF128Low76_both_signs_before_actual_controls_and_official_scores',
      at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=126,wave=409,after_round=125,
      qualified_anchor_rounds=[112,121,125],single_native_heads=heads,
      ensembles={'nonflag_residual_rff128low_equal_mean_two':heads},
      existing_native_bank='nonflag_residual_RFF128Low_bank10_20261007',
      selection='highest_full_connected_official_score_after_actual126_source_admission',
      full_future_candidate_native_replays_and_QA37_required=True,
      input_sha256={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_residual_RFF128Low10_plan_20261007.json']})
    plan.pop('full_future_candidate_native_replays_and_QA36_required',None)
    create(A/'nonflag_RFF128Low76_plan_20261007.json',plan)
    pins={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_RFF128Low76_plan_20261007.json',
      A/'nonflag_residual_RFF128_native_stage_20261007.py',A/'nonflag_residual_RFF128_codec_20261007.py']}
    create(A/'nonflag_RFF128Low76_controls_source_preparation_20261007.json',
      {'status':'compiled_weaker_L2_native6_full73_cold219_before_execution','input_sha256':pins,'actual_official_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_RFF128Low_actual_hook6_and_full73_controls','run_nonflag_RFF128Low_actual_controls_20261007.py',[],pins)
    create(A/'nonflag_RFF128Low_actual_controls_hidden_launch_20261007.json',row)
    print({'status':'started_actual_Low_controls_after_bank','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
