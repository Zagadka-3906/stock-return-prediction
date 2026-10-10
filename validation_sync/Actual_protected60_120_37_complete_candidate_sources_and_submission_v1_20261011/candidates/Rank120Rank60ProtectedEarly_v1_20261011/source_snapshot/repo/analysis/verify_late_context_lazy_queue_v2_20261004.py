"""Probe imports andactually execute a controlled predecessor-to-runner handoff."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/late_context_lazy_queue_v2_preflight_20261004'
SOURCE=ROOT/'analysis/run_late_context_lazy_queue_v2_20261004.py'


def main():
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    probe=subprocess.run([sys.executable,'-B','-X','utf8',str(SOURCE),'48','--probe'],capture_output=True,text=True,check=True)
    value=json.loads(probe.stdout);assert value['status']=='passed' and not value['model_libraries_loaded']
    fixture=OUT/'fixture';(fixture/'analysis/late_context_initialization_recovery_v2_20261004').mkdir(parents=True)
    (fixture/'results').mkdir();(fixture/'results/optimization_20261003_r29.json').write_text('{"fixture":true}',encoding='utf-8')
    proof=fixture/'analysis/late_context_initialization_recovery_v2_20261004/verification.json';proof.write_text('{"status":"passed","fixture":true}',encoding='utf-8')
    ran=fixture/'ran.json';dummy=fixture/'analysis/verified_runner_fixture.py'
    dummy.write_text('from pathlib import Path\nimport json,sys\nassert sys.argv[1:]==["30"]\nPath('+repr(str(ran))+').write_text(json.dumps({"executed":True,"round":30}),encoding="utf-8")\n',encoding='utf-8')
    spec=importlib.util.spec_from_file_location('isolated_lazy_queue_handoff_control',SOURCE)
    queue=importlib.util.module_from_spec(spec);spec.loader.exec_module(queue)
    original_argv=sys.argv[:];queue.ROOT=fixture;queue.RUNNER=dummy
    try:queue.main(30)
    finally:sys.argv=original_argv
    assert json.loads(ran.read_text(encoding='utf-8'))=={'executed':True,'round':30}
    activation=fixture/'analysis/late_context_lazy_queue_v2_activation_r30_20261004.json'
    data=json.loads(activation.read_text(encoding='utf-8'))
    for path,digest in data['input_sha256'].items():assert queue.sha(path)==digest,path
    sources=[Path(__file__),SOURCE,ROOT/'analysis/run_late_context_lazy_queue_20261004.py',
        ROOT/'analysis/late_context_lazy_queue_replacement_20261004.json',
        ROOT/'analysis/run_logs/round30_lazy_20261004_102220.stderr.log']
    with (OUT/'verification.json').open('x',encoding='utf-8') as f:
        json.dump({'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'actual_subprocess_probe':value,'actual_controlled_gate_activation_andrunpy_handoff_passed':True,
            'string_andPath_sha_checks_passed':True,'original_failure_preserved':True,
            'input_sha256':{str(p.resolve()):queue.sha(p) for p in sources},
            'scope':'Queue loading andhandoff only; unchanged V2 recovered pipeline still performs its own actual data andofficial metric checks.',
            'new_quality_scores':0,'test_data_read':False},f,ensure_ascii=False,indent=2)
    print('Lazy V2 actual process probe andhandoff passed',flush=True)


if __name__=='__main__':main()
