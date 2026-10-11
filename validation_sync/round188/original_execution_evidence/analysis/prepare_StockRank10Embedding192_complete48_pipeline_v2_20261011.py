"""Complete the independently trained seed10 family using frozen48 records, QA97, and main only."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010 as previous

FACTORY=Path(__file__).stem
NORMAL='normalize_completed_stock_rank10_embedding_complete48_after191_v1_20261011'
QUAL='qualify_stock_rank10_embedding48_selected_native14_v1_20261011'
PRED='predict_stock_rank10_embedding_complete_qualified_parent_scheme_v1_20261011'
PLAN='stock_rank10_embedding_complete48_after191_selection_plan_v1_20261011.json'
CALL='stock_rank10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
PROOF='stock_rank10_embedding192_full_execution_sources_admission_v1_20261011.json'

def basic(text):
    mapping={'StockRank20Embedding':'StockRank10Embedding','stock_rank20_embedding':'stock_rank10_embedding','rank20mean':'rank10mean','Rank20Mean':'Rank10Mean',
        'STOCK_RANK20_EMBEDDING':'STOCK_RANK10_EMBEDDING',
        'Cross120Recent252Rank10Mean_seed09_e64':'Cross120Recent252Rank10Mean_seed09_e64',
        '17062':'17801','qa91':'qa103','QA91':'QA103','qa_v91':'qa_v103'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    return re.sub(r'(?<!\d)(180|179|173|463|91)(?!\d)',lambda m:{'180':'192','179':'191','173':'175','463':'475','91':'103'}[m.group()],text)

OLD_FILES=[*previous.NAMES,*previous.EXTRAS[:9]]
FILE_MAP={}
for old in OLD_FILES:
    new=basic(old)
    new=re.sub(r'_v\d+_(20261010|20261008)\.py$', '_v1_20261011.py',new)
    new=re.sub(r'_v\d+\.py$', '_v1_20261011.py',new)
    FILE_MAP[old]=new
FILE_MAP[previous.EXTRAS[0]]=NORMAL+'.py'
FILE_MAP[previous.EXTRAS[1]]=QUAL+'.py'
FILE_MAP[previous.EXTRAS[12]]=PRED+'.py'
FILE_MAP[previous.EXTRAS[11]]=PLAN
FILE_MAP[previous.EXTRAS[13]]=CALL
FILE_MAP['prepare_StockRank20Embedding180_complete48_pipeline_v1_20261010.py']=FACTORY+'.py'
FILE_MAP['stock_rank20_embedding180_full_family_preflight_v2_20261010.json']='stock_rank10_embedding192_full_family_preflight_v1_20261011.json'
FILE_MAP[previous.EXTRAS[9]]='stock_rank10_embedding192_candidate_sources_preparation_v1_20261011.json'
FILE_MAP[previous.EXTRAS[10]]='stock_rank10_embedding192_full_registry_sources_preparation_v1_20261011.json'

def route(text):
    mapping={**FILE_MAP,**{Path(k).stem:Path(v).stem for k,v in FILE_MAP.items() if k.endswith('.py')}}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=basic(text)
    text=re.sub(r'[A-Za-z0-9_]*(?:stock_rank10|StockRank10)[A-Za-z0-9_]*',lambda m:m.group().replace('20261010','20261011').replace('20261009','20261011'),text)
    text=text.replace('StockForward20Embedding191_complete48_family_v6_after_Dual25_recovery_v1_20261010',
        'recovery16_MixedRefined191_complete27_family_v1_20261011')
    text=text.replace('actual_stock_rank10_embedding_own_training_queue_v1_20261011',
        'actual_stock_rank10_embedding_own_training_and_full5_queue_v2_20261011')
    text=text.replace('StockRank10Embedding48_selected_native14_v5_20261011',
        'StockRank10Embedding48_selected_native14_v1_20261011')
    text=text.replace('stock_rank10_embedding_complete48_after191_selection_plan_v1_20261011.json',PLAN)
    text=text.replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
    text=text.replace("while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)","from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed\n    closed(service.name)")
    return text

NAMES=[FILE_MAP[n] for n in previous.NAMES]
EXTRAS=[FILE_MAP[n] for n in previous.EXTRAS[:14]]
EXTRAS += ['stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py',
    'stock_rank10_embedding_small512_BF16_native_v1_20261011.py',
    'stock_rank10_embedding_saved_tensor_decoder_v1_20261011.py',
    'stock_rank10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json',
    'rank10_complete48_normalization_native14_sources_admission_v1_20261011.json',
    'mixed_refined191_full_execution_sources_admission_v1_20261011.json',
    'exact_verified_feature120_memoization_runtime_v1_20261010.py',
    'actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json']

def source_paths():
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS]]))

def main():
    assert allowed()
    # Existing normalizer, qualifier, predictor and actual scientific proofs are immutable authorities.
    for n in [NORMAL+'.py',QUAL+'.py',PRED+'.py',PLAN,CALL]:assert (A/n).is_file(),n
    callbacks=read(A/CALL);assert len(callbacks['records'])==11
    normal=importlib.import_module(NORMAL)
    import stock_rank10_embedding_after_complete_qualified_parent_native_stage_v1_20261011 as stage
    assert set(normal.RECIPES)==set(stage.BACKENDS)
    inputs=[A/n for n in OLD_FILES if n not in previous.EXTRAS[:2]]
    output=[]
    for source in inputs:
        target=A/FILE_MAP[source.name];assert not target.exists(),target
        text=route(source.read_text(encoding='utf8'))
        if source.name==previous.EXTRAS[5]:
            needle="    # Selected full-parent inference must not compete with an active new GPU fit."
            assert text.count(needle)==1
            text=text.replace(needle,"    closed('StockRank10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011')\n"+needle)
        compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');output.append(target)
    # Resolve every direct analysis import and exact source filename before dispatch, including inactive branches.
    import_rows=[];literal_rows=[]
    for p in output:
        tree=ast.parse(p.read_text(encoding='utf8'))
        for n in ast.walk(tree):
            if isinstance(n,(ast.Import,ast.ImportFrom)):
                modules=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module]
                for module in modules:
                    if module and (module.startswith(('stock_rank20seed10','prepare_StockRank20Seed10','qualify_stock_rank20seed10','normalize_completed_stock_rank20seed10','predict_stock_rank20seed10','register_StockRank20Seed10','publish_StockRank20Seed10','run_StockRank20Seed10','verify_StockRank20Seed10')) or 'round186' in module):
                        dep=A/(module+'.py');assert dep.is_file(),(p.name,module)
                        import_rows.append({'source':p.name,'module':module,'sha256':sha(dep)})
            if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.endswith('.py') and '/' not in n.value and '\\' not in n.value and ('186' in n.value or 'stock_rank20seed10' in n.value):
                dep=A/n.value;assert dep.is_file(),(p.name,n.value)
                literal_rows.append({'source':p.name,'path':n.value,'sha256':sha(dep)})
    # Validate the real configuration and frozen board constants; do not import registry modules that read future outputs.
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(192,191,(475,))
    assert '(192, 103, 48)' in (A/NAMES[-1]).read_text(encoding='utf8')
    assert 'len(report["connected"])' in (A/NAMES[5]).read_text(encoding='utf8'), 'Board codec must preserve the actual full dynamic record count'
    storage=importlib.import_module(Path(EXTRAS[2]).stem)
    assert len(storage.OUTPUTS)==6 and A/'optimization_20261003_r192' in storage.OUTPUTS
    assert all(p.is_relative_to(Path('E:/赛题五_本机临时/第192轮_20261010')) for p in storage.OUTPUTS.values())
    assert all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
    for recipe,modules in stage.BACKENDS.items():
        native=importlib.import_module(modules[0]);assert native.CONFIG['seed']==20261009 and native.CONFIG['epochs']==64 and native.CONFIG['training_calendar_window']==252
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*output,*[A/n for n in EXTRAS if n not in EXTRAS[9:11]]]} 
    for n in EXTRAS[9:11]:
        create(A/n,{'status':'compiled_exact48_independent_seed10_QA97_before_future_dispatch','input_sha256':pins,
            'expected_records':48,'expected_full_board':17801,'parent_rounds':[175,191],
            'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    assert all(p.is_file() for p in source_paths())
    proof=A/PROOF
    create(proof,{'status':'compiled_complete48_seed10_QA97_own64_actual11_callbacks_and_exact_imports_before_future',
        'input_sha256':pins,'actual_callback_CPU_count':11,'direct_import_checks':import_rows,'literal_source_checks':literal_rows,
        'parent_rounds':[175,191],'expected_records':48,'expected_full_board':17801,
        'reused_completed_scientific_records_no_retraining':True,'future_GPU_waits_long504_full5':True,
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    assert allowed()
    name='StockRank10Embedding192_complete48_family_v1_20261011'
    driver=EXTRAS[5]
    row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(proof):sha(proof)})
    create(A/(name+'_activation.json'),row)
    print({'full192_pipeline_queued':True,'expected_records':48,'expected_board':17402,'new_scores':0,'future_inference_pending':True},flush=True)

if __name__=='__main__':main()
