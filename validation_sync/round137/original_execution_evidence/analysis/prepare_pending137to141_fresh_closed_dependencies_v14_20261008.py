"""Freeze fresh chronological receivers after the actually qualified135 and recovered136 gates."""
from pathlib import Path
import ast, json, sys, time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def save(path,text):
    assert not path.exists(),path
    compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')

def main():
    old=A/'verify_HuberIRLS64_49_current_parent_v4_20261008.py'
    value=old.read_text(encoding='utf8').replace('CrossFamily94_round136_full_registration_v4_20261008','CrossFamily94_round136_full_registration_v6_20261008')
    value=value.replace('current_parent_v4_20261008','current_parent_v6_20261008').replace('current_parent_full_v4_20261008','current_parent_full_v6_20261008').replace('current_parent_full_location_v4_20261008','current_parent_full_location_v6_20261008').replace('current_parent_location_v4_20261008','current_parent_location_v6_20261008')
    current=A/'verify_HuberIRLS64_49_current_parent_v6_20261008.py'
    assert current.read_text(encoding='utf8')==value
    original=A/'recover_pending137to141_registration_contracts_v11_20261008.py'
    text=original.read_text(encoding='utf8').replace('v11','v14').replace('version11','version12')
    boundary='\ndef remap(text):';assert text.count(boundary)==1
    text=text.replace(boundary,"""
    MAPPING.update({
        'BF16wide40_round135_full_registration_v4_20261008':'BF16wide40_round135_full_registration_v7_20261008',
        'CrossFamily94_round136_full_registration_v4_20261008':'CrossFamily94_round136_full_registration_v6_20261008',
        'HuberIRLS64_49_current_parent_controls_v4_20261008':'HuberIRLS64_49_current_parent_controls_v6_20261008',
        'verify_HuberIRLS64_49_current_parent_v4_20261008':'verify_HuberIRLS64_49_current_parent_v6_20261008',
        'actual_HuberIRLS64_49_current_parent_location_v4_20261008':'actual_HuberIRLS64_49_current_parent_location_v6_20261008'})
"""+boundary)
    text=text.replace("if name not in MAPPING:continue","if name not in MAPPING or name.startswith('HuberIRLS64_49_current_parent_controls_'):continue")
    # Candidate aliases wrap the original predictor; model bytes and numerical code remain unchanged.
    needle="products.append((A/(MAPPING[old.stem]+'.py'),remap(old.read_text(encoding='utf8'))))"
    assert text.count(needle)==1
    patch="""value=remap(old.read_text(encoding='utf8'))
            if old.stem.startswith('prepare_') and '_selected_candidate_' in old.stem:
                if n==137:value=value.replace("freeze=A/'Huber52_pre_inference_source_freeze_v1_20261008'", "freeze=Path('E:/赛题五_本机临时/第137轮_20261008/pre_inference_source_freeze_v14')")
                if n==138:value=value.replace("freeze=A/'BF16reverse40_pre_inference_source_freeze_v1_20261008'", "freeze=Path('E:/赛题五_本机临时/第138轮_20261008/pre_inference_source_freeze_v14')")
                line="            prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json');output_scope.reverify()"
                assert value.count(line)==1,old
                value=value.replace(line,"            from short_content_addressed_native_storage_v2_20261008 import installed as short_storage\\n            with short_storage(ns,freeze/'model_source_aliases') as alias_contract:\\n                prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json')\\n            create(OUT/'short_native_source_aliases_execution.json',alias_contract)\\n            output_scope.reverify()")
            if old.stem.startswith('seal_') and '_selected_candidate_' in old.stem:
                line="        target=candidate/'evidence'/source.relative_to(A);target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);assert sha(target)==sha(source)"
                assert value.count(line)==1,old
                value=value.replace(line,"        relative=source.relative_to(A) if source.is_relative_to(A) else Path('external_frozen_metadata')/(sha(source)+'_'+source.name)\\n        target=candidate/'evidence'/relative;target.parent.mkdir(parents=True,exist_ok=True)\\n        if target.exists():assert sha(target)==sha(source)\\n        else:os.link(source,target)\\n        assert sha(target)==sha(source)")
            products.append((A/(MAPPING[old.stem]+'.py'),value))"""
    text=text.replace(needle,patch)
    # Actual reverse138 scoring records are D1. Preserve the prior missing-D2 failure as evidence.
    needle="value=remap(prospective.read_text(encoding='utf8'))";assert text.count(needle)==1
    text=text.replace(needle,needle+"""
        if n==138:
            for before,after in {
                'verify_BF16reverse138_D_scoring_scope_v2_20261008':'verify_BF16reverse138_D_scoring_scope_v1_20261008',
                'BF16reverse138_D_scoring_scope_v2_20261008.json':'BF16reverse138_D_scoring_scope_v1_20261008.json',
                ",A/'actual_BF16reverse138_complete_dependency_recovery_v6_20261008.json'":"",
                ",A/'actual_BF16reverse138_D_scoring_receiver_recovery_v4_20261008.json'":""}.items():value=value.replace(before,after)
""")
    # Keep metadata present before any prospective proof; its original sources are explicitly pinned.
    needle="if 'receiver_drafts' in old" # The original factory supplies only referenced preparation metadata.
    end="    # Pin all generated surfaces before execution; receiver preflight checks additionally pin their actual sources."
    assert text.count(end)==1
    text=text.replace(end,"""    for old,new in MAPPING.items():
        source=A/(old+'.json');target=A/(new+'.json')
        if 'receiver_drafts' in old and source.is_file() and not target.exists():
            create(target,{'status':'prepared_fresh12_declarative_drafts_before_actual_prospective_checks',
                'original_source':str(source),'original_sha256':sha(source),'new_official_scores':0,'test_labels_read':False})
"""+end)
    # Include the original alias proof and actual recovery factory in every registration source surface.
    text=text.replace("A/'pending137to141_receiver_preparation_v14_20261008.json']))",
        "A/'pending137to141_receiver_preparation_v14_20261008.json',A/'prepare_pending137to141_fresh_closed_dependencies_v14_20261008.py',A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json']))")
    helper=A/'recover_pending137to141_registration_contracts_v14_20261008.py';save(helper,text)
    import recover_pending137to141_registration_contracts_v14_20261008 as h
    h.prepare()
    pins={str(p):sha(p) for p in [Path(__file__),original,old,current,helper,A/'pending137to141_receiver_preparation_v14_20261008.json',A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json']}
    create(A/'pending137to141_closed_dependency_recovery_v14_20261008.json',{
        'status':'frozen_fresh12_five_round_receivers_before_prospective_controls_or_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'actual135_gate':7,'actual136_gate':5,'current137_controls_version':5,
        'failed11_sources_and_terminal_logs_preserved':True,'same_declared308_quality_cases':True,
        'original_native_models_and_prediction_math_unchanged':True,'new_official_scores':0,'test_labels_read':False})
    print('Fresh12 five-round surfaces prepared; full prospective checks still required.',flush=True)

if __name__=='__main__':main()
