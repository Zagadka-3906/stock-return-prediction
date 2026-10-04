"""Actual lazy probes, original runpy handoff and immutable protocol guards."""
from pathlib import Path
from types import ModuleType
import json
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from locked_read_hash_cache_20261004 import fresh_sha
import run_neural_interaction_locked_pipeline_20261004 as driver
from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
OUT=ROOT/'analysis/frozen_provenance_execution_preflight_20261004'

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v,*args,**kwargs):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)

def main():
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    sources=[Path(__file__),Path(driver.__file__),ROOT/'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT/'analysis/locked_read_hash_cache_20261004.py',
        ROOT/'analysis/run_training_round55_pipeline.py',ROOT/'analysis/run_training_round56_pipeline.py',
        ROOT/'analysis/run_neural_interaction_round_pipeline_20261004.py']
    hashes={str(p.resolve()):fresh_sha(p) for p in sources}
    dump(OUT/'frozen_before_controls.json',{'input_sha256':hashes,'new_quality_scores':0,
        'scope':'Implementation fixtures only: original wrapper runpy dispatch, metadata extension before freeze, true Windows read locking andrestoration. No training, forecasts orofficial scores.'})
    probes=[]
    for number in (55,56):
        r=subprocess.run([sys.executable,'-B','-X','utf8',str(Path(driver.__file__)),str(number),'--probe'],capture_output=True,text=True,check=True)
        value=json.loads(r.stdout);assert value['lazy_imports_only'] and value['python_rss_bytes']<50*2**20
        assert value['round']==number and len(value['gates'])==7;probes.append(value)
    fixture=OUT/'implementation_fixtures';fixture.mkdir()
    source=fixture/'immutable_input.bin';source.write_bytes(b'fixed implementation fixture')
    gate=fixture/'implementation_gate.json';dump(gate,{'status':'passed','purpose':'controlled implementation gate only','new_quality_scores':0})
    original_gates=driver.gates;driver.gates=lambda number:[gate]*7
    previous_modules={};reports=[]
    try:
        for number in (55,56):
            target=fixture/f'dispatch_{number}';target.mkdir()
            module=ModuleType(f'optimize_training_round{number}');module.__file__=str(ROOT/f'analysis/optimize_training_round{number}.py')
            module.OUT=target;module.dump=dump;module.sha=fresh_sha
            parameters={'alpha':.9,'weight':.025,'frozen_fixture_only':True}
            def freeze(module=module):
                module.dump(module.OUT/'protocol.json',{'input_sha256':{str(source.resolve()):fresh_sha(source)},
                    'parameters':parameters,'new_quality_scores':0},immutable=True)
            module.freeze=freeze;original_freeze=freeze
            finalize=ModuleType(f'finalize_training_round{number}')
            original_pipeline=ModuleType('run_neural_interaction_round_pipeline_20261004');calls=[]
            def delegated(n,module=module,calls=calls):
                assert n==number;calls.append(n);module.freeze()
                p=read(module.OUT/'protocol.json');assert p['parameters']==parameters and p['new_quality_scores']==0
                assert module.sha(source)==fresh_sha(source)
                try:source.open('r+b')
                except PermissionError:pass
                else:raise AssertionError('Scoped immutable input was writable')
            original_pipeline.main=delegated
            for name,obj in ((module.__name__,module),(finalize.__name__,finalize),(original_pipeline.__name__,original_pipeline)):
                previous_modules.setdefault(name,sys.modules.get(name));sys.modules[name]=obj
            driver.main(number)
            assert calls==[number] and module.freeze is original_freeze and module.dump is dump and module.sha is fresh_sha
            execution=read(target/'provenance_scope_execution.json');assert execution['status']=='passed' and execution['all_sha_bindings_restored']
            protocol=read(target/'protocol.json');assert len(protocol['input_sha256'])>1
            assert protocol['effective_execution_driver']['round']==number
            before=fresh_sha(target/'protocol.json')
            rejected=False
            scope=FrozenProvenanceExecutionScope(module,[Path(driver.__file__)],{'wrong_driver':True},ROOT/'analysis').install()
            try:
                try:module.freeze()
                except (AssertionError,FileExistsError):rejected=True
            finally:scope.close(failed=True)
            assert rejected and fresh_sha(target/'protocol.json')==before
            reports.append({'round':number,'actual_original_wrapper_runpy_handoff':True,
                'actual_pre_freeze_effective_source_extension':True,'original_parameter_dictionary_unchanged':True,
                'immutable_input_write_denied_andbindings_restored':True,'existing_protocol_rewrite_rejected':True})
    finally:
        driver.gates=original_gates
        for name,value in previous_modules.items():
            if value is None:sys.modules.pop(name,None)
            else:sys.modules[name]=value
    for p,d in hashes.items():assert fresh_sha(p)==d,p
    dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_lazy_subprocess_probes':probes,'controlled_actual_runpy_dispatches':reports,
        'original_stage_runner_sources_unchanged':True,'new_quality_scores':0,'official_scoring_calls':0,
        'test_labels_read':False,'input_sha256':hashes,
        'scope':'Actual Windows integrity, lazy import andoriginal wrapper dispatch controls under implementation fixtures. Full actual model/scheme parity andreal selected predecessors remain production gates.'})
    print('Actual lazy handoff andpre-freeze protocol-source controls passed',flush=True)

if __name__=='__main__':main()
