"""Freeze both residual signs and prepare actual native6/full73/cold219 controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    pairs=[('nonflag_residual_RFFRidge_native_stage_20261007.py','nonflag_residual_RFF128_native_stage_20261007.py'),
      ('run_nonflag_residual_RFFRidge_hook3_after_bank_20261007.py','run_nonflag_residual_RFF128_hook6_after_bank_20261007.py'),
      ('verify_nonflag_residual_RFFRidge37_transform_20261007.py','verify_nonflag_residual_RFF12873_transform_20261007.py')]
    mapping={
      'nonflag_residual_RFFRidge_native_bank10_v2':'nonflag_residual_RFF128_native_bank10',
      'nonflag_residual_RFFRidge_native_hook3_preflight':'nonflag_residual_RFF128_native_hook6_preflight',
      'nonflag_residual_RFFRidge37_transform_preflight':'nonflag_residual_RFF12873_transform_preflight',
      'nonflag_RFFRidge40_plan':'nonflag_RFF12876_plan',
      'nonflag_residual_RFFRidge':'nonflag_residual_RFF128','nonflag_CPU_RFFRidge':'nonflag_CPU_RFF128',
      'nonflag_cpu_rffridge_':'nonflag_cpu_rff128_',
      'passed_actual3_historical603_nonflag_RFFRidge':'passed_actual6_historical603_nonflag_RFF128',
      'remove_nonflag_RFFRidge':'remove_nonflag_RFF128',
      'round122':'round125','QA33':'QA36'}
    generated=[];originals=[]
    for before,after in pairs:
        old=A/before;originals.append(old);new=A/after;assert not new.exists()
        text=substitute(old.read_text(encoding='utf8'),mapping)
        if before.startswith('nonflag_residual'):
            text=text.replace("    assert spec['weight']>0.","    assert spec['residual_sign'] in (-1,1)\n    assert spec['weight']>0.")
            needle="            assert linear.solver=='cholesky' and linear.alpha==info['parameters']['alpha']";assert text.count(needle)==1
            text=text.replace(needle,needle+"\n            assert linear.copy_X is False and projection.n_components==128")
            text=text.replace("context.flags,native_sum,spec['weight'],prepared)","context.flags,native_sum*spec['residual_sign'],spec['weight'],prepared)")
            text=text.replace("spec['weight']*decoded_sum[pos]","spec['weight']*(decoded_sum[pos]*spec['residual_sign'])")
            text=text.replace("return values,{'rows':","return values,{'residual_sign':spec['residual_sign'],'rows':")
        if before.startswith('run_'):
            needle="        for name,names in [(n,[n]) for n in head]+[('equal_mean_two',head)]:";assert text.count(needle)==1
            text=text.replace(needle,"        for name,names,sign in [(n,c,s) for n,c in [(n,[n]) for n in head]+[('equal_mean_two',head)] for s in (-1,1)]:")
            text=text.replace("spec={'weight':.01","spec={'residual_sign':sign,'weight':.01")
            text=text.replace("records.append({'head':name,","records.append({'head':name,'residual_sign':sign,")
            text=text.replace("'native_component_counts':[1,1,2]","'native_component_counts':[1,1,1,1,2,2]")
            text=text.replace("'native_hook_cases':3","'native_hook_cases':6")
        if before.startswith('verify_'):
            text=text.replace('37','73').replace('111','219')
            text=text.replace("cases=[(n,w) for n in [*plan['single_native_heads'],'equal_mean_two'] for w in plan['weights']]+[('remove_nonflag_RFF128',0.)]",
              "cases=[(n,w,s) for n in [*plan['single_native_heads'],'equal_mean_two'] for s in (-1,1) for w in plan['weights']]+[('remove_nonflag_RFF128',0.,1)]")
            text=text.replace('for n,w in cases:','for n,w,sign in cases:')
            text=text.replace("flags,head[n],w,prepared)","flags,head[n]*sign,w,prepared)")
            text=text.replace('pct+w*head[n][positions]','pct+w*(head[n][positions]*sign)')
            text=text.replace("valid[:size],head[n][:size],w,","valid[:size],head[n][:size]*sign,w,")
            text=text.replace("controls.append({'head':n,'weight':w,","controls.append({'head':n,'weight':w,'residual_sign':sign,")
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');generated.append(new)
    compatible=A/'nonflag_residual_RFF128_compatible_parent_20261007.py';assert not compatible.exists()
    compatible.write_text("from copy import deepcopy\nfrom nonflag_residual_RFFRidge_compatible_parent_20261007 import core as original_core\ndef core(graph):\n    value=deepcopy(graph);value.pop('nonflag_CPU_RFF128_residual_CDF',None);return original_core(value)\ndef compatible(graph,reference_graph):return core(graph)==core(reference_graph)\n",encoding='utf8',newline='\n')
    generated.append(compatible)
    plan=read(A/'nonflag_RFFRidge40_plan_20261007.json')
    heads=list(read(A/'nonflag_residual_RFF12810_plan_20261007.json')['configurations'])
    plan.update(status='frozen_RFF12876_both_signs_before_actual_controls_and_official_scores',
      at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=125,wave=408,after_round=124,
      qualified_anchor_rounds=[112,121,124],single_native_heads=heads,
      ensembles={'nonflag_residual_rff128_equal_mean_two':heads},residual_signs=[-1,1],
      existing_native_bank='nonflag_residual_RFF128_bank10_20261007',new_branch='nonflag_CPU_RFF128_residual_CDF',
      expected_scored_records=76,expected_full_transform_controls=73,expected_cold_prefix_controls=219,
      selection='highest_full_connected_official_score_after_actual125_source_admission',
      full_future_candidate_native_replays_and_QA36_required=True,
      input_sha256={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_residual_RFF12810_plan_20261007.json']})
    plan.pop('full_future_candidate_native_replays_and_QA33_required',None)
    create(A/'nonflag_RFF12876_plan_20261007.json',plan)
    controller=A/'run_nonflag_RFF128_actual_controls_20261007.py';assert not controller.exists()
    text=(A/'run_nonflag_RFFRidge_actual_controls_20261007.py').read_text(encoding='utf8')
    mapping.update({'run_nonflag_residual_RFFRidge_hook3_after_bank':'run_nonflag_residual_RFF128_hook6_after_bank',
      'verify_nonflag_residual_RFFRidge37_transform':'verify_nonflag_residual_RFF12873_transform',
      'nonflag_RFFRidge_actual_native_and_transform_controls':'nonflag_RFF128_actual_native_and_transform_controls'})
    text=substitute(text,mapping).replace("['records'])==3","['records'])==6").replace("['actual_full_cases']==37","['actual_full_cases']==73").replace("['actual_cold_cases']==111","['actual_cold_cases']==219")
    text=text.replace('passed_actual3_native_hooks37_full_CDF_and111_cold_controls','passed_actual6_native_hooks73_full_CDF_and219_cold_controls')
    text=text.replace("'actual_native_hooks':3,'actual_full_cases':37,'actual_cold_cases':111","'actual_native_hooks':6,'actual_full_cases':73,'actual_cold_cases':219")
    compile(text,str(controller),'exec');controller.write_text(text,encoding='utf8',newline='\n');generated.append(controller)
    pins={str(p):sha(p) for p in [Path(__file__),*originals,*generated,A/'nonflag_RFF12876_plan_20261007.json']}
    create(A/'nonflag_RFF12876_controls_source_preparation_20261007.json',{'status':'compiled_native6_full73_cold219_before_execution',
      'input_sha256':pins,'actual_official_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('nonflag_RFF128_actual_hook6_and_full73_controls','run_nonflag_RFF128_actual_controls_20261007.py',[],pins)
    create(A/'nonflag_RFF128_actual_controls_hidden_launch_20261007.json',row)
    print({'status':'started_actual6_73_219_controls_after_bank','worker':row['owned_worker_pid']},flush=True)
if __name__=='__main__':main()
