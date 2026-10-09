"""Check scientific imports independently of service gates for every future151-153 phase."""
from pathlib import Path
import sys,re,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from recover_HuberSparse150_import_namespace_v23_20261009 import preserve_imports
META=A/'future_import_namespaces_v38_20261009.json'

def routed(number,source):
    s=preserve_imports(source,BASE_ROUTE(number,source))
    # Source filenames are immutable artifacts even when their stems resemble gates.
    original=[x for x in ast.walk(ast.parse(source)) if isinstance(x,ast.Constant)]
    current=[x for x in ast.walk(ast.parse(s)) if isinstance(x,ast.Constant)]
    assert len(original)==len(current)
    edits=[];lines=s.splitlines(keepends=True);offsets=[0]
    for line in lines:offsets.append(offsets[-1]+len(line))
    for x,y in zip(original,current):
        if isinstance(x.value,str) and isinstance(y.value,str) and x.value.endswith(('.py','.json')) and 'service_owned_workflows' not in x.value and x.value!='BF16Medium153_complete_pipeline_preparation_v17_20261009.json' and x.value!=y.value:
            assert y.lineno==y.end_lineno
            edits.append((offsets[y.lineno-1]+y.col_offset,offsets[y.end_lineno-1]+y.end_col_offset,repr(x.value)))
    for start,end,value in sorted(edits,reverse=True):s=s[:start]+value+s[end:]
    s=s.replace('HuberSparse59_round150_full_registration_v3_20261009','HuberSparse59_round150_full_registration_v11_20261009')
    for label in ('RFFSparse151','SparseAfter148152','BF16Medium153'):
        s=s.replace(label+'_prior_complete_forecast_duplicate_audit_v3_20261009',label+'_prior_complete_forecast_duplicate_audit_v9_20261009')
    for stem in ('round151_source_admission','controls_main_publication','official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round151_full_registration'):
        s=s.replace(f'RFFSparse59_{stem}_v2_20261009',f'RFFSparse59_{stem}_v3_20261009')
    for label in ('SparseAfter148152','BF16Medium153'):
        s=s.replace(label+'_prior_complete_forecast_duplicate_audit_v9_20261009',label+'_prior_complete_forecast_duplicate_audit_v10_20261009')
    return s.replace('main_publisher_v9_20261009','main_publisher_v10_20261009')

def execute(number,name,phase=None):
    global BASE_ROUTE
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    import verify_future_service_and_data_namespaces_v22_20261009 as previous
    BASE_ROUTE=previous.routed;previous.routed=routed;original_read=previous.read
    def actual_read(path):
        value=original_read(path)
        if Path(path)==previous.META:
            value={**value,'drivers':m['drivers'],'receiver_specs':m['receiver_specs'],
                'input_sha256':{**value['input_sha256'],**m['input_sha256'],str(META):sha(META)}}
        return value
    previous.read=actual_read
    from external_registry_source_paths_runtime_v1_20261009 import installed as registry_paths
    from external_publication_source_paths_runtime_v1_20261009 import installed as publication_paths
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    from contextlib import nullcontext
    try:
        if number in (151,152):
            import importlib
            storage=importlib.import_module({151:'RFFSparse151_storage_v2_20261009',152:'SparseAfter148152_storage_v1_20261009'}[number])
            with storage.installed_transfer(),registry_paths(),publication_paths(),git_io(Path('E:/赛题五_本机临时/future_typed_registry_v38_20261009')/(m['drivers'][str(number)][name]+('_'+phase if phase else ''))/'git_IO') if (name.startswith('publish_') or 'full_registration' in name) else nullcontext():previous.execute(number,name,phase)
        else:
            with registry_paths(),publication_paths():previous.execute(number,name,phase)
    finally:previous.read=original_read;previous.routed=BASE_ROUTE

