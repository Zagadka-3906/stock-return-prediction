"""Predeclare the complete125-case fine stage including freeze, two native replays, full QA56 and main."""
from pathlib import Path
import ast,io,json,re,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
FAMILY='CrossFamilyFine125'
def save(p,s):
    assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n')
def convert(s):
    mapping={
        'CrossFamily_complete_parent_CDF_v1_20261008':'CrossFamilyFine_complete_parent_CDF_v1_20261008',
        'CrossFamily_complete_parent_native_stage_v2_20261008':'CrossFamilyFine_complete_parent_native_stage_v1_20261008',
        'predict_CrossFamily_complete_parent_scheme_v2_20261008':'predict_CrossFamilyFine_complete_parent_scheme_v1_20261008',
        'CrossFamily94_round136_plan_v1_20261008':'CrossFamilyFine125_round145_plan_v2_20261008',
        'actual_CrossFamily91_current_parent_location_v2_20261008':'actual_CrossFamilyFine121_parent134_location_v1_20261008',
        'CrossFamily94_actual_controls_index_v4_20261008':'CrossFamilyFine125_actual_controls_index_v1_20261008',
        'CrossFamily94_actual_controls_index_v3_20261008':'CrossFamilyFine125_actual_controls_index_v1_20261008',
        'CrossFamily94_actual_controls_index_v1_20261008':'CrossFamilyFine125_actual_controls_index_v1_20261008',
        'CrossFamily94':'CrossFamilyFine125','CrossFamily136':'CrossFamilyFine145',
        'round136':'round145','full136':'full145','actual136':'actual145','prospective136':'prospective145','_r136':'_r145','第136轮':'第145轮',
        'qa47':'qa56','QA47':'QA56','qa_v47':'qa_v56','wave419':'wave428','wave=419':'wave=428','WAVES = (419,)':'WAVES = (428,)',
        "'waves': [419]":"'waves': [428]","'round':136":"'round':145","'round': 136":"'round': 145",'publish(136,':'publish(145,','lossless(136)':'lossless(145)',
        "namespace['snapshot'](136)":"namespace['snapshot'](145)",
        'actual_complete_QA_version=47':'actual_complete_QA_version=56',"actual_full_QA_version': 47":"actual_full_QA_version': 56",
        'passed_actual94':'passed_actual125','passed_exact_selected_anchor94':'passed_exact_selected_anchor125',
        'selected_by_all94':'selected_by_all125','all94':'all125','actual94':'actual125',
        'existing_saved_native_heads': 'existing_saved_native_heads'}
    for before,after in sorted(mapping.items(),key=lambda p:-len(p[0])):s=s.replace(before,after)
    # Receiver versions start fresh. Referenced native banks and unrelated proven runtimes retain their actual versions.
    s=re.sub(r'((?:prepare_|run_|verify_|seal_|publish_|queue_)?CrossFamilyFine(?:125|145)[A-Za-z_0-9]*?)_v\d+_20261008',r'\1_v1_20261008',s)
    s=s.replace('CrossFamilyFine125_round145_plan_v1_20261008','CrossFamilyFine125_round145_plan_v2_20261008')
    tokens=list(tokenize.generate_tokens(io.StringIO(s).readline))
    s=tokenize.untokenize([t._replace(string='125') if t.type==tokenize.NUMBER and t.string=='94' else t for t in tokens])
    return s
