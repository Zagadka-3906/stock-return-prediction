"""Prepare fresh52-case official, selected, sealing, fullQA48 and main receivers before quality."""
from pathlib import Path
import io,sys,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

STEMS=('run_CrossFamily94_official_comparison','prepare_CrossFamily94_selected_candidate',
    'seal_CrossFamily94_selected_candidate','run_CrossFamily94_round136_full_registration','publish_CrossFamily94_evidence')


def adapt(text):
    mapping={stem+'_v2_20261008':stem.replace('CrossFamily94','Huber52').replace('round136','round137')+'_v1_20261008' for stem in (
        *STEMS,'prepare_CrossFamily94_round136_sources','verify_CrossFamily94_round136_sources','verify_CrossFamily94_prospective_routes')}
    for stem in ('CrossFamily94_round136_source_admission','CrossFamily94_round136_source_preparation',
        'CrossFamily94_selected_candidate_preparation','CrossFamily94_selected_candidate_sealing',
        'CrossFamily94_controls_main_publication','CrossFamily94_scores_main_publication','CrossFamily94_official_comparison'):
        mapping[stem+'_v2_20261008']=stem.replace('CrossFamily94','Huber52').replace('round136','round137')+'_v1_20261008'
    mapping.update({'CrossFamily94_round136_plan_v1_20261008':'Huber52_round137_receiver_contract_v1_20261008',
        'CrossFamily136_storage_v1_20261008':'Huber137_storage_v1_20261008',
        'CrossFamily136_D_scoring_v1_20261008':'Huber137_D_scoring_v1_20261008',
        'CrossFamily91_current_parent_controls_v1_20261008':'HuberIRLS64_49_current_parent_controls_v2_20261008',
        'actual_CrossFamily91_current_parent_location_v1_20261008':'actual_HuberIRLS64_49_current_parent_location_v2_20261008',
        'CrossFamily_complete_parent_CDF_v1_20261008':'Huber52_complete_parent_receiver_codec_v1_20261008',
        'CrossFamily_complete_parent_native_stage_v1_20261008':'HuberIRLS64_complete_parent_native_stage_v2_20261008',
        'predict_CrossFamily_complete_parent_scheme_v1_20261008':'predict_HuberIRLS64_complete_parent_scheme_v2_20261008',
        'nonflag_CPU_CrossFamily_complete_parent_CDF':'nonflag_CPU_HuberIRLS64_complete_parent_CDF',
        'CrossFamily_complete_parent_native_replay_verification.json':'HuberIRLS64_complete_parent_native_replay_verification.json',
        'passed_actual_complete_parent_and_CrossFamily_two_full_native_independent_replays_and_cold80':'passed_actual_complete_parent_and_HuberIRLS64_two_full_native_independent_replays_and_cold80',
        'passed_actual91_current_parent_CrossFamily_CDF_and273_cold_controls':'passed_actual49_current_complete_parent_HuberIRLS64_CDF_and147_cold_controls',
        'final136_exact_current_parent_controls_fulfilled':'final137_exact_current_parent_controls_fulfilled',
        'BF16wide40_round135_full_registration_v4_20261008':'CrossFamily94_round136_full_registration_v2_20261008',
        'passed_actual30_heads91_current_CDF273cold15_historical_native_hooks':'passed_actual10_heads49_current_CDF147cold18_historical_native_hooks',
        'passed_actual30_heads91_current_CDF273cold15hooks_and24_prospective136_sources':'passed_actual10_heads49_current_CDF147cold18hooks_and24_prospective137_sources',
        'CrossFamily94':'Huber52','crossfamily_group':'HuberIRLS64_group','zero_CrossFamily_residual_identity':'zero_HuberIRLS64_residual_identity',
        'round136':'round137','full136':'full137','actual136':'actual137','prospective136':'prospective137','_r136':'_r137',
        '第136轮':'第137轮','qa47':'qa48','QA47':'QA48','qa_v47':'qa_v48',
        'publish(136,':'publish(137,','lossless(136)':'lossless(137)','collect(136, 47, 94)':'collect(137, 48, 52)',
        "namespace['snapshot'](136)":"namespace['snapshot'](137)","'round':136":"'round':137","'round': 136":"'round': 137",
        'NUMBER = 136':'NUMBER = 137','number == 136':'number == 137','WAVES = (419,)':'WAVES = (420,)',
        'wave=419':'wave=420','wave419_results':'wave420_results',"'waves': [419]":"'waves': [420]",
        'actual_complete_QA_version=47':'actual_complete_QA_version=48',"actual_full_QA_version': 47":"actual_full_QA_version': 48",
        'actual94':'actual52','all94':'all52','anchor94':'anchor52','all91_nonanchors':'all49_nonanchors',
        'actual30_existing_native_and91_current_parent_controls':'actual10_existing_native_and49_current_parent_controls'})
    value=substitute(text,mapping)
    value=value.replace('(112,134,135)','(134,135,136)').replace('(112, 134, 135)','(134, 135, 136)')
    value=value.replace('parent in (134,135)','parent in (134,135,136)').replace('parent_number in (134,135)','parent_number in (134,135,136)')
    value=value.replace('for g in range(5)','for g in range(6)')
    for before,after in (("'existing_saved_native_heads':30","'existing_saved_native_heads':10"),
        ("'actual_existing_native_head_audits':30","'actual_existing_native_head_audits':10"),
        ("'actual_full_native_OOF_heads':6","'actual_full_native_OOF_heads':2"),
        ("'actual_full_CDF_controls':91","'actual_full_CDF_controls':49"),
        ("'actual_cold_CDF_controls':273","'actual_cold_CDF_controls':147"),
        ("'actual_historical_native_hooks':15","'actual_historical_native_hooks':18"),
        ("'existing_CrossFamily_saved_native_heads': 30","'existing_Huber_saved_native_heads': 10"),
        ("'actual30_CrossFamily_saved_native_heads_source'","'actual10_Huber_saved_native_heads_source'")):
        value=value.replace(before,after)
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    value=tokenize.untokenize([token._replace(string='52') if token.type==tokenize.NUMBER and token.string=='94' else token for token in tokens])
    return value