def main():
    global BASE_ROUTE
    import verify_future_service_and_data_namespaces_v22_20261009 as previous
    import bind_future151to153_serial_receivers_v21_20261009 as earlier
    previous.ORIGINAL_ROUTE=earlier.route;BASE_ROUTE=previous.routed
    old=read(previous.META);drivers={};checks=[];inputs=[Path(__file__),Path(previous.__file__),previous.META,
        A/'recover_HuberSparse150_import_namespace_v23_20261009.py',A/'HuberSparse150_import_namespace_v23_20261009.json',A/'future_import_namespaces_v24_20261009.json',A/'HuberSparse150_volume_transfer_v25_20261009.json',A/'HuberSparse150_materialization_v27_20261009.json',A/'future_import_namespaces_v26_20261009.json',A/'future_import_namespaces_v28_20261009.json',A/'future_import_namespaces_v31_20261009.json',A/'future_import_namespaces_v35_20261009.json',A/'future_import_namespaces_v37_20261009.json',A/'optimization_20261003_r150/full_registration_execution.json',A/'two_seed154_recovery_main_v65_receipt_20261009.json',A/'external_publication_source_paths_runtime_v1_20261009.py',A/'external_publication_source_paths_runtime_v1_20261009.json',A/'main_watcher_safe_handoff_and_index_restore_v34_20261009.json',A/'HuberSparse150_registry_attempt_v30_20261009.json',A/'external_registry_source_paths_runtime_v1_20261009.py',A/'external_registry_source_paths_runtime_v1_20261009.json',A/'RFFSparse151_storage_v1_20261009.py',A/'SparseAfter148152_storage_v1_20261009.py']
    for num,mapping in old['drivers'].items():
        n=int(num);drivers[num]={}
        for name in mapping:
            p=A/name;source=p.read_text(encoding='utf8');s=routed(n,source);compile(s,str(p),'exec')
            mods=[x.module for x in ast.walk(ast.parse(s)) if isinstance(x,ast.ImportFrom)]
            assert mods==[x.module for x in ast.walk(ast.parse(source)) if isinstance(x,ast.ImportFrom)]
            py_before=[x.value for x in ast.walk(ast.parse(source)) if isinstance(x,ast.Constant) and isinstance(x.value,str) and x.value.endswith('.py')]
            py_after=[x.value for x in ast.walk(ast.parse(s)) if isinstance(x,ast.Constant) and isinstance(x.value,str) and x.value.endswith('.py')]
            assert py_before==py_after
            target=A/re.sub(r'_v\d+_20261009.py$','_serial_v38_20261009.py',name)
            code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom bind_future_import_namespaces_v38_20261009 import execute\n"
            if name.startswith('publish_'):code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+str(n)+','+repr(name)+",p.parse_args().phase)\n"
            else:code+="if __name__=='__main__':execute("+str(n)+','+repr(name)+")\n"
            with target.open('x',encoding='utf8') as f:f.write(code)
            drivers[num][name]=target.name;inputs.extend((p,target))
            checks.append({'round':n,'source':name,'all_import_modules_original':True,'all_literal_Python_source_paths_original':True})
    specs=[]
    for sid,driver,args in old['receiver_specs']:
        source=next(s for s,d in old['drivers']['153'].items() if d==driver);specs.append([sid,drivers['153'][source],args])
    create(META,{'status':'passed24_actual_import_and_source_filename_checks_before_future_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'drivers':drivers,
        'receiver_specs':specs,'checks':checks,'scientific_math_changed':False,'native_fits_repeated':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    rows={};handoffs=[]
    for n,label in ((151,'RFFSparse151'),(152,'SparseAfter148152'),(153,'BF16Medium153')):
        dup=f'verify_{label}_prior_complete_forecast_duplicate_audit_v1_20261009.py'
        dispatch={151:'dispatch_RFFSparse151_complete_pipeline_v1_20261009.py',152:'dispatch_SparseAfter148152_complete_pipeline_v1_20261009.py',153:'dispatch_BF16Medium153_complete_pipeline_v17_20261009.py'}[n]
        for source,sid,old_sid in [(dup,f'{label}_prior_complete_forecast_duplicate_audit_v{9 if n==151 else 10}_20261009',f'{label}_prior_complete_forecast_duplicate_audit_v9_20261009'),
            (dispatch,f'{label}_complete_chronological_dispatch_serial_v38_20261009',f'{label}_complete_chronological_dispatch_serial_v37_20261009')]:
            rows[sid]=start(sid,drivers[str(n)][source],[],{str(META):sha(META),str(A/drivers[str(n)][source]):sha(A/drivers[str(n)][source])})
            oldrow=read(A/'service_owned_workflows_20261006'/old_sid/'native_launch.json')
            if owned(oldrow):
                line=next(line for line in stack(oldrow['owned_worker_pid']).splitlines() if '    closed (' in line)
                parent,worker,idle=suspended_idle(oldrow,line)
                try:retire_suspended(oldrow,rows[sid])
                except BaseException:
                    if parent.is_running():parent.resume()
                    if worker.is_running():worker.resume()
                    raise
                handoffs.append({'old':oldrow,'new':rows[sid],'owned_child_free_idle_stack':idle})
            else:assert read(A/'service_owned_workflows_20261006'/old_sid/'service_execution.json')['status'] in ('failed','passed')
    create(A/'future_import_namespaces_hidden_launches_v38_20261009.json',{'launches':rows,'handoffs':handoffs,'scientific_jobs_retired':0})
    print({'typed_sources':len(checks),'owned_controllers':sum(owned(r) for r in rows.values()),'existing_passed_duplicate_audits_retained':sum(not owned(r) for r in rows.values()),'scientific_jobs_restarted':0},flush=True)

if __name__=='__main__':main()
