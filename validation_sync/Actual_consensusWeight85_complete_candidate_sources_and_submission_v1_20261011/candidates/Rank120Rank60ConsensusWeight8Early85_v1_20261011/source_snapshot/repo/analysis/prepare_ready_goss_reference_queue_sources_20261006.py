"""Build a prospective dispatch extension without touching live scientific workers."""
from pathlib import Path
import ast
import hashlib
import json

A=Path(__file__).resolve().parent
ROOT=A.parent


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(name,text):
    compile(text,str(A/name),'exec')
    with (A/name).open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)
def data(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert read(A/'ready_goss_reference_controls_github_20261006/receipt.json')['status']=='pushed_actual_controls_main_only'
    encoder=(A/'build_lossless_ranking_display_v4_20261006.py').read_text(encoding='utf-8')
    assert encoder.count('assert 93 <= number <= 94 and number != 81')==1
    create('build_lossless_ranking_display_v5_20261006.py',encoder.replace('assert 93 <= number <= 94 and number != 81','assert number in (95,96)'))
    runtime=(A/'lossless_ranking_runtime_adapter_v3_20261006.py').read_text(encoding='utf-8')
    create('lossless_ranking_runtime_adapter_v4_20261006.py',runtime.replace('assert number in (93, 94)','assert number in (95, 96)').replace('build_lossless_ranking_display_v4_20261006','build_lossless_ranking_display_v5_20261006'))
    qualified=(A/'run_quantile_distribution_views_quality_qualified_workflow_20261006.py').read_text(encoding='utf-8')
    qualified=qualified.replace('assert number in (93, 94)','assert number in (95, 96)').replace('lossless_ranking_runtime_adapter_v3_20261006','lossless_ranking_runtime_adapter_v4_20261006').replace('build_lossless_ranking_display_v4_20261006','build_lossless_ranking_display_v5_20261006')
    # Seal effective V3 factories as well as unchanged historical factories.
    qualified=qualified.replace('extra_sources = list(dict.fromkeys([*extra_sources, *additions]))','extra_sources = list(dict.fromkeys([*extra_sources, *additions, *map(Path,run["input_sha256"])]))')
    create('run_goss_reference_quality_qualified_workflow_20261006.py',qualified)
    cached=(A/'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py').read_text(encoding='utf-8')
    cached=cached.replace("assert 84 <= run['round'] <= 90","assert run['round'] in (95,96)").replace('run_recovery_qualified_workflow_v2_20261006.py','run_goss_reference_quality_qualified_workflow_20261006.py')
    create('run_goss_reference_quality_with_exact_rank_cache_20261006.py',cached)
    queue=(A/'run_dependency_queue_v6_20261006.py').read_text(encoding='utf-8')
    before="A / ('run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py'"
    after="A / ('run_goss_reference_quality_with_exact_rank_cache_20261006.py' if job['round'] in (95,96) else 'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py'"
    assert queue.count(before)==1
    create('run_dependency_queue_v7_20261006.py',queue.replace(before,after))
    monitor=(A/'monitor_actual_optimization_progress_v28_20261006.py').read_text(encoding='utf-8')
    monitor=monitor.replace('for version in (6, 5, 4):','for version in (7, 6, 5, 4):')
    monitor=monitor.replace('actual_observer_version=28','actual_observer_version=29').replace("'actual_observer_version': 28","'actual_observer_version': 29")
    monitor=monitor.replace("'gradient_sampling_native_queue_handoff_v6', 'gradient_sampling_native_queue_handoff_v6_publication'","'gradient_sampling_native_queue_handoff_v9', 'gradient_sampling_native_queue_handoff_v9_publication'")
    create('monitor_actual_optimization_progress_v29_20261006.py',monitor)
    publication=(A/'distribution_views_lossless_publication_adapter_20261006.py').read_text(encoding='utf-8')
    publication=publication.replace('if number not in (93, 94):','if number not in (95, 96):').replace('expected = 124 if number == 93 else 138','expected = 124 if number == 95 else 138').replace('Export93/94','Export95/96').replace('actual_distribution_views_immutable_export','actual_goss_reference_immutable_export')
    create('goss_reference_lossless_publication_adapter_20261006.py',publication)
    watcher=(A/'watch_validations_main_v5_20261006.py').read_text(encoding='utf-8')
    watcher=watcher.replace('    lossless(sync)\n','    lossless(sync)\n    from distribution_views_lossless_publication_adapter_20261006 import install as views\n    from goss_reference_lossless_publication_adapter_20261006 import install as goss\n    views(sync)\n    goss(sync)\n').replace('state_v5_20261006.json','state_v6_20261006.json')
    create('watch_validations_main_v6_20261006.py',watcher)
    current_plan=A/'service_owned_dependency_queue_v4_20261006/queue_plan_v6.json'
    old=read(current_plan)
    files=[Path(__file__),current_plan,*A.glob('*ready_goss*20261006.py'),*A.glob('ready_goss_reference*20261006.json')]
    files += [A/name for name in ('run_dependency_queue_v7_20261006.py','monitor_actual_optimization_progress_v29_20261006.py','watch_validations_main_v6_20261006.py','run_goss_reference_quality_qualified_workflow_20261006.py','run_goss_reference_quality_with_exact_rank_cache_20261006.py','lossless_ranking_runtime_adapter_v4_20261006.py','build_lossless_ranking_display_v5_20261006.py','goss_reference_lossless_publication_adapter_20261006.py')]
    files += [A/name for name in ('exact_daily_rank_memoization_20261006.py','exact_rank_cache_official_worker_adapter_20261006.py','exact_daily_rank_memoization_preflight_20261006/verification.json','exact_rank_cache_complete_scheme_20261006/verification.json','exact_rank_cache_complete_scheme_v2_20261006/verification.json','exact_rank_cache_windows_scoring_initializer_20261006/verification.json','exact_rank_cache_actual_scoring_adapter_v2_20261006/verification.json','gradient_sampling_memmap_native_promotion_20261006/verification.json','gradient_sampling_memmap_complete_bank_v3_github_20261006/receipt.json','ready_goss_reference_generator_preflight_v2_20261006/verification.json','ready_goss_reference_execution_preflight_v2_20261006/verification.json')]
    files += [A/f'{prefix}{number}{suffix}.py' for number in (95,96) for prefix,suffix in (('optimize_training_round','_v3'),('finalize_training_round','_v3'),('run_training_round','_v3_pipeline'))]
    pins={str(p.resolve()):sha(p) for p in dict.fromkeys(files)}
    data(A/'ready_goss_reference_quality_run_v2_20261006.json',{'status':'frozen_before_actual_complete_output_quality','explicit_parent_rounds':{'95':84,'96':95},'required_official_records':{'95':124,'96':138},'original67_through94_retained':True,'input_sha256':pins,'test_labels_read':False})
    quality=A/'ready_goss_reference_quality_run_v2_20261006.json';pins[str(quality)]=sha(quality)
    out=A/'ready_goss_reference_queue_preparation_20261006';out.mkdir()
    additions=[]
    for number,parent in ((95,84),(96,95)):
        path=out/f'round{number}_prospective_run.json'
        data(path,{'name':f'round{number}','original_script':str(A/f'run_training_round{number}_v3_pipeline.py'),'original_arguments':[],'input_sha256':pins,'recovery_driver_sha256':sha(A/'run_reboot_recovery_attempt_20261006.py')})
        additions.append({'name':f'round{number}','round':number,'previous_run':str(path),'gate':{'parent':parent,'quality_slot':True,'markers':[{'path':str(A/'gradient_sampling_memmap_native_promotion_20261006/verification.json'),'statuses':['passed']}]},'scratch':str(ROOT/f'tmp/gradient_sampling_20261005/round{number}')})
    proposal={**old,'status':'prospective_queue7_extension_not_activated','deferred_jobs':[ *old['deferred_jobs'], *additions ],'exact_rank_cached_rounds':[ *old['exact_rank_cached_rounds'],95,96],'additional_required_rounds':[95,96],'input_sha256':{**old['input_sha256'],**pins},'original_shared_state_and_registry_retained':True,'original_scientific_gates_and_all_definitions_unchanged':True,'activation_requires_actual_owned_controller_handoff_and_publisher_observer_upgrade':True}
    data(out/'prospective_queue_plan_v7.json',proposal)
    import run_dependency_queue_v6_20261006 as previous
    import run_dependency_queue_v7_20261006 as new
    checks=[]
    for job in proposal['deferred_jobs']:
        if 'round' not in job:continue
        original=read(job['previous_run'])
        actual=new.original_driver_and_bridge(job,original)
        assert actual==previous.original_driver_and_bridge(job,original)
        checks.append({'round':job['round'],'parent':job['gate']['parent'],'driver':actual[0],'arguments':actual[1]})
    assert len(checks)==25 and proposal['deferred_jobs'][:-2]==old['deferred_jobs']
    assert checks[-2]['parent']==84 and checks[-1]['parent']==95
    # The original queued dispatch expression still selects the exact same
    # launcher for all old rounds. New rounds select their complete GOSS bridge.
    tree=ast.parse((A/'run_dependency_queue_v7_20261006.py').read_text(encoding='utf-8'))
    spawn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='spawn')
    call=next(n for n in ast.walk(spawn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='update' and any(k.arg=='original_script' for k in n.keywords))
    expr=next(k.value for k in call.keywords if k.arg=='original_script')
    expression=compile(ast.fix_missing_locations(ast.Expression(expr)),'actual_queue7_dispatch','eval')
    routes={}
    for number in [*range(67,91),95,96]:
        route=eval(expression,{'A':A,'str':str,'job':{'round':number},'plan':proposal})
        expected='run_goss_reference_quality_with_exact_rank_cache_20261006.py' if number in (95,96) else 'run_recovery_qualified_workflow_with_exact_rank_cache_v2_20261006.py' if number in old['exact_rank_cached_rounds'] else 'run_recovery_qualified_workflow_v2_20261006.py'
        assert Path(route).name==expected,(number,route);routes[str(number)]=route
    for path,digest in pins.items():assert sha(path)==digest,path
    data(out/'verification.json',{'status':'passed_actual25_original_and_additional_routes_and_exact_dispatch_expression','source_sha256':pins,'routes':checks,'actual_queue_dispatch_routes':routes,'original23_routes_and_gates_unchanged':True,'new95_96_prespecified_records':[124,138],'actual_live_controller_not_replaced':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False,'handoff_and_quality_execution_pending':True})
    print('passed_actual25_routes_and_queue7_prospective_extension_no_live_work_changed',flush=True)


if __name__=='__main__':main()
