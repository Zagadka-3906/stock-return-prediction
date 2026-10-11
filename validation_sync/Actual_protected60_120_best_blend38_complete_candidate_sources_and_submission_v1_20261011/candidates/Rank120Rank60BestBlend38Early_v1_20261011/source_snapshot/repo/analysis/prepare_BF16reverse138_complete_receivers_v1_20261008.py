"""Prepare fresh reverse-neural complete40 receivers; no scientific fit, score or future input."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

STEMS=('run_BF16wide40_official_comparison','prepare_BF16wide40_selected_candidate','seal_BF16wide40_selected_candidate',
    'run_BF16wide40_round135_full_registration','verify_BF16wide40_round135_sources','publish_BF16wide40_evidence',
    'queue_BF16wide135_complete_pipeline')


def adapt(text):
    mapping={stem+'_v4_20261008':stem.replace('BF16wide40','BF16reverse40').replace('BF16wide135','BF16reverse138').replace('round135','round138')+'_v1_20261008' for stem in (*STEMS,'prepare_BF16wide40_round135_sources')}
    mapping.update({'BF16wide135_storage_v1_20261008':'BF16reverse138_storage_v1_20261008',
        'BF16wide135_D_scoring_v2_20261008':'BF16reverse138_D_scoring_v1_20261008',
        'BF16wide40_round135_plan_v1_20261008':'BF16reverse40_round138_plan_v1_20261008',
        'BF16_complete_parent_rank_CDF_v1_20261008':'BF16_reverse_complete_parent_rank_CDF_v1_20261008',
        'BF16_complete_parent_native_stage_v1_20261008':'BF16_reverse_complete_parent_native_stage_v1_20261008',
        'predict_BF16_complete_parent_rank_scheme_v1_20261008':'predict_BF16_reverse_complete_parent_scheme_v1_20261008',
        'BF16_complete_parent_rank_CDF':'BF16_reverse_complete_parent_rank_CDF',
        'BF16_complete_parent_native_replay_verification.json':'BF16_reverse_complete_parent_native_replay_verification.json',
        'passed_actual_complete_parent_and_BF16_two_full_native_independent_replays_and_cold80':'passed_actual_complete_parent_and_reverse_BF16_two_full_native_independent_replays_and_cold80',
        'actual_BF16_rank_CDF_full37_location_v1_20261008':'actual_BF16_reverse_rank_CDF_full37_location_v1_20261008',
        'actual_BF16_native_hook3_location_v1_20261008':'actual_BF16_reverse_native_hook3_location_v1_20261008',
        'BF16_complete_parent_actual_historical_native_hook3_v1_20261008':'BF16_reverse_complete_parent_actual_historical_native_hook3_v1_20261008',
        'passed_actual37_full5635800_BF16_rank_CDF_independent_and111_cold_controls':'passed_actual37_full5635800_reverse_BF16_CDF_independent_and111_cold_controls',
        'passed_actual3_historical_BF16_full_native_independent_CDF_and_whole_day_prefix_hooks':'passed_actual3_historical_reverse_BF16_native_independent_CDF_and_day_prefix_hooks',
        'nonflag_ReverseBayesFine40_round134_full_registration_v1':'Huber52_round137_full_registration_v3_20261008',
        'actual_BF16_independent_rank_controls_main_publication_v1_20261008':'reverse_BF16_plan_handoff_main_publication_v1_20261008',
        'BF16wide40_prospective_routes_v4_20261008':'BF16reverse40_prospective_routes_v1_20261008',
        'BF16wide135_receiver_preparation_v4_20261008':'BF16reverse138_receiver_preparation_v1_20261008',
        'BF16wide135_complete_dependency_plan_v4_20261008':'BF16reverse138_complete_dependency_plan_v1_20261008',
        'BF16wide135_complete_hidden_launches_v4_20261008':'BF16reverse138_complete_hidden_launches_v1_20261008',
        'BF16wide40':'BF16reverse40','BF16wide135':'BF16reverse138','round135':'round138','full135':'full138',
        'actual135':'actual138','prospective135':'prospective138','_r135':'_r138','qa46':'qa49','QA46':'QA49','qa_v46':'qa_v49',
        '第135轮':'第138轮','NUMBER = 135':'NUMBER = 138','number == 135':'number == 138',
        'WAVES = (418,)':'WAVES = (421,)','wave=418':'wave=421','wave418_results':'wave421_results',"'waves': [418]":"'waves': [421]",
        "'round':135":"'round':138","'round': 135":"'round': 138",'publish(135,':'publish(138,','lossless(135)':'lossless(138)',
        'collect(135, 46, 40)':'collect(138, 49, 40)',"namespace['snapshot'](135)":"namespace['snapshot'](138)",
        'actual_complete_QA_version=46':'actual_complete_QA_version=49',"actual_full_QA_version': 46":"actual_full_QA_version': 49"})
    for stem in ('BF16wide40_round135_source_admission','BF16wide40_round135_source_preparation','BF16wide40_controls_main_publication',
        'BF16wide40_scores_main_publication','BF16wide40_official_comparison','BF16wide40_selected_candidate_preparation',
        'BF16wide40_selected_candidate_sealing','BF16wide40_round135_full_registration'):
        mapping[stem+'_v4_20261008']=stem.replace('BF16wide40','BF16reverse40').replace('round135','round138')+'_v1_20261008'
    text=substitute(text,mapping)
    text=text.replace('(112,133,134)','(135,136,137)').replace('(112, 133, 134)','(135, 136, 137)')
    return text


def best_key(row):
    return (-row['connected_final_score'],row['expected_unique_native_models'],row['configuration']['weight'],row['case'])


def main():
    paths=[];originals=[]
    assert read(A/'BF16reverse40_round138_plan_v1_20261008.json')['expected_scored_records']==40
    for stem in STEMS:
        source=A/(stem+'_v4_20261008.py');text=adapt(source.read_text(encoding='utf8'));originals.append(source)
        if stem=='run_BF16wide40_official_comparison':
            text=text.replace('assert scheme_base==control[\'actual_parent_round\']==134',"assert scheme_base==control['actual_parent_round'] and scheme_base in (135,136,137)")
            needle="comparison_parent=min(parents,key=lambda n:(-baselines[n]['final_score'],n))";assert text.count(needle)==1
            text=text.replace(needle,"parent_models={n:read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json')['models'] for n in parents}\n    comparison_parent=min(parents,key=lambda n:(-baselines[n]['final_score'],len(parent_models[n]),n))")
            needle="    graph=read(ROOT/f'candidates/optimization_20261003_r{scheme_base}/verification.json')['whole_scheme_graph']";assert text.count(needle)==1
            text=text.replace(needle,"    final_info=read(Path(plan['actual_annual_bank'])/'2025/info.json');neural_sha=final_info['model_sha256']\n"+needle)
            needle="'first2020_active':cfg['model'] is not None and cfg['weight']>0.,";assert text.count(needle)==1
            text=text.replace(needle,"'expected_unique_native_models':len({m['sha256'] for m in parent_models[cfg['anchor_round']].values()} | ({neural_sha} if cfg['model'] is not None and cfg['weight']>0. else set())),\n                "+needle)
            text=text.replace("best=min(records,key=lambda r:(-r['connected_final_score'],r['configuration']['weight'],r['case']))","from prepare_BF16reverse138_complete_receivers_v1_20261008 import best_key\n    best=min(records,key=best_key)")
        elif stem=='prepare_BF16wide40_selected_candidate':
            text=text.replace("best=min(pilot['records'],key=lambda r:(-r['connected_final_score'],r['configuration']['weight'],r['case']))","from prepare_BF16reverse138_complete_receivers_v1_20261008 import best_key\n    best=min(pilot['records'],key=best_key)")
            text=text.replace("assert parent_number==134 and 0.<cfg['weight']<=1.","assert parent_number in (135,136,137) and 0.<cfg['weight']<=1.")
            needle="'rank_universe':cfg['universe'],'first2020_active':True";assert text.count(needle)==1
            text=text.replace(needle,"'rank_universe':cfg['universe'],'first2020_active':True,'signal_sign_on_valid_rows':-1.,'invalid_signal_bits_preserved':True")
            text=text.replace("[*parent_record['native_component_names'],cfg['model']]","[*parent_record['native_component_names'],*([cfg['model']] if component['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()} else [])]")
        elif stem=='verify_BF16wide40_round135_sources':
            text=text.replace("assert t['actual_parent_round']==134 and","assert t['actual_parent_round'] in (135,136,137) and")
        elif stem=='run_BF16wide40_round135_full_registration':
            text=text.replace('actual_registration_v4_20261008','actual_registration_v1_20261008').replace('registration_v4_file_IO_20261008','registration_v1_file_IO_20261008')
        target=A/(stem.replace('BF16wide40','BF16reverse40').replace('BF16wide135','BF16reverse138').replace('round135','round138')+'_v1_20261008.py')
        assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');paths.append(target)
    for old,new in (('BF16wide135_storage_v1_20261008.py','BF16reverse138_storage_v1_20261008.py'),
        ('verify_BF16wide135_D_scoring_scope_v2_20261008.py','verify_BF16reverse138_D_scoring_scope_v1_20261008.py')):
        source=A/old;originals.append(source);text=adapt(source.read_text(encoding='utf8'))
        text=text.replace('BF16reverse138_D_scoring_scope_v2_20261008','BF16reverse138_D_scoring_scope_v1_20261008')
        target=A/new;assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');paths.append(target)
    create(A/'BF16reverse138_receiver_drafts_v1_20261008.json',{'status':'prepared9_calendar_safe_reverse_neural_complete_receivers_before_quality',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*paths]},'new_fits':0,'new_quality_scores':0,'test_labels_read':False,
        'unique_model_SHA_union_sort_used':True,'complete_source_generator_and24_prospective_controls_still_required':True})
    from BF16reverse138_storage_v1_20261008 import OUTPUTS,EBASE
    create(A/'BF16reverse138_junction_requests_v1_20261008.json',{
        'workspace':str(ROOT),'E_base':str(EBASE),'requests':[{'logical':str(p),'target':str(t)} for p,t in OUTPUTS.items()]})
    print('Nine fresh reverse-neural receivers prepared; source generator and preflight remain before dispatch.',flush=True)


if __name__=='__main__':main()