def main():
    contract=A/'Huber52_round137_receiver_contract_v1_20261008.json';assert read(contract)['expected_scored_cases']==52
    outputs={};originals=[]
    for stem in STEMS:
        source=A/(stem+'_v2_20261008.py');originals.append(source);target=A/(stem.replace('CrossFamily94','Huber52').replace('round136','round137')+'_v1_20261008.py')
        text=adapt(source.read_text(encoding='utf8'))
        if stem.startswith('prepare_'):
            needle="'state_kind':kind,'source_path'";assert text.count(needle)==1
            text=text.replace(needle,"'state_kind':'HuberIRLS64_linear','source_path'")
            text=text.replace("parent_number in (112,134,135)","parent_number in (134,135,136)")
        if stem.startswith('run_CrossFamily94_round'):
            text=text.replace('Huber52_round137_actual_registration_v2_20261008','Huber52_round137_actual_registration_v1_20261008')
            text=text.replace('run_Huber52_round137_full_registration_v2_file_IO_20261008','run_Huber52_round137_full_registration_v1_file_IO_20261008')
            text=text.replace("'完整父方案的跨模型残差集成'","'完整父方案的Huber鲁棒残差变换'")
            text=text.replace('预定94项：三个合格锚点、90项跨模型组合、零幅度恒等对照','预定52项：三个合格锚点、48项正负Huber配置、零幅度恒等对照')
        if stem.startswith('publish_'):
            start=text.index('    for pointer in (');end=text.index("    sources += list(science.glob",start)
            text=text[:start]+'''    for pointer in ('actual_nonflag_HuberIRLS64_bank10_location_v1_20261008.json',
        'actual_HuberIRLS64_49_current_parent_location_v2_20261008.json','actual_HuberIRLS64_18_native_hooks_location_v2_20261008.json',
        'actual_HuberIRLS64_10_causal_inputs_location_v1_20261008.json'):
        folder=Path(read(A/pointer)['output']);sources += list(folder.glob('*.json'))
''' +text[end:]
        text=text.replace('跨模型集成实际证据','Huber鲁棒残差实际证据')
        assert not target.exists();compile(text,str(target),'exec');outputs[target]=text
    storage_source=A/'CrossFamily136_storage_v1_20261008.py';text=adapt(storage_source.read_text(encoding='utf8'))
    text=text.replace('number == 136','number == 137')
    storage=A/'Huber137_storage_v1_20261008.py';assert not storage.exists();compile(text,str(storage),'exec');outputs[storage]=text;originals.append(storage_source)
    guard_source=A/'verify_CrossFamily136_D_scoring_scope_v1_20261008.py';text=adapt(guard_source.read_text(encoding='utf8'))
    text=text.replace('CrossFamily136_D_scoring_scope_v1_20261008','Huber137_D_scoring_scope_v1_20261008')
    guard=A/'verify_Huber137_D_scoring_scope_v1_20261008.py';assert not guard.exists();compile(text,str(guard),'exec');outputs[guard]=text;originals.append(guard_source)
    for path,text in outputs.items():path.write_text(text,encoding='utf8',newline='\n')
    create(A/'Huber137_receiver_drafts_v1_20261008.json',{'status':'prepared7_fresh_Huber52_scientific_receivers_before_quality',
        'input_sha256':{str(path):sha(path) for path in [Path(__file__),contract,*originals,*outputs]},
        'bounded_case_count':52,'three_complete_parent_anchors':[134,135,136],'new_quality_scores':0,
        'complete_source_generator_admission_and24_prospective_controls_still_required':True})
    import Huber137_storage_v1_20261008 as storage_module
    create(A/'Huber137_junction_requests_v1_20261008.json',{'status':'fresh_exact_outputs_requested_without_moving_or_deleting_anything',
        'workspace':str(ROOT),'E_base':str(storage_module.EBASE),
        'requests':[{'logical':str(logical),'target':str(target)} for logical,target in storage_module.OUTPUTS.items()]})
    print('Five fresh52 scientific receivers, E storage helper and original D scope verifier prepared; full source/preflight work remains.',flush=True)


if __name__=='__main__':main()
