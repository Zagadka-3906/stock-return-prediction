"""Resume interrupted waiting148 controllers; keep all242 cases and32 canonical sources exact."""
from pathlib import Path
import ast,sys,time,importlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'actual_pending148_manual_resume_preparation_v5_20261009.json'
GATES={
 'JointCrossHuberOrder185_round147_full_registration_v1_20261008':'JointCrossHuberOrder185_round147_full_registration_v2_20261009',
 'AdaptiveJointCrossHuber80_native_historical_calendar_controls_v3_20261008':'AdaptiveJointCrossHuber80_native_historical_calendar_controls_v4_20261009',
 'AdaptiveJointCrossHuber238_actual_full_historical_controls_v3_20261008':'AdaptiveJointCrossHuber238_actual_full_historical_controls_v4_20261009',
 'main_publisher_v8_20261008':'main_publisher_v9_20261009'}
SCRIPTS={
 'verify_AdaptiveJointCrossHuber80_native_historical_calendar_v3_20261008.py':'verify_AdaptiveJointCrossHuber80_native_historical_calendar_v4_20261009.py',
 'verify_AdaptiveJointCrossHuber238_full_historical_controls_v3_20261008.py':'verify_AdaptiveJointCrossHuber238_full_historical_controls_v4_20261009.py',
 'bridge_actual_Adaptive148_control_pointer_aliases_v1_20261008.py':'bridge_actual_Adaptive148_control_pointer_aliases_v2_20261009.py',
 'verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py':'verify_AdaptiveJointCrossHuber242_round148_sources_v6_20261009.py',
 'publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py':'publish_AdaptiveJointCrossHuber242_evidence_v6_20261009.py',
 'run_AdaptiveJointCrossHuber242_official_comparison_v1_20261008.py':'run_AdaptiveJointCrossHuber242_official_comparison_v2_20261009.py',
 'prepare_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py':'prepare_AdaptiveJointCrossHuber242_selected_candidate_v3_20261009.py',
 'seal_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py':'seal_AdaptiveJointCrossHuber242_selected_candidate_v2_20261009.py',
 'run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py':'run_AdaptiveJointCrossHuber242_round148_full_registration_v5_20261009.py',
 'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v5_20261008.py':'dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v6_20261009.py'}
PREVIOUS_DRIVERS={
 'verify_AdaptiveJointCrossHuber242_round148_sources_v5_20261008.py':SCRIPTS['verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py'],
 'publish_AdaptiveJointCrossHuber242_evidence_v5_20261008.py':SCRIPTS['publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py'],
 'prepare_AdaptiveJointCrossHuber242_selected_candidate_v2_20261008.py':SCRIPTS['prepare_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py'],
 'run_AdaptiveJointCrossHuber242_round148_full_registration_v4_20261008.py':SCRIPTS['run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py']}
HELPERS={'verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py',
 'publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py','prepare_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py',
 'run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py'}

def routed(source,dispatcher=False):
    for before,after in {**GATES,**PREVIOUS_DRIVERS}.items():source=source.replace(before,after)
    if dispatcher:
        for old,new in SCRIPTS.items():source=source.replace(old,new)
        source=source.replace('complete_hidden_launches_v5_20261008','complete_hidden_launches_v6_20261009')
    return source

def execute(original,phase=None):
    for p,d in read(META)['input_sha256'].items():assert sha(p)==d,p
    import prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008 as generator
    paths=generator.source_paths;extras=[Path(__file__),META,*(A/p for p in SCRIPTS.values())]
    generator.source_paths=lambda:list(dict.fromkeys([*paths(),*extras]))
    if original in HELPERS:
        import recover_Adaptive148_native_dispatch_v3_20261008 as runtime
        runtime.MAP={k:GATES.get(v,v) for k,v in runtime.MAP.items()}
        runtime.MAP.update(GATES)
        runtime.DRIVERS={**runtime.DRIVERS,**{p:SCRIPTS[p] for p in HELPERS}}
        from prepare_pending148_149_phase_isolated_publishers_v1_20261008 import execute as retained
        retained(148,original,phase)
    else:
        source=routed((A/original).read_text(encoding='utf8'),original.startswith('dispatch_'))
        # Original controls retain their previously unused E output identities.
        # The live service and __file__ now explicitly identify the fresh attempt.
        namespace={'__file__':str(A/SCRIPTS[original]),'__name__':'__main__'}
        exec(compile(source,str(A/original),'exec'),namespace)

