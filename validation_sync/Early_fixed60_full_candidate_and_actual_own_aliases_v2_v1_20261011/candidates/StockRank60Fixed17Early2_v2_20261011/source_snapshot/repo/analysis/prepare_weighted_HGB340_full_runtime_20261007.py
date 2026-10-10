"""Prepare an unlaunched complete117 runtime with actual source-path preflight."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    old=A/'run_flagged_HGB88_round116_full_registration_v4_20261007.py'
    mappings={
      'run_flagged_HGB88_round116_full_registration_v4_20261007':'run_weighted_HGB340_round117_full_registration_20261007',
      'flagged_HGB88_round116_actual_registration_v4_20261007':'weighted_HGB340_round117_actual_registration_20261007',
      'flagged_HGB_small_amplitude88_official_comparison_v4':'flagged_HGB_weighted_quarters340_official_comparison',
      'flagged_HGB_small_amplitude88_scores_main_publication_v4':'flagged_HGB_weighted_quarters340_scores_main_publication',
      'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4':'flagged_HGB_weighted_quarters340_selected_candidate_sealing',
      'protected_upper_pool_HGB66_round115_full_registration_v5':'flagged_HGB88_round116_full_registration_v2',
      'flagged_HGB_small_amplitude88_selected_release_v4_20261007':'flagged_HGB_weighted_quarters340_selected_release_20261007',
      'prepare_flagged_HGB88_round116_sources_v3_20261007':'prepare_weighted_HGB340_round117_sources_20261007',
      'flagged_HGB88_round116_source_preparation_v3_20261007':'weighted_HGB340_round117_source_preparation_20261007',
      'passed_actual88_sealed_candidate_registry_and_original_QA27_source_routes':'passed_actual340_sealed_candidate_and_admitted_full117_QA28_sources',
      'passed_actual88_selected_candidate_full_graph_and_metrics_and_source_bytes':'passed_actual340_selected_candidate_full_graph_and_metrics_and_source_bytes',
      'register_flagged_HGB88_round116_artifacts_v2_20261007':'register_weighted_HGB340_round117_artifacts_20261007',
      'optimization_20261003_r116':'optimization_20261003_r117',
      'flagged_HGB88_full116_20261007':'weighted_HGB340_full117_20261007',
      'lossless_ranking_runtime_adapter_round116_20261007':'lossless_ranking_runtime_adapter_round117_20261007',
      'publish_flagged_HGB88_round116_full_validation_v2_20261007':'publish_weighted_HGB340_round117_full_validation_20261007',
      'publish(116,':'publish(117,','lossless(116)':'lossless(117)',
      '(112,114,115)':'(112,115,116)',"'existing_official_scores_registered':88":"'existing_official_scores_registered':340",
      'failed_preserved_flagged_HGB88_full116_registration':'failed_preserved_weighted_HGB340_full117_registration',
      '完整父方案的涨停HGB小权重优化':'完整父方案的涨停HGB非等权集成优化',
      '预定88项完整官方比较：三个合格锚点、84项小权重和一个消融':'预定340项完整官方比较：三个合格锚点、336项非等权集成和一个消融',
    }
    text=substitute(old.read_text(encoding='utf8'),mappings)
    needle="    prep=read(A/'weighted_HGB340_round117_source_preparation_20261007.json')"
    assert text.count(needle)==1
    text=text.replace(needle,"    prepare_sources()\n"+needle)
    needle="    protocol=register();folder=A/'optimization_20261003_r117';pins=protocol['input_sha256']"
    assert text.count(needle)==1
    before="""    import ast
    registry=A/'register_weighted_HGB340_round117_artifacts_20261007.py'
    node=ast.parse(registry.read_text(encoding='utf8'))
    body=next(n for n in node.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
    source_assign=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
    ns={'A':A,'ROOT':ROOT,'Path':Path,'__file__':str(registry)}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[source_assign],type_ignores=[])),str(registry),'exec'),ns)
    assert all(p.is_file() for p in ns['sources']),[str(p) for p in ns['sources'] if not p.is_file()]
    create(A/'weighted_HGB340_actual_source_paths_before_registration_20261007.json',{'status':'passed_all_actual117_registry_source_paths_before_alias_or_registration',
        'input_sha256':{str(p):sha(p) for p in ns['sources']},'source_count':len(ns['sources']),'new_native_fits':0,'new_quality_scores':0})
"""
    text=text.replace(needle,before+needle)
    target=A/'run_weighted_HGB340_round117_full_registration_20261007.py';assert not target.exists();compile(text,str(target),'exec')
    target.write_text(text,encoding='utf8',newline='\n')
    create(A/'weighted_HGB340_full_runtime_source_preparation_20261007.json',{'status':'compiled_future_full117_QA28_runtime_with_actual_all_source_paths_before_registration',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target]},'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
