"""Recover dependent jobs that closed with real failures before their scientific work."""
from pathlib import Path
import ast
import sys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

FILES={
 'run_HGB_quarter_numeric28_controls_after117_20261007.py':'run_HGB_quarter_numeric28_controls_after117_v4_20261007.py',
 'verify_HGB_quarter_numeric28_transform_v3_20261007.py':'verify_HGB_quarter_numeric28_transform_v4_20261007.py',
 'verify_HGB_quarter_numeric28_round118_sources_v3_20261007.py':'verify_HGB_quarter_numeric28_round118_sources_v4_20261007.py',
 'publish_HGB_quarter_numeric28_evidence_v3_20261007.py':'publish_HGB_quarter_numeric28_evidence_v4_20261007.py',
 'run_HGB_quarter_numeric28_admitted_comparison_20261007.py':'run_HGB_quarter_numeric28_admitted_comparison_v4_20261007.py',
 'run_HGB_quarter_numeric28_official_comparison_20261007.py':'run_HGB_quarter_numeric28_official_comparison_v4_20261007.py',
 'prepare_HGB_quarter_numeric28_selected_candidate_20261007.py':'prepare_HGB_quarter_numeric28_selected_candidate_v4_20261007.py',
 'seal_HGB_quarter_numeric28_selected_candidate_20261007.py':'seal_HGB_quarter_numeric28_selected_candidate_v4_20261007.py',
 'run_HGB_quarter_numeric28_round118_full_registration_v2_20261007.py':'run_HGB_quarter_numeric28_round118_full_registration_v4_20261007.py',
 'prepare_HGB_quarter_numeric28_round118_sources_v2_20261007.py':'prepare_HGB_quarter_numeric28_round118_sources_v4_20261007.py',
 'publish_HGB_quarter_numeric_audit_after117_20261007.py':'publish_HGB_quarter_numeric_audit_after117_v4_20261007.py',
 'publish_quantile_HGB_bank20_after118_20261007.py':'publish_quantile_HGB_bank20_after118_v4_20261007.py',
 **{n+'_v3_20261007.py':n+'_v4_20261007.py' for n in [
   'run_quantile_HGB88_official_comparison','run_quantile_HGB88_admitted_comparison',
   'prepare_quantile_HGB88_selected_candidate','seal_quantile_HGB88_selected_candidate',
   'prepare_quantile_HGB88_round119_sources','verify_quantile_HGB88_round119_sources',
   'run_quantile_HGB88_round119_full_registration','publish_quantile_HGB88_evidence']}}

def maps():
    mapping={o[:-3]:n[:-3] for o,n in FILES.items()}
    mapping.update({
      'weighted_HGB340_round117_full_registration':'weighted_HGB340_round117_full_registration_v2',
      'prepare_weighted_HGB340_round117_sources_20261007':'prepare_weighted_HGB340_round117_sources_v2_20261007',
      'weighted_HGB340_round117_source_preparation_20261007':'weighted_HGB340_round117_source_preparation_v2_20261007',
      'weighted_HGB340_round117_source_admission_20261007':'weighted_HGB340_round117_source_admission_v2_20261007',
      'flagged_HGB_weighted_quarters340_selected_release_20261007':'flagged_HGB_weighted_quarters340_selected_release_v4_20261007',
      'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007':'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007',
      'seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007':'seal_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007',
      'HGB_quarter_numeric_audit_main_publication_after117':'HGB_quarter_numeric_audit_main_publication_after117_v4',
      'quantile_HGB_bank20_main_publication_after118':'quantile_HGB_bank20_main_publication_after118_v4',
      'HGB_quarter_numeric_audit_github_20261007':'HGB_quarter_numeric_audit_github_v4_20261007',
      'quantile_HGB_bank20_github_20261007':'quantile_HGB_bank20_github_v4_20261007',
      'HGB_quarter_numeric28_complete_pipeline_actual_hidden_launches_20261007':'local_118_119_protocol_recovery_actual_hidden_launches_v4_20261007',
      'quantile_HGB88_complete_pipeline_actual_hidden_launches_v3_20261007':'local_118_119_protocol_recovery_actual_hidden_launches_v4_20261007',
    })
    for stem in ['HGB_quarter_numeric28','quantile_HGB88']:
        for suffix in ['selected_release','pre_inference_source_freeze','round'+('118' if stem.startswith('HGB_') else '119')+'_source_preparation']:
            mapping[stem+'_'+suffix+'_20261007']=stem+'_'+suffix+'_v4_20261007'
        if stem=='quantile_HGB88':
            mapping[stem+'_selected_release_v3_20261007']=stem+'_selected_release_v4_20261007'
            mapping[stem+'_pre_inference_source_freeze_v3_20261007']=stem+'_pre_inference_source_freeze_v4_20261007'
            mapping[stem+'_round119_source_admission_v3_20261007']=stem+'_round119_source_admission_v4_20261007'
            mapping[stem+'_round119_actual_registration_v3_20261007']=stem+'_round119_actual_registration_v4_20261007'
        else:
            mapping[stem+'_round118_source_admission_20261007']=stem+'_round118_source_admission_v4_20261007'
            mapping[stem+'_round118_actual_registration_20261007']=stem+'_round118_actual_registration_v4_20261007'
            mapping[stem+'_transform_preflight_20261007']=stem+'_transform_preflight_v4_20261007'
        mapping['candidates/'+stem+'_20261007']='candidates/'+stem+'_v4_20261007'
        mapping[stem+'_official_comparison_20261007']=stem+'_official_comparison_v4_20261007'
        mapping[stem+'_official_comparison_v3_20261007']=stem+'_official_comparison_v4_20261007'
        for phase in ['controls','scores']:
            mapping[stem+'_'+phase+'_github_20261007']=stem+'_'+phase+'_github_v4_20261007'
        mapping[stem+'_{phase}_github_20261007']=stem+'_{phase}_github_v4_20261007'
    return mapping