def main():
    services=A/'service_owned_workflows_20261006'
    stopped=['AdaptiveJointCrossHuber80_native_historical_calendar_controls_v3_20261008',
        'AdaptiveJointCrossHuber238_actual_full_historical_controls_v3_20261008',
        'AdaptiveJointCrossHuber148_complete_chronological_dispatch_v5_20261008',
        'actual_Adaptive148_control_pointer_aliases_v1_20261008']
    for name in stopped:
        folder=services/name;assert not owned(read(folder/'native_launch.json')) and (folder/'user_requested2355_interruption_20261008.json').exists()
    # These controllers were stopped while waiting, before any immutable scientific output was created.
    for path in [Path('E:/赛题五_本机临时/AdaptiveJointCrossHuber80_native_historical_calendar_v3_20261008'),
        Path('E:/赛题五_本机临时/AdaptiveJointCrossHuber238_parent134_historical_v3_20261008'),
        A/'actual_AdaptiveJointCrossHuber80_native_calendar_location_v3_20261008.json',
        A/'actual_AdaptiveJointCrossHuber238_parent134_location_v3_20261008.json',
        A/'actual_Adaptive148_control_pointer_aliases_v1_20261008.json']:
        assert not path.exists(),path
    products=[];proofs=[]
    for old,new in SCRIPTS.items():
        original=A/old;assert original.is_file()
        source="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom resume_pending148_verified_gates_v5_20261009 import execute\n"
        if old.startswith('publish_'):
            source+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(old)+",p.parse_args().phase)\n"
        else:source+="if __name__=='__main__':execute("+repr(old)+")\n"
        compile(source,str(A/new),'exec')
        with (A/new).open('x',encoding='utf8') as stream:stream.write(source)
        products.append(A/new)
        before=original.read_text(encoding='utf8');after=routed(before,old.startswith('dispatch_'));ast.parse(after)
        proofs.append({'original':str(original),'original_sha256':sha(original),'new_driver':str(A/new),'changes_only_explicit_upstream_identity_and_wrapper_names':True})
    prospective=A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json'
    for p,d in read(prospective)['input_sha256'].items():assert sha(p)==d,p
    sources=[Path(__file__),prospective,A/'pending148_149_phase_isolation_preparation_v1_20261008.json',
        A/'recover_Adaptive148_native_dispatch_v3_20261008.py',A/'recover_Adaptive148_own_full_service_identity_v4_20261008.py',
        *(A/p for p in SCRIPTS),*products,*(services/n/'user_requested2355_interruption_20261008.json' for n in stopped)]
    pins={str(p):sha(p) for p in sources}
    create(META,{'status':'prepared_manual_resume148_waiting_only_controls_and_dispatch_current_verified147_gate',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'source_binding_controls':proofs,
        'all242_case_parameters_and_original32_generated_sources_unchanged':True,'existing_corrected_native_storage_dispatch_preserved':True,
        'real_phase_isolation_regression_preserved':True,'previously_unused_output_paths_verified_before_reuse':True,
        'old_services_not_marked_scientifically_passed':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for name,driver in [
        (GATES[stopped[0]],SCRIPTS['verify_AdaptiveJointCrossHuber80_native_historical_calendar_v3_20261008.py']),
        (GATES[stopped[1]],SCRIPTS['verify_AdaptiveJointCrossHuber238_full_historical_controls_v3_20261008.py']),
        ('actual_Adaptive148_control_pointer_aliases_v2_20261009',SCRIPTS['bridge_actual_Adaptive148_control_pointer_aliases_v1_20261008.py']),
        ('AdaptiveJointCrossHuber148_complete_chronological_dispatch_v6_20261009',SCRIPTS['dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v5_20261008.py'])]:
        rows[name]=start(name,driver,[],{str(Path(__file__)):sha(__file__),str(META):sha(META),str(A/driver):sha(A/driver)})
    create(A/'actual_pending148_manual_resume_hidden_launches_v5_20261009.json',rows)
    print({'waiting148_started':{n:r['owned_worker_pid'] for n,r in rows.items()}},flush=True)
if __name__=='__main__':main()
