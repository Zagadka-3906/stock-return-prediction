"""Resume the untouched Pure149 frontier with current native/full/duplicate service identities."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'actual_pending149_manual_resume_preparation_v6_20261009.json'
GATES={
 'PureRFFHuber80_native_historical_calendar_controls_v2_20261008':'PureRFFHuber80_native_historical_calendar_controls_v3_20261009',
 'PureRFFHuber124_actual_full_historical_controls_v2_20261008':'PureRFFHuber124_actual_full_historical_controls_v3_20261009',
 'Pure149_prior_complete_forecast_duplicate_audit_v1_20261008':'Pure149_prior_complete_forecast_duplicate_audit_v2_20261009',
 'main_publisher_v8_20261008':'main_publisher_v9_20261009'}
SCRIPTS={
 'verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py':'verify_PureRFFHuber80_native_historical_calendar_v3_20261009.py',
 'verify_PureRFFHuber124_full_historical_controls_v2_20261008.py':'verify_PureRFFHuber124_full_historical_controls_v3_20261009.py',
 'verify_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.py':'verify_Pure149_prior_complete_forecast_duplicate_audit_v2_20261009.py',
 'verify_PureRFFHuber128_round149_sources_v2_20261008.py':'verify_PureRFFHuber128_round149_sources_v5_20261009.py',
 'publish_PureRFFHuber128_evidence_v2_20261008.py':'publish_PureRFFHuber128_evidence_v5_20261009.py',
 'run_PureRFFHuber128_official_comparison_v2_20261008.py':'run_PureRFFHuber128_official_comparison_v3_20261009.py',
 'prepare_PureRFFHuber128_selected_candidate_v1_20261008.py':'prepare_PureRFFHuber128_selected_candidate_v2_20261009.py',
 'seal_PureRFFHuber128_selected_candidate_v1_20261008.py':'seal_PureRFFHuber128_selected_candidate_v2_20261009.py',
 'run_PureRFFHuber128_round149_full_registration_v2_20261008.py':'run_PureRFFHuber128_round149_full_registration_v4_20261009.py',
 'dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py':'dispatch_PureRFFHuber149_complete_pipeline_v5_20261009.py'}
PREVIOUS_DRIVERS={
 'verify_PureRFFHuber128_round149_sources_v4_20261008.py':SCRIPTS['verify_PureRFFHuber128_round149_sources_v2_20261008.py'],
 'publish_PureRFFHuber128_evidence_v4_20261008.py':SCRIPTS['publish_PureRFFHuber128_evidence_v2_20261008.py'],
 'run_PureRFFHuber128_round149_full_registration_v3_20261008.py':SCRIPTS['run_PureRFFHuber128_round149_full_registration_v2_20261008.py']}
HELPERS={'verify_PureRFFHuber128_round149_sources_v2_20261008.py','publish_PureRFFHuber128_evidence_v2_20261008.py',
 'run_PureRFFHuber128_round149_full_registration_v2_20261008.py'}

def routed(source,dispatcher=False):
    for old,new in {**GATES,**PREVIOUS_DRIVERS}.items():source=source.replace(old,new)
    if dispatcher:
        for old,new in SCRIPTS.items():source=source.replace(old,new)
        source=source.replace('complete_hidden_launches_v4_20261008','complete_hidden_launches_v5_20261009')
    return source

def execute(original,phase=None):
    for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
    import prepare_PureRFFHuber128_round149_sources_v2_20261008 as generator
    paths=generator.source_paths;extra=[Path(__file__),META,*(A/n for n in SCRIPTS.values())]
    generator.source_paths=lambda:list(dict.fromkeys([*paths(),*extra]))
    if original in HELPERS:
        import prepare_Pure149_duplicate_bound_receivers_v3_20261008 as prior
        path=Path(prior.__file__);source=routed(path.read_text(encoding='utf8'))
        needle="p.read_text(encoding='utf8')";assert source.count(needle)==1
        source=source.replace(needle,"ROUTE_CURRENT_SERVICES(p.read_text(encoding='utf8'))")
        namespace={'__file__':str(path),'__name__':'actual_verified149_manual_resume_runtime','ROUTE_CURRENT_SERVICES':routed}
        exec(compile(source,str(path),'exec'),namespace)
        namespace['DRIVERS']={**namespace['DRIVERS'],**{n:SCRIPTS[n] for n in HELPERS}}
        prior.execute=namespace['execute']
        from prepare_pending148_149_phase_isolated_publishers_v1_20261008 import execute as retained
        retained(149,original,phase)
    else:
        source=routed((A/original).read_text(encoding='utf8'),original.startswith('dispatch_'))
        exec(compile(source,str(A/original),'exec'),{'__file__':str(A/SCRIPTS[original]),'__name__':'__main__'})

def main():
    services=A/'service_owned_workflows_20261006'
    stopped=['PureRFFHuber80_native_historical_calendar_controls_v2_20261008','PureRFFHuber124_actual_full_historical_controls_v2_20261008',
        'Pure149_prior_complete_forecast_duplicate_audit_v1_20261008','PureRFFHuber149_complete_chronological_dispatch_v4_20261008']
    for name in stopped:
        f=services/name;assert not owned(read(f/'native_launch.json')) and (f/'user_requested2355_interruption_20261008.json').exists()
    for p in [Path('E:/赛题五_本机临时/PureRFFHuber80_native_historical_calendar_v2_20261008'),
        Path('E:/赛题五_本机临时/PureRFFHuber124_parent134_historical_v2_20261008'),
        Path('E:/赛题五_本机临时/Pure149_prior_complete_forecast_duplicate_audit_v1_20261008'),
        A/'actual_PureRFFHuber80_native_calendar_location_v2_20261008.json',A/'actual_PureRFFHuber124_parent134_location_v2_20261008.json',
        A/'actual_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.json',A/'Pure149_prior_complete_forecast_duplicate_audit_raw_v1_20261008.json']:
        assert not p.exists(),p
    products=[]
    for old,new in SCRIPTS.items():
        assert (A/old).is_file()
        source="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom resume_pending149_verified_gates_v6_20261009 import execute\n"
        if old.startswith('publish_'):source+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(old)+",p.parse_args().phase)\n"
        else:source+="if __name__=='__main__':execute("+repr(old)+")\n"
        compile(source,str(A/new),'exec')
        with (A/new).open('x',encoding='utf8') as stream:stream.write(source)
        products.append(A/new);ast.parse(routed((A/old).read_text(encoding='utf8'),old.startswith('dispatch_')))
    prospective=A/'PureRFFHuber128_prospective_routes_v2_20261008.json'
    for p,d in read(prospective)['input_sha256'].items():assert sha(p)==d,p
    inputs=[Path(__file__),prospective,A/'prepare_Pure149_duplicate_bound_receivers_v3_20261008.py',
        A/'pending148_149_phase_isolation_preparation_v1_20261008.json',*(A/n for n in SCRIPTS),*products,
        *(services/n/'user_requested2355_interruption_20261008.json' for n in stopped)]
    pins={str(p):sha(p) for p in inputs}
    create(META,{'status':'prepared_manual_resume149_native_full_duplicate_and_chronological_waits',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'all128_scoring_cases_and32_canonical_sources_unchanged':True,
        'previously_unused_E_output_paths_verified_before_reuse':True,'duplicate_all_numeric_SHA_and_available8_metrics_guards_preserved':True,
        'phase_isolation_preserved':'actual_isolated_publisher_phase_preflight_v1_20261008.json',
        'old_stopped_services_not_claimed_scientifically_passed':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for name,driver in [(GATES[stopped[0]],SCRIPTS['verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py']),
        (GATES[stopped[1]],SCRIPTS['verify_PureRFFHuber124_full_historical_controls_v2_20261008.py']),
        (GATES[stopped[2]],SCRIPTS['verify_Pure149_prior_complete_forecast_duplicate_audit_v1_20261008.py']),
        ('PureRFFHuber149_complete_chronological_dispatch_v5_20261009',SCRIPTS['dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py'])]:
        rows[name]=start(name,driver,[],{str(Path(__file__)):sha(__file__),str(META):sha(META),str(A/driver):sha(A/driver)})
    create(A/'actual_pending149_manual_resume_hidden_launches_v6_20261009.json',rows)
    print({'waiting149_started':{n:r['owned_worker_pid'] for n,r in rows.items()}},flush=True)
if __name__=='__main__':main()
