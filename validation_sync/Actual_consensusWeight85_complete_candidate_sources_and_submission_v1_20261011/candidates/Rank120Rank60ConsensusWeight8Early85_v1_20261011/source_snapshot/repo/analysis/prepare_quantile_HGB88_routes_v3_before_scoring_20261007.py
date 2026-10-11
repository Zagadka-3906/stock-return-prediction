"""Fix the actual native-wrapper sealing contract before any119 official score or inference."""
from pathlib import Path
import sys,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,create,sha
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    files={
      'run_quantile_HGB88_official_comparison_20261007.py':'run_quantile_HGB88_official_comparison_v3_20261007.py',
      'prepare_quantile_HGB88_selected_candidate_20261007.py':'prepare_quantile_HGB88_selected_candidate_v3_20261007.py',
      'seal_quantile_HGB88_selected_candidate_20261007.py':'seal_quantile_HGB88_selected_candidate_v3_20261007.py',
      'prepare_quantile_HGB88_round119_sources_v2_20261007.py':'prepare_quantile_HGB88_round119_sources_v3_20261007.py',
      'verify_quantile_HGB88_round119_sources_v2_20261007.py':'verify_quantile_HGB88_round119_sources_v3_20261007.py',
      'run_quantile_HGB88_round119_full_registration_v2_20261007.py':'run_quantile_HGB88_round119_full_registration_v3_20261007.py',
      'publish_quantile_HGB88_evidence_v2_20261007.py':'publish_quantile_HGB88_evidence_v3_20261007.py',
      'run_quantile_HGB88_admitted_comparison_20261007.py':'run_quantile_HGB88_admitted_comparison_v3_20261007.py'}
    services=['quantile_HGB88_round119_source_admission','quantile_HGB88_full85_controls_main_publication','quantile_HGB88_official_comparison',
      'quantile_HGB88_scores_main_publication','quantile_HGB88_selected_candidate_preparation','quantile_HGB88_selected_candidate_sealing','quantile_HGB88_round119_full_registration']
    maps={**{o[:-3]:n[:-3] for o,n in files.items()},**{n:n+'_v3' for n in services},
      'quantile_HGB88_round119_source_admission_20261007':'quantile_HGB88_round119_source_admission_v3_20261007',
      'quantile_HGB88_selected_release_20261007':'quantile_HGB88_selected_release_v3_20261007',
      'quantile_HGB88_pre_inference_source_freeze_20261007':'quantile_HGB88_pre_inference_source_freeze_v3_20261007',
      'quantile_HGB88_round119_actual_registration_20261007':'quantile_HGB88_round119_actual_registration_v3_20261007',
      'quantile_HGB88_complete_pipeline_actual_hidden_launches_20261007':'quantile_HGB88_complete_pipeline_actual_hidden_launches_v3_20261007'}
    paths=[Path(__file__)]
    for old,new in files.items():
        text=substitute((A/old).read_text(encoding='utf8'),maps)
        if old.startswith('seal_'):
            oldstatus='passed_actual_full_refined_graph_saved_native_independent_two_replays_and_cold80'
            assert text.count(oldstatus)==1;text=text.replace(oldstatus,'passed_actual_quantile_full_refined_graph_saved_native_independent_two_replays_and_cold80')
        elif old.startswith('verify_'):
            needle='    for p in sources:';assert needle in text
            text=text.replace(needle,"    sources += [A/'prepare_quantile_HGB88_routes_v3_before_scoring_20261007.py',A/'quantile_HGB88_routes_source_preparation_v3_20261007.json']\n"+needle)
        elif old.startswith('publish_'):
            needle="    if phase=='scores':\n        for row in proof['records']:";assert needle in text
            text=text.replace(needle,"    sources += [A/'prepare_quantile_HGB88_routes_v3_before_scoring_20261007.py',A/'quantile_HGB88_routes_source_preparation_v3_20261007.json',\n      A/'quantile_HGB88_actual_idle_waiter_handoff_v3_20261007/verification.json',\n      A/'handoff_quantile_HGB88_idle_waiters_v3_20261007.py',A/'quantile_HGB88_complete_pipeline_actual_hidden_launches_v3_20261007.json']\n"+needle)
        p=A/new;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8');paths += [A/old,p]
    wrapper=A/'predict_refined_quantile_HGB_scheme_v2_20261007.py';tree=ast.parse(wrapper.read_text(encoding='utf8'))
    actual=next(node.value for node in ast.walk(tree) if isinstance(node,ast.Dict) for key,node in zip(node.keys,node.values)
      if isinstance(key,ast.Constant) and key.value=='status' and isinstance(node,ast.Constant) and str(node.value).startswith('passed_actual_quantile_full_refined_graph'))
    seal=(A/files['seal_quantile_HGB88_selected_candidate_20261007.py']).read_text(encoding='utf8');assert repr(actual) in seal
    create(A/'quantile_HGB88_routes_source_preparation_v3_20261007.json',{'status':'compiled_actual_native_wrapper_status_matches_seal_before_scientific_execution',
      'input_sha256':{str(p):sha(p) for p in [*paths,wrapper]},'actual_wrapper_emitted_status':actual,
      'previous_status_mismatch_preserved':True,'new_native_fits':0,'new_quality_scores':0,'new_future_inferences':0})
    print({'status':'compiled','actual_native_seal_contract':actual},flush=True)
if __name__=='__main__':main()