def main():
    mapping=maps(); old_jobs=[]
    for file in ['HGB_quarter_numeric28_complete_pipeline_actual_hidden_launches_20261007.json','quantile_HGB88_complete_pipeline_actual_hidden_launches_v3_20261007.json']:
        old_jobs.extend(read(A/file)['launches'])
    old_jobs += ['HGB_quarter_numeric_audit_main_publication_after117','quantile_HGB_bank20_main_publication_after118']
    for name in old_jobs:
        folder=A/'service_owned_workflows_20261006'/name
        assert not owned(read(folder/'native_launch.json')),name
        assert read(folder/'service_execution.json')['status']=='failed',name
        mapping[name]=name.removesuffix('_v3')+'_v4'
    generated={}
    for old,new in FILES.items():
        original=(A/old).read_text(encoding='utf8')
        if old.startswith('prepare_') and '_round' in old:
            tree=ast.parse(original)
            main_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
            main_text='\n'.join(original.splitlines()[main_node.lineno-1:main_node.end_lineno])
            text=f'''from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import {Path(old).stem} as original_generator
NAMES=original_generator.NAMES
RECOVERY_MAP={mapping!r}
def generate(parent):
    return {{name:substitute(text,RECOVERY_MAP) for name,text in original_generator.generate(parent).items()}}
'''+substitute(main_text,mapping)+"\nif __name__=='__main__':main()\n"
        else:
            text=substitute(original,mapping)
        if old.startswith('prepare_') and 'selected_candidate' in old:
            needle="    bank=A/"
            start=text.index(needle)
            text=text[:start]+'''    import optimize_training_round95_v3 as protocol_runtime
    from resolve_sealed_scientific_protocol_20261007 import resolve
    scientific_protocol, protocol_pins, protocol_proof=resolve(parent_candidate,parent_release,parent_prediction['whole_scheme_graph'],protocol_runtime)
    create(OUT/'scientific_protocol_resolution_before_future_features.json',protocol_proof)
'''+text[start:]
            needle="pins={**pilot['input_sha256'],"
            assert text.count(needle)==1
            text=text.replace(needle,"pins={**protocol_pins,**pilot['input_sha256'],")
            needle="protocol=deepcopy(read(parent_release/'protocol.json'));"
            assert text.count(needle)==1
            text=text.replace(needle,"protocol=deepcopy(scientific_protocol);")
            needle="    for relative,info in parent_manifest['files'].items():"
            text=text.replace(needle,"    pins[str(A/'resolve_sealed_scientific_protocol_20261007.py')]=sha(A/'resolve_sealed_scientific_protocol_20261007.py')\n"+needle)
        # Keep all old source preparation evidence; add the actual recovery evidence.
        if old.startswith(('verify_','publish_')) and 'evidence' in old or old.startswith('verify_') and '_sources_' in old:
            needle='    for p in sources:'
            if needle in text:
                text=text.replace(needle,"    sources += [A/'prepare_local_118_119_protocol_recovery_v4_20261007.py',A/'local_118_119_protocol_recovery_source_preparation_v4_20261007.json',A/'resolve_sealed_scientific_protocol_20261007.py']\n"+needle,1)
        compile(text,str(A/new),'exec'); generated[new]=text
    for name in generated:assert not (A/name).exists(),name
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'local_118_119_protocol_recovery_source_preparation_v4_20261007.json',{
      'status':'compiled_fresh_local_routes_all17_predecessor_services_actual_failed',
      'input_sha256':{str(A/name):sha(A/name) for name in generated},
      'replaced_failed_services':old_jobs,'service_mapping':{n:mapping[n] for n in old_jobs},
      'old_scopes_preserved':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'compiled','sources':len(generated),'actual_closed_failed_services':len(old_jobs)})

if __name__=='__main__':main()
