"""Fresh exclusive selected output/scoring paths and complete post-generation route checks."""
from pathlib import Path
import sys,subprocess,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(name,value):
    p=A/name;assert not p.exists(),p;compile(value,str(p),'exec');p.write_text(value,encoding='utf8',newline='\n');return p
def main():
    assert read(A/'service_owned_workflows_20261006/ConeRidgeAlpha100_selected_candidate_preparation_v7_20261008/service_execution.json')['status']=='failed'
    outputs=[]
    old=A/'ConeRidgeAlpha144_storage_v4_20261008.py';value=old.read_text(encoding='utf8');value=value.replace('OUTPUTS = {',"OUTPUTS = {\n    ROOT/'candidates/ConeRidgeAlpha100_v3_20261008': EBASE/'candidate_v3',\n    ROOT/'analysis/ConeRidgeAlpha100_selected_release_v3_20261008': EBASE/'selected_release_v3',")
    outputs.append(save('ConeRidgeAlpha144_storage_v5_20261008.py',value))
    from ConeRidgeAlpha144_storage_v5_20261008 import OUTPUTS,empty
    for logical,target in OUTPUTS.items():
        if logical.name not in ('ConeRidgeAlpha100_v3_20261008','ConeRidgeAlpha100_selected_release_v3_20261008'):continue
        assert not logical.exists() and not target.exists();target.mkdir()
        command="New-Item -ItemType Junction -Path '"+str(logical).replace("'","''")+"' -Target '"+str(target).replace("'","''")+"' | Out-Null"
        r=subprocess.run(['powershell.exe','-NoLogo','-NoProfile','-NonInteractive','-Command',command],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert r.returncode==0,r.stderr;empty(logical)
    maps={'ConeRidgeAlpha100_selected_release_v2_20261008':'ConeRidgeAlpha100_selected_release_v3_20261008','ConeRidgeAlpha100_v2_20261008':'ConeRidgeAlpha100_v3_20261008','ConeRidgeAlpha144_storage_v4_20261008':'ConeRidgeAlpha144_storage_v5_20261008','prepare_ConeRidgeAlpha100_round144_sources_v5_20261008':'prepare_ConeRidgeAlpha100_round144_sources_v6_20261008','ConeRidgeAlpha100_round144_source_admission_v5_20261008':'ConeRidgeAlpha100_round144_source_admission_v6_20261008','ConeRidgeAlpha100_round144_source_preparation_v5_20261008':'ConeRidgeAlpha100_round144_source_preparation_v6_20261008'}
    def adapt(value):
        for before,after in maps.items():value=value.replace(before,after)
        return value
    for role in ('prepare','seal'):
        value=adapt((A/f'{role}_ConeRidgeAlpha100_selected_candidate_v7_20261008.py').read_text(encoding='utf8')).replace('ConeRidgeAlpha100_selected_candidate_preparation_v7_20261008','ConeRidgeAlpha100_selected_candidate_preparation_v8_20261008')
        value=value.replace('pre_inference_source_freeze_v2','pre_inference_source_freeze_v3').replace('ConeRidgeAlpha144_D_scoring_v5_20261008/selected/scoring_validation_only','ConeRidgeAlpha144_D_scoring_v5_20261008/selected_v3/scoring_validation_only')
        outputs.append(save(f'{role}_ConeRidgeAlpha100_selected_candidate_v8_20261008.py',value))
    routes={'ConeRidgeAlpha100_selected_release_v1_20261008':'ConeRidgeAlpha100_selected_release_v3_20261008','ConeRidgeAlpha100_v1_20261008':'ConeRidgeAlpha100_v3_20261008','ConeRidgeAlpha144_storage_v3_20261008':'ConeRidgeAlpha144_storage_v5_20261008','prepare_ConeRidgeAlpha100_round144_sources_v4_20261008':'prepare_ConeRidgeAlpha100_round144_sources_v6_20261008','ConeRidgeAlpha100_round144_source_admission_v4_20261008':'ConeRidgeAlpha100_round144_source_admission_v6_20261008','ConeRidgeAlpha100_round144_source_preparation_v4_20261008':'ConeRidgeAlpha100_round144_source_preparation_v6_20261008','ConeRidgeAlpha100_scores_github_v1_20261008':'ConeRidgeAlpha100_scores_github_v2_20261008'}
    generator='''from pathlib import Path
import hashlib,time
import prepare_ConeRidgeAlpha100_round144_sources_v4_20261008 as original
from run_dependency_queue_v3_20261006 import read,sha,create
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
ROUTES=ROUTES_LITERAL
def routed(text):
    for before,after in ROUTES.items():text=text.replace(before,after)
    return text
def generate(parent):
    values={name:routed(text) for name,text in original.generate(parent).items()}
    for name,text in values.items():
        assert 'ConeRidgeAlpha100_selected_release_v1_20261008' not in text and 'ConeRidgeAlpha100_selected_release_v2_20261008' not in text,name
        compile(text,name,'exec')
    return values
def source_paths():
    paths=[Path(routed(str(p))) for p in original.source_paths()]
    extra=[Path(__file__),A/'recover144_fresh_selected_scoring_and_source_routes_v2_20261008.py',A/'short_content_addressed_native_storage_v1_20261008.py',A/'prepare_ConeRidgeAlpha100_selected_candidate_v8_20261008.py',A/'seal_ConeRidgeAlpha100_selected_candidate_v8_20261008.py',A/'run_ConeRidgeAlpha100_round144_full_registration_v9_20261008.py',A/'connected_API_full_round_transport_v1_20261008.py']
    for name in ('ConeRidgeAlpha100_selected_candidate_preparation_v8_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v8_20261008'):
        folder=A/'service_owned_workflows_20261006'/name;extra.extend(folder.glob('*.json'));extra.extend(folder.glob('*.log'))
    return list(dict.fromkeys([*paths,*extra]))
def main():
    ready_path=A/'ConeRidgeAlpha100_selected_release_v3_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual100_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'ConeRidgeAlpha100_official_comparison_v5_20261008/verification.json');assert len(pilot['records'])==100 and pilot['best']==ready['best']
    proof_path=A/'ConeRidgeAlpha100_round144_source_admission_v6_20261008.json';proof=read(proof_path)
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name],name
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\\n')
    create(A/'ConeRidgeAlpha100_round144_source_preparation_v6_20261008.json',{'status':'passed_actual100_sealed_candidate_and_admitted_full144_QA55_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':144,'scored_records':100,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
'''.replace('ROUTES_LITERAL',repr(routes))
    outputs.append(save('prepare_ConeRidgeAlpha100_round144_sources_v6_20261008.py',generator))
    source=A/'verify_ConeRidgeAlpha100_prospective_routes_v7_20261008.py';value=adapt(source.read_text(encoding='utf8')).replace('ConeRidgeAlpha100_prospective_routes_v5_20261008.json','ConeRidgeAlpha100_prospective_routes_v6_20261008.json').replace('ConeRidgeAlpha144_receiver_preparation_v5_20261008.json','ConeRidgeAlpha144_receiver_preparation_v6_20261008.json').replace('cross_volume_byte_probe_v7','cross_volume_byte_probe_v8').replace('prepare_ConeRidgeAlpha100_selected_candidate_v7_20261008.py','prepare_ConeRidgeAlpha100_selected_candidate_v8_20261008.py')
    outputs.append(save('verify_ConeRidgeAlpha100_prospective_routes_v8_20261008.py',value))
    from verify_ConeRidgeAlpha100_prospective_routes_v8_20261008 import main as preflight
    preflight()
    proof=read(A/'ConeRidgeAlpha100_prospective_routes_v6_20261008.json');assert proof['actual_graph_controls']==2619
    original=read(A/'ConeRidgeAlpha100_round144_source_admission_v4_20261008.json')
    for p,d in original['input_sha256'].items():assert sha(p)==d,p
    pins={**original['input_sha256'],**proof['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),*outputs,A/'short_content_addressed_native_storage_v1_20261008.py']}}
    create(A/'ConeRidgeAlpha100_round144_source_admission_v6_20261008.json',{**original,'input_sha256':pins,'generated_source_sha256':proof['generated_source_sha256'],'selected_output_storage_recovery_version':3,'actual24_generated_sources_complete_fresh_selected_release_paths_verified':True,'new_quality_scores':0})
    value=adapt((A/'run_ConeRidgeAlpha100_round144_full_registration_v8_20261008.py').read_text(encoding='utf8')).replace('actual_registration_v8_20261008','actual_registration_v9_20261008').replace('full_registration_v8_file_IO_20261008','full_registration_v9_file_IO_20261008').replace('ConeRidgeAlpha100_selected_candidate_sealing_v7_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v8_20261008')
    outputs.append(save('run_ConeRidgeAlpha100_round144_full_registration_v9_20261008.py',value))
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[('ConeRidgeAlpha100_selected_candidate_preparation_v8_20261008','prepare_ConeRidgeAlpha100_selected_candidate_v8_20261008.py'),('ConeRidgeAlpha100_selected_candidate_sealing_v8_20261008','seal_ConeRidgeAlpha100_selected_candidate_v8_20261008.py'),('ConeRidgeAlpha100_round144_full_registration_v9_20261008','run_ConeRidgeAlpha100_round144_full_registration_v9_20261008.py')]
    launches={n:start(n,driver,[],{}) for n,driver in jobs};create(A/'actual144_selected_fresh_routes_launches_v2_20261008.json',{'launches':launches,'input_sha256':{str(p):sha(p) for p in [Path(__file__),*outputs]},'new_quality_scores':0})
    print(json.dumps({'started':list(launches)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
