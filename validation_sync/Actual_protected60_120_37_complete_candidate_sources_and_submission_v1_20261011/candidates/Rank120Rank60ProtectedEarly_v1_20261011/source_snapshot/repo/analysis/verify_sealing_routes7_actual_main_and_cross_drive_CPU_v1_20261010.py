"""Execute real routing condition and actual D→E storage scope; no inference or fake terminal states."""
from pathlib import Path
from types import SimpleNamespace
import sys,ast,copy,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    broker=A/'route_verified_Dual25_recovery_dependencies_v7_20261010.py';proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v7_20261010.json';proof=read(proofpath)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    tree=ast.parse(broker.read_text(encoding='utf8'));execute=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
    branch=next(n for n in execute.body if isinstance(n,ast.If) and any(isinstance(v,ast.Attribute) and v.attr=='run_path' for v in ast.walk(n)))
    function=ast.FunctionDef(name='actual_dispatch',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='driver'),ast.arg(arg='source')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=[copy.deepcopy(branch)],decorator_list=[])
    events=[];scope={'runpy':SimpleNamespace(run_path=lambda path,**kwargs:events.append((path,kwargs)))}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),str(broker)+'::actual_main_dispatch_branch','exec'),scope)
    sealers=sorted(n for n in proof['driver_wrappers'] if n.startswith('seal_') and n.endswith('_20261010.py'))
    records=[]
    for name in [*sealers,'run_StockTop10Embedding175_full_registration_v3_20261010.py']:
        before=len(events);scope['actual_dispatch'](name,A/name);assert len(events)==before+1 and events[-1]==(str(A/name),{'run_name':'__main__'})
        if name.startswith('seal_'):
            source_tree=ast.parse((A/name).read_text(encoding='utf8'));guards=[n for n in source_tree.body if isinstance(n,ast.If) and '__main__' in ast.unparse(n.test)]
            assert len(guards)==1 and any(isinstance(n,ast.Name) and n.id=='installed_transfer' for n in ast.walk(guards[0]))
        records.append({'source':name,'actual_main_context_dispatch':True,'original_sealer_storage_scope_preserved':name.startswith('seal_')})
    source=A/'actual_sealing_transfer_CPU_fixture_v7_20261010.bin';assert not source.exists();data=bytes(range(256))*4+b'actual_D_to_E_sealing_storage_scope_only';source.write_bytes(data)
    import stock_top10_embedding175_storage_v1_20261010 as storage
    folder=Path('E:/赛题五_本机临时/第175轮_20261010/tmp/actual_cross_drive_sealing_scope_CPU_v7_20261010');assert not folder.exists();folder.mkdir(parents=True)
    target=folder/'actual_exact_copy.bin';original_link=os.link
    assert source.resolve().drive.upper()=='D:' and target.parent.resolve().drive.upper()=='E:'
    with storage.installed_transfer():
        assert os.link is not original_link;os.link(source,target);assert target.read_bytes()==data and sha(source)==sha(target)
    assert os.link is original_link
    paths=[Path(__file__),broker,proofpath,Path(storage.__file__),source,target,*[A/n for n in sealers]]
    create(A/'sealing_routes7_actual_main_and_cross_drive_CPU_v1_20261010.json',{'status':'passed_actual_original_storage_main_guard_dispatch_and_real_D_to_E_exact_copy_and_function_restoration','records':records,'actual_main_cases':len(records),'actual_sealers':len(sealers),'cross_drive_fixture_bytes':len(data),'actual_source_drive':'D:','actual_target_drive':'E:','input_sha256':{str(p):sha(p) for p in paths},'new_model_fits':0,'new_quality_scores':0,'new_inference':0,'test_labels_read':False})
    print({'actual_main_dispatch_cases':len(records),'actual_cross_drive_bytes':len(data),'os_link_restored':True},flush=True)
if __name__=='__main__':main()
