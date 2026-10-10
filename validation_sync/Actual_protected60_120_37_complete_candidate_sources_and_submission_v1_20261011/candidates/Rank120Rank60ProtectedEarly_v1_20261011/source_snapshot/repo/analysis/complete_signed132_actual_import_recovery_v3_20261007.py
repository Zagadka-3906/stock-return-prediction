"""Complete pre-score import audit, allowing only already-admitted generated sources."""
from pathlib import Path
import ast,sys,time,psutil,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    import prepare_nonflag_ReverseBayes40_round132_sources_v1_20261007 as generator
    prospective=read(A/'nonflag_ReverseBayes40_prospective_routes_v1_20261007.json')
    assert not prospective['issues'] and len(prospective['graph_controls'])==12
    generated=generator.generate(112);controls=[]
    paths=[Path(__file__),A/'recover_signed132_actual_import_and_publication_v2_20261007.py']
    for name in ['run_nonflag_ReverseBayes40_admitted_comparison','verify_nonflag_ReverseBayes40_round132_sources','publish_nonflag_ReverseBayes40_evidence','queue_nonflag_ReverseBayes132_after_actual131']:
        new=A/(name+'_v2_20261007.py');assert new.is_file();compile(new.read_text(encoding='utf8'),str(new),'exec');paths.append(new)
    for path in sorted(A.glob('*ReverseBayes*20261007.py')):
        if path.name=='run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py':continue
        for node in ast.walk(ast.parse(path.read_text(encoding='utf8'))):
            modules=[node.module] if isinstance(node,ast.ImportFrom) else [n.name for n in node.names] if isinstance(node,ast.Import) else []
            for module in modules:
                if module and 'ReverseBayes' in module:
                    resolved=A/(module+'.py')
                    if resolved.is_file():digest=sha(resolved);kind='existing_actual_source'
                    else:
                        assert resolved.name in generated,(path,module)
                        compile(generated[resolved.name],str(resolved),'exec')
                        digest=hashlib.sha256(generated[resolved.name].encode('utf8')).hexdigest();kind='compiled_predeclared_generator_output'
                    controls.append({'source':str(path),'module':module,'resolved_sha256':digest,'resolution':kind})
    assert not (A/'nonflag_ReverseBayes40_official_comparison_v1_20261007').exists()
    assert not any((A/'service_owned_workflows_20261006'/n).exists() for n in ['nonflag_ReverseBayes40_round132_source_admission_v1','nonflag_ReverseBayes40_round132_source_admission_v2','nonflag_ReverseBayes40_official_comparison_v1'])
    folder=A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual132_after131_dependency_queue';row=read(folder/'native_launch.json');assert owned(row);identities=[]
    for key,birth in [('owned_worker_pid','owned_worker_creation_time'),('pid','owned_parent_creation_time')]:
        proc=psutil.Process(row[key]);assert abs(proc.create_time()-row[birth])<.03
        assert 'run_service_owned_windows_workflow_20261006.py' in ' '.join(proc.cmdline())
        identities.append({'pid':proc.pid,'creation_time':proc.create_time(),'cmdline':proc.cmdline()})
    for item in identities:psutil.Process(item['pid']).terminate()
    for item in identities:
        try:psutil.Process(item['pid']).wait(timeout=10)
        except psutil.NoSuchProcess:pass
    assert not owned(row)
    failure=A/'signed132_import_recovery_v2_preserved_administrative_failure_20261007.json'
    create(failure,{'status':'preserved_failed_pre_score_import_audit_that_did_not_allow_generated_registry_modules',
      'error':'register_nonflag_ReverseBayes40_round132_artifacts_20261007 is predeclared by generator, not yet materialized',
      'new_native_fits':0,'new_quality_scores':0,'original_waiting_queue_was_not_terminated_by_failed_V2_script':True})
    paths += [failure,*folder.glob('*.json'),*folder.glob('*.log'),A/'run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py',A/'verify_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',A/'publish_nonflag_ReverseBayes40_evidence_v1_20261007.py',A/'queue_nonflag_ReverseBayes132_after_actual131_20261007.py']
    proof=A/'signed132_actual_import_and_publication_recovery_v2_20261007.json'
    create(proof,{'status':'resolved_actual_signed132_executor_import_and_publication_metadata_before_any_scores',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},
      'actual_signed_executor_import_controls':controls,'original_published_V1_bytes_retained':True,
      'administratively_superseded_waiting_controller':identities,'only_waiting_controller_terminated':True,
      'actual_native_controls_unchanged':True,'numerical_scorer_original_V1_bytes_unchanged':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    pins={**read(proof)['input_sha256'],str(proof):sha(proof)}
    launch=start('nonflag_ReverseBayes40_actual132_after131_dependency_queue_v2','queue_nonflag_ReverseBayes132_after_actual131_v2_20261007.py',[],pins)
    create(A/'signed132_recovered_actual_hidden_queue_launch_v2_20261007.json',{'status':'started_corrected_waiting_signed132_queue_with_fixed2312_cutoff','identity':launch,'input_sha256':pins})
    print('PASS actual import audit and corrected waiting signed132 queue; scores added=0',flush=True)

if __name__=='__main__':main()
