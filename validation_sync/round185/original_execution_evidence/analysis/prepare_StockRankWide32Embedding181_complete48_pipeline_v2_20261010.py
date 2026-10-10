"""Freeze own ID32 rank1d capacity complete48/QA92 qualification sources before futureX."""
from pathlib import Path
import sys,re,ast,copy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010 as previous

ACTUAL_PARENT='StockRank20Embedding180_complete48_family_v6_registry_recovery_v2_dispatch_v4_future_children_v5_20261010'
def route(text):
    mapping={
      'StockForward20Embedding179_complete48_family_v6_after_Dual25_recovery_v1_20261010':ACTUAL_PARENT,
      'prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010':Path(__file__).stem,
      'prepare_stock_rank20_embedding_full5_native42_screen46_v1_20261010':'prepare_stock_rank_wide32_embedding1024_ID32_own64_v1_20261010',
      'actual_stock_rank20_embedding_own_training_queue_v1_20261010':'actual_stock_rank_wide32_embedding1024_ID32_own64_controls46_queue_v1_20261010',
      'stock_rank20_embedding180':'stock_rank_wide32_embedding181',
      'StockRank20Embedding180':'StockRankWide32Embedding181',
      'stock_rank20_embedding':'stock_rank_wide32_embedding',
      'StockRank20EmbeddingSmall512':'StockRankWide32Embedding1024',
      'StockRank20Embedding':'StockRankWide32Embedding',
      'STOCK_RANK20_EMBEDDING':'STOCK_RANK_WIDE32_EMBEDDING',
      'stock_identity_embedding_network_v1_20261010':'stock_identity_embedding32_network_v1_20261010',
      'embedding16_cross120':'embedding32_cross120','StockEmbedding16':'StockEmbedding32',
      'rank20mean':'rank1d','rank20_mean':'rank1d','Rank20Mean':'RankHuber010',
      'MLP512':'MLP1024','small512':'wide1024','eleven_parent':'twelve_parent',
      '180':'181','179':'180','173':'174',
      'qa91':'qa92','QA91':'QA92','qa_v91':'qa_v92','17062':'17110','463':'464'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=text.replace('embedding16_cross120','embedding32_cross120')
    post={'register_StockRankWide32Embedding181_round181_artifacts_v3_20261010': 'register_StockRankWide32Embedding181_round181_artifacts_v4_20261010', 'publish_StockRankWide32Embedding181_round181_full_validation_v3_20261010': 'publish_StockRankWide32Embedding181_round181_full_validation_v4_20261010', 'optimize_training_round181_v3': 'optimize_training_round181_v4', 'finalize_training_round181_v3': 'finalize_training_round181_v4', 'lossless_ranking_runtime_adapter_round181_v3_20261008': 'lossless_ranking_runtime_adapter_round181_v4_20261008', 'build_lossless_ranking_display_round181_v3_20261008': 'build_lossless_ranking_display_round181_v4_20261008', 'verify_lossless_ranking_display_round181_v3_20261008': 'verify_lossless_ranking_display_round181_v4_20261008', 'collect_full_lossless_round181_qa92_v3_20261010': 'collect_full_lossless_round181_qa92_v4_20261010', 'normalize_completed_stock_rank_wide32_embedding_complete48_after180_v5_20261010': 'normalize_completed_stock_rank_wide32_embedding_complete48_after180_v6_20261010', 'qualify_stock_rank_wide32_embedding48_selected_native14_v5_20261010': 'qualify_stock_rank_wide32_embedding48_selected_native14_v6_20261010', 'stock_rank_wide32_embedding181_storage_v2_20261010': 'stock_rank_wide32_embedding181_storage_v3_20261010', 'prepare_StockRankWide32Embedding181_selected_candidate_v5_20261010': 'prepare_StockRankWide32Embedding181_selected_candidate_v6_20261010', 'seal_StockRankWide32Embedding181_selected_candidate_v2_20261010': 'seal_StockRankWide32Embedding181_selected_candidate_v3_20261010', 'run_StockRankWide32Embedding181_complete_family_v6_20261010': 'run_StockRankWide32Embedding181_complete_family_v7_20261010', 'run_StockRankWide32Embedding181_full_registration_v5_20261010': 'run_StockRankWide32Embedding181_full_registration_v6_20261010', 'verify_StockRankWide32Embedding181_full48_preflight_v5_20261010': 'verify_StockRankWide32Embedding181_full48_preflight_v6_20261010', 'run_StockRankWide32Embedding181_selected_candidate_feature_cache_v6_20261010': 'run_StockRankWide32Embedding181_selected_candidate_feature_cache_v7_20261010', 'stock_rank_wide32_embedding181_candidate_sources_preparation_v5_20261010': 'stock_rank_wide32_embedding181_candidate_sources_preparation_v6_20261010', 'stock_rank_wide32_embedding181_full_registry_sources_preparation_v3_20261010': 'stock_rank_wide32_embedding181_full_registry_sources_preparation_v4_20261010', 'stock_rank_wide32_embedding_complete48_after180_selection_plan_v1_20261010': 'stock_rank_wide32_embedding_complete48_after180_selection_plan_v2_20261010', 'predict_stock_rank_wide32_embedding_complete_qualified_parent_scheme_v1_20261010': 'predict_stock_rank_wide32_embedding_complete_qualified_parent_scheme_v2_20261010', 'stock_rank_wide32_embedding_actual_twelve_parent_callbacks_CPU_controls_v1_20261010': 'stock_rank_wide32_embedding_actual_twelve_parent_callbacks_CPU_controls_v2_20261010', 'actual_stock_rank_wide32_embedding48_after180_normalization_queue_v5_20261010': 'actual_stock_rank_wide32_embedding48_after180_normalization_queue_v6_20261010', 'StockRankWide32Embedding48_selected_native14_v5_20261010': 'StockRankWide32Embedding48_selected_native14_v6_20261010', 'StockRankWide32Embedding181_complete48_family_v6_20261010': 'StockRankWide32Embedding181_complete48_family_v7_20261010', 'stock_rank_wide32_embedding181_full_family_preflight_v2_20261010': 'stock_rank_wide32_embedding181_full_family_preflight_v3_20261010', 'stock_rank_wide32_embedding181_full_execution_sources_admission_v1_20261010': 'stock_rank_wide32_embedding181_full_execution_sources_admission_v2_20261010'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(post,key=len,reverse=True)),lambda m:post[m.group()],text)
    return re.sub(r'\b91\b','92',text)
