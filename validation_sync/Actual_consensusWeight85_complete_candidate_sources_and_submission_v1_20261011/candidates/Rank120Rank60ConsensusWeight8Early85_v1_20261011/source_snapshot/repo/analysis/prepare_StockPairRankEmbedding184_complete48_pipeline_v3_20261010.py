"""Freeze48 pair-objective records plus174/183 anchors, QA95, before any future inference."""
from pathlib import Path
import sys,re,ast,copy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_StockRankWide32Embedding181_complete48_pipeline_v2_20261010 as previous
FACTORY=Path(__file__).stem
def route(text):
    mapping={'prepare_StockRankWide32Embedding181_complete48_pipeline_v2_20261010':FACTORY,
      'StockRank20Embedding180_complete48_family_v6_registry_recovery_v2_dispatch_v4_future_children_v5_20261010':'StockRank20Embedding183_complete85_family_v6_20261010',
      'stock_rank_wide32_embedding':'stock_pairrank_embedding','StockRankWide32Embedding1024':'StockPairRankEmbeddingSmall512','StockRankWide32Embedding':'StockPairRankEmbedding','STOCK_RANK_WIDE32_EMBEDDING':'STOCK_PAIRRANK_EMBEDDING',
      'StockRankWide32_capacity':'StockPairRank_objective','stock_identity_embedding32_network':'stock_identity_embedding_network',
      'embedding32_cross120_rank1d_recent252_wide1024_BF16_e64':'embedding16_cross120_pairrank1d_recent252_small512_BF16_e32',
      'embedding_rank1d_direct':'embedding_rank1d_direct',
      'wide1024':'small512','MLP1024':'MLP512','StockEmbedding32':'StockEmbedding16','RankHuber010':'PairRankHuberAux',
      'twelve_parent':'thirteen_parent','17110':'17306','qa92':'qa95','QA92':'QA95','qa_v92':'qa_v95'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=re.sub(r'(?<!\d)(181|180|464|92)(?!\d)',lambda m:{'181':'184','180':'183','464':'467','92':'95'}[m.group()],text)
    text=text.replace('_e64','_e32').replace("['epochs']==64","['epochs']==32")
    text=text.replace('stock_pairrank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json','stock_pairrank_embedding_own32_controls46_sources_admission_v1_20261010.json')
    text=text.replace('prepare_stock_pairrank_embedding1024_ID32_own64_v1_20261010.py','prepare_stock_pairrank_embedding_own32_controls46_v1_20261010.py')
    text=text.replace('actual_stock_pairrank_embedding1024_ID32_own64_controls46_queue_v1_20261010','actual_stock_pairrank_embedding_own32_controls46_queue_v1_20261010')
    text=text.replace('stock_pairrank_embedding32_cross120_rank1d_recent252_small512_BF16_e32','stock_pairrank_embedding16_cross120_pairrank1d_recent252_small512_BF16_e32')
    versions={'register_StockPairRankEmbedding184_round184_artifacts_v4_20261010.py': 'register_StockPairRankEmbedding184_round184_artifacts_v5_20261010.py', 'publish_StockPairRankEmbedding184_round184_full_validation_v4_20261010.py': 'publish_StockPairRankEmbedding184_round184_full_validation_v5_20261010.py', 'optimize_training_round184_v4.py': 'optimize_training_round184_v4.py', 'finalize_training_round184_v4.py': 'finalize_training_round184_v4.py', 'lossless_ranking_runtime_adapter_round184_v4_20261008.py': 'lossless_ranking_runtime_adapter_round184_v5_20261008.py', 'build_lossless_ranking_display_round184_v4_20261008.py': 'build_lossless_ranking_display_round184_v5_20261008.py', 'verify_lossless_ranking_display_round184_v4_20261008.py': 'verify_lossless_ranking_display_round184_v5_20261008.py', 'collect_full_lossless_round184_qa95_v4_20261010.py': 'collect_full_lossless_round184_qa95_v5_20261010.py', 'normalize_completed_stock_pairrank_embedding_complete48_after183_v6_20261010.py': 'normalize_completed_stock_pairrank_embedding_complete48_after183_v7_20261010.py', 'qualify_stock_pairrank_embedding48_selected_native14_v6_20261010.py': 'qualify_stock_pairrank_embedding48_selected_native14_v7_20261010.py', 'stock_pairrank_embedding184_storage_v3_20261010.py': 'stock_pairrank_embedding184_storage_v4_20261010.py', 'prepare_StockPairRankEmbedding184_selected_candidate_v6_20261010.py': 'prepare_StockPairRankEmbedding184_selected_candidate_v7_20261010.py', 'seal_StockPairRankEmbedding184_selected_candidate_v3_20261010.py': 'seal_StockPairRankEmbedding184_selected_candidate_v4_20261010.py', 'run_StockPairRankEmbedding184_complete_family_v7_20261010.py': 'run_StockPairRankEmbedding184_complete_family_v8_20261010.py', 'run_StockPairRankEmbedding184_full_registration_v6_20261010.py': 'run_StockPairRankEmbedding184_full_registration_v7_20261010.py', 'verify_StockPairRankEmbedding184_full48_preflight_v6_20261010.py': 'verify_StockPairRankEmbedding184_full48_preflight_v7_20261010.py', 'run_StockPairRankEmbedding184_selected_candidate_feature_cache_v7_20261010.py': 'run_StockPairRankEmbedding184_selected_candidate_feature_cache_v8_20261010.py', 'stock_pairrank_embedding184_candidate_sources_preparation_v6_20261010.json': 'stock_pairrank_embedding184_candidate_sources_preparation_v7_20261010.json', 'stock_pairrank_embedding184_full_registry_sources_preparation_v4_20261010.json': 'stock_pairrank_embedding184_full_registry_sources_preparation_v5_20261010.json', 'stock_pairrank_embedding_complete48_after183_selection_plan_v2_20261010.json': 'stock_pairrank_embedding_complete48_after183_selection_plan_v3_20261010.json', 'predict_stock_pairrank_embedding_complete_qualified_parent_scheme_v2_20261010.py': 'predict_stock_pairrank_embedding_complete_qualified_parent_scheme_v3_20261010.py', 'stock_pairrank_embedding_actual_thirteen_parent_callbacks_CPU_controls_v2_20261010.json': 'stock_pairrank_embedding_actual_thirteen_parent_callbacks_CPU_controls_v3_20261010.json', 'route_StockPairRank184_exact_verified_children_v1_20261010.py': 'route_StockPairRank184_exact_verified_children_v2_20261010.py', 'StockPairRank184_exact_child_sources_v1_20261010.json': 'StockPairRank184_exact_child_sources_v2_20261010.json', 'stock_pairrank_embedding184_full_execution_sources_admission_v1_20261010.json': 'stock_pairrank_embedding184_full_execution_sources_admission_v2_20261010.json'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(versions,key=len,reverse=True)),lambda m:versions[m.group()],text)
    return text
