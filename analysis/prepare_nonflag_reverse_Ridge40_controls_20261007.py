"""Prepare the next independent sign axis using the already fitted Ridge bank."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    replacements={
      'nonflag_residual_HGB_CDF_transform_20261007':'nonflag_reverse_RFF_CDF_transform_20261007',
      'nonflag_residual_Ridge_native_stage_20261007':'nonflag_reverse_Ridge_native_stage_20261007',
      'run_nonflag_residual_Ridge_hook3_after_bank_20261007':'run_nonflag_reverse_Ridge_hook3_after_bank_20261007',
      'verify_nonflag_residual_Ridge37_transform_20261007':'verify_nonflag_reverse_Ridge37_transform_20261007',
      'nonflag_residual_Ridge_native_hook3_preflight_20261007':'nonflag_reverse_Ridge_native_hook3_preflight_20261007',
      'nonflag_residual_Ridge37_transform_preflight_20261007':'nonflag_reverse_Ridge37_transform_preflight_20261007',
      'nonflag_Ridge40_plan_20261007':'nonflag_reverse_Ridge40_plan_20261007',
      'passed_actual37_full5635800_nonflag_residual_Ridge':'passed_actual37_full5635800_nonflag_reverse_Ridge',
      'passed_actual3_historical603_nonflag_Ridge':'passed_actual3_historical603_nonflag_reverse_Ridge',
      'round121':'round124','QA32':'QA35'}
    pairs=[('nonflag_residual_Ridge_native_stage_20261007.py','nonflag_reverse_Ridge_native_stage_20261007.py'),
      ('run_nonflag_residual_Ridge_hook3_after_bank_20261007.py','run_nonflag_reverse_Ridge_hook3_after_bank_20261007.py'),
      ('verify_nonflag_residual_Ridge37_transform_20261007.py','verify_nonflag_reverse_Ridge37_transform_20261007.py')]
    generated=[];originals=[]
    for before,after in pairs:
        old=A/before;originals.append(old);new=A/after;assert not new.exists()
        text=substitute(old.read_text(encoding='utf8'),replacements)
        if before.startswith('nonflag_residual'):
            text=text.replace("    assert spec['weight']>0.","    assert spec['residual_sign']==-1\n    assert spec['weight']>0.")
            needle="independent_pct[pos]+spec['weight']*decoded_sum[pos]";assert text.count(needle)==1
            text=text.replace(needle,"independent_pct[pos]-spec['weight']*decoded_sum[pos]")
            text=text.replace("return values,{'rows':", "return values,{'residual_sign':-1,'rows':")
        else:
            needle='pins={';assert text.count(needle)==1
            text=text.replace(needle,"paths.append(A/'nonflag_residual_HGB_CDF_transform_20261007.py')\n    "+needle)
        if before.startswith('run_'):
            text=text.replace("spec={'weight':.01", "spec={'residual_sign':-1,'weight':.01")
        if before.startswith('verify_'):
            needle='pct+w*head[n][positions]';assert text.count(needle)==1
            text=text.replace(needle,'pct-w*head[n][positions]')
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');generated.append(new)
    controller=A/'run_nonflag_reverse_Ridge_actual_controls_20261007.py';assert not controller.exists()
    text=(A/'run_nonflag_reverse_RFF_actual_controls_20261007.py').read_text(encoding='utf8').replace('nonflag_reverse_RFF','nonflag_reverse_Ridge').replace('round123','round124')
    compile(text,str(controller),'exec');controller.write_text(text,encoding='utf8',newline='\n');generated.append(controller)
    plan=read(A/'nonflag_Ridge40_plan_20261007.json')
    plan.update(status='frozen_reverse_Ridge40_before_actual_controls_and_official_scores',
      at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=124,wave=407,after_round=123,
      qualified_anchor_rounds=[112,121,123],residual_sign=-1,
      selection='highest_full_connected_official_score_after_actual124_source_admission',
      new_native_fits_by_comparison=0,full_future_candidate_native_replays_and_QA35_required=True,
      input_sha256={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_Ridge40_plan_20261007.json']})
    plan.pop('full_future_candidate_native_replays_and_QA32_required',None)
    create(A/'nonflag_reverse_Ridge40_plan_20261007.json',plan)
    pins={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_reverse_Ridge40_plan_20261007.json',
      A/'nonflag_reverse_RFF_CDF_transform_20261007.py',A/'nonflag_residual_HGB_CDF_transform_20261007.py']}
    create(A/'nonflag_reverse_Ridge40_controls_source_preparation_20261007.json',
      {'status':'compiled_fresh_reverse_Ridge_native3_full37_controls_before_execution',
       'input_sha256':pins,'new_native_fits':0,'actual_official_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_reverse_Ridge_actual_hook3_and_full37_controls','run_nonflag_reverse_Ridge_actual_controls_20261007.py',[],pins)
    create(A/'nonflag_reverse_Ridge_actual_controls_hidden_launch_20261007.json',row)
    print({'status':'started_reverse_Ridge_controls','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
