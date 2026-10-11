"""Derive a new Return-after-entire163 contract, preserving frozen163 sources."""
from pathlib import Path
import sys,io,tokenize
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha

NAMES={
'protected_tail_after157_native_stage_v2_20261010':'protected_Return_after163_native_stage_v3_20261010',
'predict_protected_tail_after157_complete_scheme_v2_20261010':'predict_protected_Return_after163_complete_scheme_v3_20261010',
'protected_tail_after_complete157_native_v2_20261010':'protected_Return_after_complete163_native_v3_20261010',
'prepare_Huber_protected_pilot67_and_selected_native14_v1_20261010':'prepare_Return_protected_pilot67_and_selected_native14_v1_20261010',
'actual_protected_Huber_selected_native14_location_v1_20261010':'actual_protected_Return_selected_native14_location_v1_20261010',
'protected_Huber_after157_native_predictor_preparation_v1_20261010':'protected_Return_after163_native_predictor_preparation_v1_20261010',
'protected_Huber_selected_native14_v1_20261010':'protected_Return_selected_native14_v1_20261010',
'BF16Huber010161':'BF16ReturnHuber050166',
'Huber010_high_impact65':'Return_after163_high_impact65',
'HuberProtected163':'ReturnProtected167',
'protected163':'protected167',
'round163':'round167','r163':'r167','第163':'第167',
'round162':'round166','r162':'r166','ReusedNN162':'ReusedNN166',
'round161':'round165','r161':'r165',
'r157':'r163','complete157':'complete163','parent157':'parent163',
'huber010':'returnhuber050','Huber010':'ReturnHuber050',
'qa74':'qa78','QA74':'QA78','v74_20261010':'v78_20261010',
}
def route(s):
    placeholders={}
    for i,(old,new) in enumerate(NAMES.items()):
        key=f'__RETURN167_REPLACE_{i}__';s=s.replace(old,key);placeholders[key]=new
    for key,new in placeholders.items():s=s.replace(key,new)
    nums={'163':'167','162':'166','161':'165','157':'163','74':'78','446':'450'}
    return tokenize.untokenize([t._replace(string=nums.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])

def main():
    outputs={}
    stage=route((A/'protected_tail_after157_native_stage_v2_20261010.py').read_text(encoding='utf8'))
    stage=stage.replace("assert torch.cuda.is_available() and 0.<spec['weight']<=1. and .1<=spec['protect_fraction']<=.5","assert torch.cuda.is_available() and 0.<spec['weight']<=1.\n    if spec['codec']!='CDF':assert .1<=spec['protect_fraction']<=.5")
    a=stage.index('    args=');b=stage.index('    assert ns.sha(path)',a)
    stage=stage[:a]+'''    if spec['codec']=='CDF':
        args=(context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])
    else:args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])
    value=codec.transform(parent,raw,*args);oracle=codec.pandas_oracle(parent,independent,*args)
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    if spec['codec']=='CDF':
        cohort=codec.selected(context.flags,context.valid,spec['role'])
        assert np.array_equal(value[~cohort].view('u8'),np.asarray(parent,dtype=np.float64)[~cohort].view('u8'))
    else:codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])
''' + stage[b:]
    outputs[NAMES['protected_tail_after157_native_stage_v2_20261010']+'.py']=stage
    predictor=route((A/'predict_protected_tail_after157_complete_scheme_v2_20261010.py').read_text(encoding='utf8'))
    a=predictor.index('PARENT_FILENAME=');b=predictor.index('\n',a)
    predictor=predictor[:a]+"PARENT_FILENAME='predict_protected_tail_after157_complete_scheme_v2_20261010.py'"+predictor[b:]
    predictor=predictor.replace('PROTECTED_TAIL_AFTER_COMPLETE157','PROTECTED_RETURN_AFTER_COMPLETE163')
    # Parent163 contains this existing157 graph, which must stay intact.
    assert "'BF16_flag_after152157_complete_parent_rank_CDF'" in predictor
    outputs[NAMES['predict_protected_tail_after157_complete_scheme_v2_20261010']+'.py']=predictor
    pilot=route((A/'prepare_Huber_protected_pilot67_and_selected_native14_v1_20261010.py').read_text(encoding='utf8'))
    pilot=pilot.replace("'TailProtected162_complete76_family_v1_20261010'","'ReusedNN166Quality19_round166_full_registration_v1_20261009'")
    # Avoid contention with the single GPU until own20day six-fit/full5/native42 checks finish.
    needle='    import numpy as np,polars as pl';assert pilot.count(needle)==1
    pilot=pilot.replace(needle,"    closed('actual_forward20_own_controls_and_training_queue_v1_20261010')\n"+needle)
    outputs[NAMES['prepare_Huber_protected_pilot67_and_selected_native14_v1_20261010']+'.py']=pilot
    for name in ('protected163_storage_v2_20261010.py','prepare_protected163_selected_candidate_v2_20261010.py','seal_protected163_selected_candidate_v2_20261010.py'):
        s=route((A/name).read_text(encoding='utf8'))
        if name.startswith('prepare_'):
            # Handle CDF winner through its role-aware signature as well as tail codecs.
            old="selected=transform(raw,neural,dates,flags,valid,cfg['weight'],cfg['protect_fraction'],cfg['sign'])"
            assert s.count(old)==1
            s=s.replace(old,"selected=transform(raw,neural,dates,flags,valid,*((cfg['role'],cfg['weight'],cfg['sign']) if cfg['codec']=='CDF' else (cfg['weight'],cfg['protect_fraction'],cfg['sign'])))")
        outputs[route(name)]=s
    import prepare_protected163_full_registry_sources_v1_20261010 as oldroutes
    for name in oldroutes.NAMES:
        s=route((A/name).read_text(encoding='utf8'))
        s=s.replace('wave446','wave450')
        if name.startswith('publish_'):
            s=s.replace('最佳保护低位排序方案执行完整157后新增Huber原生阶段','最佳方案执行完整163后新增直接收益率原生阶段')
            s=s.replace('Huber65项','直接收益率65项').replace('完整161和162','完整165和166')
            s=s.replace('verified_TLS_Git_retry_runtime_v2_20261008','verified_TLS_Git_retry_runtime_v3_20261010')
        outputs[route(name)]=s
    names=[route(n) for n in oldroutes.NAMES]
    paths=[route(p.name) for p in oldroutes.source_paths() if p.name!='prepare_Huber163_complete67_sources_v1_20261010.py']
    paths.extend([Path(__file__).name,'predict_protected_tail_after157_complete_scheme_v2_20261010.py','protected_tail_after157_native_stage_v2_20261010.py'])
    outputs['prepare_protected167_full_registry_sources_v1_20261010.py']="from pathlib import Path\nA=Path(__file__).resolve().parent\nNAMES="+repr(names)+"\ndef source_paths():return [A/n for n in "+repr(list(dict.fromkeys(paths)))+"]\n"
    for name in ('run_protected163_complete_family_v1_20261010.py','run_protected163_full_registration_v1_20261010.py'):
        s=route((A/name).read_text(encoding='utf8')).replace("'TailProtected162_complete76_family_v1_20261010'","'ReusedNN166Quality19_round166_full_registration_v1_20261009'")
        s=s.replace('ReusedNN166Quality19_round167_full_registration_v1_20261009','ReusedNN167Quality19_round167_full_registration_v1_20261009')
        outputs[route(name)]=s
    for name,s in outputs.items():assert not (A/name).exists(),name;compile(s,str(A/name),'exec')
    for name,s in outputs.items():(A/name).write_text(s,encoding='utf8',newline='\n')
    proof={'status':'compiled_only_own_Return163_parent_chain_and67_routes_actual_preflight_and_GPU_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in outputs]]},'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False}
    for n in ('protected167_candidate_sources_preparation_v2_20261010.json','protected167_full_registry_source_preparation_v1_20261010.json','protected_Return_after163_native_predictor_preparation_v1_20261010.json'):create(A/n,proof)
    print('Compiled new Return-after-entire163 sources; original163 preserved, admission pending',flush=True)
if __name__=='__main__':main()
