"""Correct only administrative40/52 counts in fresh execution sources, preserving originals."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def save(old,new,text):
    source=A/old;target=A/new;compile(text,str(target),'exec');assert not target.exists();target.write_text(text,encoding='utf8',newline='\n');return source,target

def main():
    service=A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1'
    assert read(service/'service_execution.json')['status']=='failed'
    assert not (A/'optimization_20261003_r128').exists() and not (ROOT/'candidates/optimization_20261003_r128').exists()
    prep=A/'nonflag_RidgeFine52_round128_source_preparation_v1_20261007.json'
    for p,d in read(prep)['input_sha256'].items():assert sha(p)==d,p
    proofpath=A/'nonflag_RidgeFine52_administrative52_count_recovery_v2_20261007.json'
    names={
      'register_nonflag_RidgeFine52_round128_artifacts_20261007.py':'register_nonflag_RidgeFine52_round128_artifacts_v2_20261007.py',
      'publish_nonflag_RidgeFine52_round128_full_validation_20261007.py':'publish_nonflag_RidgeFine52_round128_full_validation_v2_20261007.py',
      'optimize_training_round128.py':'optimize_training_round128_metadata_v2_20261007.py',
      'finalize_training_round128.py':'finalize_training_round128_metadata_v2_20261007.py',
      'run_nonflag_RidgeFine52_round128_full_registration_v1_20261007.py':'run_nonflag_RidgeFine52_round128_full_registration_v2_20261007.py'}
    changed=[];pairs=[]
    for old,new in names.items():
        text=(A/old).read_text(encoding='utf8');before=text
        counts={"len(pilot['records']) == 40":"len(pilot['records']) == 52", "'expected_scored_records': 40":"'expected_scored_records': 52",
          "'existing_actual_official_records': 40":"'existing_actual_official_records': 52", "record['expected_scored_records'] == 40":"record['expected_scored_records'] == 52",
          "len(record['ranking']) == 40":"len(record['ranking']) == 52", "manifest['scored_records'] == full['scored_records'] == 40":"manifest['scored_records'] == full['scored_records'] == 52",
          "'scored_records': 40":"'scored_records': 52", "'original_official_pilot_records_registered': 40":"'original_official_pilot_records_registered': 52"}
        for a,b in counts.items():
            if a in text:changed.append({'source':old,'before':a,'after':b,'occurrences':text.count(a)});text=text.replace(a,b)
        if old.startswith('register_'):
            text=text.replace("    pins = {", "    sources += [A/'recover_nonflag_RidgeFine52_full128_counts_v2_20261007.py',A/'nonflag_RidgeFine52_administrative52_count_recovery_v2_20261007.json',A/'optimize_training_round128_metadata_v2_20261007.py',A/'finalize_training_round128_metadata_v2_20261007.py',A/'run_nonflag_RidgeFine52_round128_full_registration_v2_20261007.py',A/'publish_nonflag_RidgeFine52_round128_full_validation_v2_20261007.py']\n    pins = {")
        if old.startswith('publish_'):
            text=text.replace("    for path in extra:","    extra += [A/'recover_nonflag_RidgeFine52_full128_counts_v2_20261007.py',A/'nonflag_RidgeFine52_administrative52_count_recovery_v2_20261007.json',A/'register_nonflag_RidgeFine52_round128_artifacts_v2_20261007.py',A/'optimize_training_round128_metadata_v2_20261007.py',A/'finalize_training_round128_metadata_v2_20261007.py',A/'run_nonflag_RidgeFine52_round128_full_registration_v2_20261007.py']\n    extra += list((A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1').glob('*.json'))+list((A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1').glob('*.log'))\n    for path in extra:")
            text=text.replace('112、119、120合格锚点','112、121、127合格锚点').replace('登记第119轮88项非涨停残差HGB与完整父方案组合验证并发布完整榜与全量QA','登记第128轮52项Ridge细幅度验证并保留登记恢复记录')
        if old.startswith('run_'):
            text=text.replace("nonflag_RidgeFine52_round128_actual_registration_v1_20261007","nonflag_RidgeFine52_round128_actual_registration_v2_20261007")
            text=text.replace("    from prepare_nonflag_RidgeFine52_round128_sources_v1_20261007 import main as prepare_sources\n    prepare_sources()", "    assert read(A/'nonflag_RidgeFine52_administrative52_count_recovery_v2_20261007.json')['status']=='passed_actual52_scores_and_immutable_candidate_administrative_count_recovery'\n    import importlib.util\n    for original,fresh in [('optimize_training_round128','optimize_training_round128_metadata_v2_20261007.py'),('finalize_training_round128','finalize_training_round128_metadata_v2_20261007.py')]:\n        spec=importlib.util.spec_from_file_location(original,A/fresh);module=importlib.util.module_from_spec(spec);sys.modules[original]=module;spec.loader.exec_module(module)")
            text=text.replace('from register_nonflag_RidgeFine52_round128_artifacts_20261007 import','from register_nonflag_RidgeFine52_round128_artifacts_v2_20261007 import')
            text=text.replace("registry=A/'register_nonflag_RidgeFine52_round128_artifacts_20261007.py'","registry=A/'register_nonflag_RidgeFine52_round128_artifacts_v2_20261007.py'")
            text=text.replace('from publish_nonflag_RidgeFine52_round128_full_validation_20261007 import','from publish_nonflag_RidgeFine52_round128_full_validation_v2_20261007 import')
            text=text.replace('nonflag_RidgeFine52_actual_source_paths_before_registration_20261007.json','nonflag_RidgeFine52_actual_source_paths_before_registration_v2_20261007.json')
        pairs.extend(save(old,new,text));assert text!=before
    pilot=A/'nonflag_RidgeFine52_official_comparison_v1_20261007/verification.json';ready=A/'nonflag_RidgeFine52_selected_release_v1_20261007/selected_candidate_ready_for_registration.json'
    p=read(pilot);r=read(ready);assert len(p['records'])==52 and p['best']==r['best'] and r['sealed_candidate_complete']
    manifest=Path(r['source_candidate'])/'manifest.json'
    for relative,item in read(manifest)['files'].items():assert sha(manifest.parent/relative)==item['sha256'],relative
    for fresh in names.values():compile((A/fresh).read_text(encoding='utf8'),str(A/fresh),'exec')
    create(proofpath,{'status':'passed_actual52_scores_and_immutable_candidate_administrative_count_recovery','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),prep,pilot,ready,manifest,*pairs,*service.glob('*.json'),*service.glob('*.log')]},
      'count_changes':changed,'actual52_pilot_records_preserved':True,'selected_whole_graph_and_native_bytes_and_CSV_and_original_freeze_unchanged':True,
      'metadata_modules_temporarily_bound_to_explicit_fresh_execution_sources':True,'original_generated_and_admitted_sources_retained_byte_for_byte':True,
      'original_failure_retained':True,'new_native_fits':0,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})

if __name__=='__main__':main()
