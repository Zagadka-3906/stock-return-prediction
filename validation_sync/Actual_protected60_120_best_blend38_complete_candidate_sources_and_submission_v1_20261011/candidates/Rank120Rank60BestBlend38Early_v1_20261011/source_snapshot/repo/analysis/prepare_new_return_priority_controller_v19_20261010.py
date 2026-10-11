"""Preserve live Top training and replace repetitive dispatch with a new return objective."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    src=(A/'run_continuous_fast_reused_frontiers_v18_20261010.py').read_text(encoding='utf8')
    src=src.replace("OUT=A/'continuous_fast_reused_frontiers_v18_20261010'","OUT=A/'continuous_fast_reused_frontiers_v19_20261010'")
    pos=src.index('\ndef main():')
    src=src[:pos]+'''
_original_allowed=prior.allowed
def allowed_both():
    control=read(A/'current_user_runtime_control_20261009.json')
    return control['status']=='optimization_active_after_explicit_manual_resume' and _original_allowed()
prior.allowed=allowed_both
''' +src[pos:]
    needle='        row=start_service(name,driver,[],pins);create(OUT/(name+\'_launch.json\'),row)'
    assert src.count(needle)==1
    src=src.replace(needle,"        folder=A/'service_owned_workflows_20261006'/name\n        if folder.exists():\n            row=read(folder/'native_launch.json');assert owned(row) or read(folder/'service_execution.json')['status']=='passed'\n        else:row=start_service(name,driver,[],pins)\n        create(OUT/(name+'_launch.json'),row)")
    src=src.replace('range(165,1001)','range(165,166)')
    end=src.index("if __name__=='__main__':main()")
    src=src[:end]+'''
    screen='actual_TopWeighted_after163_high_impact65_screen_v1_20261010'
    write(OUT/'state.json',{'status':'waiting_stronger_parent65_before_next_new_training','round':165,'actual_service':screen,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    if not prior.closed(screen):return
    result=read(Path(read(A/'actual_TopWeighted_after163_high_impact65_screen_location_v1_20261010.json')['output'])/'verification.json')
    current=read(A/'latest_verified_submission_delivery_v2_20261008.json')
    if result['best']['connected_final_score']>current['official_score']:
        write(OUT/'state.json',{'status':'priority_winning65_requires_complete_parent_native_qualification','best':result['best'],'current_qualified_score':current['official_score'],'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
        return
    proof=A/'ReturnHuber050_own_bank_controls_source_admission_v1_20261010.json'
    for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_BF16_medium2048_returnhuber050_seed09_restart_control_v1_20261009','verify_neural_BF16_medium2048_returnhuber050_seed09_restart_v1_20261009.py'),('BF16ReturnHuber050166_independent_small_CPU_v1_20261009','verify_BF16ReturnHuber050166_independent_small_CPU_v1_20261009.py'),('actual_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009','train_neural_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009.py'),('BF16ReturnHuber050166_independent_full5_GPU_controls_v1_20261009','verify_BF16ReturnHuber050166_full5_independent_GPU_v1_20261009.py'),('BF16ReturnHuber050166_actual_native42_calendar_v1_20261009','verify_BF16ReturnHuber050166_native42_calendar_v1_20261009.py')]
    for name,driver in tasks:
        if not prior.allowed():return
        p=A/driver
        pins={str(q):sha(q) for q in (p,proof,A/'neural_BF16_medium2048_returnhuber050_seed09_e64_native_v1_20261009.py')}
        folder=A/'service_owned_workflows_20261006'/name
        assert not folder.exists(),('exclusive_output_existing_requires_own_recovery',name)
        row=start_service(name,driver,[],pins);create(OUT/(name+'_launch.json'),row)
        write(OUT/'state.json',{'status':'actual_direct_return_own_training_or_controls_running','round':166,'recipe':'returnhuber050','actual_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'new_quality_scores':0})
        if not prior.closed(name):return
    from build_reused_return_neural_frontier_v11_20261010 import build
    value=build(166,'returnhuber050','nonflag_valid',10)
    create(A/'ReusedNN166_prepared_frontier_v1_20261010.json',value)
    name=prior.launch_frontier(value)
    write(OUT/'state.json',{'status':'actual_new_return166_full_qualification_running','round':166,'full_service':name,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    if not prior.closed(name):return
    create(OUT/'round166_fully_qualified.json',{'status':'passed_full_quality_freeze_inference_causal_QA_and_main','receipt':read(A/'github_validation_sync_main_20261005/round166_receipt.json')})
    write(OUT/'state.json',{'status':'new_return166_complete_next_direction_requires_evidence_review','round':166,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
if __name__=='__main__':main()
'''
    target=A/'run_continuous_fast_reused_frontiers_v19_20261010.py';assert not target.exists();compile(src,str(target),'exec');target.write_text(src,encoding='utf8',newline='\n')
    create(A/'new_return_priority_controller_v19_source_admission_20261010.json',{'status':'compiled_only_not_executed','source_sha256':sha(target),'live_Top_training_reused_without_restart':True,'winning65_prioritized_before_return_training':True,'no_new_scores':True})
    print(target)
if __name__=='__main__':main()
