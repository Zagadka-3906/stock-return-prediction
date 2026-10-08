"""Prepare52-case full-scoring, freeze, inference, QA51 and main receivers before quality."""
from pathlib import Path
import io,sys,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
STEMS=('run_HuberCrossFamily112_official_comparison','prepare_HuberCrossFamily112_selected_candidate',
    'seal_HuberCrossFamily112_selected_candidate','run_HuberCrossFamily112_round139_full_registration','publish_HuberCrossFamily112_evidence')


def adapt(text):
    mapping={stem+'_v1_20261008':stem.replace('HuberCrossFamily112','SpectralGram52').replace('round139','round140')+'_v1_20261008' for stem in (
        *STEMS,'prepare_HuberCrossFamily112_round139_sources','verify_HuberCrossFamily112_round139_sources',
        'verify_HuberCrossFamily112_prospective_routes','queue_HuberCrossFamily139_complete_pipeline')}
    mapping.update({'HuberCrossFamily112_round139_plan_v1_20261008':'SpectralGram52_round140_plan_v1_20261008',
        'HuberCrossFamily139_storage_v1_20261008':'SpectralGram140_storage_v1_20261008',
        'HuberCrossFamily139_D_scoring_v1_20261008':'SpectralGram140_D_scoring_v1_20261008',
        'HuberCrossFamily109_current_parent_controls_v1_20261008':'SpectralGram49_current_parent_controls_v1_20261008',
        'actual_HuberCrossFamily109_current_parent_location_v1_20261008':'actual_SpectralGram49_current_parent_location_v1_20261008',
        'verify_HuberCrossFamily109_current_parent_v1_20261008':'verify_SpectralGram49_current_parent_v1_20261008',
        'HuberCrossFamily_complete_parent_CDF_v1_20261008':'SpectralGram64_complete_parent_CDF_v1_20261008',
        'HuberCrossFamily_complete_parent_native_stage_v1_20261008':'SpectralGram64_complete_parent_native_stage_v1_20261008',
        'predict_HuberCrossFamily_complete_parent_scheme_v1_20261008':'predict_SpectralGram64_complete_parent_scheme_v1_20261008',
        'nonflag_CPU_HuberCrossFamily_complete_parent_CDF':'nonflag_CPU_SpectralGram64_complete_parent_CDF',
        'HuberCrossFamily_complete_parent_native_replay_verification.json':'SpectralGram64_complete_parent_native_replay_verification.json',
        'passed_actual_complete_parent_and_HuberCrossFamily_two_full_native_independent_replays_and_cold80':'passed_actual_complete_parent_and_SpectralGram64_two_full_native_independent_replays_and_cold80',
        'passed_actual109_current_parent_HuberCrossFamily_CDF_and327_cold_controls':'passed_actual49_current_parent_SpectralGram_CDF_and147_cold_controls',
        'final139_exact_current_parent_controls_fulfilled':'final140_exact_current_parent_controls_fulfilled',
        'BF16reverse40_round138_full_registration_v1_20261008':'HuberCrossFamily112_round139_full_registration_v1_20261008',
        'HuberCrossFamily139_preliminary_historical_main_publication_v1_20261008':'SpectralGram140_historical_causal_main_publication_v1_20261008',
        'HuberCrossFamily112_actual_controls_index_v1_20261008':'SpectralGram52_actual_controls_index_v1_20261008',
        'actual_HuberCrossFamily18_native_hooks_location_v1_20261008':'actual_SpectralGram24_native_hooks_location_v2_20261008',
        'actual_HuberCrossFamily_multiyear_calendar_location_v1_20261008':'actual_SpectralGram_multiyear_calendar_location_v1_20261008',
        'passed_actual25_heads109_current_CDF327cold18_historical_native_hooks':'passed_actual20_heads49_current_CDF147cold24_historical_native_hooks',
        'passed_actual25_heads109_current_CDF327cold18hooks_and24_prospective139_sources':'passed_actual20_heads49_current_CDF147cold24hooks_and24_prospective140_sources',
        'HuberCrossFamily112':'SpectralGram52','HuberCrossFamily139':'SpectralGram140',
        'HuberCrossFamily_group':'SpectralGram_group','zero_HuberCrossFamily_residual_identity':'zero_SpectralGram_residual_identity',
        'round139':'round140','full139':'full140','actual139':'actual140','prospective139':'prospective140','_r139':'_r140',
        '第139轮':'第140轮','qa50':'qa51','QA50':'QA51','qa_v50':'qa_v51',
        'publish(139,':'publish(140,','lossless(139)':'lossless(140)','collect(139, 50, 112)':'collect(140, 51, 52)',
        "namespace['snapshot'](139)":"namespace['snapshot'](140)","'round':139":"'round':140","'round': 139":"'round': 140",
        'NUMBER = 139':'NUMBER = 140','number == 139':'number == 140','WAVES = (422,)':'WAVES = (423,)',
        'wave=422':'wave=423','wave422_results':'wave423_results',"'waves': [422]":"'waves': [423]",
        'actual_complete_QA_version=50':'actual_complete_QA_version=51',"actual_full_QA_version': 50":"actual_full_QA_version': 51",
        'actual112':'actual52','all112':'all52','anchor112':'anchor52','all109_nonanchors':'all49_nonanchors',
        'actual25_existing_native_and109_current_parent_controls':'actual20_existing_native_and49_current_parent_controls'})
    for stem in ('HuberCrossFamily112_round139_source_admission','HuberCrossFamily112_round139_source_preparation',
        'HuberCrossFamily112_controls_main_publication','HuberCrossFamily112_scores_main_publication','HuberCrossFamily112_official_comparison',
        'HuberCrossFamily112_selected_candidate_preparation','HuberCrossFamily112_selected_candidate_sealing','HuberCrossFamily112_round139_full_registration'):
        mapping[stem+'_v1_20261008']=stem.replace('HuberCrossFamily112','SpectralGram52').replace('round139','round140')+'_v1_20261008'
    value=substitute(text,mapping)
    value=value.replace('(136,137,138)','(137,138,139)').replace('(136, 137, 138)','(137, 138, 139)')
    value=value.replace('for g in range(6)','for g in range(8)')
    for before,after in (("'existing_saved_native_heads':25","'existing_saved_native_heads':20"),
        ("'actual_existing_native_head_audits':25","'actual_existing_native_head_audits':20"),
        ("'actual_full_native_OOF_heads':5","'actual_full_native_OOF_heads':4"),
        ("'actual_full_CDF_controls':109","'actual_full_CDF_controls':49"),
        ("'actual_cold_CDF_controls':327","'actual_cold_CDF_controls':147"),
        ("'actual_historical_native_hooks':18","'actual_historical_native_hooks':24"),
        ("'existing_HuberCrossFamily_saved_native_heads': 25","'existing_SpectralGram_saved_native_heads': 20"),
        ("'actual25_HuberCrossFamily_saved_native_heads_source'","'actual20_SpectralGram_saved_native_heads_source'")):
        value=value.replace(before,after)
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    return tokenize.untokenize([token._replace(string='52') if token.type==tokenize.NUMBER and token.string=='112' else token for token in tokens])


