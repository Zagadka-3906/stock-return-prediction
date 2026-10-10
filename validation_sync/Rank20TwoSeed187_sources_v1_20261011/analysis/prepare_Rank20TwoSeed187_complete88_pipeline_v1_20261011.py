"""Freeze the complete88 two-physical-model candidate, registry, QA98 and main flow."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_StockRank20Seed10Embedding186_complete48_pipeline_v2_20261011 as previous
FACTORY=Path(__file__).stem
NORMAL='normalize_completed_rank20_two_seed88_after186_v1_20261011'
QUAL='qualify_rank20_two_seed88_selected_native14_v1_20261011'
PRED='predict_rank20_two_seed_complete_qualified_parent_scheme_v1_20261011'
PLAN='rank20_two_seed_complete88_after186_plan_v1_20261011.json'
CALL='rank20_two_seed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
PROOF='rank20_two_seed187_full_execution_sources_admission_v1_20261011.json'

def base(text):
    text=text.replace('StockRank20Seed10Embedding186','Rank20TwoSeed187').replace('stock_rank20seed10_embedding186','rank20_two_seed187')
    text=text.replace('qa97','qa98').replace('QA97','QA98').replace('qa_v97','qa_v98').replace('17402','17490')
    return re.sub(r'(?<!\d)(186|185|469|97|48|44|132)(?!\d)',lambda m:{'186':'187','185':'186','469':'470','97':'98','48':'88','44':'84','132':'252'}[m.group()],text)

FILE_MAP={}
for old in [*previous.NAMES,*previous.EXTRAS[2:9]]:
    FILE_MAP[old]=re.sub(r'_v2_20261011\.py$','_v1_20261011.py',base(old))
for old,new in [(previous.EXTRAS[0],NORMAL+'.py'),(previous.EXTRAS[1],QUAL+'.py'),(previous.EXTRAS[12],PRED+'.py'),
    (previous.EXTRAS[11],PLAN),(previous.EXTRAS[13],CALL),
    (Path(previous.__file__).name,FACTORY+'.py'),
    (previous.EXTRAS[9],'rank20_two_seed187_candidate_sources_preparation_v1_20261011.json'),
    (previous.EXTRAS[10],'rank20_two_seed187_full_registry_sources_preparation_v1_20261011.json'),
    ('stock_rank20seed10_embedding186_full_family_preflight_v2_20261011.json','rank20_two_seed187_full_family_preflight_v1_20261011.json')]:FILE_MAP[old]=new

def route(text):
    text=text.replace('StockTopPairEmbedding185_complete48_family_v9_complete_references_v9_20261010','__ACTUAL_PREVIOUS_FAMILY_SERVICE__')
    mapping={**FILE_MAP,**{Path(k).stem:Path(v).stem for k,v in FILE_MAP.items() if k.endswith('.py')}}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=base(text)
    text=text.replace('__ACTUAL_PREVIOUS_FAMILY_SERVICE__','StockRank20Seed10Embedding186_complete48_family_v2_20261011')
    replacements={
        'StockRank20Seed10Embedding88_selected_native14_v1_20261011':'actual_rank20_two_seed88_selected_native14_v1_20261011',
        'actual_stock_rank20seed10_embedding88_selected_native14_location_v1_20261010.json':'actual_rank20_two_seed88_selected_native14_location_v1_20261011.json',
        'stock_rank20seed10_embedding88_selected_native14_v1_20261010':'rank20_two_seed88_selected_native14_v1_20261011',
        'stock_rank20seed10_embedding_complete88_after186_selection_plan_v1_20261011.json':PLAN,
        'passed_normalized88_actual_TRAIN_official_records_selected_stage_and_full_inference_pending':'passed_normalized88_actual_TRAIN_official_records_selected_native_and_full_future_pending',
        'passed_selected_fully_qualified_anchor88_no_new_native_stage_claimed':'passed_selected_fully_qualified_anchor88_no_new_native_stage_claimed',
        'stock_rank20seed10_embedding_complete_parent_native_replay_verification.json':'rank20_two_seed_complete_parent_native_replay_verification.json',
        'passed_actual_complete_qualified_parent_stock_rank20seed10_embedding_two_full_native_independent_replays_and_cold80':'passed_actual_complete175_two_seed_two_full_native_independent_scalar_mix_and_cold80',
    }
    for old,new in replacements.items():text=text.replace(old,new)
    return text

NAMES=[FILE_MAP[n] for n in previous.NAMES]
EXTRAS=[NORMAL+'.py',QUAL+'.py',*[FILE_MAP[n] for n in previous.EXTRAS[2:14]]]
EXTRAS += ['rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py',
    'rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011.py',
    'rank20_two_seed_raw_signal_v1_20261010.py','rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json',
    'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json',
    'rank20_two_seed_complete88_normalization_native14_sources_admission_v1_20261011.json',
    'exact_verified_feature120_memoization_runtime_v1_20261010.py','actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json']

def source_paths():return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS]]))

def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old));return text.replace(old,new)

def candidate(text):
    text=once(text,'    import stock_rank20seed10_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as native_stage',
        '    import rank20_two_seed_after_qualified_parent_native_stage_v1_20261010 as cdf_stage\n    import rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011 as protected_stage')
    text=once(text,"GRAPH_KEY='stock_rank20seed10_embedding_after_complete_qualified_parent_v1_20261010'","GRAPH_KEY=None  # Selected exact codec chooses its frozen graph key inside main.")
    text=once(text,"    comparison_parent=pilot['actual_comparison_parent_round']","    native_stage=cdf_stage if cfg['codec']=='CDF' else protected_stage\n    GRAPH_KEY=native_stage.GRAPH_KEY\n    comparison_parent=pilot['actual_comparison_parent_round']")
    text=text.replace("A/'stock_rank20seed10_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py'","Path(cdf_stage.__file__),Path(protected_stage.__file__)")
    start=text.index('    from '+NORMAL+' import RECIPES');end=text.index('    freeze=Path(',start)
    text=text[:start]+"""    assert parent_number==175 and cfg['recipe']==cdf_stage.RECIPE
    import rank20_two_seed_raw_signal_v1_20261010 as mixing
    codecs={'CDF':'BF16Medium153_complete_parent_rank_CDF_v1_20261009','valid_pool_protection_v1':'protected_upper_tail_rank_permutation_v1_20261010','official_Top_protection_v2':'protected_official_top_rank_permutation_v2_20261010'}
    transform=importlib.import_module(codecs[cfg['codec']]).transform
    leaves=best['native_bank_components'];assert len(leaves)==2
    members=[]
    for i,leaf in enumerate(leaves):
        bank=Path(leaf['bank']);info=read(bank/'2025/info.json');meta=info['training_meta']
        native=importlib.import_module(native_stage.BACKENDS[cfg['recipe']][2*i]);CONFIG=native.CONFIG
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and info['year']==2025
        assert info['configuration']==CONFIG and CONFIG['seed']==(20261009,20261010)[i]
        assert meta['last']<meta['cutoff_exclusive']==fold_cutoff(2025) and meta['last_label_end']<meta['cutoff_exclusive']
        member={'name':leaf['name'],'source_path':str(bank/'2025/model.joblib'),'path':str(CANDIDATE/(leaf['name']+'_final2025.joblib')),
            'sha256':info['model_sha256'],'configuration':CONFIG,'training_info':info}
        assert sha(member['source_path'])==member['sha256'];pins[member['source_path']]=member['sha256'];members.append(member)
    assert members[0]['sha256']!=members[1]['sha256']
    component={'seed_components':members}
