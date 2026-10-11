"""Preserve seven live receivers; recover the failed exclusive administrative output path."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    plan_path=A/'SpectralGram140_complete_dependency_plan_v3_20261008.json';plan=read(plan_path)
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    jobs=plan['jobs'];launches={}
    for name,driver,args in jobs[:-1]:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
        assert owned(row) and row['actual_native_console_handle']==0 and (folder/'stderr.log').stat().st_size==0,name
        launches[name]=row
    failed_name=jobs[-1][0];failed=A/'service_owned_workflows_20261006'/failed_name
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    assert read(failed/'service_execution.json')['failure'].startswith('FileExistsError:')
    assert not any((A/'SpectralGram52_official_comparison_v1_20261008').iterdir())
    source=A/'run_SpectralGram52_round140_full_registration_v2_20261008.py';target=A/'run_SpectralGram52_round140_full_registration_v3_20261008.py'
    replacements={'SpectralGram52_round140_actual_registration_v1_20261008':'SpectralGram52_round140_actual_registration_v3_20261008',
        'run_SpectralGram52_round140_full_registration_v1_file_IO_20261008':'run_SpectralGram52_round140_full_registration_v3_file_IO_20261008'}
    text=source.read_text(encoding='utf8');updated=text
    for before,after in replacements.items():
        assert before in updated;updated=updated.replace(before,after)
    normalized=ast.parse(text)
    for node in ast.walk(normalized):
        if isinstance(node,ast.Constant) and isinstance(node.value,str):
            for before,after in replacements.items():node.value=node.value.replace(before,after)
    assert ast.dump(normalized)==ast.dump(ast.parse(updated))
    assert not target.exists();target.write_text(updated,encoding='utf8',newline='\n')
    recovery=A/'SpectralGram140_registration_admin_path_recovery_v4_20261008.json'
    files=[Path(__file__),plan_path,source,target,failed/'native_launch.json',failed/'job_definition.json',failed/'service_execution.json',failed/'stderr.log']
    create(recovery,{'status':'passed_constant_only_fresh_registration_output_paths_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in files},
        'constant_mapping':replacements,'AST_math_and_control_flow_unchanged':True,'preserved_seven_live_receivers':list(launches),
        'new_quality_scores':0,'new_future_X_calls':0,'test_labels_read':False})
    pins={**plan['input_sha256'],**{str(p):sha(p) for p in [*files,recovery]}}
    name='SpectralGram52_round140_full_registration_v3_20261008'
    launches[name]=start(name,target.name,[],pins)
    create(A/'SpectralGram140_complete_hidden_launches_v4_20261008.json',{
        'status':'started_eight_lazy140_receivers_with_preserved_science2_and_fresh_registration3',
        'launches':launches,'input_sha256':pins,'round':140,'expected_official_cases':52,'QA_version':51,
        'science_receiver_version':2,'registration_receiver_version':3,'administrative_dispatch_version':4,
        'new_quality_scores_by_dispatch':0,'new_fits_by_dispatch':0,'test_labels_read':False})
    print('Seven live science2 receivers preserved; fresh registration3 completes eight-step140 pipeline.',flush=True)

if __name__=='__main__':main()
