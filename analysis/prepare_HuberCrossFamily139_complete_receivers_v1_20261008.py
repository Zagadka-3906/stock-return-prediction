"""Prepare fresh112-case scientific receivers; preserve all earlier model and score bytes."""
from pathlib import Path
import io,sys,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
STEMS=('run_CrossFamily94_official_comparison','prepare_CrossFamily94_selected_candidate',
    'seal_CrossFamily94_selected_candidate','run_CrossFamily94_round136_full_registration','publish_CrossFamily94_evidence')


def adapt(text):
    mapping={stem+'_v4_20261008':stem.replace('CrossFamily94','HuberCrossFamily112').replace('round136','round139')+'_v1_20261008' for stem in (
        *STEMS,'prepare_CrossFamily94_round136_sources','verify_CrossFamily94_round136_sources',
        'verify_CrossFamily94_prospective_routes','queue_CrossFamily136_complete_pipeline')}
    mapping.update({'CrossFamily94_round136_plan_v1_20261008':'HuberCrossFamily112_round139_plan_v1_20261008',
        'CrossFamily136_storage_v1_20261008':'HuberCrossFamily139_storage_v1_20261008',
        'CrossFamily136_D_scoring_v1_20261008':'HuberCrossFamily139_D_scoring_v1_20261008',
        'CrossFamily91_current_parent_controls_v1_20261008':'HuberCrossFamily109_current_parent_controls_v1_20261008',
        'actual_CrossFamily91_current_parent_location_v1_20261008':'actual_HuberCrossFamily109_current_parent_location_v1_20261008',
        'verify_CrossFamily91_current_parent_v1_20261008':'verify_HuberCrossFamily109_current_parent_v1_20261008',
        'CrossFamily_complete_parent_CDF_v1_20261008':'HuberCrossFamily_complete_parent_CDF_v1_20261008',
        'CrossFamily_complete_parent_native_stage_v2_20261008':'HuberCrossFamily_complete_parent_native_stage_v1_20261008',
        'predict_CrossFamily_complete_parent_scheme_v2_20261008':'predict_HuberCrossFamily_complete_parent_scheme_v1_20261008',
        'nonflag_CPU_CrossFamily_complete_parent_CDF':'nonflag_CPU_HuberCrossFamily_complete_parent_CDF',
        'CrossFamily_complete_parent_native_replay_verification.json':'HuberCrossFamily_complete_parent_native_replay_verification.json',
        'passed_actual_complete_parent_and_CrossFamily_two_full_native_independent_replays_and_cold80':'passed_actual_complete_parent_and_HuberCrossFamily_two_full_native_independent_replays_and_cold80',
        'passed_actual91_current_parent_CrossFamily_CDF_and273_cold_controls':'passed_actual109_current_parent_HuberCrossFamily_CDF_and327_cold_controls',
        'final136_exact_current_parent_controls_fulfilled':'final139_exact_current_parent_controls_fulfilled',
        'BF16wide40_round135_full_registration_v4_20261008':'BF16reverse40_round138_full_registration_v1_20261008',
        'CrossFamily_preliminary_controls_main_publication_v1_20261008':'HuberCrossFamily139_preliminary_historical_main_publication_v1_20261008',
        'CrossFamily94_actual_controls_index_v3_20261008':'HuberCrossFamily112_actual_controls_index_v1_20261008',
        'CrossFamily136_receiver_preparation_v4_20261008':'HuberCrossFamily139_receiver_preparation_v1_20261008',
        'CrossFamily136_D_scoring_scope_v1_20261008':'HuberCrossFamily139_D_scoring_scope_v1_20261008',
        'CrossFamily94':'HuberCrossFamily112','CrossFamily136':'HuberCrossFamily139',
        'crossfamily_group':'HuberCrossFamily_group','zero_CrossFamily_residual_identity':'zero_HuberCrossFamily_residual_identity',
        'round136':'round139','full136':'full139','actual136':'actual139','prospective136':'prospective139','_r136':'_r139',
        '第136轮':'第139轮','qa47':'qa50','QA47':'QA50','qa_v47':'qa_v50',
        'publish(136,':'publish(139,','lossless(136)':'lossless(139)','collect(136, 47, 94)':'collect(139, 50, 112)',
        "namespace['snapshot'](136)":"namespace['snapshot'](139)","'round':136":"'round':139","'round': 136":"'round': 139",
        'NUMBER = 136':'NUMBER = 139','number == 136':'number == 139','WAVES = (419,)':'WAVES = (422,)',
        'wave=419':'wave=422','wave419_results':'wave422_results',"'waves': [419]":"'waves': [422]",
        'actual_complete_QA_version=47':'actual_complete_QA_version=50',"actual_full_QA_version': 47":"actual_full_QA_version': 50",
        'actual94':'actual112','all94':'all112','anchor94':'anchor112','all91_nonanchors':'all109_nonanchors',
        'actual30_existing_native_and91_current_parent_controls':'actual25_existing_native_and109_current_parent_controls',
        'passed_actual30_heads91_current_CDF273cold15_historical_native_hooks':'passed_actual25_heads109_current_CDF327cold18_historical_native_hooks',
        'passed_actual30_heads91_current_CDF273cold15hooks_and24_prospective136_sources':'passed_actual25_heads109_current_CDF327cold18hooks_and24_prospective139_sources'})
    for stem in ('CrossFamily94_round136_source_admission','CrossFamily94_round136_source_preparation',
        'CrossFamily94_controls_main_publication','CrossFamily94_scores_main_publication','CrossFamily94_official_comparison',
        'CrossFamily94_selected_candidate_preparation','CrossFamily94_selected_candidate_sealing','CrossFamily94_round136_full_registration'):
        mapping[stem+'_v4_20261008']=stem.replace('CrossFamily94','HuberCrossFamily112').replace('round136','round139')+'_v1_20261008'
    value=substitute(text,mapping)
    value=value.replace('(112,134,135)','(136,137,138)').replace('(112, 134, 135)','(136, 137, 138)')
    value=value.replace('parent in (134,135)','parent in (136,137,138)').replace('parent_number in (134,135)','parent_number in (136,137,138)')
    value=value.replace('for g in range(5)','for g in range(6)').replace("plan['anchor_rounds']","plan['anchors']")
    for before,after in (("'existing_saved_native_heads':30","'existing_saved_native_heads':25"),
        ("'actual_existing_native_head_audits':30","'actual_existing_native_head_audits':25"),
        ("'actual_full_native_OOF_heads':6","'actual_full_native_OOF_heads':5"),
        ("'actual_full_CDF_controls':91","'actual_full_CDF_controls':109"),
        ("'actual_cold_CDF_controls':273","'actual_cold_CDF_controls':327"),
        ("'actual_historical_native_hooks':15","'actual_historical_native_hooks':18"),
        ("'existing_CrossFamily_saved_native_heads': 30","'existing_HuberCrossFamily_saved_native_heads': 25"),
        ("'actual30_CrossFamily_saved_native_heads_source'","'actual25_HuberCrossFamily_saved_native_heads_source'")):
        value=value.replace(before,after)
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    return tokenize.untokenize([token._replace(string='112') if token.type==tokenize.NUMBER and token.string=='94' else token for token in tokens])


