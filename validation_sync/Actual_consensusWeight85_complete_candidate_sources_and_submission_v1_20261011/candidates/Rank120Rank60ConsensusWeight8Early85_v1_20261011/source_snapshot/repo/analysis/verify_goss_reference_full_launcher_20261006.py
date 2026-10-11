"""Exercise actual nested launchers and frozen provenance without running a scientific stage."""
from pathlib import Path
import ast
import importlib
import json
import runpy
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

OUT=A/'goss_reference_full_launcher_preflight_20261006'


def main():
    assert not OUT.exists();OUT.mkdir()
    plan_path=A/'service_owned_dependency_queue_v4_20261006/queue_plan_v7.json'
    plan=read(plan_path)
    from run_dependency_queue_v7_20261006 import original_driver_and_bridge
    from locked_read_hash_cache_20261004 import fresh_sha
    import frozen_provenance_execution_scope_20261004 as provenance
    import parallel_candidate_scoring_one_20261005 as pool
    import exact_rank_cache_official_worker_adapter_20261006 as cache
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    import refresh_optimization_boundary_evidence_20261004 as qualification
    original_scope=provenance.FrozenProvenanceExecutionScope
    original_initialize,original_evaluate=pool._initialize,pool._evaluate
    original_ranking,original_qa=ranking.main,qa.main
    original_gate=qualification.complete_round_evidence
    driver_file=A/'run_ready_goss_reference_round_v2_20261006.py'
    tree=ast.parse(driver_file.read_text(encoding='utf-8'))
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
    setup=[n for n in body if (
        isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('module','release','scope') for t in n.targets)
        or isinstance(n,ast.Assign) and any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Attribute) and t.value.attr=='modules' for t in n.targets))]
    assert len(setup)==5
    static=[Path(__file__),driver_file,A/'run_goss_reference_quality_with_exact_rank_cache_20261006.py',A/'run_goss_reference_quality_qualified_workflow_20261006.py',A/'lossless_ranking_runtime_adapter_v4_20261006.py',A/'goss_reference_lossless_publication_adapter_20261006.py',A/'build_lossless_ranking_display_v5_20261006.py',A/'verify_lossless_ranking_display_v6_20261006.py',plan_path,A/'ready_goss_reference_actual_handoff_20261006/verification.json']
    pins={str(p):sha(p) for p in static}
    create(OUT/'frozen_before_actual_launcher_controls.json',{'input_sha256':pins,'actual_launcher_execution_required':True,'only_final_scientific_pipeline_call_intercepted_before_stages':True,'models_and_quality_not_run':True,'test_labels_read':False})
    cases=[]
    for number,parent in ((95,84),(96,95)):
        job=next(j for j in plan['deferred_jobs'] if j.get('round')==number)
        original=read(job['previous_run'])
        pipeline,args,bridge,prior=original_driver_and_bridge(job,original)
        assert prior is None and args==[]
        case=OUT/f'round{number}';case.mkdir()
        bridge.update(round=number,original_driver=pipeline,original_arguments=args)
        bridge['input_sha256']={**bridge['input_sha256'],**plan['input_sha256'],str(plan_path):sha(plan_path),**pins}
        bridge_file=case/'qualified_run.json';create(bridge_file,bridge)
        actual_run_path=runpy.run_path
        called=[]

        def pipeline_control(path,*arguments,**kwargs):
            if Path(path).resolve()!=Path(pipeline).resolve():
                return actual_run_path(path,*arguments,**kwargs)
            assert not called,'Scientific driver dispatched twice'
            assert provenance.FrozenProvenanceExecutionScope is not original_scope
            assert pool._initialize is cache.initialize and pool._evaluate is cache.evaluate
            assert qa.main.__code__.co_filename.endswith('lossless_ranking_runtime_adapter_v4_20261006.py')
            assert ranking.main.__code__.co_filename.endswith('lossless_ranking_runtime_adapter_v4_20261006.py')
            from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
            env={'number':number,'parent_number':parent,'ROOT':ROOT,'Path':Path,'__file__':str(driver_file),'run':A/'ready_goss_reference_quality_run_v2_20261006.json','sys':sys,'importlib':importlib,'fresh_sha':fresh_sha,'FrozenProvenanceExecutionScope':FrozenProvenanceExecutionScope}
            exec(compile(ast.fix_missing_locations(ast.Module(body=setup,type_ignores=[])),str(driver_file),'exec'),env)
            module,release,scope=env['module'],env['release'],env['scope']
            try:
                assert module.PREVIOUS_NUMBER==parent
                assert module.__file__.endswith(f'optimize_training_round{number}_v3.py')
                assert release.__file__.endswith(f'finalize_training_round{number}_v3.py')
                assert sys.modules[f'optimize_training_round{number}'] is module
                required=[A/f'optimize_training_round{number}_v3.py',A/f'finalize_training_round{number}_v3.py',A/f'run_training_round{number}_v3_pipeline.py',A/'ready_goss_reference_search_engine_v2_20261006.py',A/'ready_goss_reference_release_engine_v2_20261006.py',A/'predict_ready_goss_reference_scheme_v2_20261006.py',A/'run_goss_reference_quality_with_exact_rank_cache_20261006.py',A/'exact_rank_cache_official_worker_adapter_20261006.py',A/'run_goss_reference_quality_qualified_workflow_20261006.py',bridge_file]
                assert all(scope.extra[str(p.resolve())]==sha(p) for p in required)
                assert scope.metadata['effective_recovery_launcher']==str(A/'run_goss_reference_quality_qualified_workflow_20261006.py')
                assert scope.metadata['effective_exact_rank_cache_launcher']==str(A/'run_goss_reference_quality_with_exact_rank_cache_20261006.py')
                assert scope.metadata['rank_cache_maximum_bytes_per_worker']==1024**3
                assert scope.metadata['scientific_grid_full_rows_and_official_evaluator_unchanged'] is True
                called.append({'round':number,'explicit_parent_round':parent,'effective_optimize_factory':module.__file__,'effective_release_factory':release.__file__,'frozen_scope_actual_extra_files':len(scope.extra),'required_effective_source_sha256':{str(p):scope.extra[str(p.resolve())] for p in required},'actual_provenance_metadata':scope.metadata,'actual_nested_launchers_executed':True,'cache_and_full_lossless_QA_bindings_checked':True,'scientific_stage_methods_called':0})
            finally:
                report=scope.close();assert report=={'scope_started':False}
            return env

        before_argv=sys.argv
        runpy.run_path=pipeline_control
        sys.argv=[str(A/'run_goss_reference_quality_with_exact_rank_cache_20261006.py'),pipeline,str(bridge_file)]
        try:
            actual_run_path(sys.argv[0],run_name='__main__')
        finally:
            runpy.run_path=actual_run_path;sys.argv=before_argv
        assert len(called)==1
        assert provenance.FrozenProvenanceExecutionScope is original_scope
        assert pool._initialize is original_initialize and pool._evaluate is original_evaluate and not pool._POOLS
        assert ranking.main is original_ranking and qa.main is original_qa
        assert qualification.complete_round_evidence is original_gate
        hidden=read(case/'hidden_child_process_launches.json');assert hidden['actual_child_creations']==[] and hidden['all_creation_flags_restored']
        cases+=called
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual_two_nested_GOSS_launchers_V3_sources_cache_full_QA_and_provenance_restoration','controls':cases,'input_sha256':pins,'actual_scientific_stages_not_called':True,'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False,'actual_parent_replay_full_quality_and_candidate_still_required':True})
    print(json.dumps({'status':'passed_actual_two_nested_GOSS_launcher_controls','rounds':[95,96],'new_quality_scores':0},ensure_ascii=False),flush=True)


if __name__=='__main__':
    try:main()
    except BaseException as error:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_actual_nested_launcher_control','error':f'{type(error).__name__}: {error}'})
        raise