def main():
    proposal=A/'CrossFamilyFine125_round145_plan_v1_20261008.json';plan=read(proposal)
    plan.update({'status':'frozen125_case_grid_and_predeclared_absolute_amplitude_tie_rule_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'final_selection_rule':'official_S_desc_unique_physical_model_SHA_count_asc_absolute_amplitude_asc_case_asc',
        'comparison_parent_rule':'official_S_desc_unique_physical_model_SHA_count_asc_round_asc','prior_plan_sha256':sha(proposal)})
    plan['input_sha256'].update({str(Path(__file__)):sha(__file__),str(proposal):sha(proposal)})
    create(A/'CrossFamilyFine125_round145_plan_v2_20261008.json',plan)
    products={};originals=[]
    def product(old,name=None,adapt=None):
        old=A/old;originals.append(old);value=convert(old.read_text(encoding='utf8'))
        if adapt:value=adapt(value)
        target=A/(name or convert(old.name));products[target]=value;return value
    # Same-volume aliases keep large review and candidate artifacts on E; D is used only by original official cache guards.
    product('CrossFamily136_storage_v1_20261008.py','CrossFamilyFine145_storage_v1_20261008.py',lambda s:s.replace('number == 136','number == 145'))
    # Existing predictor's independent native path changes solely to the already controlled signed/finer codec.
    product('predict_CrossFamily_complete_parent_scheme_v2_20261008.py','predict_CrossFamilyFine_complete_parent_scheme_v1_20261008.py')
    product('verify_CrossFamily136_D_scoring_scope_v1_20261008.py','verify_CrossFamilyFine145_D_scoring_scope_v1_20261008.py')
    def scorer(s):
        s=s.replace("    closed('ConeRidgeAlpha100_round144_full_registration_v12_20261008')","    closed('KrylovGram52_round141_full_registration_v18_20261008')")
        s=s.replace("row['configuration']['weight'],row['case']","abs(row['configuration']['weight']),row['case']")
        s=s.replace("control['status']=='passed_actual91_current_parent_CrossFamily_CDF_and273_cold_controls' and control['final136_exact_current_parent_controls_fulfilled']", "control['status']=='passed_actual120_new_signed_full_CDF360_cold_controls_and_identity_on_exact134_parent' and control['actual_stage_base_round']==134")
        # convert() maps the old final136 label to final145 before this specialized replacement.
        s=s.replace("control['status']=='passed_actual91_current_parent_CrossFamily_CDF_and273_cold_controls' and control['final145_exact_current_parent_controls_fulfilled']", "control['status']=='passed_actual120_new_signed_full_CDF360_cold_controls_and_identity_on_exact134_parent' and control['actual_stage_base_round']==134")
        s=s.replace("    parent=min(parents,key=lambda n:(-baselines[n]['final_score'],len(predictions[n]['models']),n))", "    comparison_parent=min(parents,key=lambda n:(-baselines[n]['final_score'],len({r['sha256'] for r in predictions[n]['models'].values()}),n))\n    parent=134")
        s=s.replace("    assert parent==control['actual_comparison_parent_round']==control['actual_scheme_base_round'] and parent in (134,135)", "    assert parent==control['actual_stage_base_round']==plan['fixed_scientific_stage_base_round']")
        s=s.replace("'actual_comparison_parent_round':parent","'actual_comparison_parent_round':comparison_parent")
        s=s.replace("metrics['final_score']-baselines[parent]['final_score']","metrics['final_score']-baselines[comparison_parent]['final_score']")
        s=s.replace("'existing_saved_native_heads':30","'existing_saved_native_heads':20")
        s=s.replace("'all91_nonanchors_full_and_cold_controls_passed'","'all121_nonanchors_full_and363_cold_controls_passed'")
        s=s.replace("'components':{f'group{g}':[list(names) for names,sign in codec.GROUPS[g]] for g in range(5)}", "'components':{'group4':[list(names) for names,sign in codec.GROUPS[4]]}")
        s=s.replace('candidate_future_freeze_replays_QA56_and_main_pending','candidate_future_freeze_replays_QA56_and_main_pending')
        return s
    product('run_CrossFamily94_official_comparison_v5_20261008.py','run_CrossFamilyFine125_official_comparison_v1_20261008.py',scorer)
    def candidate(s):
        s=s.replace('parent_number in (112,134,135)','parent_number in (134,136,141,144)')
        s=s.replace("parent_number in (134,135) and 0.<cfg['weight']<=.1","parent_number==134 and 0.<abs(cfg['weight'])<=.00325")
        s=s.replace("freeze=A/'CrossFamilyFine125_pre_inference_source_freeze_v1_20261008'", "freeze=Path('E:/赛题五_本机临时/第145轮_20261008/pre_inference_source_freeze_v1')")
        s=s.replace('actual30_existing_native_and91_current_parent_controls','actual20_existing_native_and121_fixed_base_controls')
        s=s.replace("        graph=deepcopy(parent_prediction['whole_scheme_graph']);rebase_graph(graph)", "        graph=deepcopy(parent_prediction['whole_scheme_graph']);assert GRAPH_KEY not in graph;rebase_graph(graph)")
        return s
    product('prepare_CrossFamily94_selected_candidate_v5_20261008.py','prepare_CrossFamilyFine125_selected_candidate_v1_20261008.py',candidate)
    product('seal_CrossFamily94_selected_candidate_v5_20261008.py','seal_CrossFamilyFine125_selected_candidate_v1_20261008.py')
    # Use the unmodified generic full-registration path; the failed136 recovery is deliberately not copied.
    def full(s):
        s=s.replace('BF16reverse40','CrossFamilyFine125').replace('BF16reverse138_storage_v1_20261008','CrossFamilyFine145_storage_v1_20261008')
        s=s.replace('round138','round145').replace('full138','full145').replace('actual138','actual145').replace('_r138','_r145').replace('第138轮','第145轮').replace('QA49','QA56')
        s=re.sub(r'(CrossFamilyFine125[A-Za-z_0-9]*?)_v14_20261008',r'\1_v1_20261008',s)
        s=s.replace('run_CrossFamilyFine125_round145_full_registration_v14_file_IO_20261008','run_CrossFamilyFine125_round145_full_registration_v1_file_IO_20261008')
        s=s.replace('Huber52_round137_full_registration_v14_20261008','KrylovGram52_round141_full_registration_v18_20261008')
        s=s.replace('parent_number in (135,136,137)','parent_number in (134,136,141,144)')
        s=s.replace('publish(138,','publish(145,').replace('lossless(138)','lossless(145)').replace('lossless_ranking_runtime_adapter_round138_20261007','lossless_ranking_runtime_adapter_round145_20261007')
        s=s.replace('40','125') if False else s
        s=s.replace('passed_actual40_','passed_actual125_').replace('预定40项：三个合格锚点、36项宽网络融合、零权重恒等对照','预定125项：四个合格锚点、120项细权重重调、零权重恒等对照')
        s=s.replace("'existing_official_scores_registered':40","'existing_official_scores_registered':125")
        s=s.replace('完整父方案与BF16宽网络排序融合','完整父方案跨模型细权重重调')
        s=s.replace('from file_backed_hidden_git_runtime_20261007 import installed','from verified_TLS_Git_retry_runtime_v2_20261008 import installed')
        return s
    old=A/'run_BF16reverse40_round138_full_registration_v14_20261008.py';originals.append(old);products[A/'run_CrossFamilyFine125_round145_full_registration_v1_20261008.py']=full(old.read_text(encoding='utf8'))
    for name in ('build_lossless_ranking_display_round144_20261007.py','verify_lossless_ranking_display_round144_20261007.py','lossless_ranking_runtime_adapter_round144_20261007.py'):
        old=A/name;originals.append(old);value=old.read_text(encoding='utf8').replace('144','145').replace('qa_v55','qa_v56')
        value=value.replace('ConeRidgeAlpha145_storage_v6_20261008','CrossFamilyFine145_storage_v1_20261008')
        products[A/name.replace('144','145')]=value
    # Historical evidence publisher is adapted in a dedicated receiver, so it never assumes30 heads or91 controls.
    for p,v in products.items():save(p,v)
    create(A/'CrossFamilyFine145_receiver_drafts_v1_20261008.json',{'status':'prepared_physical_and_scientific145_receivers_before_prospective_checks_and_quality',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products,A/'CrossFamilyFine125_round145_plan_v2_20261008.json']},
        'official_cases':125,'stage_base_round':134,'qualified_anchors':[134,136,141,144],'qa_version':56,'wave':428,
        'new_quality_scores':0,'test_labels_read':False,'all_generated_registry_collector_source_and_admission_receivers_still_required':True})
    print(json.dumps({'prepared_source_files':len(products),'quality_not_admitted':True,'registry_and_prospective_checks_still_required':True}),flush=True)
if __name__=='__main__':main()
