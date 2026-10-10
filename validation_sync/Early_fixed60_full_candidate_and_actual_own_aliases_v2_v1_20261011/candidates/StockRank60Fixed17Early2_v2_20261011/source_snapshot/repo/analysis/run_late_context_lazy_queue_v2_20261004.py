"""Wait without importing model libraries, then execute the verified V2 runner."""
from pathlib import Path
import hashlib
import json
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/'analysis/run_late_context_recovered_pipeline_v2_20261004.py'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(number,probe=False):
    assert 30<=number<=48
    if probe:
        assert not any(name in sys.modules for name in ('numpy','torch','polars','pandas','sklearn'))
        import psutil
        print(json.dumps({'status':'passed','round':number,'model_libraries_loaded':False,
            'python_rss_bytes':psutil.Process().memory_info().rss,'runner_sha256':sha(RUNNER),
            'queue_sha256':sha(Path(__file__))}),flush=True)
        return
    state_path=ROOT/f'analysis/ongoing_optimization_r{number}_state.json'
    gate=ROOT/f'results/optimization_20261003_r{number-1}.json'
    frozen={str(path.resolve()):sha(path) for path in (Path(__file__),RUNNER,
        ROOT/'analysis/late_context_initialization_recovery_v2_20261004/verification.json')}
    def state():
        state_path.write_text(json.dumps({'round':number,'stage':'waiting_for_previous_round_lightweight_queue',
            'status':'running','updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'continuous_optimization_authorized':True,'model_libraries_loaded':False,
            'test_labels_read':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state();last=time.monotonic()
    while not gate.exists():
        time.sleep(10)
        if time.monotonic()-last>=50:state();last=time.monotonic()
    for path,digest in frozen.items():assert sha(path)==digest,path
    audit=ROOT/f'analysis/late_context_lazy_queue_v2_activation_r{number}_20261004.json'
    assert not audit.exists()
    with audit.open('x',encoding='utf-8') as stream:
        json.dump({'status':'activated','round':number,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'input_sha256':frozen,'predecessor_result_sha256':sha(gate),
            'scope':'Only delay heavy imports. Execute unchanged verified V2 runner with all original pipeline gates.'},stream,ensure_ascii=False,indent=2)
    sys.argv=[str(RUNNER),str(number)]
    runpy.run_path(str(RUNNER),run_name='__main__')


if __name__=='__main__':main(int(sys.argv[1]),probe='--probe' in sys.argv[2:])
