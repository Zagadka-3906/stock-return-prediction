"""Preserve successful frozen inference and failed1 sealing; resume exact source bytes with valid E evidence paths."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    failed=A/'service_owned_workflows_20261006/ConeRidgeFine68_selected_candidate_sealing_v1_20261008'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    assert 'is not in the subpath' in (failed/'stderr.log').read_text(encoding='utf8')
    candidate=ROOT/'candidates/ConeRidgeFine68_v1_20261008';prediction=read(candidate/'verification.json')
    assert prediction['status']=='passed' and len(prediction['models'])==19
    for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert prediction[key]
    assert read(candidate/'ConeRidge64_complete_parent_native_replay_verification.json')['status']=='passed_actual_complete_parent_and_ConeRidge64_two_full_native_independent_replays_and_cold80'
    assert not (candidate/'manifest.json').exists()
    original=A/'seal_ConeRidgeFine68_selected_candidate_v1_20261008.py';text=original.read_text(encoding='utf8')
    before="os.link(source,target);assert sha(target)==info['sha256']"
    after="assert sha(target)==info['sha256'] if target.exists() else (os.link(source,target) is None and sha(target)==info['sha256'])"
    assert text.count(before)==1;text=text.replace(before,after)
    before="target=candidate/'evidence'/source.relative_to(A);target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);assert sha(target)==sha(source)"
    after="""relative=source.relative_to(A) if source.is_relative_to(A) else Path('external_frozen_metadata')/(sha(source)+'_'+source.name)
        target=candidate/'evidence'/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert sha(target)==sha(source)
        else:os.link(source,target)
        assert sha(target)==sha(source)"""
    assert text.count(before)==1;text=text.replace(before,after)
    target=A/'seal_ConeRidgeFine68_selected_candidate_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    old_full=A/'run_ConeRidgeFine68_round143_full_registration_v1_20261008.py';value=old_full.read_text(encoding='utf8')
    value=value.replace('ConeRidgeFine68_selected_candidate_sealing_v1_20261008','ConeRidgeFine68_selected_candidate_sealing_v2_20261008')
    value=value.replace('round143_actual_registration_v1_20261008','round143_actual_registration_v2_20261008').replace('full_registration_v1_file_IO','full_registration_v2_file_IO')
    full2=A/'run_ConeRidgeFine68_round143_full_registration_v2_20261008.py';assert not full2.exists()
    needle="with installed(A/'run_ConeRidgeFine68_round143_full_registration_v2_file_IO_20261008'),installed_transfer():main()"
    assert value.count(needle)==1
    replacement="""import prepare_ConeRidgeFine68_round143_sources_v1_20261008 as generator
    original_paths=generator.source_paths
    recovery_sources=[Path(__file__),A/'seal_ConeRidgeFine68_selected_candidate_v2_20261008.py',A/'ConeRidgeFine143_E_snapshot_sealing_recovery_v2_20261008.json',
        A/'recover_ConeRidgeFine143_E_snapshot_sealing_v2_20261008.py',
        A/'service_owned_workflows_20261006/ConeRidgeFine68_selected_candidate_sealing_v1_20261008/service_execution.json',
        A/'service_owned_workflows_20261006/ConeRidgeFine68_selected_candidate_sealing_v1_20261008/stderr.log']
    # Administrative source-list addition in this isolated worker; generated scientific source bytes are unchanged.
    generator.source_paths=lambda:list(dict.fromkeys([*original_paths(),*recovery_sources]))
    try:
        with installed(A/'run_ConeRidgeFine68_round143_full_registration_v2_file_IO_20261008'),installed_transfer():main()
    finally:generator.source_paths=original_paths"""
    value=value.replace(needle,replacement);compile(value,str(full2),'exec');full2.write_text(value,encoding='utf8',newline='\n')
    sources=[Path(__file__),original,target,old_full,full2,candidate/'verification.json',candidate/'ConeRidge64_complete_parent_native_replay_verification.json',failed/'service_execution.json',failed/'stderr.log']
    create(A/'ConeRidgeFine143_E_snapshot_sealing_recovery_v2_20261008.json',{
        'status':'prepared_fresh_seal2_from_passed_two_full1599600_and_cold80_native_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'original_failed_seal1_and_partial_source_links_preserved':True,
        'only_changes':'hash-verify existing copied source files; use bounded hashed external path for E freeze metadata; add administrative recovery sources before registry',
        'actual_selected_native_models':19,'new_model_fits':0,'new_official_scores':0,'new_inference_calls':0,
        'all_original_scientific_source_and_parameter_freeze_preserved':True,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in sources};rows={}
    for name,path in (('ConeRidgeFine68_selected_candidate_sealing_v2_20261008',target),('ConeRidgeFine68_round143_full_registration_v2_20261008',full2)):
        rows[name]=start(name,path.name,[],pins)
    create(A/'ConeRidgeFine143_E_snapshot_sealing_hidden_launches_v2_20261008.json',{
        'status':'started_fresh_seal2_full_registration2_preserving_actual_passed_inference_and_failed1_evidence','launches':rows,
        'input_sha256':pins,'new_official_scores':0,'new_inference_calls':0})
    print('Fresh143 seal2 and full-registration2 started; original full/native/cold inference is retained.',flush=True)
if __name__=='__main__':main()
