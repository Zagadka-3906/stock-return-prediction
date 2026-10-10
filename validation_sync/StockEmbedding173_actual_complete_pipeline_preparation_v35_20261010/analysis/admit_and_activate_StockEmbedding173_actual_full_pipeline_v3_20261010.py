"""Actual import-route admission and corrected literal173 display checks before exclusive dispatch."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,read,sha
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    original=A/'verify_StockEmbedding173_full36_preflight_v2_20261010.py';text=original.read_text(encoding='utf8')
    assert text.count('assert number == 172')==1;text=text.replace('assert number == 172','assert number == 173')
    text=text.replace('run_StockEmbedding173_full_registration_v2_20261010.py','run_StockEmbedding173_full_registration_v3_20261010.py').replace('run_StockEmbedding173_complete_family_v2_20261010.py','run_StockEmbedding173_complete_family_v3_20261010.py').replace('stock_embedding173_full_family_preflight_v2','stock_embedding173_full_family_preflight_v3')
    preflight=save('verify_StockEmbedding173_full36_preflight_v3_20261010.py',text)
    old=A/'run_StockEmbedding173_full_registration_v2_20261010.py';text=old.read_text(encoding='utf8').replace('run_StockEmbedding173_complete_family_v2_20261010.py','run_StockEmbedding173_complete_family_v3_20261010.py').replace('verify_StockEmbedding173_full36_preflight_v2_20261010.py','verify_StockEmbedding173_full36_preflight_v3_20261010.py').replace('stock_embedding173_full_family_preflight_v2','stock_embedding173_full_family_preflight_v3')
    registration=save('run_StockEmbedding173_full_registration_v3_20261010.py',text)
    originalfamily=A/'run_StockEmbedding173_complete_family_v2_20261010.py';text=originalfamily.read_text(encoding='utf8').replace('verify_StockEmbedding173_full36_preflight_v2_20261010','verify_StockEmbedding173_full36_preflight_v3_20261010').replace('run_StockEmbedding173_full_registration_v2_20261010.py','run_StockEmbedding173_full_registration_v3_20261010.py').replace('stock_embedding173_full_family_preflight_v2','stock_embedding173_full_family_preflight_v3')
    family=save('run_StockEmbedding173_complete_family_v3_20261010.py',text)
    from prepare_stock_embedding173_full_registry_sources_v2_20261010 import source_paths
    sources=list(dict.fromkeys([*source_paths(),preflight,registration,family,A/'stock_embedding173_actual_execution_routes_admission_v2_20261010.json']))
    imported=[]
    for path in sources:
        assert path.is_file(),path
        if path.suffix!='.py':continue
        tree=ast.parse(path.read_text(encoding='utf8'))
        for node in ast.walk(tree):
            names=[n.name for n in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.level==0 and node.module else []
            for name in names:
                #Only actual files in the shared workspace are local-route checks.
                local=A/(name+'.py');rootlocal=ROOT/(name+'.py')
                if not local.exists() and not rootlocal.exists():
                    if name.startswith(('stock_embedding','StockEmbedding','prepare_stock','qualify_stock','normalize_completed_stock','predict_stock','register_Stock','publish_Stock','run_Stock','verify_Stock','seal_Stock')):raise AssertionError(('missing_new_local_module',name,path))
                    continue
                assert importlib.util.find_spec(name) is not None,(name,path)
                imported.append({'from_source':str(path),'local_module':name})
    #The registry's only import-time data dependency is its pending ready file;
    #substitute this one field during a source-route-only import, never main().
    registry=A/'register_StockEmbedding173_round173_artifacts_v2_20261010.py'
    import run_dependency_queue_v3_20261006 as io
    original_read=io.read;pending=A/'StockEmbedding173_selected_release_v1_20261010/selected_candidate_ready_for_registration.json'
    def bounded_read(path):
        if Path(path)==pending:return {'source_release':str(A/'optimization_20261003_r170'),'source_candidate':str(ROOT/'candidates/optimization_20261003_r170')}
        return original_read(path)
    io.read=bounded_read
    try:
        module=importlib.import_module(registry.stem);assert callable(module.main) and module.OUT==A/'optimization_20261003_r173'
    finally:io.read=original_read
    for p in (preflight,registration,family):importlib.import_module(p.stem)
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round173.py');assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(173,172,(456,))
    import stock_embedding173_storage_v1_20261010 as storage
    assert len(storage.OUTPUTS)==6 and storage.EBASE.name=='第173轮_20261010'
    assert 'assert number == 173' in preflight.read_text(encoding='utf8')
    for p in sources:assert p.is_file()
    proof=A/'stock_embedding173_actual_local_import_and_scalar_routes_admission_v3_20261010.json'
    create(proof,{'status':'passed_actual173_local_module_routes_pending_registry_source_import_and173_172_456_scalars','input_sha256':{str(p):sha(p) for p in [Path(__file__),*sources]},'local_import_routes':imported,'actual_pending_registry_top_ready_field_was_only_mocked_for_import_not_registration':True,'selected36_scores14_controls_and_full_future_execution_pending':True,'new_quality_scores':0,'new_native_fits':0})
    assert allowed();row=start_service('StockEmbedding173_complete36_family_v3_20261010',family.name,[],{str(family):sha(family),str(proof):sha(proof)})
    create(A/'actual_StockEmbedding173_complete36_family_activation_v3_20261010.json',row)
    print({'actual_family_worker':row['owned_worker_pid'],'actual_local_import_routes':len(imported),'QA':84,'new_future_inference':False},flush=True)
if __name__=='__main__':main()