"""+text[end:]
    start=text.index('    # Resolve saved raw-panel locations');end=text.index('    with LockedReadHashCache(pins)',start)
    text=text[:start]+"""    own_pointers=[A/'actual_StockRank20EmbeddingSmall512_full5_independent_location_v1_20261009.json',A/'actual_StockRank20Seed10EmbeddingSmall512_full5_independent_location_v1_20261009.json']
    neural_folders=[Path(read(p)['output']) for p in own_pointers];neural_paths=[p/'combined_raw.parquet' for p in neural_folders]
    pins.update({str(p):sha(p) for p in [raw_path,*own_pointers,*neural_paths,Path(mixing.__file__)]})
"""+text[end:]
    start=text.index('        neural_frame=pl.read_parquet(');end=text.index('\n        selected=transform(',start)
    text=text[:start]+"""        neural_frames=[pl.read_parquet(p) for p in neural_paths]
        assert all(p.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date'])) for p in neural_frames)
        raw=np.load(raw_path,mmap_mode='r')
        neural=mixing.combine(*[p['pred_raw'].to_numpy() for p in neural_frames],cfg['second_seed_weight'])
        independent=mixing.scalar_oracle(*[p['pred_raw'].to_numpy() for p in neural_frames],cfg['second_seed_weight'])
        assert np.array_equal(neural.view('u8'),independent.view('u8'));del independent
        assert cfg['stage_kind'] in ('rank20_two_seed_raw_average','rank20_two_seed_raw_average_protected_tail') and cfg['decay'] is None
"""+text[end:]
    text=text.replace("str(neural_folder/'verification.json')","[str(p/'verification.json') for p in neural_folders]")
    text=text.replace("'actual6_mature_native_and_full_independent_controls'","'actual12_mature_native_and_full_independent_controls'")
    text=text.replace("native_stage.CODECS[cfg['codec']]","codecs[cfg['codec']]")
    text=once(text,"|{component['sha256']}","|{m['sha256'] for m in members}")
    old="*([cfg['model']] if component['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()} else [])"
    text=once(text,old,"*[member['name'] for member in members if member['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()}]")
    return text

def main():
    assert allowed();assert len(read(A/CALL)['records'])==11
    for n in [NORMAL+'.py',QUAL+'.py',PRED+'.py',PLAN,CALL]:assert (A/n).is_file(),n
    inputs=[A/n for n in [*previous.NAMES,*previous.EXTRAS[2:9]]];outputs=[]
    for p in inputs:
        text=route(p.read_text(encoding='utf8'))
        if p.name==previous.EXTRAS[3]:text=candidate(text)
        if p.name==previous.NAMES[0]:
            text=once(text,'            from stock_rank20seed10_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY',
                "            from rank20_two_seed_after_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as CDF_KEY\n            from rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011 import GRAPH_KEY as PROTECTED_KEY\n            GRAPH_KEY=CDF_KEY if cfg['codec']=='CDF' else PROTECTED_KEY")
            text=once(text,"assert len(measured['ordered_native_components'])==1","assert len(measured['ordered_native_components'])==2")
        if p.name==previous.EXTRAS[7]:
            text=text.replace('passed_selected_protected_tail_six_states14_native_and14_cold_and7_prefit_rejections','passed_selected_two_seed88_six_pairs14_native14_cold7_prefit_refusals')
            text=once(text,"(len(control['records']),control['actual_historical_cases'],control['actual_calendar_cases'],control['actual_cold_cases'])==(14,10,4,14)",
                "(len(control['records']),control['actual_native_cases'],control['actual_cold_cases'])==(14,14,14)")
            text=once(text,"control['actual_saved_states']==6","control['actual_saved_states']==12")
        target=A/FILE_MAP[p.name];assert not target.exists(),target
        compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    imports=[];literals=[]
    for p in outputs:
        for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
            if isinstance(node,ast.ImportFrom) and node.module and ('187' in node.module or node.module.startswith(('rank20_two_seed','normalize_completed_rank20_two_seed','qualify_rank20_two_seed','predict_rank20_two_seed'))):
                dep=A/(node.module+'.py');assert dep.is_file(),(p.name,node.module);imports.append({'source':p.name,'module':node.module,'sha256':sha(dep)})
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith('.py') and '/' not in node.value and '\\' not in node.value and ('187' in node.value or 'rank20_two_seed' in node.value):
                dep=A/node.value;assert dep.is_file(),(p.name,node.value);literals.append({'source':p.name,'path':node.value,'sha256':sha(dep)})
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(187,186,(470,))
    assert '(187, 98, 88)' in (A/NAMES[-1]).read_text(encoding='utf8')
    storage=importlib.import_module(Path(EXTRAS[2]).stem)
    assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,*[A/n for n in EXTRAS if n not in EXTRAS[9:11]]]}
    for n in EXTRAS[9:11]:create(A/n,{'status':'compiled_exact88_two_seed_QA98_before_future_dispatch','input_sha256':pins,
        'expected_records':88,'expected_full_board':17490,'parent_rounds':[175,186],'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    assert all(p.is_file() for p in source_paths())
    proof=A/PROOF
    create(proof,{'status':'compiled_complete88_two_physical_seed_models_QA98_CPU11_and_exact_sources_before_future',
        'input_sha256':pins,'direct_import_checks':imports,'literal_source_checks':literals,'actual_callback_CPU_count':11,
        'expected_records':88,'expected_full_board':17490,'actual_models_per_nonidentity_signal':2,'parent_rounds':[175,186],
        'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    assert allowed();name='Rank20TwoSeed187_complete88_family_v1_20261011';driver=EXTRAS[5]
    row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(proof):sha(proof)})
    create(A/(name+'_activation.json'),row)
    print({'complete187_two_seed88_QA98_queued':True,'new_scores':0,'future_qualification_pending':True},flush=True)

if __name__=='__main__':main()
