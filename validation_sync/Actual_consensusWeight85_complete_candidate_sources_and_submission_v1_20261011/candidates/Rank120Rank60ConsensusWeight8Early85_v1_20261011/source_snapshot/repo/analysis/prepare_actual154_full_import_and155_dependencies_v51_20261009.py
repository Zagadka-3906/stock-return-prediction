"""Repair exact executable imports and service identities without changing artifact filenames."""
from pathlib import Path
from copy import deepcopy
import sys,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def write(name,text):
    ast.parse(text);p=A/name
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p

def gates(text,mapping):
    class Routes(ast.NodeTransformer):
        def visit_Constant(self,node):
            if isinstance(node.value,str) and node.value in mapping:
                return ast.copy_location(ast.Constant(mapping[node.value]),node)
            return node
    tree=Routes().visit(ast.parse(text));ast.fix_missing_locations(tree)
    return ast.unparse(tree)+'\n'

def main():
    raw=A/'run_BF16TwoSeed79_round154_full_registration_v4_20261009.py'
    s=raw.read_text(encoding='utf8');assert s.count('BF16TwoSeed79_round154_actual_registration_v3_20261009')==1
    s=s.replace('BF16TwoSeed79_round154_actual_registration_v3_20261009','BF16TwoSeed79_round154_actual_registration_v4_20261009')
    raw_new=write('run_BF16TwoSeed79_round154_full_registration_v5_20261009.py',s)
    original=A/'run_BF16TwoSeed154_safe_registration_v5_20261009.py';s=original.read_text(encoding='utf8')
    assert s.count('import run_BF16TwoSeed79_round154_full_registration_v2_20261009 as receiver')==1
    s=s.replace('import run_BF16TwoSeed79_round154_full_registration_v2_20261009 as receiver','import run_BF16TwoSeed79_round154_full_registration_v5_20261009 as receiver')
    s=s.replace("A/'run_BF16TwoSeed79_round154_full_registration_v4_20261009.py'","A/'run_BF16TwoSeed79_round154_full_registration_v5_20261009.py'")
    s=s.replace('/safe_full_main_v5','/safe_full_main_v6')
    s=s.replace('from run_dependency_queue_v3_20261006 import read,sha','from run_dependency_queue_v3_20261006 import read,sha,owned,create\nimport time')
    assert s.count('def main():')==1
    s=s.replace('def main():',"def main():\n    old=A/'service_owned_workflows_20261006/BF16TwoSeed79_round154_full_registration_v1_20261009'\n    while owned(read(old/'native_launch.json')):time.sleep(5)\n    assert read(old/'service_execution.json')['status']=='failed'\n    assert not (A/'optimization_20261003_r154/full_registration_execution.json').exists()\n    create(A/'BF16TwoSeed154_full_import_recovery_original_failure_v51_20261009.json',read(old/'service_execution.json'))")
    full=write('run_BF16TwoSeed154_safe_registration_v6_20261009.py',s)
    oldmeta=A/'BF16Seed10_155_complete_pipeline_preparation_v2_20261009.json';newmeta=A/'BF16Seed10_155_complete_pipeline_preparation_v3_20261009.json'
    mapping={'BF16TwoSeed79_round154_full_registration_v1_20261009':'BF16TwoSeed79_round154_full_registration_v2_20261009',
        'BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009':'BF16Seed10_155_prior_complete_forecast_duplicate_audit_v2_20261009'}
    pairs=[('verify_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.py','verify_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v2_20261009.py'),
        ('verify_BF16Seed10_80_round155_sources_current153_v2_20261009.py','verify_BF16Seed10_80_round155_sources_current154_v3_20261009.py'),
        ('publish_BF16Seed10_80_evidence_v1_20261009.py','publish_BF16Seed10_80_evidence_v2_20261009.py'),
        ('run_BF16Seed10_80_round155_full_registration_v1_20261009.py','run_BF16Seed10_80_round155_full_registration_v2_20261009.py'),
        ('run_BF16Seed10_155_safe_registration_v2_20261009.py','run_BF16Seed10_155_safe_registration_v3_20261009.py'),
        ('dispatch_BF16Seed10_155_complete_pipeline_v2_20261009.py','dispatch_BF16Seed10_155_complete_pipeline_v3_20261009.py')]
    files=[Path(__file__),raw,raw_new,original,full,oldmeta];drivers={}
    for old,new in pairs:
        src=A/old;s=gates(src.read_text(encoding='utf8'),mapping)
        s=s.replace(oldmeta.name,newmeta.name)
        if 'safe_registration' in new:
            s=s.replace('import run_BF16Seed10_80_round155_full_registration_v1_20261009 as receiver','import run_BF16Seed10_80_round155_full_registration_v2_20261009 as receiver')
            s=s.replace('/safe_full_main_v2','/safe_full_main_v3')
        if new.startswith('publish_'):s=s.replace("'safe_' + phase + '_main_v1'","'safe_' + phase + '_main_v2'")
        if new.startswith('dispatch_'):s=s.replace('BF16Seed10_155_complete_hidden_launches_v2_20261009.json','BF16Seed10_155_complete_hidden_launches_v3_20261009.json')
        dst=write(new,s);files.extend((src,dst));drivers[old]=new
    m=deepcopy(read(oldmeta));m['receiver_specs']=[[sid,drivers.get(driver,driver),args] for sid,driver,args in m['receiver_specs']]
    m['input_sha256'].update({str(p):sha(p) for p in files});m.update(status='prepared155_actual154_full2_dependencies_and_exact_safe_receiver_imports',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),scientific_configuration_changed=False)
    create(newmeta,m)
    routes={'run_BF16TwoSeed154_safe_registration_v6_20261009.py':'run_BF16TwoSeed79_round154_full_registration_v5_20261009',
        'run_BF16Seed10_155_safe_registration_v3_20261009.py':'run_BF16Seed10_80_round155_full_registration_v2_20261009'}
    controls=[]
    for name,target in routes.items():
        tree=ast.parse((A/name).read_text(encoding='utf8'))
        imports=[n.name for n in ast.walk(tree) if isinstance(n,ast.alias) and n.asname=='receiver']
        assert imports==[target],(name,imports);controls.append({'wrapper':name,'actual_receiver_import':target,'passed':True})
    for old,new in pairs:
        if 'safe_registration' in new:continue
        tree=ast.parse((A/new).read_text(encoding='utf8'));strings=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        assert 'BF16TwoSeed79_round154_full_registration_v1_20261009' not in strings
        if 'prior_complete_forecast_duplicate' in new:
            assert 'actual_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.json' in strings
        controls.append({'source':new,'obsolete_exact_service_gate_absent':True,'canonical_pointer_filenames_preserved':True})
    create(A/'actual154_full_import_and155_dependency_controls_v51_20261009.json',{'status':'passed_exact_AST_receiver_imports_and_service_only_routes','controls':controls,'input_sha256':{str(p):sha(p) for p in files+[newmeta]},'new_quality_scores':0,'scientific_model_or_scoring_changed':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for name,driver in [('BF16TwoSeed79_round154_full_registration_v2_20261009',full.name),
        ('BF16Seed10_155_prior_complete_forecast_duplicate_audit_v2_20261009',pairs[0][1]),
        ('BF16Seed10_155_complete_chronological_dispatch_v3_20261009',pairs[-1][1])]:
        rows[name]=start(name,driver,[],{str(A/driver):sha(A/driver),str(newmeta):sha(newmeta)})
    create(A/'actual154_full_import_and155_recovery_launches_v51_20261009.json',{'launches':rows,'scientific_jobs_stopped_or_restarted':0,'old_failed_versions_preserved':True})
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
