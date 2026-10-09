"""Declare eight registration/QA64 routes for each of five comparison parents; stage fixed148."""
from pathlib import Path
import sys,ast,hashlib,time,re
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_BF16reverse40_round138_sources_v14_20261008 as previous
from prepare_BF16Medium153_core_drafts_v1_20261009 import route
NAMES={
 'register_BF16reverse40_round138_artifacts_20261008.py':'register_BF16Medium78_round153_artifacts_20261009.py',
 'publish_BF16reverse40_round138_full_validation_20261008.py':'publish_BF16Medium78_round153_full_validation_20261009.py',
 'optimize_training_round138.py':'optimize_training_round153.py',
 'finalize_training_round138.py':'finalize_training_round153.py',
 'lossless_ranking_runtime_adapter_round138_20261007.py':'lossless_ranking_runtime_adapter_round153_v2_20261008.py',
 'build_lossless_ranking_display_round138_20261007.py':'build_lossless_ranking_display_round153_v2_20261008.py',
 'verify_lossless_ranking_display_round138_20261007.py':'verify_lossless_ranking_display_round153_v2_20261008.py',
 'collect_full_lossless_round138_qa49_20261007.py':'collect_full_lossless_round153_qa64_20261009.py'}

def source_paths():
    names=['BF16Medium78_round153_plan_v1_20261009.json','BF16Medium78_round153_proposal_v1_20261009.json',
      'BF16Medium78_synthetic73_cold219_v1_20261009.json','BF16Medium153_storage_v1_20261009.py',
      'verify_BF16Medium153_D_scoring_scope_v1_20261009.py','BF16Medium153_D_scoring_scope_v1_20261009.json',
      'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py','BF16Medium153_complete_parent_native_stage_v1_20261009.py',
      'predict_BF16Medium153_complete_parent_scheme_v1_20261009.py','BF16Medium153_complete_native_predictor_preparation_v1_20261009.json',
      'run_BF16Medium78_official_comparison_v2_20261009.py','prepare_BF16Medium78_selected_candidate_v1_20261009.py',
      'seal_BF16Medium78_selected_candidate_v1_20261009.py','run_BF16Medium78_round153_full_registration_v3_20261009.py',
      'BF16Medium153_clean_registration_anchor_contract_v3_20261009.json','BF16Medium153_core_draft_preparation_v1_20261009.json',
      'prepare_BF16Medium153_core_drafts_v1_20261009.py','verify_BF16Medium78_prospective_routes_v1_20261009.py',
      'BF16Medium78_prospective_routes_v1_20261009.json','verify_BF16Medium78_round153_sources_v1_20261009.py',
      'BF16Medium78_round153_source_admission_v1_20261009.json','BF16Medium78_actual_controls_index_v1_20261009.json',
      'BF16Medium78_round153_source_preparation_v1_20261009.json','BF16Medium78_selected_release_v1_20261009/selected_candidate_ready_for_registration.json',
      'publish_BF16Medium78_evidence_v2_20261009.py','BF16Medium78_scores_github_v1_20261009/receipt.json',
      'BF16Medium153_actual_receiver_bindings_v2_20261009.json','prepare_BF16Medium153_actual_receiver_bindings_v2_20261009.py',
      'verify_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.py',
      'actual_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.json',
      'actual_BF16Medium153_full5_independent_location_v1_20261009.json','actual_BF16Medium153_native42_calendar_location_v1_20261009.json',
      'actual_BF16Medium153_full73_training_location_v1_20261009.json','neural_BF16_medium2048_seed09_e64_frontier_v1_20261009.json',
      'neural_BF16_medium2048_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_seed09_independent_forward_v1_20261009.py',
      'lossless_chunked_safe_main_runtime_v1_20261009.py','lossless_chunked_safe_main_runtime_v1_20261009.json',
      'verified_TLS_Git_retry_runtime_v2_20261008.py','short_content_addressed_native_storage_v2_20261008.py',
      'resolve_sealed_scientific_protocol_v2_20261007.py','publish_explicit_parent_training_round_v2_20261005.py']
    return list(dict.fromkeys([Path(__file__),Path(previous.__file__),*(A/n for n in names),*(A/n for n in NAMES.values())]))

