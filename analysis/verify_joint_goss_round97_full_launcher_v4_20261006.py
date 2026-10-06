"""Run actual nested execution bridges and publication routing without scientific stages."""
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
OUT=A/'joint_goss_round97_full_launcher_preflight_v4_20261006'

def main():
    assert not OUT.exists();OUT.mkdir()
    import frozen_provenance_execution_scope_20261004 as provenance
    import parallel_candidate_scoring_one_20261005 as pool
    import exact_rank_cache_official_worker_adapter_20261006 as cache
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    import refresh_optimization_boundary_evidence_20261004 as qualification
    from locked_read_hash_cache_20261004 import fresh_sha
    originals=(provenance.FrozenProvenanceExecutionScope,pool._initialize,pool._evaluate,ranking.main,qa.main,qualification.complete_round_evidence)
    runfile=A/'joint_goss_membership_quality_run_v3_20261006.json'
    run=read(runfile)
    driver_file=A/'run_joint_goss_membership_round_v3_20261006.py'
    paths=[Path(__file__),runfile,A/'joint_goss_membership_round97_previous_run_v3_20261006.json',
        A/'service_owned_dependency_queue_v4_20261006/queue_plan_v7.json',*map(Path,run['input_sha256'])]
    pins={str(p.resolve()):sha(p) for p in dict.fromkeys(paths)}
    for p,digest in run['input_sha256'].items():assert pins[p]==digest,p
    create(OUT/'frozen_before_actual_launcher_controls.json',{'input_sha256':pins,
        'scientific_stages_intercepted_only_at_final_pipeline_dispatch':True,
        'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    from run_dependency_queue_v10_20261006 import original_driver_and_bridge
    job={'name':'round97','round':97,'previous_run':str(paths[2])}
    pipeline,args,bridge,prior=original_driver_and_bridge(job,read(paths[2]))
    assert prior is None and args==[] and pipeline==str(A/'run_training_round97_v3_pipeline.py')
    bridge.update(round=97,original_driver=pipeline,original_arguments=args)
    bridge['input_sha256'].update(pins)
    bridge_file=OUT/'qualified_run.json';create(bridge_file,bridge)
    tree=ast.parse(driver_file.read_text(encoding='utf-8'))
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
    setup=[n for n in body if (
        isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('module','release','scope') for t in n.targets)
        or isinstance(n,ast.Assign) and any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Attribute) and t.value.attr=='modules' for t in n.targets))]
    assert len(setup)==5
    actual_run_path=runpy.run_path;called=[]
    def pipeline_control(path,*arguments,**kwargs):
        if Path(path).resolve()!=Path(pipeline).resolve():return actual_run_path(path,*arguments,**kwargs)
        assert not called
        assert provenance.FrozenProvenanceExecutionScope is not originals[0]
        assert pool._initialize is cache.initialize and pool._evaluate is cache.evaluate
        assert qa.main.__code__.co_filename.endswith('lossless_ranking_runtime_adapter_v5_20261006.py')
        assert ranking.main.__code__.co_filename.endswith('lossless_ranking_runtime_adapter_v5_20261006.py')
        env={'number':97,'parent_number':95,'ROOT':ROOT,'Path':Path,'__file__':str(driver_file),
            'run':runfile,'sys':sys,'importlib':importlib,'fresh_sha':fresh_sha,
            'FrozenProvenanceExecutionScope':provenance.FrozenProvenanceExecutionScope}
        exec(compile(ast.fix_missing_locations(ast.Module(body=setup,type_ignores=[])),str(driver_file),'exec'),env)
        module,release,scope=env['module'],env['release'],env['scope']
        try:
            assert module.PREVIOUS_NUMBER==95 and module.WAVES==(378,379,380)
            assert module.__file__.endswith('optimize_training_round97_v3.py')
            assert release.__file__.endswith('finalize_training_round97_v3.py')
            assert sys.modules['optimize_training_round97'] is module
            required=[A/name for name in ('optimize_training_round97_v3.py','finalize_training_round97_v3.py',
                'run_training_round97_v3_pipeline.py','joint_goss_membership_search_engine_v3_20261006.py',
                'joint_goss_membership_retention_grid_v2_20261006.py',
                'predict_joint_goss_membership_scheme_v3_20261006.py',
                'run_joint_goss_quality_qualified_workflow_v3_20261006.py',
                'run_joint_goss_quality_with_exact_rank_cache_v3_20261006.py',
                'lossless_ranking_runtime_adapter_v5_20261006.py',
                'verify_lossless_ranking_display_v7_20261006.py')]+[bridge_file]
            assert all(scope.extra[str(p.resolve())]==sha(p) for p in required)
            assert scope.metadata['effective_recovery_launcher']==str(A/'run_joint_goss_quality_qualified_workflow_v3_20261006.py')
            assert scope.metadata['effective_exact_rank_cache_launcher']==str(A/'run_joint_goss_quality_with_exact_rank_cache_v3_20261006.py')
            assert scope.metadata['rank_cache_maximum_bytes_per_worker']==1024**3
            assert scope.metadata['scientific_grid_full_rows_and_official_evaluator_unchanged']
            called.append({'round':97,'explicit_parent_round':95,'scientific_stage_methods_called':0,
                'wave_arm_counts':[73,24,54],'required_effective_source_sha256':{str(p):scope.extra[str(p.resolve())] for p in required},
                'actual_nested_bridges_executed':True,'cache_and_full_original_QA_bound':True,
                'scope_extra_files':len(scope.extra)})
            from predict_joint_goss_membership_scheme_v3_20261006 import copy_sources
            copied=OUT/'private_copied_candidate_source_control'
            copy_sources(module,copied)
            assert sha(copied/'optimize_training_round97.py')==sha(A/'optimize_training_round97_v3.py')
            assert sha(copied/'optimize_training_round95.py')==sha(A/'optimize_training_round95_v3.py')
            assert sha(copied/'finalize_training_round97.py')==sha(A/'finalize_training_round97_v3.py')
            create(copied/'manifest.json',{'private_control_only_not_actual_candidate':True})
            try:copy_sources(module,copied)
            except AssertionError:pass
            else:raise AssertionError('Sealed candidate editing was not rejected')
        finally:assert scope.close()=={'scope_started':False}
        return env
    argv=sys.argv;runpy.run_path=pipeline_control
    sys.argv=[str(A/'run_joint_goss_quality_with_exact_rank_cache_v3_20261006.py'),pipeline,str(bridge_file)]
    try:actual_run_path(sys.argv[0],run_name='__main__')
    finally:runpy.run_path=actual_run_path;sys.argv=argv
    assert len(called)==1
    assert (provenance.FrozenProvenanceExecutionScope,pool._initialize,pool._evaluate,ranking.main,qa.main,qualification.complete_round_evidence)==originals
    assert not pool._POOLS
    hidden=read(OUT/'hidden_child_process_launches.json')
    assert hidden['actual_child_creations']==[] and hidden['all_creation_flags_restored']
    import watch_validations_main_v7_20261006 as publisher
    tree=ast.parse(Path(publisher.__file__).read_text(encoding='utf-8'))
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
    setup=[]
    for node in body:
        if isinstance(node,ast.Try):break
        setup.append(node)
    env=vars(publisher).copy()
    exec(compile(ast.fix_missing_locations(ast.Module(body=setup,type_ignores=[])),str(publisher.__file__),'exec'),env)
    import collect_full_lossless_round_publication_20261006 as collector
    original_collect=collector.collect;routes=[]
    class StopCollect(Exception):pass
    def checked_collect(number,version,count):
        routes.append({'round':number,'QA_version':version,'expected_records':count})
        raise StopCollect
    try:
        assert env['sync'].snapshot.__code__.co_filename.endswith('joint_goss_lossless_publication_adapter_v1_20261006.py')
        collector.collect=checked_collect
        for number in (97,95,96,93,94):
            try:env['sync'].snapshot(number)
            except StopCollect:pass
            else:raise AssertionError('Full immutable collector not invoked')
        assert routes==[{'round':n,'QA_version':v,'expected_records':c} for n,v,c in ((97,7,151),(95,6,124),(96,6,138),(93,6,124),(94,6,138))]
    finally:
        collector.collect=original_collect
        env['sync'].snapshot=env['old_snapshot'];env['sync'].complete_round_evidence=env['old_gate']
        env['qualification'].close();env['restore_children']()
    for p,digest in pins.items():assert sha(p)==digest,p
    proof={'status':'passed_actual_joint97_nested_bridges_full_QA_and_preserved93_through96_main_export_routes',
        'controls':called,'publication_collect_routes':routes,'input_sha256':pins,
        'actual_candidate_source97_and_parent95_effective_versions_preserved':True,
        'sealed_candidate_edit_rejected':True,'all_function_bindings_and_child_flags_restored':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False,
        'actual151_scores_candidate_causal_full_ranking_and_main_receipt_still_required':True}
    create(OUT/'verification.json',proof);print(json.dumps({'status':proof['status'],'publication_collect_routes':routes},ensure_ascii=False),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_joint97_full_launcher_control','error':f'{type(exc).__name__}: {exc}'})
        raise
