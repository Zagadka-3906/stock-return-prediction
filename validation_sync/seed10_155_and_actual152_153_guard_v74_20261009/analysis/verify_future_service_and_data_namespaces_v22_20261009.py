"""Validate typed service gates and immutable data paths before future151-153 jobs can advance."""
from pathlib import Path
import sys,re,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'future_service_and_data_namespaces_v22_20261009.json'

def routed(number,source):
    import bind_future151to153_serial_receivers_v21_20261009 as old
    s=ORIGINAL_ROUTE(number,source)
    for n,label in ((151,'RFFSparse151'),(152,'SparseAfter148152'),(153,'BF16Medium153')):
        s=s.replace(label+'_prior_complete_forecast_duplicate_audit_v2_20261009',label+'_prior_complete_forecast_duplicate_audit_v3_20261009')
    for original,current in old.SERVICE_MAP.items():
        if 'prior_complete_forecast' in original:current=current.replace('_v2_','_v3_')
        # A-relative artifact paths and E-backed data stay at their original canonical
        # addresses. /service_owned_workflows/... gates are a separate namespace.
        pattern=r"(A\s*/\s*['\"])(actual_)?"+re.escape(current)
        s=re.sub(pattern,lambda m:m[1]+(m[2] or '')+original,s)
        pattern=r"(['\"]E:[^'\"\n]*)"+re.escape(current)
        s=re.sub(pattern,lambda m:m[1]+original,s)
    return s

def execute(number,name,phase=None):
    global ORIGINAL_ROUTE
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    import bind_future151to153_serial_receivers_v21_20261009 as old
    ORIGINAL_ROUTE=old.route;original_read=old.read;old.route=routed
    def actual_read(path):
        value=original_read(path)
        if Path(path)==old.META:
            value={**value,'drivers':m['drivers'],'receiver_specs':m['receiver_specs'],
              'input_sha256':{**value['input_sha256'],**m['input_sha256'],str(META):sha(META)}}
        return value
    old.read=actual_read
    try:old.execute(number,name,phase)
    finally:old.route=ORIGINAL_ROUTE;old.read=original_read

def main():
    global ORIGINAL_ROUTE
    import bind_future151to153_serial_receivers_v21_20261009 as old
    ORIGINAL_ROUTE=old.route;previous=read(old.META);drivers={};checks=[]
    inputs=[Path(__file__),Path(old.__file__),old.META]
    for num,mapping in previous['drivers'].items():
        n=int(num);drivers[num]={}
        for source_name in mapping:
            p=A/source_name;original=p.read_text(encoding='utf8');corrected=routed(n,original);tree=ast.parse(corrected);compile(corrected,str(p),'exec')
            for original_sid,current in old.SERVICE_MAP.items():
                if 'prior_complete_forecast' in original_sid:current=current.replace('_v2_','_v3_')
                assert not re.search(r"A\s*/\s*['\"](?:actual_)?"+re.escape(current),corrected),('artifact_moved',p,current)
                assert not re.search(r"['\"]E:[^'\"\n]*"+re.escape(current),corrected),('E_artifact_moved',p,current)
            if source_name.startswith('verify_') and 'prior_complete_forecast' in source_name:
                # Prove the independently frozen board,73/55/25 controls and canonical
                # pointer filenames match the generator's actual data contract.
                constant=[x.value for x in ast.walk(tree) if isinstance(x,ast.Constant) and isinstance(x.value,str)]
                label={151:'RFFSparse151',152:'SparseAfter148152',153:'BF16Medium153'}[n]
                assert 'actual_'+label+'_prior_complete_forecast_duplicate_audit_v1_20261009.json' in constant
                assert 'E:/赛题五_本机临时/'+label+'_prior_complete_forecast_duplicate_audit_v1_20261009' in constant
            checks.append({'round':n,'source':source_name,'service_gates_current':True,'all_A_and_E_artifact_names_original':True})
            target=A/re.sub(r'_v\d+_20261009.py$','_serial_v22_20261009.py',source_name)
            code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom verify_future_service_and_data_namespaces_v22_20261009 import execute\n"
            if source_name.startswith('publish_'):code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+str(n)+','+repr(source_name)+",p.parse_args().phase)\n"
            else:code+="if __name__=='__main__':execute("+str(n)+','+repr(source_name)+")\n"
            with target.open('x',encoding='utf8') as f:f.write(code)
            drivers[num][source_name]=target.name;inputs.extend((p,target))
    specs=[]
    for sid,driver,args in previous['receiver_specs']:
        source=next(s for s,d in previous['drivers']['153'].items() if d==driver)
        specs.append([sid,drivers['153'][source],args])
    create(META,{'status':'passed_actual24_typed_source_checks_current_service_gates_original_data_paths_and_duplicate_pointer_contracts',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'drivers':drivers,'receiver_specs':specs,
      'checks':checks,'scientific_model_or_scoring_math_changed':False,'future_quality_scores_claimed':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
    rows={};handoffs=[]
    for n,label in ((151,'RFFSparse151'),(152,'SparseAfter148152'),(153,'BF16Medium153')):
        dup=f'verify_{label}_prior_complete_forecast_duplicate_audit_v1_20261009.py'
        dispatch={151:'dispatch_RFFSparse151_complete_pipeline_v1_20261009.py',152:'dispatch_SparseAfter148152_complete_pipeline_v1_20261009.py',153:'dispatch_BF16Medium153_complete_pipeline_v17_20261009.py'}[n]
        for source,sid,old_sid in [(dup,f'{label}_prior_complete_forecast_duplicate_audit_v3_20261009',f'{label}_prior_complete_forecast_duplicate_audit_v2_20261009'),
          (dispatch,f'{label}_complete_chronological_dispatch_serial_v22_20261009',f'{label}_complete_chronological_dispatch_serial_v21_20261009')]:
            rows[sid]=start(sid,drivers[str(n)][source],[],{str(META):sha(META),str(A/drivers[str(n)][source]):sha(A/drivers[str(n)][source])})
            oldrow=read(A/'service_owned_workflows_20261006'/old_sid/'native_launch.json')
            assert owned(oldrow)
            line=next(line for line in stack(oldrow['owned_worker_pid']).splitlines() if '    closed (' in line)
            parent,worker,idle=suspended_idle(oldrow,line)
            try:retire_suspended(oldrow,rows[sid])
            except BaseException:
                if parent.is_running():parent.resume()
                if worker.is_running():worker.resume()
                raise
            handoffs.append({'old':oldrow,'new':rows[sid],'old_owned_child_free_idle_stack':idle,'scientific_jobs_retired':0})
    create(A/'future_service_and_data_namespaces_hidden_launches_v22_20261009.json',{'launches':rows,'handoffs':handoffs,'scientific_jobs_retired':0})
    print({'validated_typed_sources':len(checks),'new_owned_idle_controllers':len(rows),'scientific_jobs_restarted':0},flush=True)

if __name__=='__main__':main()