NAMES=[route(n) for n in previous.NAMES]
EXTRAS=[route(n) for n in previous.EXTRAS[:17]]
EXTRAS += ['same_day_ranknet_loss_v1_20261010.py','same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json',
 'stock_pairrank_embedding_small512_BF16_native_v1_20261010.py','stock_pairrank_embedding_saved_tensor_decoder_v1_20261010.py',
 'route_StockPairRank184_exact_verified_children_v2_20261010.py','StockPairRank184_exact_child_sources_v2_20261010.json']
def source_paths():
    paths=[Path(__file__),*[A/n for n in NAMES+EXTRAS],*previous.source_paths()]
    proof=A/'StockPairRank184_exact_child_sources_v2_20261010.json'
    if proof.exists():paths += [A/n for n in read(proof)['driver_wrappers'].values()]
    return list(dict.fromkeys(paths))
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();inputs=[];outputs=[]
    original=A/'predict_stock_rank_wide32_embedding_complete_qualified_parent_scheme_v2_20261010.py';inputs.append(original)
    text=route(original.read_text(encoding='utf8'))
    needle='def parent_filename(graph):\n'
    text=text.replace(needle,needle+"    from stock_rank_wide32_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as capacity_key\n    if capacity_key in graph:return 'predict_stock_rank_wide32_embedding_complete_qualified_parent_scheme_v2_20261010.py'\n")
    text=re.sub(r"spec\['original_complete_parent_round'\] in \([^\n]+\)","spec['original_complete_parent_round'] in "+repr(tuple(range(169,184))),text)
    predictor=save(route(original.name),text);outputs.append(predictor);pred=importlib.import_module(predictor.stem)
    parents=[r['parent'] for r in read(A/'stock_rank_wide32_embedding_actual_twelve_parent_callbacks_CPU_controls_v2_20261010.json')['records']]+[original.name];rows=[]
    for filename in parents:
        p=A/filename;tree=ast.parse(pred.prepared_parent(p.read_text(encoding='utf8')));nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')];assert len(nodes)==1
        events=[];calls=[];context=object();ns=object();spec=object();component=object();components=[component]
        def before(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and (e is component or e is components);events.append('whole_parent_first');return 22,{}
        def after(a,b):
            assert a is context and b==22 and len(calls)==1;events.append('pair_stage_last');return 33
        scope=dict(ns=ns,spec=spec,component=component,components=components,calls=calls,after_parent=before,STOCK_PAIRRANK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=after)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(p)+'::actual_CPU_callback','exec'),scope)
        assert scope[nodes[0].name](context,11)==33 and events==['whole_parent_first','pair_stage_last'];rows.append({'parent':filename,'sha256':sha(p),'actual_callback_order':events,'CPU_stub_only_no_model_inference_claimed':True})
    assert len(rows)==13
    callbacks=A/EXTRAS[13]
    create(callbacks,{'status':'passed_actual_thirteen_complete_parent_callback_expressions','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,predictor]},'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    plan=read(A/previous.EXTRAS[11]);plan.update(status='predeclared48_pairrank_ID16_own32_after174_and_qualified174183_anchors_before_scores',fully_qualified_anchors=[174,183])
    for family in plan['families']:family.update(name=route(family['name']),stage_kind='stock_pairrank_embedding_rank1d_direct',actual_service=route(family['actual_service']),main_receipt='StockPairRank_objective_native42_official46_main_receipt_v1_20261010.json')
    planpath=A/EXTRAS[11];create(planpath,plan)
    for old in [*previous.NAMES,*previous.EXTRAS[:9]]:
        p=A/old;inputs.append(p);outputs.append(save(route(old),route(p.read_text(encoding='utf8'))))
    child_sources=[p.name for p in outputs if p.name.startswith(('run_','seal_','prepare_')) and ('184' in p.name)]
    runtime_name='route_StockPairRank184_exact_verified_children_v2_20261010.py'
    wrappers={n:Path(n).stem+'_verified_children_v1.py' for n in child_sources}
    # The normalizer and qualifier are wrapped too, to resolve the actual183 parent.
    for n in EXTRAS[:2]:wrappers[n]=Path(n).stem+'_verified_children_v1.py'
    for source,target in wrappers.items():outputs.append(save(target,"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_StockPairRank184_exact_verified_children_v1_20261010 import execute\nif __name__=='__main__':execute("+repr(source)+")\n"))
    runtime='''from pathlib import Path
import sys,importlib,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
def execute(driver):
    import route_verified_Dual25_recovery_dependencies_v7_20261010 as parent
    parent.installed()
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    assert checks.allowed()
    proof=A/'StockPairRank184_exact_child_sources_v2_20261010.json';data=read(proof)
    for p,d in data['input_sha256'].items():assert sha(p)==d,p
    previous=launch.start_service
    def start(name,source,args,pins):return previous(name,data['driver_wrappers'].get(source,source),args,{**pins,str(proof):sha(proof),str(Path(__file__)):sha(__file__)})
    launch.start_service=start
    actual_run=runpy.run_path
    def routed(path,*args,**kwargs):return actual_run(str(A/data['driver_wrappers'][Path(path).name]) if Path(path).name.startswith('prepare_') and Path(path).name in data['driver_wrappers'] else path,*args,**kwargs)
    runpy.run_path=routed
    source=A/driver
    if driver.startswith('seal_') or '_full_registration_' in driver:
        runpy.run_path(str(source),run_name='__main__');return
    module=importlib.import_module(source.stem)
    if hasattr(module,'closed'):module.closed=checks.closed
    if hasattr(module,'start_service'):module.start_service=start
    module.main()
'''
    runtime=save(runtime_name,runtime);outputs.append(runtime)
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,planpath,callbacks,A/'stock_pairrank_embedding_own32_controls46_sources_admission_v1_20261010.json',A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json']}
    create(A/'StockPairRank184_exact_child_sources_v2_20261010.json',{'status':'compiled_exact_new184_children_preserve_original_storage_main_context','driver_wrappers':wrappers,'input_sha256':pins})
    for name in EXTRAS[9:11]:create(A/name,{'status':'compiled_exact48_pairrank_ID16_QA95_before_future_dispatch','input_sha256':pins,'expected_records':48,'expected_full_board':17306,'parent_rounds':[174,183],'new_quality_scores':0,'test_labels_read':False})
    for p in source_paths():assert p.is_file(),p
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(184,183,(467,))
    assert '(184, 95, 48)' in (A/NAMES[-1]).read_text(encoding='utf8')
    for n in EXTRAS[:9]:importlib.import_module(Path(n).stem)
    proof=A/'stock_pairrank_embedding184_full_execution_sources_admission_v2_20261010.json'
    create(proof,{'status':'compiled_complete48_own_pairrank_ID16_QA95_main_sources_before_future','input_sha256':pins,'expected_records':48,'expected_full_board':17306,'actual_callbacks_CPU':13,'parent_rounds':[174,183],'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})
    tasks=[('actual_stock_pairrank_embedding48_after183_normalization_queue_v7_20261010',EXTRAS[0]),('StockPairRankEmbedding48_selected_native14_v7_20261010',EXTRAS[1]),('StockPairRankEmbedding184_complete48_family_v8_20261010',EXTRAS[5])]
    for name,n in tasks:
        assert allowed();driver=wrappers[n];row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'complete48_QA95_sources_frozen':True,'actual_CPU_parent_callbacks':13,'scores_and_future_qualification_pending':True},flush=True)
if __name__=='__main__':main()