NAMES=[route(n) for n in previous.NAMES]
EXTRAS=[route(n) for n in previous.EXTRAS]
EXTRAS += ['stock_rank_wide32_explicit_architecture_recovery_v1_20261010.json','stock_identity_embedding32_network_v1_20261010.py','stock_rank_wide32_embedding_wide1024_BF16_native_v1_20261010.py','stock_rank_wide32_embedding_saved_tensor_decoder_v1_20261010.py','stock_rank_wide32_main_publisher_recovery_v2_20261010.json']
def source_paths():
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*previous.source_paths()]))
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed();inputs=[];outputs=[]
    alias=read(A/'Dual25_verified_recovery_exact_dependency_aliases_v5_20261010.json')['service_aliases']
    assert alias['StockRank20Embedding180_complete48_family_v6_20261010']==ACTUAL_PARENT
    original=A/'predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py';inputs.append(original)
    text=route(original.read_text(encoding='utf8'));needle='def parent_filename(graph):\n';assert text.count(needle)==1
    text=text.replace(needle,needle+"    from stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as capacity_parent_key\n    if capacity_parent_key in graph:return 'predict_stock_rank20_embedding_complete_qualified_parent_scheme_v1_20261010.py'\n")
    text=re.sub(r"spec\['original_complete_parent_round'\] in \([^\n]+\)","spec['original_complete_parent_round'] in "+repr(tuple(range(169,181))),text)
    predictor=save('predict_stock_rank_wide32_embedding_complete_qualified_parent_scheme_v2_20261010.py',text);outputs.append(predictor);pred=importlib.import_module(predictor.stem)
    parents=[r['parent'] for r in read(A/'stock_rank20_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261010.json')['records']]+[original.name];rows=[]
    for filename in parents:
        p=A/filename;tree=ast.parse(pred.prepared_parent(p.read_text(encoding='utf8')));nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def before(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and (e is component or e is components);events.append('whole_parent_first');return 22,{}
        def after(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('capacity_stage_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=before,STOCK_RANK_WIDE32_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=after)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_CPU_callback','exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','capacity_stage_last'];rows.append({'parent':filename,'sha256':sha(p),'actual_callback_order':events,'stub_CPU_only_no_saved_model_inference_claimed':True})
    assert len(rows)==12
    callbacks=A/'stock_rank_wide32_embedding_actual_twelve_parent_callbacks_CPU_controls_v2_20261010.json'
    create(callbacks,{'status':'passed_actual_twelve_complete_parent_callback_expressions','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,predictor]},'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    plan=read(A/'stock_rank20_embedding_complete48_after179_selection_plan_v1_20261010.json')
    plan.update(status='predeclared48_rank1d_ID32_capacity_two_grids174_and_qualified174180_anchors_before_own_scores',fully_qualified_anchors=[174,180])
    for family in plan['families']:
        family.update(name=route(family['name']),base_round=174,stage_kind='stock_rank_wide32_embedding_rank1d_direct',actual_service=route(family['actual_service']),main_receipt='StockRankWide32_capacity_native42_official46_main_receipt_v1_20261010.json')
    planpath=A/'stock_rank_wide32_embedding_complete48_after180_selection_plan_v2_20261010.json';create(planpath,plan)
    selected=[n for n in previous.EXTRAS if n.endswith('.py') and ('180' in n or 'after179_v5' in n or 'selected_native14_v5' in n)]
    for old in [*previous.NAMES,*selected]:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        # The immutable capacity queue has a distinct name; its passed terminal
        # receipt includes all own controls/6 fits/native42 and17+29 comparisons.
        outputs.append(save(route(old),text))
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,planpath,callbacks,A/'stock_rank_wide32_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json',A/'stock_rank_wide32_explicit_architecture_recovery_v1_20261010.json']}
    for old in [previous.EXTRAS[9],previous.EXTRAS[10]]:create(A/route(old),{'status':'compiled_exact48_rank1d_ID32_QA92_before_actual_future_dispatch','input_sha256':pins,'expected_records':48,'expected_full_board':17110,'parent_rounds':[174,180],'new_quality_scores':0,'test_labels_read':False})
    for p in source_paths():assert p.is_file(),p
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(181,180,(464,))
    assert '(181, 92, 48)' in (A/NAMES[-1]).read_text(encoding='utf8')
    for n in selected:importlib.import_module(Path(route(n)).stem)
    proof=A/'stock_rank_wide32_embedding181_full_execution_sources_admission_v2_20261010.json'
    create(proof,{'status':'compiled_complete48_own_rank1d_ID32_QA92_and_main_sources_before_future','input_sha256':pins,'expected_records':48,'expected_full_board':17110,'parent_rounds':[174,180],'actual_parent_service':ACTUAL_PARENT,'actual_callbacks_CPU':12,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})
    tasks=[('actual_stock_rank_wide32_embedding48_after180_normalization_queue_v6_20261010','normalize_completed_stock_rank_wide32_embedding_complete48_after180_v6_20261010.py'),('StockRankWide32Embedding48_selected_native14_v6_20261010','qualify_stock_rank_wide32_embedding48_selected_native14_v6_20261010.py'),('StockRankWide32Embedding181_complete48_family_v7_20261010','run_StockRankWide32Embedding181_complete_family_v7_20261010.py')]
    for name,n in tasks:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'capacity_complete48_QA92_queues_started':True,'callbacks_actual_CPU':12,'own_quality_and_future_pending':True},flush=True)
if __name__=='__main__':main()
