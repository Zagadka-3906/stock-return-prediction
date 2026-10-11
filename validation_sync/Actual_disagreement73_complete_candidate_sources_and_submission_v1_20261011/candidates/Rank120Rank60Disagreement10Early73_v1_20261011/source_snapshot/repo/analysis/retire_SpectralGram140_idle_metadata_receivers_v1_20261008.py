"""Retire only exact-owned idle140 receivers before quality; preserve all frozen evidence."""
from pathlib import Path
import subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    proof_path=A/'SpectralGram52_prospective_routes_v2_20261008.json';proof=read(proof_path)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==882
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    assert not any((A/'SpectralGram52_official_comparison_v1_20261008').iterdir())
    assert not Path('E:/赛题五_本机临时/SpectralGram49_current_parent_v1_20261008').exists()
    fitter=read(A/'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/native_launch.json');assert owned(fitter)
    launch_path=A/'SpectralGram140_complete_hidden_launches_v1_20261008.json';launches=read(launch_path)['launches'];assert len(launches)==8
    audits={};pairs=[]
    for name,row in launches.items():
        assert owned(row) and Path(row['stderr']).stat().st_size==0,name
        dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
        assert dump.returncode==0
        assert '    closed (' in dump.stdout or ('    main (seal_' in dump.stdout) or ('    main (run_' in dump.stdout and '_full_registration_' in dump.stdout),(name,dump.stdout)
        worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid'])
        assert worker.memory_info().rss<256*2**20 and not worker.children()
        assert parent.create_time()==row['owned_parent_creation_time'] and worker.parent().pid==parent.pid
        audits[name]={'identity':row,'actual_idle_stack':dump.stdout};pairs.append((name,parent,worker))
    for name,parent,worker in reversed(pairs):
        row=audits[name]['identity'];assert owned(row) and parent.create_time()==row['owned_parent_creation_time']
        worker.terminate();worker.wait(timeout=10)
        try:
            if parent.is_running():
                assert parent.create_time()==row['owned_parent_creation_time'];parent.terminate();parent.wait(timeout=10)
        except psutil.NoSuchProcess:pass
        create(A/'service_owned_workflows_20261006'/name/'administrative_metadata_supersession_v1_20261008.json',{
            'status':'superseded_exact_owned_idle_receiver_before_first140_quality','original_identity':row,
            'reason':'Fresh2 receiver fields report the verified147 cold and24 calendar controls and clear the correct140 pending field.',
            'new_quality_scores':0,'training_workers_stopped':0,'shared_WMI_provider_untouched':True})
    assert owned(fitter)
    create(A/'SpectralGram140_exact_idle_metadata_supersession_v1_20261008.json',{
        'status':'passed_exact_eight_idle140_receivers_superseded_before_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'retired_receiver_audits':audits,'input_sha256':{str(p):sha(p) for p in [Path(__file__),proof_path,launch_path]},
        'original_gpu_fitter_still_owned':fitter,'training_workers_stopped':0,'new_quality_scores':0,'test_labels_read':False})
    print('Eight exact idle140 receivers retired; original GPU training and135139 queues preserved.',flush=True)

if __name__=='__main__':main()
