"""Build fresh94-case selected inference, sealing, full QA47, publication and dispatch sources before scoring."""
from pathlib import Path
import io,sys,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def family(text):
    stems=('prepare_BF16wide40_round135_sources','prepare_BF16wide40_selected_candidate','seal_BF16wide40_selected_candidate',
        'run_BF16wide40_round135_full_registration','verify_BF16wide40_round135_sources','publish_BF16wide40_evidence','run_BF16wide40_official_comparison')
    files={stem+'_v4_20261008':stem.replace('BF16wide40','CrossFamily94').replace('round135','round136')+'_v1_20261008' for stem in stems}
    for stem in ('BF16wide40_round135_source_admission','BF16wide40_selected_candidate_preparation','BF16wide40_selected_candidate_sealing',
        'BF16wide40_controls_main_publication','BF16wide40_scores_main_publication','BF16wide40_official_comparison'):
        files[stem+'_v4_20261008']=stem.replace('BF16wide40','CrossFamily94').replace('round135','round136')+'_v1_20261008'
    mapping={**files,'BF16wide135_storage_v1_20261008':'CrossFamily136_storage_v1_20261008',
        'BF16wide40':'CrossFamily94','第135轮':'第136轮','round135':'round136','full135':'full136','actual135':'actual136','_r135':'_r136',
        'qa46':'qa47','QA46':'QA47','qa_v46':'qa_v47','publish(135,':'publish(136,','lossless(135)':'lossless(136)',
        'passed_actual40_BF16_complete_parent_rank_CDF_full_official_comparisons':'passed_actual94_CrossFamily_complete_parent_full_official_comparisons',
        'passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual94_selected_candidate_full_graph_and_metrics_and_source_bytes',
        'passed_actual40_sealed_candidate_and_admitted_full135_QA46_sources':'passed_actual94_sealed_candidate_and_admitted_full136_QA47_sources',
        'passed_exact_selected_anchor40_candidate_reuse':'passed_exact_selected_anchor94_candidate_reuse',
        'predict_BF16_complete_parent_rank_scheme_v1_20261008':'predict_CrossFamily_complete_parent_scheme_v1_20261008',
        'BF16_complete_parent_native_replay_verification.json':'CrossFamily_complete_parent_native_replay_verification.json',
        'passed_actual_complete_parent_and_BF16_two_full_native_independent_replays_and_cold80':'passed_actual_complete_parent_and_CrossFamily_two_full_native_independent_replays_and_cold80'}
    value=substitute(text,mapping)
    tokens=list(tokenize.generate_tokens(io.StringIO(value).readline))
    value=tokenize.untokenize([token._replace(string='94') if token.type==tokenize.NUMBER and token.string=='40' else token for token in tokens])
    value=value.replace('(112,133,134)','(112,134,135)').replace('(112, 133, 134)','(112, 134, 135)')
    value=value.replace('BF16wide135_D_scoring_v2_20261008','CrossFamily136_D_scoring_v1_20261008')
    return value


