"""Actual byte-identical R50 stage dispatch, basis runpy dispatch andSHA guards."""
from pathlib import Path
from types import ModuleType
import json
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from locked_read_hash_cache_20261004 import fresh_sha
from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
import run_joint_and_basis_locked_pipeline_20261004 as driver
OUT=ROOT/'analysis/joint_and_basis_frozen_provenance_preflight_20261004'

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v,*args,**kwargs):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)

def main():
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    sources=[Path(__file__),Path(driver.__file__),ROOT/'analysis/frozen_provenance_execution_scope_20261004.py',
        ROOT/'analysis/locked_read_hash_cache_20261004.py',
        *[ROOT/f'analysis/run_training_round{n}_pipeline.py' for n in (50,51,52)],
        ROOT/'analysis/run_additive_basis_round_pipeline_20261004.py']
    hashes={str(p.resolve()):fresh_sha(p) for p in sources}
    dump(OUT/'frozen_before_controls.json',{'input_sha256':hashes,'new_quality_scores':0,
        'scope':'Implementation fixtures; R50 runner relocated byte-identically to an isolated ROOT to preserve live state. All stage adapters are fixtures; no quality scoring.'})
    probes=[]
    for number in (50,51,52):
        r=subprocess.run([sys.executable,'-B','-X','utf8',str(Path(driver.__file__)),str(number),'--probe'],capture_output=True,text=True,check=True)
        value=json.loads(r.stdout);assert value['lazy_imports_only'] and value['python_rss_bytes']<50*2**20
        assert len(value['gates'])==(8 if number==50 else 7);probes.append(value)
    fixture=OUT/'implementation_fixtures';fixture.mkdir()
    source=fixture/'immutable_input.bin';source.write_bytes(b'fixed joint andbasis fixture')
    gate=fixture/'implementation_gate.json';dump(gate,{'status':'passed','new_quality_scores':0})
    old_gates=driver.gates;old_runpy=driver.runpy.run_path;driver.gates=lambda number:[gate]*8
    original_modules={};reports=[]
    def bind(module):
        original_modules.setdefault(module.__name__,sys.modules.get(module.__name__));sys.modules[module.__name__]=module
    try:
        for number in (50,51,52):
            target=fixture/f'dispatch_{number}';target.mkdir();events=[]
            module=ModuleType(f'optimize_training_round{number}');module.__file__=str(ROOT/f'analysis/optimize_training_round{number}.py')
            module.OUT=target;module.dump=dump;module.sha=fresh_sha
            parameters={'alpha':.9,'weight':.025,'implementation_fixture_only':True}
            def freeze(module=module,events=events):
                events.append('freeze');module.dump(module.OUT/'protocol.json',{'input_sha256':{str(source.resolve()):fresh_sha(source)},
                    'parameters':parameters,'new_quality_scores':0},immutable=True)
                assert module.sha(source)==fresh_sha(source)
                try:source.open('r+b')
                except PermissionError:pass
                else:raise AssertionError('Immutable input write was allowed')
            module.freeze=freeze;original_freeze=freeze;bind(module)
            release=ModuleType(f'finalize_training_round{number}');bind(release)
            if number==50:
                relocated=fixture/'isolated_round50_ROOT';(relocated/'analysis').mkdir(parents=True)
                copied=relocated/'analysis/run_training_round50_pipeline.py';copied.write_bytes((ROOT/'analysis/run_training_round50_pipeline.py').read_bytes())
                assert fresh_sha(copied)==hashes[str((ROOT/'analysis/run_training_round50_pipeline.py').resolve())]
                (relocated/'results').mkdir();dump(relocated/'results/optimization_20261003_r49.json',{'status':'complete','fixture_only':True})
                for folder in ('whole_scheme_runtime_preflight_20261004','whole_scheme_future_runtime_qa_20261004',
                    'whole_scheme_score_preflight_20261004','whole_scheme_round50_proposal_preflight_20261004','whole_scheme_round50_release_preflight_20261004'):
                    (relocated/'analysis'/folder).mkdir();dump(relocated/'analysis'/folder/'verification.json',{'status':'passed','fixture_only':True})
                for stage in ('build','independent','forward','reverse','retention_refinement','temporal_refinement'):
                    setattr(module,stage,lambda stage=stage,events=events:events.append(stage))
                for stage in ('select','calibrate','predict'):
                    setattr(release,stage,lambda stage=stage,events=events:events.append('release.'+stage))
                checks=ModuleType('verify_methods_round50');checks.main=lambda:events.append('checks');bind(checks)
                parallel=ModuleType('parallel_candidate_scoring_four_20261004');parallel.shutdown=lambda name:events.append('shutdown.'+name);bind(parallel)
                publish=ModuleType('publish_training_round')
                def publish_fixture(n,*args):
                    assert n==50;events.append('publish');return {'winner':{'connected_final_score':0.},'score_gain':0.,'fixture_only':True}
                publish.publish=publish_fixture;bind(publish)
                ranking=ModuleType('build_all_model_rankings_20261003');ranking.main=lambda:events.append('ranking');bind(ranking)
                qa=ModuleType('verify_all_model_rankings_20261003');qa.main=lambda:events.append('ranking_qa');bind(qa)
                def relocated_run(path,**kwargs):
                    assert Path(path).resolve()==(ROOT/'analysis/run_training_round50_pipeline.py').resolve()
                    return old_runpy(str(copied),**kwargs)
                driver.runpy.run_path=relocated_run
            else:
                driver.runpy.run_path=old_runpy
                runner=ModuleType('run_additive_basis_round_pipeline_20261004')
                def delegated(n,module=module,events=events):
                    assert n==number;events.append(f'delegate.{n}');module.freeze()
                runner.main=delegated;bind(runner)
            driver.main(number)
            assert module.freeze is original_freeze and module.dump is dump and module.sha is fresh_sha
            execution=read(target/'provenance_scope_execution.json');assert execution['status']=='passed' and execution['all_sha_bindings_restored']
            protocol=read(target/'protocol.json');assert protocol['parameters']==parameters and protocol['effective_execution_driver']['round']==number
            if number==50:
                expected=['freeze','build','independent','forward','reverse','retention_refinement','temporal_refinement',
                    'shutdown.optimize_training_round50','release.select','release.calibrate','release.predict','checks','publish','ranking','ranking_qa']
                assert events==expected,events
                assert read(relocated/'analysis/ongoing_optimization_r50_state.json')['stage']=='round_complete_next_round_pending'
            else:assert events==[f'delegate.{number}','freeze']
            before=fresh_sha(target/'protocol.json');scope=FrozenProvenanceExecutionScope(module,[Path(driver.__file__)],{'wrong_driver':True},ROOT/'analysis').install();rejected=False
            try:
                try:module.freeze()
                except (AssertionError,FileExistsError):rejected=True
            finally:scope.close(failed=True)
            assert rejected and fresh_sha(target/'protocol.json')==before
            reports.append({'round':number,'actual_original_byte_identical_runner_dispatched':True,
                'stage_events_under_fixture_adapters':events,'driver_source_extended_before_freeze':True,
                'parameters_unchanged_andimmutable_write_denied':True,'existing_protocol_rewrite_rejected':True,
                'all_bindings_restored':True,'original_50_live_state_file_not_used_by_fixture':number==50})
    finally:
        driver.gates=old_gates;driver.runpy.run_path=old_runpy
        for name,obj in original_modules.items():
            if obj is None:sys.modules.pop(name,None)
            else:sys.modules[name]=obj
    for path,digest in hashes.items():assert fresh_sha(path)==digest,path
    dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':hashes,'actual_lazy_probes':probes,'actual_dispatch_controls':reports,
        'new_quality_scores':0,'official_scoring_calls':0,'test_labels_read':False,
        'scope':'Actual Windows guards andbyte-identical runner control flow with fixture stage adapters. Real selected graph/model numerical controls remain mandatory production gates; no timing orquality gain inferred.'})
    print('Actual byte-identical joint/basis runner dispatch andimmutable controls passed',flush=True)

if __name__=='__main__':main()
