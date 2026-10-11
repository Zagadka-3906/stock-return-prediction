"""Real overlapping Windows processes must acquire and release the same named mutex serially."""
from pathlib import Path
import sys,subprocess,time,json,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read
OUT=Path('E:/赛题五_本机临时/serial_main_publication_mutex_controls_v1_20261009')

def main():
    import serial_main_publication_mutex_v1_20261009 as module
    OUT.mkdir(exist_ok=False)
    worker=OUT/'worker.py'
    code="import sys,time,json,os\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nfrom serial_main_publication_mutex_v1_20261009 import MainPublicationMutex\nm=MainPublicationMutex('Local\\\\SaiTi5_MainMutex_actual_two_process_control_20261009');started=time.time();m.acquire();a=time.time();time.sleep(1.5);b=time.time();m.close();Path(sys.argv[2]).write_text(json.dumps({'pid':os.getpid(),'started':started,'acquired':a,'released':b,'events':m.events}))\n"
    worker.write_text(code,encoding='utf8')
    rows=[]
    for i in range(2):
        p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(worker),str(A),str(OUT/f'worker{i}.json')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
        rows.append(p)
    for p in rows:
        stdout,stderr=p.communicate(timeout=20);assert p.returncode==0,stderr.decode()
    result=sorted([read(OUT/f'worker{i}.json') for i in range(2)],key=lambda r:r['acquired'])
    assert result[1]['started']<result[0]['released'] and result[1]['acquired']>=result[0]['released']
    assert result[1]['events'][0]['wait_seconds']>1.
    pins={str(p):sha(p) for p in (Path(__file__),Path(module.__file__),worker)}
    create(OUT/'verification.json',{'status':'passed_actual_two_overlapping_hidden_Windows_processes_serial_named_mutex',
      'input_sha256':pins,'records':result,'acquisition_intervals_nonoverlapping':True,'second_process_waited_while_first_owned':True,
      'actual_git_mutations_by_test':0,'test_labels_read':False})
    create(A/'serial_main_publication_mutex_v1_20261009.json',{'status':'passed_actual_two_process_serial_publication_lock','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'input_sha256':pins})
    print({'overlapping_processes':2,'maximum_simultaneous_mutex_owners':1,'hidden_children':True},flush=True)

if __name__=='__main__':main()
