"""Bind the actual153 dispatched drivers, independently of immutable science paths."""
from pathlib import Path
from copy import deepcopy
import sys,ast,re,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
META=A/'BF16Medium153_actual_receiver_dispatch_v42_20261009.json'
DISPATCH='dispatch_BF16Medium153_complete_pipeline_v17_20261009.py'
FULL='run_BF16Medium78_round153_full_registration_v3_20261009.py'

def adjusted(source,name,original_route):
    from bind_BF16Medium153_registration_guard_labels_v41_20261009 import repaired
    s=original_route(153,source)
    if name==FULL:s=repaired(s)
    tree=ast.parse(s);lines=s.splitlines(keepends=True);offsets=[0]
    for line in lines:offsets.append(offsets[-1]+len(line))
    edits=[]
    for node in ast.walk(tree):
        if not isinstance(node,ast.Constant) or not isinstance(node.value,str):continue
        old=node.value;new=old
        if name==DISPATCH and old=='future151to153_serial_receiver_binding_v21_20261009.json':new=META.name
        elif not old.endswith(('.json','.py')):
            new=re.sub(r'BF16Medium153_prior_complete_forecast_duplicate_audit_v(?:1|2|3|9)_20261009',
                'BF16Medium153_prior_complete_forecast_duplicate_audit_v10_20261009',new)
            new=new.replace('SparseAfter14829_round152_full_registration_v1_20261009','SparseAfter14829_round152_full_registration_v2_20261009')
            new=new.replace('BF16Medium78_round153_source_admission_v1_20261009','BF16Medium78_round153_source_admission_v2_20261009')
        if new!=old:
            assert node.lineno==node.end_lineno
            edits.append((offsets[node.lineno-1]+node.col_offset,offsets[node.end_lineno-1]+node.end_col_offset,repr(new)))
    for start,end,new in sorted(edits,reverse=True):s=s[:start]+new+s[end:]
    return s

def execute(name,phase=None):
    import bind_future_import_namespaces_v38_20261009 as runtime
    import prepare_BF16Medium78_round153_sources_v1_20261009 as generator
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    original_route,original_read,original_paths=runtime.routed,runtime.read,generator.source_paths
    runtime.routed=lambda number,s:adjusted(s,name,original_route) if number==153 else original_route(number,s)
    def metadata(path):
        value=original_read(path)
        if Path(path)==runtime.META:
            value=deepcopy(value);value['drivers']['153']=m['drivers']['153'];value['receiver_specs']=m['receiver_specs']
            value['input_sha256'].update(m['input_sha256']);value['input_sha256'][str(META)]=sha(META)
        return value
    runtime.read=metadata
    generator.source_paths=lambda:list(dict.fromkeys([*original_paths(),Path(__file__),META,
        A/'BF16Medium153_actual_receiver_dispatch_controls_v42_20261009.json',*(A/d for d in m['drivers']['153'].values()),
        A/'bind_BF16Medium153_registration_guard_labels_v41_20261009.py',A/'BF16Medium153_actual_guard_label_controls_v41_20261009.json']))
    try:runtime.execute(153,name,phase)
    finally:runtime.routed,runtime.read,generator.source_paths=original_route,original_read,original_paths

def main():
    import bind_future_import_namespaces_v38_20261009 as runtime
    import verify_future_service_and_data_namespaces_v22_20261009 as previous
    import bind_future151to153_serial_receivers_v21_20261009 as earlier
    import prepare_BF16Medium78_round153_sources_v1_20261009 as generator
    previous.ORIGINAL_ROUTE=earlier.route;runtime.BASE_ROUTE=previous.routed
    old=read(runtime.META);drivers={};checks=[];sources=[Path(__file__),runtime.META,
        A/'BF16Medium153_registration_guard_labels_v41_20261009.json',
        A/'bind_BF16Medium153_registration_guard_labels_v41_20261009.py',
        A/'BF16Medium153_actual_guard_label_controls_v41_20261009.json',
        A/'BF16Medium78_prospective_routes_v1_20261009.json']
    for name in old['drivers']['153']:
        if 'prior_complete_forecast' in name:continue
        original=(A/name).read_text(encoding='utf8');s=adjusted(original,name,runtime.routed)
        compile(s,str(A/name),'exec');tree=ast.parse(s)
        constants=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        gates=[c for c in constants if re.fullmatch(r'(?:BF16Medium|SparseAfter148|actual_BF16).*_20261009',c)]
        assert not any('prior_complete_forecast_duplicate_audit_v2_' in c for c in gates)
        if name==DISPATCH:assert META.name in constants
        if name.startswith('verify_'):assert 'BF16Medium153_prior_complete_forecast_duplicate_audit_v10_20261009' in constants
        target=A/re.sub(r'_v\d+_20261009.py$','_actual_v42_20261009.py',name)
        code='from bind_BF16Medium153_actual_receiver_dispatch_v42_20261009 import execute\n'
        if name.startswith('publish_'):
            code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(name)+",p.parse_args().phase)\n"
        else:code+="if __name__=='__main__':execute("+repr(name)+")\n"
        compile(code,str(target),'exec')
        with target.open('x',encoding='utf8') as f:f.write(code)
        drivers[name]=target.name;sources.extend((A/name,target));checks.append({'source':name,'actual_driver':target.name,'gates':gates,'compiled':True})
    specs=[]
    for sid,driver,args in old['receiver_specs']:
        name=next(n for n,d in old['drivers']['153'].items() if d==driver)
        sid=sid.replace('round153_source_admission_v1_','round153_source_admission_v2_')
        specs.append([sid,drivers[name],args])
    import hashlib
    generated={str(y):{n:hashlib.sha256(s.encode()).hexdigest() for n,s in generator.generate(y).items()} for y in range(148,153)}
    assert generated==read(A/'BF16Medium78_prospective_routes_v1_20261009.json')['generated_source_sha256']
    proof=A/'BF16Medium153_actual_receiver_dispatch_controls_v42_20261009.json'
    create(proof,{'status':'passed_actual_seven153_dispatch_bindings_and40_scientific_programs_preserved',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'checks':checks,'receiver_specs':specs,'all40_generated_sources_byte_exact':True,
        'failed_admission1_and_dispatch41_preserved':True,'scientific_jobs_restarted':0,'new_quality_scores':0,'test_labels_read':False})
    sources.append(proof)
    create(META,{'status':'prepared_actual153_dispatch_receivers_after_old_namespace_admission_failed_before_quality',
        'input_sha256':{str(p):sha(p) for p in sources},'drivers':{'153':drivers},'receiver_specs':specs,
        'expected_quality_cases':78,'QA_version':64,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('BF16Medium153_complete_chronological_dispatch_actual_v42_20261009',drivers[DISPATCH],[],{str(META):sha(META)})
    create(A/'BF16Medium153_actual_receiver_dispatch_hidden_launch_v42_20261009.json',row)
    print({'new_dispatch_worker':row['owned_worker_pid'],'science_programs_unchanged':40,'receivers':len(specs)},flush=True)
if __name__=='__main__':main()
