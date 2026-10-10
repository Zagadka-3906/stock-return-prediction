"""Reuse all eight actually written admitted source bytes; record fresh preparation pins at the actual admission5 path."""
from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    old=A/'run_CrossFamily94_round136_full_registration_v5_20261008.py'
    terminal=A/'service_owned_workflows_20261006/CrossFamily94_round136_full_registration_v5_20261008/service_execution.json'
    assert read(terminal)['status']=='failed'
    assert read(A/'service_owned_workflows_20261006/CrossFamily94_selected_candidate_sealing_v5_20261008/service_execution.json')['status']=='passed'
    import prepare_CrossFamily94_round136_sources_v4_20261008 as generator
    pilot=read(A/'CrossFamily94_official_comparison_v1_20261008/verification.json');admission=A/'CrossFamily94_round136_source_admission_v5_20261008.json'
    expected=read(admission)['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    generated=generator.generate(pilot['actual_comparison_parent_round']);assert len(generated)==8 and set(generated)==set(expected)
    for name,value in generated.items():assert sha(A/name)==expected[name],name
    text=old.read_text(encoding='utf8').replace('actual_registration_v5_20261008','actual_registration_v6_20261008').replace('full_registration_v5_file_IO_20261008','full_registration_v6_file_IO_20261008')
    text=text.replace("'CrossFamily94_round136_source_admission_v4_20261008.json':'CrossFamily94_round136_source_admission_v5_20261008.json'", "'CrossFamily94_round136_source_admission_v4_20261008.json':'CrossFamily94_round136_source_admission_v5_20261008.json','CrossFamily94_round136_source_preparation_v4_20261008.json':'CrossFamily94_round136_source_preparation_v5_20261008.json'")
    needle='    from prepare_CrossFamily94_round136_sources_v4_20261008 import main as prepare_sources';assert text.count(needle)==1
    replacement="""    def prepare_sources():
        # The failed5 worker wrote every frozen generated source, then failed only while hashing a missing old admission path.
        # Do not overwrite or regenerate those scientific source bytes.
        proof_path=A/'CrossFamily94_round136_source_admission_v5_20261008.json';proof=read(proof_path)
        ready_path=A/'CrossFamily94_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
        pilot=read(A/'CrossFamily94_official_comparison_v1_20261008/verification.json')
        assert ready['sealed_candidate_complete'] and ready['best']==pilot['best'] and len(pilot['records'])==94
        generated=actual_generator.generate(pilot['actual_comparison_parent_round'])
        expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
        assert len(generated)==8 and set(generated)==set(expected)
        for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
        for name,value in generated.items():
            import hashlib
            assert sha(A/name)==hashlib.sha256(value.encode()).hexdigest()==expected[name],name
            compile(value,str(A/name),'exec')
        create(A/'CrossFamily94_round136_source_preparation_v5_20261008.json',{
            'status':'passed_actual94_sealed_candidate_and_admitted_full136_QA47_sources',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':136,'scored_records':94,
            'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
            'input_sha256':{str(path):sha(path) for path in [Path(__file__),Path(actual_generator.__file__),ready_path,proof_path,*[A/name for name in generated]]},
            'all8_already_written_generated_sources_rehashed_exact_to_original24_source_preflight':True,
            'new_generated_scientific_source_writes':0,'old_registration5_failure_preserved':True,
            'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
"""
    text=text.replace(needle,replacement)
    text=text.replace("prep=read(A/'CrossFamily94_round136_source_preparation_v4_20261008.json')", "prep=read(A/'CrossFamily94_round136_source_preparation_v5_20261008.json')")
    path=A/'run_CrossFamily94_round136_full_registration_v6_20261008.py';assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
    sources=[Path(__file__),old,path,terminal,admission,*[A/name for name in generated]]
    pins={str(p):sha(p) for p in sources}
    create(A/'CrossFamily136_exact_generated_source_recovery_v6_20261008.json',{
        'status':'frozen_actual_eight_generated_sources_exact_to_admitted24_routes_before_registration6',
        'input_sha256':pins,'original_failed5_preserved':True,'scientific_source_bytes_changed':0,
        'new_scores':0,'new_inference_calls':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('CrossFamily94_round136_full_registration_v6_20261008',path.name,[],pins)
    create(A/'CrossFamily136_exact_generated_source_registration_hidden_launch_v6_20261008.json',row)
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
