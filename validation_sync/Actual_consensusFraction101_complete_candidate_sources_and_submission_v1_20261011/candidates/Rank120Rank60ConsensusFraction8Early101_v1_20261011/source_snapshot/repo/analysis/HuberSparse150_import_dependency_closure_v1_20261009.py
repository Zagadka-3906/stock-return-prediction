"""Pin the inherited best_key import without changing admitted scientific source or prospective bytes."""
from pathlib import Path
import ast,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
META=A/'HuberSparse150_import_dependency_closure_v1_20261009.json'
PROOF=A/'HuberSparse150_inherited_best_key_AST_byteproof_v1_20261009.json'
EXTRAS=['run_HuberSparse59_official_comparison_v1_20261008.py',
    'HuberSparse150_import_dependency_closure_v1_20261009.py',
    'verify_HuberSparse59_round150_sources_v2_20261009.py',
    'publish_HuberSparse59_evidence_v2_20261009.py',
    'dispatch_HuberSparse150_complete_pipeline_v2_20261009.py']

def prepare():
    old=A/'run_HuberSparse59_official_comparison_v1_20261008.py';new=A/'run_HuberSparse59_official_comparison_v2_20261009.py'
    trees=[ast.parse(p.read_text(encoding='utf8')) for p in (old,new)]
    functions=[next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='best_key') for t in trees]
    texts=[ast.dump(n,include_attributes=False) for n in functions];assert texts[0]==texts[1]
    candidate=A/'prepare_HuberSparse59_selected_candidate_v2_20261009.py'
    assert 'from run_HuberSparse59_official_comparison_v1_20261008 import best_key' in candidate.read_text(encoding='utf8')
    files=[*(A/n for n in EXTRAS),old,new,candidate]
    for p in files:compile(p.read_text(encoding='utf8'),str(p),'exec')
    pins={str(p):sha(p) for p in dict.fromkeys(files)}
    create(PROOF,{'status':'passed_actual_old_and_new_best_key_function_AST_identical_and_actual_import_source_pinned','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'best_key_AST_sha256':hashlib.sha256(texts[0].encode()).hexdigest(),'scientific_functions_changed':False,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
    create(META,{'status':'frozen_additional_actual_inherited_import_and_runtime_receivers_before_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':{**pins,str(PROOF):sha(PROOF)},'prospective32_generated_bytes_and440_graph_proof_unchanged':True,'quality_admitted':False,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})

def execute(name,*args):
    meta=read(META)
    for p,d in meta['input_sha256'].items():assert sha(p)==d,p
    import prepare_HuberSparse59_round150_sources_v2_20261009 as generator
    previous=generator.source_paths
    def paths():return list(dict.fromkeys([*previous(),*(A/n for n in EXTRAS),PROOF,META]))
    generator.source_paths=paths
    namespace={'__name__':'actual150_import_closure_bound_runtime','__file__':str(A/{
        'verify_HuberSparse59_round150_sources_v1_20261009.py':'verify_HuberSparse59_round150_sources_v2_20261009.py',
        'publish_HuberSparse59_evidence_v1_20261009.py':'publish_HuberSparse59_evidence_v2_20261009.py',
        'dispatch_HuberSparse150_complete_pipeline_v1_20261009.py':'dispatch_HuberSparse150_complete_pipeline_v2_20261009.py'}[name])}
    source=(A/name).read_text(encoding='utf8')
    if name.startswith('dispatch_'):
        source=source.replace('verify_HuberSparse59_round150_sources_v1_20261009.py','verify_HuberSparse59_round150_sources_v2_20261009.py')
        source=source.replace('publish_HuberSparse59_evidence_v1_20261009.py','publish_HuberSparse59_evidence_v2_20261009.py')
        source=source.replace('HuberSparse150_complete_hidden_launches_v1_20261009','HuberSparse150_complete_hidden_launches_v2_20261009')
    exec(compile(source,str(A/name),'exec'),namespace)
    if name.startswith('verify_'):
        original_create=namespace['create']
        def pinned_create(path,value):
            if Path(path).name in ('HuberSparse59_actual_controls_index_v1_20261008.json','HuberSparse59_round150_source_admission_v1_20261008.json'):
                value={**value,'input_sha256':{**value['input_sha256'],**meta['input_sha256'],str(META):sha(META)},'actual_inherited_best_key_import_pinned':True}
            return original_create(path,value)
        namespace['create']=pinned_create
    namespace['main'](*args)

if __name__=='__main__':prepare()
