"""Freeze finer signed145 codec and actual historical native/full controls; no quality/inference claims."""
from pathlib import Path
import sys,ast,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(p,s):
    assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n')
def main():
    proposal=A/'CrossFamilyFine125_round145_proposal_v1_20261008.json';plan=read(proposal);assert len(plan['new_cases'])==120
    old=A/'CrossFamily_complete_parent_CDF_v1_20261008.py';s=old.read_text(encoding='utf8')
    s=s.replace("group in range(len(GROUPS)) and share in (.25, .5, .75)","group == 4 and share in (.25, .375, .5, .625, .75)")
    s=s.replace('0. <= amplitude <= .1','-.00325 <= amplitude <= .00325')
    codec=A/'CrossFamilyFine_complete_parent_CDF_v1_20261008.py';save(codec,s)
    # Only admission bounds change. All numerical function bodies match the original AST after replacing those assertions.
    def mathematical_ast(value):
        t=ast.parse(value)
        for node in ast.walk(t):
            if isinstance(node,ast.FunctionDef) and node.name in ('mixture','apply_prepared'):node.body=[x for x in node.body if not isinstance(x,ast.Assert)]
        return ast.dump(t,include_attributes=False)
    assert mathematical_ast(old.read_text(encoding='utf8'))==mathematical_ast(s)
    original_native=A/'CrossFamily_complete_parent_native_stage_v2_20261008.py';s=original_native.read_text(encoding='utf8')
    s=s.replace('from CrossFamily_complete_parent_CDF_v1_20261008 import','from CrossFamilyFine_complete_parent_CDF_v1_20261008 import')
    s=s.replace("spec['amplitude']>0. and spec['amplitude']<=.1 and spec['share'] in (.25,.5,.75)","0. < abs(spec['amplitude']) <= .00325 and spec['share'] in (.25,.375,.5,.625,.75) and spec['group']==4")
    native=A/'CrossFamilyFine_complete_parent_native_stage_v1_20261008.py';save(native,s)
    source=A/'verify_CrossFamily15_native_historical_hooks_v2_20261008.py';s=source.read_text(encoding='utf8')
    s=s.replace('import os,sys,time','import os,sys,time,itertools').replace('CrossFamily15_native_historical_hooks_v2_20261008','CrossFamilyFine30_native_historical_hooks_v1_20261008')
    s=s.replace('CrossFamily_complete_parent_CDF_v1_20261008','CrossFamilyFine_complete_parent_CDF_v1_20261008').replace('CrossFamily_complete_parent_native_stage_v2_20261008','CrossFamilyFine_complete_parent_native_stage_v1_20261008')
    s=s.replace('CrossFamily94_round136_plan_v1_20261008.json',proposal.name)
    s=s.replace("for year,share,amplitude in zip((2021,2022,2024),(.25,.5,.75),(.005,.025,.1)):","for year in (2021,2022,2024):")
    s=s.replace('for group in range(5):',"for share,amplitude in itertools.product((.25,.375,.5,.625,.75),(-.001,.001)):\n            group=4")
    s=s.replace('actual_CrossFamily15_native_hooks_location_v2_20261008','actual_CrossFamilyFine30_native_hooks_location_v1_20261008')
    s=s.replace("'actual_hooks':15,'actual_cold_hooks':15","'actual_hooks':30,'actual_cold_hooks':30").replace('passed_actual15_historical_native_crossfamily_hooks_and15_cold_prefixes','passed_actual30_historical_native_crossfamily_fine_hooks_and30_cold_prefixes')
    s=s.replace("'groups':5","'groups':1,'shares':5,'signed_amplitudes':2")
    s=s.replace("    for path,digest in pins.items():assert sha(path)==digest,path","    assert len(records)==30\n    for path,digest in pins.items():assert sha(path)==digest,path")
    hooks=A/'verify_CrossFamilyFine30_native_historical_hooks_v1_20261008.py';save(hooks,s)
    outputs=[codec,native,hooks];pins={str(p):sha(p) for p in [Path(__file__),proposal,old,original_native,source,*outputs]}
    create(A/'CrossFamilyFine145_math_control_source_preparation_v1_20261008.json',{'status':'frozen_fine_signed_codec_and_native_hooks_before_actual_execution',
        'input_sha256':pins,'numerical_AST_preserved_after_assertion_only_bound_extensions':True,'actual_hook_cases':30,'actual_cold_hooks':30,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False,'complete145_quality_receivers_still_required':True})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('CrossFamilyFine30_actual_native_historical_controls_v1_20261008',hooks.name,[],pins)
    create(A/'CrossFamilyFine145_native_hooks_hidden_launch_v1_20261008.json',{'launch':row,'input_sha256':pins,'new_quality_scores':0})
    print(json.dumps({'actual_native_hooks_started':row['owned_worker_pid'],'full120_CDF_controls_still_required':True}),flush=True)
if __name__=='__main__':main()
