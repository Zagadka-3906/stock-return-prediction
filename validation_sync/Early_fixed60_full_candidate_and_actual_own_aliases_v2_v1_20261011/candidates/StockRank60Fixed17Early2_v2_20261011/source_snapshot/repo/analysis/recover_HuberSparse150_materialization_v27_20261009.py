"""Reconcile eight already-written admitted programs and supply complete generator globals."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'HuberSparse150_materialization_v27_20261009.json'
NAME='run_HuberSparse59_round150_full_registration_v2_20261009.py'
DRIVER='run_HuberSparse59_round150_full_registration_recovery_v27_20261009.py'

def verify_preparation():
    import prepare_HuberSparse59_round150_sources_v2_20261009 as g
    p=read(A/'HuberSparse59_round150_source_preparation_v1_20261008.json')
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    admission=read(A/'HuberSparse59_round150_source_admission_v1_20261008.json')
    generated=g.generate(p['actual_comparison_parent_round'])
    expected=admission['generated_source_sha256'][str(p['actual_comparison_parent_round'])]
    for name,source in generated.items():assert sha(A/name)==hashlib.sha256(source.encode()).hexdigest()==expected[name],name

def routed(source):
    return BASE_ROUTE(source).replace('HuberSparse59_round150_full_registration_v5_20261009','HuberSparse59_round150_full_registration_v6_20261009').replace('actual_registration_recovery_v25','actual_registration_recovery_v27').replace('recovery_v25_file_IO','recovery_v27_file_IO')

def execute():
    global BASE_ROUTE
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    import recover_HuberSparse150_volume_transfer_v25_20261009 as previous
    import prepare_HuberSparse59_round150_sources_v2_20261009 as g
    original_read=previous.read;BASE_ROUTE=previous.routed;previous.routed=routed;original_main=g.main;g.main=verify_preparation
    def bound(path):
        value=original_read(path)
        if Path(path)==previous.META:value={**value,'drivers':{**value['drivers'],NAME:DRIVER},'input_sha256':{**value['input_sha256'],**m['input_sha256'],str(META):sha(META)}}
        return value
    previous.read=bound
    try:previous.execute(NAME)
    finally:previous.read=original_read;previous.routed=BASE_ROUTE;g.main=original_main

def main():
    import prepare_HuberSparse59_round150_sources_v2_20261009 as g
    admission=A/'HuberSparse59_round150_source_admission_v1_20261008.json';proof=read(admission)
    pilot=read(A/'HuberSparse59_official_comparison_v1_20261008/verification.json')
    ready_path=A/'HuberSparse59_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['sealed_candidate_complete'] and ready['best']==pilot['best']
    generated=g.generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    assert len(generated)==8
    for name,source in generated.items():assert sha(A/name)==hashlib.sha256(source.encode()).hexdigest()==expected[name],name
    folder=A/'service_owned_workflows_20261006/HuberSparse59_round150_full_registration_v5_20261009'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
    code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_HuberSparse150_materialization_v27_20261009 import execute\nif __name__=='__main__':execute()\n"
    with (A/DRIVER).open('x',encoding='utf8') as f:f.write(code)
    inputs=[Path(__file__),A/DRIVER,A/'recover_HuberSparse150_volume_transfer_v25_20261009.py',A/'HuberSparse150_volume_transfer_v25_20261009.json',admission,ready_path,
        *(folder/n for n in ('job_definition.json','native_launch.json','service_execution.json','stderr.log')),*(A/n for n in generated)]
    create(META,{'status':'passed_actual_eight_generated_programs_exact_original_admission_hashes_after_generator_namespace_failure',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},
        'actual_scientific_generated_bytes_changed':False,'new_scores':0,'new_fits':0,'test_labels_read':False})
    create(A/'HuberSparse59_round150_source_preparation_v1_20261008.json',{'status':'passed_actual59_sealed_candidate_and_admitted_full150_QA61_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(g.__file__),ready_path,admission,META,Path(__file__),*(A/n for n in generated)]},
        'new_quality_scores':0,'test_labels_read':False,'already_written_generated_bytes_exact_admitted_hashes':True})
    verify_preparation()
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('HuberSparse59_round150_full_registration_v6_20261009',DRIVER,[],{str(META):sha(META),str(A/DRIVER):sha(A/DRIVER)})
    create(A/'HuberSparse150_materialization_hidden_launch_v27_20261009.json',row)
    print({'owned_full150_worker':row['owned_worker_pid'],'generated_programs_reconciled':8},flush=True)

if __name__=='__main__':main()