def main():
    plan_path=A/'HuberCrossFamily112_round139_plan_v1_20261008.json';assert read(plan_path)['expected_scored_cases']==112
    outputs={};sources=[Path(__file__),plan_path]
    for stem in STEMS:
        original=A/(stem+'_v4_20261008.py');sources.append(original);text=adapt(original.read_text(encoding='utf8'))
        if stem.startswith('prepare_'):
            text=text.replace("'state_kind':kind,'source_path'","'state_kind':row['native_stage_state_kind'],'source_path'")
            needle="*[component['name'] for component in components]";assert text.count(needle)==1
            text=text.replace(needle,"*[component['name'] for component in components if component['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()}]")
            text=text.replace("freeze=A/'HuberCrossFamily112_pre_inference_source_freeze_v1_20261008'", "freeze=Path('E:/赛题五_本机临时/第139轮_20261008/pre_inference_source_freeze_v1')")
        if stem.startswith('publish_'):
            first=text.index('    for pointer in (');last=text.index('    sources += list(science.glob',first)
            text=text[:first]+'''    for pointer in ('actual_HuberCrossFamily109_current_parent_location_v1_20261008.json',
        'actual_HuberCrossFamily18_native_hooks_location_v1_20261008.json','actual_HuberCrossFamily_multiyear_calendar_location_v1_20261008.json'):
        folder=Path(read(A/pointer)['output']);sources += list(folder.glob('*.json'))
''' +text[last:]
        if stem.startswith('run_CrossFamily94_round'):
            text=text.replace('actual_registration_v4_20261008','actual_registration_v1_20261008').replace('registration_v4_file_IO_20261008','registration_v1_file_IO_20261008')
            text=text.replace('预定94项：三个合格锚点、90项跨模型组合、零幅度恒等对照','预定112项：三个合格锚点、108项Huber跨模型组合、零幅度恒等对照')
        target=A/(stem.replace('CrossFamily94','HuberCrossFamily112').replace('round136','round139')+'_v1_20261008.py')
        assert not target.exists();compile(text,str(target),'exec');outputs[target]=text
    for before,after in (('CrossFamily136_storage_v1_20261008.py','HuberCrossFamily139_storage_v1_20261008.py'),
        ('verify_CrossFamily136_D_scoring_scope_v1_20261008.py','verify_HuberCrossFamily139_D_scoring_scope_v1_20261008.py')):
        original=A/before;sources.append(original);text=adapt(original.read_text(encoding='utf8'));target=A/after
        assert not target.exists();compile(text,str(target),'exec');outputs[target]=text
    for path,text in outputs.items():path.write_text(text,encoding='utf8',newline='\n')
    create(A/'HuberCrossFamily139_receiver_drafts_v1_20261008.json',{'status':'prepared7_fresh_complete112_scientific_receivers_before_quality',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},'new_fits':0,'new_official_scores':0,
        'source_generator_prospective_admission_current_parent_and_dispatch_still_required':True,'test_labels_read':False})
    from HuberCrossFamily139_storage_v1_20261008 import OUTPUTS,EBASE
    create(A/'HuberCrossFamily139_junction_requests_v1_20261008.json',{'workspace':str(ROOT),'E_base':str(EBASE),
        'requests':[{'logical':str(p),'target':str(t)} for p,t in OUTPUTS.items()]})
    print('Seven fresh112 scientific receivers compiled, with source freeze and large outputs on E.',flush=True)


if __name__=='__main__':main()