def main():
    plan=A/'SpectralGram52_round140_plan_v1_20261008.json';assert read(plan)['expected_scored_cases']==52
    sources=[Path(__file__),plan];outputs={}
    for stem in STEMS:
        original=A/(stem+'_v1_20261008.py');sources.append(original);text=adapt(original.read_text(encoding='utf8'))
        text=text.replace('E:/赛题五_本机临时/第139轮_20261008','E:/赛题五_本机临时/第140轮_20261008')
        text=text.replace('预定112项：三个合格锚点、108项Huber跨模型组合、零幅度恒等对照','预定52项：三个合格锚点、48项正负主成分截断变换、零幅度恒等对照')
        target=A/(stem.replace('HuberCrossFamily112','SpectralGram52').replace('round139','round140')+'_v1_20261008.py')
        assert not target.exists();compile(text,str(target),'exec');outputs[target]=text
    for before,after in (('HuberCrossFamily139_storage_v1_20261008.py','SpectralGram140_storage_v1_20261008.py'),
        ('verify_HuberCrossFamily139_D_scoring_scope_v1_20261008.py','verify_SpectralGram140_D_scoring_scope_v1_20261008.py')):
        original=A/before;sources.append(original);text=adapt(original.read_text(encoding='utf8'))
        text=text.replace('E:/赛题五_本机临时/第139轮_20261008','E:/赛题五_本机临时/第140轮_20261008');target=A/after
        assert not target.exists();compile(text,str(target),'exec');outputs[target]=text
    for path,text in outputs.items():path.write_text(text,encoding='utf8',newline='\n')
    create(A/'SpectralGram140_receiver_drafts_v1_20261008.json',{'status':'prepared7_calendar_aware_complete52_scientific_receivers_before_quality',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},'new_official_scores':0,
        'source_generator_prospective_current_parent_admission_and_queue_still_required':True,'test_labels_read':False})
    from SpectralGram140_storage_v1_20261008 import OUTPUTS,EBASE
    create(A/'SpectralGram140_junction_requests_v1_20261008.json',{'workspace':str(ROOT),'E_base':str(EBASE),
        'requests':[{'logical':str(p),'target':str(t)} for p,t in OUTPUTS.items()]})
    print('Seven complete52 scientific receivers compiled; all140 large outputs and source freeze use E.',flush=True)


if __name__=='__main__':main()