def main():
    originals={stem:A/(stem+'_v4_20261008.py') for stem in ('prepare_BF16wide40_selected_candidate','seal_BF16wide40_selected_candidate',
        'run_BF16wide40_round135_full_registration','publish_BF16wide40_evidence')}
    outputs={}
    prep=family(originals['prepare_BF16wide40_selected_candidate'].read_text(encoding='utf8'))
    prep=prep.replace("GRAPH_KEY='BF16_complete_parent_rank_CDF'","GRAPH_KEY='nonflag_CPU_CrossFamily_complete_parent_CDF'")
    prep=prep.replace('    from BF16_complete_parent_rank_CDF_v1_20261008 import transform\n    from neural_BF16_micro8192_native_v1_20261008 import CONFIG',
        '    from CrossFamily_complete_parent_CDF_v1_20261008 import transform,mixture,GROUPS\n    from run_CrossFamily94_official_comparison_v1_20261008 import best_key')
    old="best=min(pilot['records'],key=lambda r:(-r['connected_final_score'],r['configuration']['weight'],r['case']))"
    assert prep.count(old)==1;prep=prep.replace(old,"best=min(pilot['records'],key=best_key)")
    start=prep.index('    assert parent_number==134 and');end=prep.index('    freeze=',start)
    prep=prep[:start]+'''    assert parent_number in (134,135) and 0.<cfg['weight']<=.1
    plan=read(A/'CrossFamily94_round136_plan_v1_20261008.json')
    components=[]
    for head in dict.fromkeys(h for names,sign in GROUPS[cfg['group']] for h in names):
        row=plan['heads'][head];info_path=Path(row['infos']['2025']);info=read(info_path);kind=row['state_kind']
        assert info['year']==2025 and info['last_training_label_date']<info['exclusive_cutoff']==fold_cutoff(2025) and info['last_training_label_end']<=info['exclusive_cutoff']
        component={'head':head,'name':info['name'],'state_kind':kind,'source_path':info['native_model_path'],
            'path':str(CANDIDATE/(info['name']+'.joblib')),'sha256':info['native_model_sha256'],
            'independent_state_source_path':info['independent_'+kind+'_state_path'],
            'independent_state_path':str(CANDIDATE/(info['name']+'.json')),
            'independent_state_sha256':info['independent_'+kind+'_state_sha256'],'training_info':info}
        for path,digest in ((component['source_path'],component['sha256']),(component['independent_state_source_path'],component['independent_state_sha256'])):
            assert sha(path)==digest; pins[path]=digest
        pins[str(info_path)]=sha(info_path);components.append(component)
    assert [component['head'] for component in components]==best['ordered_native_components']
''' +prep[end:]
    start=prep.index('    neural_folder=');end=prep.index('    with LockedReadHashCache(pins)',start)
    prep=prep[:start]+'''    raw_paths={h:Path(row['oof']) for h,row in plan['heads'].items()}
    pins.update({str(path):sha(path) for path in [raw_path,*raw_paths.values()]})
''' +prep[end:]
    start=prep.index('        neural_frame=');end=prep.index("        assert hashlib.sha256",start)
    prep=prep[:start]+'''        raw=np.load(raw_path,mmap_mode='r')
        arrays={h:np.load(path,mmap_mode='r') for h,path in raw_paths.items()}
        residual=mixture(arrays,cfg['group'],cfg['share'])
        selected=transform(raw,residual,dates,flags,valid,cfg['weight'])
''' +prep[end:]
    prep=prep.replace("'actual6_mature_native_and_full_independent_controls':str(neural_folder/'verification.json')",
        "'actual30_existing_native_and91_current_parent_controls':str(A/'CrossFamily94_actual_controls_index_v1_20261008.json')")
    prep=prep.replace("'actual_all40_official_controls'","'actual_all94_official_controls'")
    start=prep.index("        graph[GRAPH_KEY]=");end=prep.index('        winner=',start)
    prep=prep[:start]+'''        graph[GRAPH_KEY]={**cfg,'amplitude':cfg['weight'],'universe':cfg['universe'],'first2020_identity':True,
            'position':'after_complete_qualified_parent','ordered_native_components':components,
            'teacher_feature':'qualified106_current_forecast_average_rank_over_N',
            'transformation':'inverseCDF_complete_parent(parent_day_average_rank_over_N+amplitude*ordered_signed_nested_residual_mixture)',
            'original_complete_parent_round':parent_number,'original_complete_parent_graph_preserved':True}
''' +prep[end:]
    prep=prep.replace("|{component['sha256']}","|{component['sha256'] for component in components}")
    prep=prep.replace("[*parent_record['native_component_names'],cfg['model']]","[*parent_record['native_component_names'],*[component['name'] for component in components]]")
    prep=prep.replace('        selection={',"        assert len(unique)==best['expected_unique_native_models']\n        selection={")
    assert 'neural_folder' not in prep and 'BF16_complete_parent_rank_CDF_v1' not in prep
    outputs[A/'prepare_CrossFamily94_selected_candidate_v1_20261008.py']=prep
    seal=family(originals['seal_BF16wide40_selected_candidate'].read_text(encoding='utf8'))
    outputs[A/'seal_CrossFamily94_selected_candidate_v1_20261008.py']=seal
    full=family(originals['run_BF16wide40_round135_full_registration'].read_text(encoding='utf8'))
    full=full.replace("'nonflag_ReverseBayesFine40_round134_full_registration_v1'","'BF16wide40_round135_full_registration_v4_20261008'")
    full=full.replace('CrossFamily94_round135_source_preparation_v4_20261008','CrossFamily94_round136_source_preparation_v1_20261008')
    full=full.replace('CrossFamily94_round136_source_preparation_v4_20261008','CrossFamily94_round136_source_preparation_v1_20261008')
    full=full.replace('CrossFamily94_round136_actual_registration_v3_20261008','CrossFamily94_round136_actual_registration_v1_20261008')
    full=full.replace('CrossFamily94_round136_actual_registration_v4_20261008','CrossFamily94_round136_actual_registration_v1_20261008')
    full=full.replace('run_CrossFamily94_round136_full_registration_v4_file_IO_20261008','run_CrossFamily94_round136_full_registration_v1_file_IO_20261008')
    full=full.replace('run_CrossFamily94_round136_full_registration_v3_file_IO_20261008','run_CrossFamily94_round136_full_registration_v1_file_IO_20261008')
    full=full.replace("'完整父方案与BF16宽网络排序融合'","'完整父方案的跨模型残差集成'")
    full=full.replace("'预定40项：三个合格锚点、36项宽网络融合、零权重恒等对照'","'预定94项：三个合格锚点、90项跨模型组合、零幅度恒等对照'")
    outputs[A/'run_CrossFamily94_round136_full_registration_v1_20261008.py']=full
    pub=family(originals['publish_BF16wide40_evidence'].read_text(encoding='utf8'))
    pub=pub.replace("closed('nonflag_ReverseBayesFine40_round134_full_registration_v1')","closed('BF16wide40_round135_full_registration_v4_20261008')")
    pub=pub.replace("'BF16_complete_parent_actual_historical_native_hook3_v1_20261008' if phase=='controls'","'CrossFamily91_current_parent_controls_v1_20261008' if phase=='controls'")
    start=pub.index('    index=read(');end=pub.index('    best=None',start)
    pub=pub[:start]+'''    index=read(A/'CrossFamily94_actual_controls_index_v1_20261008.json')
    assert index['status']=='passed_actual30_heads91_current_CDF273cold15_historical_native_hooks'
    for path,digest in index['input_sha256'].items():assert sha(path)==digest,path
    sources += [Path(path) for path in index['original_external_metadata']]
    for pointer in ('actual_CrossFamily_bank30_synthetic_location_v1_20261008.json',
        'actual_CrossFamily91_current_parent_location_v1_20261008.json','actual_CrossFamily15_native_hooks_location_v1_20261008.json'):
        folder=Path(read(A/pointer)['output']);sources += list(folder.glob('*.json'))
    sources += list(science.glob('*.json'))+list(science.glob('*.log'))
''' +pub[end:]
    pub=pub.replace("'actual_complete_bank_fits':6","'actual_existing_native_head_audits':30")
    pub=pub.replace("'actual_full_GPU_rows':5635800","'actual_full_native_OOF_heads':6")
    pub=pub.replace("'actual_full_CDF_controls':37","'actual_full_CDF_controls':91").replace("'actual_cold_CDF_controls':111","'actual_cold_CDF_controls':273").replace("'actual_historical_native_hooks':3","'actual_historical_native_hooks':15")
    pub=pub.replace('BF16宽网络实际证据','跨模型集成实际证据')
    outputs[A/'publish_CrossFamily94_evidence_v1_20261008.py']=pub
    for path,text in outputs.items():assert not path.exists();compile(text,str(path),'exec')
    for path,text in outputs.items():path.write_text(text,encoding='utf8',newline='\n')
    create(A/'CrossFamily136_receiver_draft_sources_v1_20261008.json',{'status':'prepared_fresh136_selected_seal_full_and_evidence_drafts_before_scoring',
        'input_sha256':{str(path):sha(path) for path in [Path(__file__),*originals.values(),*outputs]},'actual_new_quality_scores':0,'prospective24_routes_still_required':True})
    print('Four fresh136 scientific receivers compiled;24 prospective controls still required before quality.',flush=True)


if __name__=='__main__':main()
