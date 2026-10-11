"""Freeze a new residual-sign axis and prepare real controls without fitting new models."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def fresh(name,text):
    path=A/name;assert not path.exists(),path
    compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
    return path

def main():
    helper=fresh('nonflag_reverse_RFF_CDF_transform_20261007.py','''"""Reverse only the predeclared residual; retain the original exact CDF recipe."""
import numpy as np
from nonflag_residual_HGB_CDF_transform_20261007 import prepare,apply_prepared as original_apply
def apply_prepared(parent,reference,flags,residual,weight,prepared):
    return original_apply(parent,reference,flags,-np.asarray(residual),weight,prepared)
def transform(parent,reference,dates,flags,valid,residual,weight,universe):
    return apply_prepared(parent,reference,flags,residual,weight,prepare(reference,dates,flags,valid,universe))
''')
    originals=[];generated=[helper]
    cases=[('nonflag_residual_RFFRidge_native_stage_20261007.py','nonflag_reverse_RFF_native_stage_20261007.py'),
        ('run_nonflag_residual_RFFRidge_hook3_after_bank_20261007.py','run_nonflag_reverse_RFF_hook3_after_bank_20261007.py'),
        ('verify_nonflag_residual_RFFRidge37_transform_20261007.py','verify_nonflag_reverse_RFF37_transform_20261007.py'),
        ('run_nonflag_RFFRidge_actual_controls_20261007.py','run_nonflag_reverse_RFF_actual_controls_20261007.py')]
    replacements={
        'nonflag_residual_HGB_CDF_transform_20261007':'nonflag_reverse_RFF_CDF_transform_20261007',
        'nonflag_residual_RFFRidge_native_stage_20261007':'nonflag_reverse_RFF_native_stage_20261007',
        'run_nonflag_residual_RFFRidge_hook3_after_bank_20261007':'run_nonflag_reverse_RFF_hook3_after_bank_20261007',
        'verify_nonflag_residual_RFFRidge37_transform_20261007':'verify_nonflag_reverse_RFF37_transform_20261007',
        'nonflag_residual_RFFRidge_native_hook3_preflight_20261007':'nonflag_reverse_RFF_native_hook3_preflight_20261007',
        'nonflag_residual_RFFRidge37_transform_preflight_20261007':'nonflag_reverse_RFF37_transform_preflight_20261007',
        'nonflag_RFFRidge_actual_native_and_transform_controls_20261007':'nonflag_reverse_RFF_actual_native_and_transform_controls_20261007',
        'nonflag_RFFRidge40_plan_20261007':'nonflag_reverse_RFF40_plan_20261007',
        'round122':'round123','QA33':'QA34',
        'passed_actual37_full5635800_nonflag_residual_RFFRidge':'passed_actual37_full5635800_nonflag_reverse_RFF',
        'passed_actual3_historical603_nonflag_RFFRidge':'passed_actual3_historical603_nonflag_reverse_RFF'}
    for before,after in cases:
        original=A/before;originals.append(original);text=original.read_text(encoding='utf8')
        for old,new in replacements.items():text=text.replace(old,new)
        if before.startswith('nonflag_residual'):
            text=text.replace("    assert spec['weight']>0.","    assert spec['residual_sign']==-1\n    assert spec['weight']>0.")
            needle="independent_pct[pos]+spec['weight']*decoded_sum[pos]";assert text.count(needle)==1
            text=text.replace(needle,"independent_pct[pos]-spec['weight']*decoded_sum[pos]")
            text=text.replace("return values,{'rows':", "return values,{'residual_sign':-1,'rows':")
        if before.startswith('run_nonflag_residual'):
            text=text.replace("spec={'weight':.01", "spec={'residual_sign':-1,'weight':.01")
        if before.startswith('verify_'):
            needle='pct+w*head[n][positions]';assert text.count(needle)==1
            text=text.replace(needle,'pct-w*head[n][positions]')
        generated.append(fresh(after,text))
    plan=read(A/'nonflag_RFFRidge40_plan_20261007.json')
    plan.update(status='frozen_reverse_RFF40_before_actual_controls_and_official_scores',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=123,wave=406,after_round=122,
        qualified_anchor_rounds=[112,121,122],residual_sign=-1,
        selection='highest_full_connected_official_score_after_actual123_source_admission',
        new_native_fits_by_comparison=0,
        full_future_candidate_native_replays_and_QA34_required=True,
        input_sha256={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_RFFRidge40_plan_20261007.json']})
    plan.pop('full_future_candidate_native_replays_and_QA33_required',None)
    create(A/'nonflag_reverse_RFF40_plan_20261007.json',plan)
    pins={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_reverse_RFF40_plan_20261007.json']}
    create(A/'nonflag_reverse_RFF40_controls_source_preparation_20261007.json',
        {'status':'compiled_fresh_reverse_RFF_native3_and_full37_controls_before_execution',
         'input_sha256':pins,'new_native_fits':0,'actual_official_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_reverse_RFF_actual_hook3_and_full37_controls','run_nonflag_reverse_RFF_actual_controls_20261007.py',[],pins)
    create(A/'nonflag_reverse_RFF_actual_controls_hidden_launch_20261007.json',row)
    print({'status':'started_reverse_controls','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
