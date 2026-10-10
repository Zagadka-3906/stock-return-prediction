"""Retire only lazy135 waiters before scores; fresh receivers retain D scoring and E large outputs."""
from pathlib import Path
import ast,hashlib,sys,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def main():
    proof_path=A/'actual_BF16wide135_D_scoring_receiver_recovery_v3_20261008.json';assert not proof_path.exists()
    old_launch_path=A/'BF16wide135_complete_hidden_launches_v1_20261008.json';old=read(old_launch_path)['launches']
    from BF16wide135_storage_v1_20261008 import OUTPUTS,empty
    for path in OUTPUTS:empty(path)
    train_path=A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json'
    train=read(train_path);assert owned(train)
    diagnostic=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    audited={};pairs=[]
    for name,row in old.items():
        assert owned(row)
        folder=A/'service_owned_workflows_20261006'/name
        assert not (folder/'service_execution.json').exists()
        dump=subprocess.run([str(diagnostic),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,
            encoding='utf8',errors='replace',timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
        inline_seal=(name=='BF16wide40_selected_candidate_sealing_v1_20261008' and '    main (seal_BF16wide40_selected_candidate_v1_20261008.py:13)' in dump.stdout)
        assert dump.returncode==0 and ('closed (' in dump.stdout or inline_seal),(name,dump.stdout,dump.stderr)
        worker,parent=psutil.Process(row['owned_worker_pid']),psutil.Process(row['pid'])
        assert parent.create_time()==row['owned_parent_creation_time'] and worker.parent().pid==parent.pid
        assert worker.memory_info().rss<256*2**20 and worker.create_time()==row['owned_worker_creation_time']
        audited[name]={'identity':row,'actual_lazy_dependency_stack':dump.stdout,'retired_before_quality_or_future_X':True}
        pairs.append((parent,worker))
    file_names=['prepare_BF16wide40_round135_sources','run_BF16wide40_official_comparison',
        'prepare_BF16wide40_selected_candidate','seal_BF16wide40_selected_candidate',
        'run_BF16wide40_round135_full_registration','verify_BF16wide40_prospective_routes',
        'verify_BF16wide40_round135_sources','publish_BF16wide40_evidence','queue_BF16wide135_complete_pipeline',
        'record_BF16wide135_receiver_preparation']
    files={stem+'_v1_20261008.py':stem+'_v2_20261008.py' for stem in file_names}
    mapping={old_name:new_name for old_name,new_name in files.items()}
    mapping.update({old_name.removesuffix('.py'):new_name.removesuffix('.py') for old_name,new_name in files.items()})
    for name in old:mapping[repr(name)]=repr(name.replace('_v1_20261008','_v2_20261008'))
    for stem in ('BF16wide40_prospective_routes','BF16wide135_receiver_preparation','BF16wide40_round135_source_admission',
        'BF16wide40_round135_source_preparation','BF16wide40_controls_github','BF16wide40_scores_github',
        'BF16wide135_complete_dependency_plan','BF16wide135_complete_hidden_launches'):
        mapping[stem+'_v1_20261008']=stem+'_v2_20261008'
    outputs={}
    for previous,new in files.items():
        text=(A/previous).read_text(encoding='utf8');text=substitute(text,mapping)
        # Service identities change, but both physical E outputs remain the original exact empty junctions.
        text=text.replace("OUT=A/'BF16wide40_official_comparison_v2_20261008'","OUT=A/'BF16wide40_official_comparison_v1_20261008'")
        text=text.replace("folder=A/'BF16wide40_official_comparison_v2_20261008'","folder=A/'BF16wide40_official_comparison_v1_20261008'")
        if previous.startswith('run_BF16wide40_official_comparison'):
            before="scoring=OUT/'scoring_validation_only';scoring.mkdir()"
            after="scoring=A/'BF16wide135_D_scoring_v2_20261008/comparison/scoring_validation_only';scoring.mkdir(parents=True)"
            assert text.count(before)==1;text=text.replace(before,after)
        if previous.startswith('prepare_BF16wide40_selected_candidate'):
            before="scoring=OUT/'scoring_validation_only';scoring.mkdir()"
            after="scoring=A/'BF16wide135_D_scoring_v2_20261008/selected/scoring_validation_only';scoring.mkdir(parents=True)"
            assert text.count(before)==1;text=text.replace(before,after)
        if previous.startswith('verify_BF16wide40_prospective_routes'):
            text=text.replace('BF16wide135_transfer_probe_v1_20261008.bin','BF16wide135_transfer_probe_v2_20261008.bin')
            text=text.replace("/transfer_probe.bin'","/transfer_probe_v2.bin'")
            marker='    names += [source,target]'
            text=text.replace(marker,marker+"\n    from verify_BF16wide135_D_scoring_scope_v2_20261008 import main as scope_checks\n    scope_checks()\n    names += [A/'verify_BF16wide135_D_scoring_scope_v2_20261008.py',A/'BF16wide135_D_scoring_scope_v2_20261008.json',A/'actual_BF16wide135_D_scoring_receiver_recovery_v3_20261008.json']")
        if previous.startswith('prepare_BF16wide40_round135_sources'):
            text=text.replace("names=[Path(__file__).name,", "names=[Path(__file__).name,'verify_BF16wide135_D_scoring_scope_v2_20261008.py','BF16wide135_D_scoring_scope_v2_20261008.json','actual_BF16wide135_D_scoring_receiver_recovery_v3_20261008.json',")
        if previous.startswith('run_BF16wide40_round135_full_registration'):
            text=text.replace('BF16wide40_round135_actual_registration_v1_20261008','BF16wide40_round135_actual_registration_v2_20261008')
            text=text.replace('run_BF16wide40_round135_full_registration_v1_file_IO_20261008','run_BF16wide40_round135_full_registration_v2_file_IO_20261008')
        if previous.startswith('queue_BF16wide135'):
            text=text.replace('source_paths' , 'source_paths')
        assert not (A/new).exists();compile(text,str(A/new),'exec');outputs[A/new]=text
    for parent,worker in pairs:
        assert worker.is_running() and parent.is_running()
        worker.terminate();parent.terminate()
    gone,alive=psutil.wait_procs([p for pair in pairs for p in pair],timeout=5)
    assert not alive
    assert owned(train),'Never stop or restart the live annual fitter.'
    for path in OUTPUTS:empty(path)
    for p,text in outputs.items():p.write_text(text,encoding='utf8',newline='\n')
    create(proof_path,{'status':'retired_exact7_lazy135_waiters_before_quality_and_prepared_fresh_D_scoring_receivers',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_retired_waiters':audited,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old_launch_path,train_path,*outputs]},
        'changes':['Only comparison/selected scoring temporary directories stay on D, satisfying all original cache scope guards.',
            'Exact empty E model/release/alias/board junctions and all numerical transforms are retained.',
            'All scientific sources and original preflight/dispatch records remain immutable.'],
        'annual_fitter_identity_unchanged_and_live':train,'original_actual_quality_scores':0,'original_future_X_calls':0,
        'new_actual_D_scope_and24_receiver_preflight_still_required':True,'test_labels_read':False})
    print('Only seven verified lazy135 waiters retired; actual fitter remains live. Fresh D-scoring receivers prepared.',flush=True)


if __name__=='__main__':main()
