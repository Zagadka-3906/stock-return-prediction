"""Queue all81 official comparisons and complete candidate/QA/main phases after actual controls."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_BF16Drop05_156_prospective_receivers_v1_20261009 import transform

def main():
    prospective=A/'BF16Drop05_81_prospective_routes_v1_20261009.json';p=read(prospective)
    assert (p['prospective_sources'],len(p['graph_controls']),len(p['baseline_controls']),len(p['physical_model_count_absolute_weight_sort_controls']))==(64,2400,24,16)
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    pairs=[('verify_BF16Seed10_80_round155_sources_v1_20261009.py','verify_BF16Drop05_81_round156_sources_v2_20261009.py'),
        ('verify_BF16Seed10_155_prospective_service_v1_20261009.py','verify_BF16Drop05_156_prospective_service_v2_20261009.py'),
        ('dispatch_BF16Seed10_155_complete_pipeline_v1_20261009.py','dispatch_BF16Drop05_156_complete_pipeline_v2_20261009.py'),
        ('run_BF16Seed10_155_safe_registration_v1_20261009.py','run_BF16Drop05_156_safe_registration_v2_20261009.py')]
    sources=[Path(__file__),A/'prepare_BF16Drop05_156_complete_pipeline_v1_20261009.py',prospective,A/'verify_BF16Drop05_81_prospective_routes_v3_20261009.py',
        A/'BF16Drop05_156_prospective_assertion_correction_v2_20261009.json']
    for old,new in pairs:
        src,dst=A/old,A/new;s=transform(src.read_text(encoding='utf8'))
        s=s.replace('BF16Drop05_156_complete_pipeline_preparation_v1_20261009','BF16Drop05_156_complete_pipeline_preparation_v2_20261009').replace('dispatch_BF16Drop05_156_complete_pipeline_v1_20261009.py','dispatch_BF16Drop05_156_complete_pipeline_v2_20261009.py')
        s=s.replace('BF16TwoSeed79_round154_full_registration_v1_20261009','BF16Seed10_80_round155_full_registration_v1_20261009')
        for x,y in [('==56','==64'),('==2100','==2400'),("'prospective_sources':56","'prospective_sources':64"),
            ('cold56_prospective','cold64_prospective'),('complete56_routes','complete64_routes'),
            ('(56,2100,21,14)','(64,2400,24,16)'),("'passed_source_routes':56","'passed_source_routes':64"),
            ("'passed_graphs':2100","'passed_graphs':2400"),('actual154_and_duplicate','actual155_and_duplicate')]:s=s.replace(x,y)
        if old.startswith('run_'):
            needle="A/'dispatch_BF16Drop05_156_complete_pipeline_v2_20261009.py'"
            assert s.count(needle)==1
            s=s.replace(needle,needle+",A/'verify_BF16Drop05_81_prospective_routes_v3_20261009.py',A/'BF16Drop05_156_prospective_assertion_correction_v2_20261009.json'")
        compile(s,str(dst),'exec');assert not dst.exists();dst.write_text(s,encoding='utf8');sources.extend((src,dst))
    specs=[('BF16Drop05_81_round156_source_admission_v1_20261009','verify_BF16Drop05_81_round156_sources_v2_20261009.py',[]),
        ('BF16Drop05_81_controls_main_publication_v1_20261009','publish_BF16Drop05_81_evidence_v1_20261009.py',['controls']),
        ('BF16Drop05_81_official_comparison_v1_20261009','run_BF16Drop05_81_official_comparison_v1_20261009.py',[]),
        ('BF16Drop05_81_scores_main_publication_v1_20261009','publish_BF16Drop05_81_evidence_v1_20261009.py',['scores']),
        ('BF16Drop05_81_selected_candidate_preparation_v1_20261009','prepare_BF16Drop05_81_selected_candidate_v1_20261009.py',[]),
        ('BF16Drop05_81_selected_candidate_sealing_v1_20261009','seal_BF16Drop05_81_selected_candidate_v1_20261009.py',[]),
        ('BF16Drop05_81_round156_full_registration_v1_20261009','run_BF16Drop05_156_safe_registration_v2_20261009.py',[])]
    sources.extend(A/d for _,d,_ in specs)
    sources.extend([A/'run_BF16Drop05_81_round156_full_registration_v1_20261009.py',
        A/'verify_BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.py'])
    for f in sources:
        assert f.is_file(),f
        if f.suffix=='.py':compile(f.read_text(encoding='utf8'),str(f),'exec')
    # Exercise actual comparison-parent guards for all eight future anchors and
    # both invalid neighbors before the candidate has a chance to run.
    guards=[]
    for filename in ('prepare_BF16Drop05_81_selected_candidate_v1_20261009.py','run_BF16Drop05_81_round156_full_registration_v1_20261009.py'):
        tree=ast.parse((A/filename).read_text(encoding='utf8'))
        assertion=next(n for n in ast.walk(tree) if isinstance(n,ast.Assert) and ast.unparse(n.test).startswith('parent_number in '))
        code=compile(ast.fix_missing_locations(ast.Module(body=[assertion],type_ignores=[])),filename,'exec')
        for parent in range(147,157):
            try:exec(code,{'parent_number':parent});accepted=True
            except AssertionError:accepted=False
            assert accepted==(148<=parent<=155),(filename,parent)
            guards.append({'source':filename,'parent':parent,'accepted':accepted})
    guardproof=A/'BF16Drop05_156_actual_parent_guard_controls_v2_20261009.json'
    create(guardproof,{'status':'passed20_actual_comparison_parent_receiver_membership_guards',
        'controls':guards,'input_sha256':{str(A/n):sha(A/n) for n in ('prepare_BF16Drop05_81_selected_candidate_v1_20261009.py','run_BF16Drop05_81_round156_full_registration_v1_20261009.py')},
        'new_quality_scores':0,'test_labels_read':False});sources.append(guardproof)
    meta=A/'BF16Drop05_156_complete_pipeline_preparation_v2_20261009.json'
    create(meta,{'status':'prepared_complete156_seven_receivers_after64_routes2400_graphs_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in dict.fromkeys(sources)},
        'receiver_specs':specs,'fixed_stage_base_round':148,'comparison_anchor_rounds':list(range(148,156)),
        'expected_quality_cases':81,'native_saved_annual_states_required':6,'QA_version':67,'wave':439,
        'actual20_parent_guard_controls':guards,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={}
    for name,driver in [('BF16Drop05_156_complete_prospective_controls_v1_20261009','verify_BF16Drop05_156_prospective_service_v2_20261009.py'),
        ('BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009','verify_BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009.py'),
        ('BF16Drop05_156_complete_chronological_dispatch_v1_20261009','dispatch_BF16Drop05_156_complete_pipeline_v2_20261009.py')]:
        launches[name]=start(name,driver,[],{str(meta):sha(meta),str(A/driver):sha(A/driver)})
    create(A/'BF16Drop05_156_complete_hidden_controller_launches_v2_20261009.json',launches)
    print({'complete_receivers':7,'prospective_sources':64,'graph_controls':2400,'parent_guard_controls':20,
        'waiting_controller_workers':{n:r['owned_worker_pid'] for n,r in launches.items()}},flush=True)
if __name__=='__main__':main()