def replace_node(s,node,expression):
    old=ast.get_source_segment(s,node);start=sum(len(x) for x in s.splitlines(keepends=True)[:node.lineno-1])+node.col_offset
    assert s[start:start+len(old)]==old
    return s[:start]+expression+s[start+len(old):]

def generate(parent):
    assert parent in (148,149,150,151,152);result={}
    for old,text in previous.generate(135).items():
        name=NAMES[old];s=route(text)
        for src,dst in NAMES.items():
            before=route(src);s=s.replace(before,dst).replace(before.removesuffix('.py'),dst.removesuffix('.py'))
        s=s.replace('_r135',f'_r{parent}').replace('round135_receipt.json',f'round{parent}_receipt.json')
        s=s.replace('PREVIOUS_NUMBER = 135',f'PREVIOUS_NUMBER = {parent}').replace("'explicit_parent_round': 135",f"'explicit_parent_round': {parent}")
        s=s.replace('explicit_comparison_parent_round=135',f'explicit_comparison_parent_round={parent}')
        if name.startswith('register_'):
            s=s.replace("'signal_sign_on_valid_rows':-1.,'invalid_signal_bits_preserved':True","'sign':cfg['sign'],'invalid_signal_bits_preserved':True")
            s=s.replace("r['direct_rank_comparison_configuration']['weight'], r['original_comparison_case']", "abs(r['direct_rank_comparison_configuration']['weight']), r['original_comparison_case']")
            tree=ast.parse(s);node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
            s=replace_node(s,node.value,"read(A / "+repr(f'optimization_20261003_r{parent}/selection.json')+")[\"winner\"][\"metrics\"][\"final_score\"]")
        if name=='optimize_training_round153.py':
            tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREVIOUS' for t in n.targets))
            s=replace_node(s,node.value,"ROOT / "+repr(f'analysis/optimization_20261003_r{parent}'))
        if name.startswith('publish_'):
            start=s.index("    payload[(prefix/'README.md').as_posix()] += (");end=s.index('    previous = ',start)
            s=s[:start]+"    payload[(prefix/'README.md').as_posix()] += ('\\n本轮78项：148至152五个合格锚点、新中型BF16网络在完整148后叠加正负信号与三种有效群体各12权重、零权重对照。六个成熟年度模型、5635800独立预测、42原生与42冷检查、73完整历史组合及219截断，均以实际证据为准；按完整连续官方S、物理模型数、绝对权重选优。保留完整榜原六视图QA64，仅main。实际测试标签未读取，选模偏差未校正，未证明穷尽。\\n').encode('utf8')\n"+s[end:]
        compile(s,str(A/name),'exec');result[name]=s
    assert len(result)==8 and set(result)==set(NAMES.values())
    return result

def main():
    ready_path=A/'BF16Medium78_selected_release_v1_20261009/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual78_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'BF16Medium78_official_comparison_v1_20261009/verification.json');assert len(pilot['records'])==78 and pilot['best']==ready['best']
    admission=A/'BF16Medium78_round153_source_admission_v1_20261009.json';proof=read(admission)
    assert proof['complete40_routes_and_graph_controls_passed'] and proof['prior_complete_forecast_duplicate_audit_passed']
    for f,d in proof['input_sha256'].items():assert sha(f)==d,f
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    for name,s in generated.items():assert not (A/name).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[name]
    for name,s in generated.items():(A/name).write_text(s,encoding='utf8',newline='\n')
    create(A/'BF16Medium78_round153_source_preparation_v1_20261009.json',{'status':'passed_actual78_sealed_candidate_and_admitted_full153_QA64_sources',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
