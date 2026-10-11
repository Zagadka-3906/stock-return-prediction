"""Prepare127 native6 and full73/cold219 controls; no official selection before completed126."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    mapping={'nonflag_residual_RFF128_native_stage_20261007':'nonflag_residual_RFF128_native_stage_20261007',
        'nonflag_residual_RFF128_codec_20261007':'nonflag_residual_RFF128_codec_20261007',
        'nonflag_CPU_RFF128_residual_CDF':'nonflag_CPU_RFF128_residual_CDF',
        'nonflag_residual_RFF128':'nonflag_residual_RFF128Hi','nonflag_RFF12876':'nonflag_RFF128Hi76',
        'nonflag_RFF128_actual':'nonflag_RFF128Hi_actual','passed_actual6_historical603_nonflag_RFF128':'passed_actual6_historical603_nonflag_RFF128Hi',
        'remove_nonflag_RFF128':'remove_nonflag_RFF128Hi','round125':'round127','QA36':'QA38'}
    pairs=[('run_nonflag_residual_RFF128_hook6_after_bank_20261007.py','run_nonflag_residual_RFF128Hi_hook6_after_bank_20261007.py'),
        ('verify_nonflag_residual_RFF12873_transform_20261007.py','verify_nonflag_residual_RFF128Hi73_transform_20261007.py'),
        ('run_nonflag_RFF128_actual_controls_20261007.py','run_nonflag_RFF128Hi_actual_controls_20261007.py')]
    paths=[Path(__file__)]
    for before,after in pairs:
        old=A/before;new=A/after;assert not new.exists()
        text=substitute(old.read_text(encoding='utf8'),mapping)
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');paths.extend((old,new))
    plan=read(A/'nonflag_RFF12876_plan_20261007.json');heads=list(read(A/'nonflag_residual_RFF128Hi10_plan_20261007.json')['configurations'])
    plan.update(status='frozen_RFF128Hi76_both_signs_before_actual_controls_and_official_scores',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=127,wave=410,after_round=126,qualified_anchor_rounds=[112,121,126],
        single_native_heads=heads,ensembles={'nonflag_residual_rff128hi_equal_mean_two':heads},
        existing_native_bank='nonflag_residual_RFF128Hi_bank10_20261007',
        selection='highest_full_connected_official_score_only_after_real126_closure_and_actual127_source_admission',
        full_future_candidate_native_replays_and_QA38_required=True)
    plan.pop('full_future_candidate_native_replays_and_QA36_required',None)
    planpath=A/'nonflag_RFF128Hi76_plan_20261007.json';create(planpath,plan);paths.append(planpath)
    paths.extend((A/'nonflag_residual_RFF128Hi10_plan_20261007.json',A/'nonflag_residual_RFF128_native_stage_20261007.py',A/'nonflag_residual_RFF128_codec_20261007.py'))
    pins={str(p):sha(p) for p in paths}
    create(A/'nonflag_RFF128Hi76_controls_source_preparation_20261007.json',
        {'status':'compiled_stronger_L2_native6_full73_cold219_controls','input_sha256':pins,'new_quality_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_RFF128Hi_actual_hook6_and_full73_controls','run_nonflag_RFF128Hi_actual_controls_20261007.py',[],pins)
    create(A/'nonflag_RFF128Hi_actual_controls_hidden_launch_20261007.json',row)
if __name__=='__main__':main()
