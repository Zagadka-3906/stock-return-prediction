"""Prepare independent recent252-after-whole167 round; preserve every frozen source."""
from pathlib import Path
import sys,io,tokenize
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

MAP={
 'ReturnProtected167_selected_native14_v1_20261010':'RecentReturn252_after167_selected_native14_v1_20261010',
 'prepare_Return_protected_pilot67_and_selected_native14_v1_20261010':'qualify_RecentReturn252_after167_selected_native14_v2_20261010',
 'protected_Return_after163_native_stage_v3_20261010':'protected_RecentReturn252_after167_native_stage_v1_20261010',
 'predict_protected_Return_after163_complete_scheme_v3_20261010':'predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010',
 'predict_protected_Return_after163_complete_scheme_v4_20261010':'predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010',
 'protected_Return_after_complete163_native_v3_20261010':'protected_RecentReturn252_after_complete167_native_v1_20261010',
 'protected_Return_after163_native_predictor_preparation_v1_20261010':'RecentReturn252_after167_selected_native14_source_admission_v1_20261010',
 'protected_Return_selected_native14_v1_20261010':'protected_RecentReturn252_selected_native14_v1_20261010',
 'actual_protected_Return_selected_native14_location_v1_20261010':'actual_protected_RecentReturn252_selected_native14_location_v1_20261010',
 'Return_after163_high_impact65':'RecentReturn252_after167_high_impact65',
 'ReturnProtected167':'RecentReturn252Protected168',
 'protected167':'protected168',
 'round167':'round168','r167':'r168','第167':'第168',
 'round166':'round167','r166':'r167','ReusedNN166':'ReusedNN167',
 'round165':'round166','r165':'r166',
 'r163':'r167','complete163':'complete167','parent163':'parent167','after163':'after167',
 'returnhuber050':'recent252returnhuber050','ReturnHuber050':'RecentReturn252Huber050',
 'qa78':'qa79','QA78':'QA79','v78_20261010':'v79_20261010',
 'wave450':'wave451',
}

def route(text):
    swaps={}
    for i,(old,new) in enumerate(sorted(MAP.items(),key=lambda x:-len(x[0]))):
        token=f'__RECENT168_REPLACE_{i}__';text=text.replace(old,token);swaps[token]=new
    for token,new in swaps.items():text=text.replace(token,new)
    numbers={'167':'168','166':'167','165':'166','163':'167','78':'79','450':'451'}
    return tokenize.untokenize([t._replace(string=numbers.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])

def main():
    assert allowed()
    assert read(A/'github_validation_sync_main_20261005/round167_receipt.json')['scored_records']==67
    import prepare_protected167_full_registry_sources_v1_20261010 as oldroutes
    outputs={};inputs=[Path(__file__)]
    originals=['protected167_storage_v2_20261010.py','prepare_protected167_selected_candidate_v3_20261010.py','seal_protected167_selected_candidate_v2_20261010.py',*oldroutes.NAMES]
    for name in originals:
        source=A/name;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        if name.startswith('prepare_protected167_selected'):
            text=text.replace('parent_number in (167,166,167)','parent_number in (166,167)')
        if name.startswith('register_'):
            text=text.replace("'qualified161','qualified162'","'qualified166','qualified167'")
        if name.startswith('publish_'):
            text=text.replace('直接收益率','近期252日训练窗口收益率').replace('第168轮76项','第168轮67项')
        outputs[route(name)]=text
    names=[route(n) for n in oldroutes.NAMES]
    source_names=[*outputs,'prepare_RecentReturn252Protected168_complete67_v1_20261010.py','protected168_candidate_sources_preparation_v2_20261010.json','protected168_full_registry_source_preparation_v1_20261010.json','qualify_RecentReturn252_after167_selected_native14_v2_20261010.py','protected_RecentReturn252_after167_native_stage_v1_20261010.py','predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010.py','RecentReturn252_after167_selected_native14_source_admission_v1_20261010.json','RecentReturn252_after167_callback_prototype_correction_v2_20261010.json','recover_RecentReturn252_after167_selected_native14_v2_20261010.py','predict_protected_Return_after163_complete_scheme_v4_20261010.py','protected_Return_after163_native_stage_v3_20261010.py','predict_protected_tail_after157_complete_scheme_v2_20261010.py','protected_tail_after157_native_stage_v2_20261010.py','owned_idle_publication_wait_runtime_v1_20261010.py','lossless_chunked_safe_main_runtime_v1_20261009.py','serial_main_publication_mutex_v1_20261009.py','byte_exact_ranking_stream_runtime_v1_20261010.py','byte_exact_publication_encoder_runtime_v1_20261010.py','late_bound_dynamic_snapshot_encoder_runtime_v1_20261010.py','late_bound_snapshot_encoder_actual_CPU_controls_v1_20261010.json']
    outputs['prepare_protected168_full_registry_sources_v1_20261010.py']="from pathlib import Path\nA=Path(__file__).resolve().parent\nNAMES="+repr(names)+"\ndef source_paths():return [A/n for n in "+repr(list(dict.fromkeys(source_names)))+"]\n"
    for name,text in outputs.items():assert not (A/name).exists(),name;compile(text,str(A/name),'exec')
    # Candidate must point at actual whole167+recent decoder and the independently admitted native14 service.
    candidate=outputs['prepare_protected168_selected_candidate_v3_20261010.py']
    assert 'predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010.py' in candidate
    assert "parent_number==167" in candidate
    assert "RecentReturn252_after167_selected_native14_v1_20261010" in candidate
    assert "neural_BF16_medium2048_recent252returnhuber050_seed09_e64_bank6_v1_20261009" in candidate
    for name,text in outputs.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    proof={'status':'compiled_only_recent252_complete167_base67_routes_QA79_native14_and_full_inference_pending','input_sha256':{str(p):sha(p) for p in [*inputs,*[A/n for n in outputs]]},'actual_scheme_base_round':167,'comparison_parent_round':167,'expected_records':67,'expected_QA':79,'source_outputs':list(outputs),'new_quality_scores':0,'new_native_fits':0,'test_X_read':False,'test_labels_read':False}
    for name in ('protected168_candidate_sources_preparation_v2_20261010.json','protected168_full_registry_source_preparation_v1_20261010.json'):create(A/name,proof)
    print({'compiled_new_files':len(outputs),'round':168,'base':167,'full_inference_not_yet_dispatched':True},flush=True)
if __name__=='__main__':main()
