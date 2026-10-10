"""Freeze complete149 mixed-objective/window candidates, registry, QA100 and verified main."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_Rank20TwoSeed187_complete88_pipeline_v2_20261011 as previous
NORMAL='normalize_completed_three_cached_mixed149_after188_v1_20261011'
QUAL='qualify_three_cached_mixed149_selected_native14_v1_20261011'
PRED='predict_three_cached_mixed_complete_qualified_parent_scheme_v2_20261011'
PLAN='three_cached_mixed_complete149_after188_plan_v1_20261011.json'
CALL='three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011.json'
FACTORY=Path(__file__).stem
PROOF='mixed_objective_window189_full_execution_sources_admission_v2_20261011.json'

def base(text):
    text=text.replace('Rank20TwoSeed187','MixedObjectiveWindow189').replace('rank20_two_seed187','mixed_objective_window189')
    for old,new in [('wave470','wave472'),('qualified186','qualified188'),('round187','round189'),('round186','round188'),('_r187','_r189'),('_r186','_r188'),('第187轮','第189轮'),('qa98','qa100'),('QA98','QA100'),('qa_v98','qa_v100'),('17490','17687')]:text=text.replace(old,new)
    for prefix in ['complete','full','anchor','normalized','all','actual','exact','selected']:
        text=text.replace(prefix+'88',prefix+'149')
    text=text.replace('pilot88','pilot149')
    text=re.sub(r'(?<![A-Za-z0-9_])(187|186|470|98|88|84)(?![A-Za-z0-9_])',lambda m:{'187':'189','186':'188','470':'472','98':'100','88':'149','84':'144'}[m.group()],text)
    text=text.replace('(144,252)','(144,432)').replace('(144, 252)','(144, 432)')
    return text

FILE_MAP={}
for old in [*previous.NAMES,*previous.EXTRAS[2:9]]:
    FILE_MAP[old]=re.sub(r'_v2_20261011\.py$','_v2_20261011.py',base(old))
for old,new in [(previous.EXTRAS[0],NORMAL+'.py'),(previous.EXTRAS[1],QUAL+'.py'),(previous.EXTRAS[12],PRED+'.py'),(previous.EXTRAS[11],PLAN),(previous.EXTRAS[13],CALL),(Path(previous.__file__).name,FACTORY+'.py'),(previous.EXTRAS[9],'mixed_objective_window189_candidate_sources_preparation_v2_20261011.json'),(previous.EXTRAS[10],'mixed_objective_window189_full_registry_sources_preparation_v2_20261011.json'),('rank20_two_seed187_full_family_preflight_v2_20261011.json','mixed_objective_window189_full_family_preflight_v2_20261011.json')]:FILE_MAP[old]=new
NAMES=[FILE_MAP[n] for n in previous.NAMES]
EXTRAS=[NORMAL+'.py',QUAL+'.py',*[FILE_MAP[n] for n in previous.EXTRAS[2:14]]]
EXTRAS += ['rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011.py','rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011.py','rank20_short_long_after_qualified_parent_native_stage_v1_20261011.py','rank20_two_seed_raw_signal_v1_20261010.py','rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json','three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011.json','three_cached_mixed149_normalization_native14_sources_admission_v1_20261011.json','exact_verified_feature120_memoization_runtime_v1_20261010.py','actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json','start_fast_completed_owned_service_v1_20261011.py']
def source_paths():return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS]]))
def once(text,old,new):assert text.count(old)==1,(old,text.count(old));return text.replace(old,new)
def route(text):
    mapping={**FILE_MAP,**{Path(k).stem:Path(v).stem for k,v in FILE_MAP.items() if k.endswith('.py')}}
    placeholders={k:'__EXACT_189_SOURCE_'+str(i)+'__' for i,k in enumerate(mapping)}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:placeholders[m.group()],text)
    text=base(text)
    for key,placeholder in placeholders.items():text=text.replace(placeholder,mapping[key])
    routes=read(A/'complete180_registered_continuation_routes_v13_20261011.json')
    parent=routes['service_aliases']['StockRank20LongEmbedding188_complete48_family_v1_20261011']
    text=text.replace('StockRank20Seed10Embedding186_complete48_family_v2_20261011',parent)
    text=text.replace('actual_rank20_two_seed88_selected_native14_v1_20261011','actual_three_cached_mixed149_selected_native14_v1_20261011')
    text=text.replace('actual_rank20_two_seed88_selected_native14_location_v1_20261011.json','actual_three_cached_mixed149_selected_native14_location_v1_20261011.json')
    text=text.replace('rank20_two_seed88_selected_native14_v1_20261011','three_cached_mixed149_selected_native14_v1_20261011')
    text=text.replace('passed_selected_two_seed88_six_pairs14_native14_cold7_prefit_refusals','passed_selected_three_cached_mixed149_six_pairs14_native14_cold7_prefit_refusals')
    text=text.replace('rank20_two_seed_complete_parent_native_replay_verification.json','rank5_rank20_mixed_complete_parent_native_replay_verification.json')
    text=text.replace('passed_actual_complete175_two_seed_two_full_native_independent_scalar_mix_and_cold80','passed_actual_complete175_mixed_horizon_two_full_native_independent_scalar_mix_and_cold80')
    text=text.replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
    return text
def candidate(text):
    text=once(text,'    import rank20_two_seed_after_qualified_parent_native_stage_v1_20261010 as cdf_stage\n    import rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011 as protected_stage', '    import rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011 as cdf_stage\n    import rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011 as near_stage\n    import rank20_short_long_after_qualified_parent_native_stage_v1_20261011 as window_stage')
    text=once(text,"    native_stage=cdf_stage if cfg['codec']=='CDF' else protected_stage", "    native_stage=importlib.import_module(best['native_stage_module']) if cfg['model'] is not None else cdf_stage\n    mix_field='long504_weight' if native_stage is window_stage else 'rank5_weight'")
    text=text.replace('Path(cdf_stage.__file__),Path(protected_stage.__file__)','Path(cdf_stage.__file__),Path(near_stage.__file__),Path(window_stage.__file__)')
    text=text.replace("cfg['recipe']==cdf_stage.RECIPE","cfg['recipe']==native_stage.RECIPE")
    text=text.replace("CONFIG['seed']==(20261009,20261010)[i]","CONFIG['seed']==20261009\n        assert CONFIG['label_horizon_trading_days']==leaf['label_horizon_trading_days']\n        assert CONFIG['training_calendar_window']==leaf['training_calendar_window']")
    text=text.replace('seed_components','horizon_components').replace("cfg['second_seed_weight']","cfg[mix_field]")
    old="    own_pointers=[A/'actual_StockRank20EmbeddingSmall512_full5_independent_location_v1_20261009.json',A/'actual_StockRank20Seed10EmbeddingSmall512_full5_independent_location_v1_20261009.json']"
    new="    own_pointer_by_bank={'stock_rank20_embedding_small512_BF16_bank6_v1_20261010':'actual_StockRank20EmbeddingSmall512_full5_independent_location_v1_20261009.json','stock_rank5_embedding_small512_BF16_bank6_v1_20261010':'actual_StockRank5EmbeddingSmall512_full5_independent_location_v1_20261009.json','stock_rank20long_embedding_small512_BF16_bank6_v1_20261010':'actual_StockRank20LongEmbeddingSmall512_full5_independent_location_v1_20261009.json'}\n    own_pointers=[A/own_pointer_by_bank[Path(leaf['bank']).name] for leaf in leaves]"
    text=once(text,old,new)
    text=text.replace("cfg['stage_kind'] in ('rank20_two_seed_raw_average','rank20_two_seed_raw_average_protected_tail')", "cfg['stage_kind'] in ('rank5_rank20_mixed_raw_average','rank20_short_long_mixed_raw_average')")
    text=text.replace("'transformation':'per-day protected-tail parent-value permutation by mature neural ranks; official_Top_v2 additionally applies documented oneULP cutoff-tie lift'", "'transformation':'per-day CDF perturbation of whole qualified175 by the independently matured two-model raw average'")
    return text
def main():
    assert allowed();assert len(read(A/CALL)['records'])==11
    assert read(A/PLAN)['expected_records']==149
    helper=A/'start_fast_completed_owned_service_v1_20261011.py'
    if not helper.exists():
        helper.write_text("from pathlib import Path\nfrom handoff_ready_goss_full_execution_20261006 import start_service as original\nfrom run_dependency_queue_v3_20261006 import read\nA=Path(__file__).resolve().parent\ndef start_service(name,driver,args,pins):\n try:return original(name,driver,args,pins)\n except AssertionError:\n  f=A/'service_owned_workflows_20261006'/name\n  if (f/'service_execution.json').exists() and read(f/'service_execution.json')['status']=='passed':return read(f/'native_launch.json')\n  raise\n",encoding='utf8',newline='\n')
    inputs=[A/n for n in [*previous.NAMES,*previous.EXTRAS[2:9]]];outputs=[]
    for source in inputs:
        text=route(source.read_text(encoding='utf8'))
        if source.name==previous.EXTRAS[3]:text=candidate(text)
        if source.name==previous.NAMES[0]:
            start=text.index('            from rank20_two_seed_after_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as CDF_KEY');end=text.index('            assert GRAPH_KEY not in graph',start)
            text=text[:start]+"            import importlib\n            GRAPH_KEY=importlib.import_module(measured['native_stage_module']).GRAPH_KEY\n"+text[end:]
            text=text.replace("[str(Path('E:/赛题五_本机临时')/(f['name']+'_screen_v1_20261010')/'frozen_before_any_new_controls_or_scores.json') for f in read(A/"+repr(PLAN)+")[\'families\']]", "[str(Path(f['output'])/'frozen_before_any_new_controls_or_scores.json') for f in read(A/"+repr(PLAN)+")[\'families\']]")
        if source.name==previous.NAMES[0]:
            text=text.replace("'existing_own_stock_rank20_rank_Huber_native_bank_fits': 6", "'existing_own_cached_mixed_native_bank_fits': 18, 'physical_models_per_selected_signal': 2")
            text=text.replace("['rank20_rank_tiny_and_protected17','rank20_rank_large29','qualified175','qualified188']", "['mixed_horizon49','near_pure49','mixed_window49','qualified175','qualified188']")
            text=text.replace('actual6_BF16_wide_native_bank_source','actual_selected_mixed_native_qualification_source')
        if source.name==previous.EXTRAS[5]:text=text.replace('from handoff_ready_goss_full_execution_20261006 import start_service','from start_fast_completed_owned_service_v1_20261011 import start_service')
        if source.name==previous.EXTRAS[6]:
            text=text.replace("['实际17项保护及29项大权重融合与完整175和188锚点；连续官方S优先']","['实际三组49项跨目标、小比例和跨窗口融合；完整175/188锚点，连续官方S优先']")
        target=A/FILE_MAP[source.name];assert not target.exists(),target;compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    aliases=[]
    for filename in NAMES[2:4]:
        source=A/filename;canonical=re.sub(r'_v2_20261011(?=\.py$)','',filename);target=A/canonical
        assert target.exists()
        old_functions=[ast.dump(n,include_attributes=False) for n in ast.parse(target.read_text(encoding='utf8')).body if isinstance(n,ast.FunctionDef)]
        new_functions=[ast.dump(n,include_attributes=False) for n in ast.parse(source.read_text(encoding='utf8')).body if isinstance(n,ast.FunctionDef)]
        assert old_functions==new_functions,(filename,canonical)
        aliases.extend([target,A/filename.replace('_v2_20261011.py','_v1_20261011.py')])
    imports=[];literals=[]
    for source in outputs:
        for node in ast.walk(ast.parse(source.read_text(encoding='utf8'))):
            if isinstance(node,ast.ImportFrom) and node.module and ('189' in node.module or node.module.startswith(('three_cached_mixed','normalize_completed_three','qualify_three','predict_three'))):
                p=A/(node.module+'.py');assert p.is_file(),(source.name,node.module);imports.append({'source':source.name,'module':node.module,'sha256':sha(p)})
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith('.py') and '/' not in node.value and '\\' not in node.value and ('189' in node.value or 'three_cached_mixed' in node.value):
                p=A/node.value;assert p.is_file(),(source.name,node.value);literals.append({'source':source.name,'path':node.value,'sha256':sha(p)})
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(189,188,(472,))
    assert '(189, 100, 149)' in (A/NAMES[-1]).read_text(encoding='utf8')
    storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
    for source in outputs:
        if source.name.startswith('register_'):
            assert 'wave472_results.json' in source.read_text(encoding='utf8') and 'wave470_results.json' not in source.read_text(encoding='utf8')
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,*aliases,*[A/n for n in EXTRAS if n not in EXTRAS[9:11]]]}
    for name in EXTRAS[9:11]:create(A/name,{'status':'compiled_exact149_three_mixed_variants_QA100_before_future','input_sha256':pins,'expected_records':149,'expected_full_board':17687,'parent_rounds':[175,188],'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    assert all(p.is_file() for p in source_paths())
    create(A/PROOF,{'status':'compiled_complete149_two_model_variant_replay_QA100_CPU11_and_exact_sources_before_future','input_sha256':pins,'direct_import_checks':imports,'literal_source_checks':literals,'actual_callback_CPU_count':11,'expected_records':149,'expected_full_board':17687,'actual_models_per_nonidentity_signal':2,'parent_rounds':[175,188],'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    import subprocess,psutil
    from handoff_ready_goss_full_execution_20261006 import retire
    old=A/'service_owned_workflows_20261006/MixedObjectiveWindow189_complete149_family_v1_20261011'
    identity=read(old/'native_launch.json');assert owned(identity) and not psutil.Process(identity['owned_worker_pid']).children()
    stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(identity['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
    assert '(idle)' in stack and 'closed' in stack
    create(A/'mixed189_wave_literal_before_science_recovery_v2_20261011.json',{'status':'verified_source1_idle_before_any_scientific_outputs_and_fixed_source2_wave472_literal','original_identity':identity,'idle_stack':stack,'new_fits':0,'new_scores':0,'original_v1_sources_preserved':True})
    assert allowed();retire(identity,'Exact idle189 helper replaced with wave472 source2 before any scientific outputs; unchanged prior49 scoring')
    assert allowed();name='MixedObjectiveWindow189_complete149_family_v2_20261011';row=start_service(name,EXTRAS[5],[],{str(A/EXTRAS[5]):sha(A/EXTRAS[5]),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)
    print({'complete189_149_QA100_queued':True,'new_scores':0,'future_qualification_pending':True},flush=True)
if __name__=='__main__':main()
