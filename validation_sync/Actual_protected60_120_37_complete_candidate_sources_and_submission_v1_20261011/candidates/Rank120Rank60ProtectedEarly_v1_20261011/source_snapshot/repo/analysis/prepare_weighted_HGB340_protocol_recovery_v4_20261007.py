"""Create fresh recovery scopes without changing scores or old frozen inference files."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

M={
 'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007':'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007',
 'seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007':'seal_flagged_HGB_weighted_quarters340_selected_candidate_v4_20261007',
 'flagged_HGB_weighted_quarters340_selected_release_20261007':'flagged_HGB_weighted_quarters340_selected_release_v4_20261007',
 'candidates/flagged_HGB_weighted_quarters340_20261007':'candidates/flagged_HGB_weighted_quarters340_v4_20261007',
 'flagged_HGB_weighted_quarters340_pre_inference_source_freeze_20261007':'flagged_HGB_weighted_quarters340_pre_inference_source_freeze_v4_20261007',
 'flagged_HGB_weighted_quarters340_selected_candidate_preparation':'flagged_HGB_weighted_quarters340_selected_candidate_preparation_v4',
 'flagged_HGB_weighted_quarters340_selected_candidate_sealing':'flagged_HGB_weighted_quarters340_selected_candidate_sealing_v4',
 'prepare_weighted_HGB340_round117_sources_20261007':'prepare_weighted_HGB340_round117_sources_v2_20261007',
 'verify_weighted_HGB340_round117_sources_20261007':'verify_weighted_HGB340_round117_sources_v2_20261007',
 'weighted_HGB340_round117_source_admission_20261007':'weighted_HGB340_round117_source_admission_v2_20261007',
 'weighted_HGB340_round117_source_preparation_20261007':'weighted_HGB340_round117_source_preparation_v2_20261007',
 'run_weighted_HGB340_round117_full_registration_20261007':'run_weighted_HGB340_round117_full_registration_v2_20261007',
 'weighted_HGB340_round117_actual_registration_20261007':'weighted_HGB340_round117_actual_registration_v2_20261007',
}

def main():
    generated={}
    for old in [
      'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007',
      'seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007',
      'prepare_weighted_HGB340_round117_sources_20261007',
      'verify_weighted_HGB340_round117_sources_20261007',
      'run_weighted_HGB340_round117_full_registration_20261007']:
        text=substitute((A/(old+'.py')).read_text(encoding='utf8'),M)
        if old.startswith('prepare_flagged_'):
            needle="    bank=A/'cpu_conditional_residual_hgb_bank20_20261007'"
            assert text.count(needle)==1
            text=text.replace(needle,"""    import optimize_training_round95_v3 as protocol_runtime
    from resolve_sealed_scientific_protocol_20261007 import resolve
    scientific_protocol, protocol_pins, protocol_proof = resolve(parent_candidate, parent_release, parent_prediction['whole_scheme_graph'], protocol_runtime)
    create(OUT/'scientific_protocol_resolution_before_future_features.json', protocol_proof)
"""+needle)
            text=text.replace("pins={**pilot['input_sha256'],", "pins={**protocol_pins,**pilot['input_sha256'],")
            text=text.replace("protocol=deepcopy(read(parent_release/'protocol.json'));", "protocol=deepcopy(scientific_protocol);")
            text=text.replace("sources=[Path(__file__),", "sources=[Path(__file__),")
            # Pin the resolver before the source snapshot and lock it throughout inference.
            needle="    for relative,info in parent_manifest['files'].items():"
            text=text.replace(needle,"    pins[str(A/'resolve_sealed_scientific_protocol_20261007.py')]=sha(A/'resolve_sealed_scientific_protocol_20261007.py')\n"+needle)
        elif old.startswith('prepare_weighted_'):
            # Literal template replacements must map old prototype values directly to recovery routes.
            text=(text.replace("'run_weighted_HGB340_round117_full_registration_20261007'", "'run_weighted_HGB340_round117_full_registration_v2_20261007'")
                      .replace("'flagged_HGB_weighted_quarters340_selected_release_20261007'", "'flagged_HGB_weighted_quarters340_selected_release_v4_20261007'"))
            needle="        A / 'all_forecast_percentile_runtime_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\\n        A / 'resolve_sealed_scientific_protocol_20261007.py',")
        compile(text,str(A/(M[old]+'.py')),'exec')
        generated[M[old]+'.py']=text
    for name in generated: assert not (A/name).exists(),name
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'weighted_HGB340_protocol_recovery_source_preparation_v4_20261007.json',{
      'status':'passed_fresh_recovery_sources_old_failed_scope_and340_scores_preserved',
      'input_sha256':{str(A/name):sha(A/name) for name in generated},
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
