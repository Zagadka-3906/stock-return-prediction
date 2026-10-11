"""Replace only incomplete lazy2 dispatch; qualify all service path references before any new scoring."""
from pathlib import Path
import ast,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def main():
    proof_path=A/'actual_BF16wide135_complete_dependency_recovery_v5_20261008.json';assert not proof_path.exists()
    old_plan=A/'BF16wide135_complete_dependency_plan_v2_20261008.json';jobs=read(old_plan)['jobs']
    from BF16wide135_storage_v1_20261008 import OUTPUTS,empty
    for path in OUTPUTS:empty(path)
    train_path=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json';train=read(train_path);assert owned(train)
    audited={};pairs=[]
    for name,_,_ in jobs:
        folder=A/'service_owned_workflows_20261006'/name
        if not (folder/'native_launch.json').exists():continue
        row=read(folder/'native_launch.json')
        if not owned(row):
            assert read(folder/'service_execution.json')['status']=='failed' and 'sealing' in name
            audited[name]={'identity':row,'original_failed':read(folder/'service_execution.json')};continue
        dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],
            capture_output=True,text=True,encoding='utf8',errors='replace',timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
        assert dump.returncode==0 and 'closed (' in dump.stdout,(name,dump.stdout)
        worker,parent=psutil.Process(row['owned_worker_pid']),psutil.Process(row['pid'])
        assert worker.memory_info().rss<256*2**20 and parent.create_time()==row['owned_parent_creation_time'] and worker.parent().pid==parent.pid
        pairs.append((parent,worker));audited[name]={'identity':row,'actual_lazy_dependency_stack':dump.stdout}
    assert len(pairs)==5
    stems=['prepare_BF16wide40_round135_sources','run_BF16wide40_official_comparison','prepare_BF16wide40_selected_candidate',
        'seal_BF16wide40_selected_candidate','run_BF16wide40_round135_full_registration','verify_BF16wide40_round135_sources',
        'publish_BF16wide40_evidence','queue_BF16wide135_complete_pipeline','record_BF16wide135_receiver_preparation']
    files={stem+'_v2_20261008.py':stem+'_v3_20261008.py' for stem in stems}
    files['verify_BF16wide40_prospective_routes_v3_20261008.py']='verify_BF16wide40_prospective_routes_v4_20261008.py'
    mapping={**files,**{o.removesuffix('.py'):n.removesuffix('.py') for o,n in files.items()}}
    mapping['verify_BF16wide40_prospective_routes_v2_20261008']='verify_BF16wide40_prospective_routes_v4_20261008'
    for name,_,_ in jobs:mapping[name]=name.replace('_v2_20261008','_v3_20261008')
    for stem in ('BF16wide40_prospective_routes','BF16wide135_receiver_preparation','BF16wide40_round135_source_admission',
        'BF16wide40_round135_source_preparation','BF16wide40_controls_github','BF16wide40_scores_github',
        'BF16wide135_complete_dependency_plan','BF16wide135_complete_hidden_launches'):
        mapping[stem+'_v2_20261008']=stem+'_v3_20261008'
    outputs={}
    for previous,new in files.items():
        text=substitute((A/previous).read_text(encoding='utf8'),mapping)
        text=text.replace("OUT=A/'BF16wide40_official_comparison_v3_20261008'","OUT=A/'BF16wide40_official_comparison_v1_20261008'")
        text=text.replace("folder=A/'BF16wide40_official_comparison_v3_20261008'","folder=A/'BF16wide40_official_comparison_v1_20261008'")
        if previous.startswith('seal_'):
            text=text.replace('service_owned_workflows_20261006/BF16wide40_selected_candidate_preparation_v1_20261008',
                'service_owned_workflows_20261006/BF16wide40_selected_candidate_preparation_v3_20261008')
        if previous.startswith('verify_BF16wide40_prospective'):
            text=text.replace('BF16wide135_transfer_probe_v2_20261008.bin','BF16wide135_transfer_probe_v3_20261008.bin')
            text=text.replace('/transfer_probe_v2.bin','/transfer_probe_v3.bin')
            text=text.replace("    names += [source,target]","    names += [source,target,A/'actual_BF16wide135_complete_dependency_recovery_v5_20261008.json']")
        if previous.startswith('prepare_BF16wide40_round135_sources'):
            text=text.replace("names=[Path(__file__).name,","names=[Path(__file__).name,'actual_BF16wide135_complete_dependency_recovery_v5_20261008.json',")
        if previous.startswith('run_BF16wide40_round135_full_registration'):
            text=text.replace('BF16wide40_round135_actual_registration_v2_20261008','BF16wide40_round135_actual_registration_v3_20261008')
            text=text.replace('run_BF16wide40_round135_full_registration_v2_file_IO_20261008','run_BF16wide40_round135_full_registration_v3_file_IO_20261008')
        assert not (A/new).exists();compile(text,str(A/new),'exec')
        for node in ast.walk(ast.parse(text)):
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.startswith('service_owned_workflows_20261006/BF16wide40_'):
                assert node.value.endswith('_v3_20261008'),node.value
        outputs[A/new]=text
    for parent,worker in pairs:worker.terminate();parent.terminate()
    _,alive=psutil.wait_procs([p for pair in pairs for p in pair],timeout=5);assert not alive
    assert owned(train)
    for path in OUTPUTS:empty(path)
    for p,text in outputs.items():p.write_text(text,encoding='utf8',newline='\n')
    create(proof_path,{'status':'retired_exact5_incomplete_lazy2_waiters_preserved_failed_seal_and_prepared_complete3_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'audited_old_jobs':audited,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old_plan,train_path,*outputs]},
        'actual_retired_lazy_waiters':5,'annual_fitter_unchanged_live':train,'all_explicit_new_service_path_references_use3':True,
        'original_quality_scores':0,'original_future_X_calls':0,'new24_receiver_and_dependency_checks_required':True,'test_labels_read':False})
    print('Five lazy2 waiters retired; failed seal preserved. Complete3 sources use consistent service references.',flush=True)


if __name__=='__main__':main()
