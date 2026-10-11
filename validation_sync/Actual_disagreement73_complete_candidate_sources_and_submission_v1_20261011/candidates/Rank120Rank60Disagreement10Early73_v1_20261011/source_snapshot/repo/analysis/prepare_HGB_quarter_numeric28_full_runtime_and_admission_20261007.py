"""Prepare complete118 runtime/admission from frozen117 routes, retaining all gates."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    route=read(A/'HGB_quarter_numeric28_workflow_source_preparation_20261007.json')['routes']
    import prepare_HGB_quarter_numeric28_round118_sources_20261007 as g
    extra={
      'prepare_weighted_HGB340_round117_sources_20261007':'prepare_HGB_quarter_numeric28_round118_sources_20261007',
      'weighted_HGB340_round117_source_preparation_20261007':'HGB_quarter_numeric28_round118_source_preparation_20261007',
      'weighted_HGB340_round117_source_admission_20261007':'HGB_quarter_numeric28_round118_source_admission_20261007',
      'passed_actual337_controls_and24_prospective117_complete_source_schema_paths_and_graph_routes':'passed_actual25_controls_and24_prospective118_complete_source_schema_paths_and_graph_routes',
      'passed_actual340_sealed_candidate_and_admitted_full117_QA28_sources':'passed_actual28_sealed_candidate_and_admitted_full118_QA29_sources',
      'weighted_HGB340_round117_actual_registration_20261007':'HGB_quarter_numeric28_round118_actual_registration_20261007',
      'weighted_HGB340_full117_20261007':'HGB_quarter_numeric28_full118_20261007',
      'weighted_HGB340_actual_source_paths_before_registration_20261007':'HGB_quarter_numeric28_actual_source_paths_before_registration_20261007',
      'weighted_HGB340_round117_full_registration':'HGB_quarter_numeric28_round118_full_registration',
      'optimization_20261003_r117':'optimization_20261003_r118',
      'publish(117,':'publish(118,','lossless(117)':'lossless(118)',
      "'existing_official_scores_registered':340":"'existing_official_scores_registered':28",
      'failed_preserved_weighted_HGB340_full117_registration':'failed_preserved_HGB_quarter_numeric28_full118_registration',
      '预定340项完整官方比较：三个合格锚点、336项非等权集成和一个消融':'预定28项完整官方比较：三个合格锚点、24项浮点加法顺序和一个消融',
      '完整父方案的涨停HGB非等权集成优化':'完整父方案的HGB浮点加法顺序补测',
      **{o[:-3]:n[:-3] for o,n in g.NAMES.items()}}
    routes={**route,**extra}
    runtime_old=A/'run_weighted_HGB340_round117_full_registration_20261007.py'
    runtime=save('run_HGB_quarter_numeric28_round118_full_registration_20261007.py',substitute(runtime_old.read_text(encoding='utf8'),routes))
    verifier_old=A/'verify_weighted_HGB340_round117_sources_20261007.py'
    text=substitute(verifier_old.read_text(encoding='utf8'),routes)
    text=text.replace('controls and25','controls and25').replace("len(controls['controls'])==337","len(controls['controls'])==25")
    text=text.replace("len(plan['ensembles'])==28","len(plan['ensembles'])==2").replace("plan['expected_scored_records']==340","plan['expected_scored_records']==28")
    text=text.replace('for parent in (112,115,116):','for parent in (112,116,117):').replace('for n in (112,115,116)','for n in (112,116,117)')
    text=text.replace("'register_weighted_HGB340_round117_artifacts_20261007.py'","'register_HGB_quarter_numeric28_round118_artifacts_20261007.py'")
    text=text.replace('original_registry_alias_round117.json','original_registry_alias_round118.json').replace('round117_full_scope','round118_full_scope')
    text=text.replace("prefix = Path('validation_sync/round117')","prefix = Path('validation_sync/round118')")
    text=text.replace("namespace['snapshot'](117)","namespace['snapshot'](118)").replace('collect(117, 28, 340)','collect(118, 29, 28)')
    text=text.replace("actual_full_QA_version': 28","actual_full_QA_version': 29").replace('validation_sync/round116','validation_sync/round117')
    text=text.replace('expected_scored_records=340','expected_scored_records=28').replace('len(graph_controls)==87','len(graph_controls)==9')
    text=text.replace("'actual_full_transform_controls':337","'actual_full_transform_controls':25").replace("'graph_metadata_controls':87","'graph_metadata_controls':9")
    text=text.replace('canonical117_sources_written','canonical118_sources_written').replace('full117_future_inference_and_QA28','full118_future_inference_and_QA29')
    verifier=save('verify_HGB_quarter_numeric28_round118_sources_20261007.py',text)
    create(A/'HGB_quarter_numeric28_full_runtime_and_admission_source_preparation_20261007.json',{'status':'compiled_complete118_runtime_and_actual25_controls_admission_routes',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),runtime_old,runtime,verifier_old,verifier,Path(g.__file__)]},'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()
