"""Audit and correct nonflag prototypes before any round120 execution."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_nonflag_HGB40_science_sources_20261007 import FILES

def mapping():
    m={n[:-3]:n[:-3].replace('_20261007','_v2_20261007') for n in FILES.values()}
    m.update({
      'prepare_nonflag_HGB40_round120_sources_20261007':'prepare_nonflag_HGB40_round120_sources_v2_20261007',
      'nonflag_HGB40_round120_source_admission_20261007':'nonflag_HGB40_round120_source_admission_v2_20261007',
      'nonflag_HGB40_round120_source_preparation_20261007':'nonflag_HGB40_round120_source_preparation_v2_20261007',
      'nonflag_HGB40_selected_release_20261007':'nonflag_HGB40_selected_release_v2_20261007',
      'nonflag_HGB40_official_comparison_20261007':'nonflag_HGB40_official_comparison_v2_20261007',
      'candidates/quantile_HGB88_v4_20261007':'candidates/nonflag_HGB40_v2_20261007',
      'nonflag_HGB40_pre_inference_source_freeze_20261007':'nonflag_HGB40_pre_inference_source_freeze_v2_20261007',
      'nonflag_HGB40_round120_actual_registration_20261007':'nonflag_HGB40_round120_actual_registration_v2_20261007',
      'quantile_HGB88_round119_full_registration_v4':'quantile_HGB88_round119_full_registration_v5',
      'HGB_quarter_numeric28_round118_full_registration_v4':'HGB_quarter_numeric28_round118_full_registration_v5',
      'quantile_HGB_full85_transform_preflight':'nonflag_residual_HGB37_transform_preflight',
      'refined_quantile_HGB_native_replay_verification.json':'nonflag_residual_HGB_native_replay_verification.json',
      'actual20_mature_native_independent_prefix_controls':'actual10_mature_native_independent_prefix_controls',
      'frozen_selected_quantile_HGB88_before_future_inference':'frozen_selected_nonflag_HGB40_before_future_inference',
      'passed_actual40_sealed_candidate_and_admitted_full119_QA30_sources':'passed_actual40_sealed_candidate_and_admitted_full120_QA31_sources',
      'passed_all_actual119_registry_source_paths_before_alias_or_registration':'passed_all_actual120_registry_source_paths_before_alias_or_registration',
      'passed_actual_pre_inference_source_snapshot_and_quantile_HGB88_native_candidate':'passed_actual_pre_inference_source_snapshot_and_nonflag_HGB40_native_candidate',
    })
    return m

def main():
    m=mapping();generated={}
    for old in FILES.values():
        new=m[old[:-3]]+'.py';text=substitute((A/old).read_text(encoding='utf8'),m)
        if old.startswith('publish_'):
            text=text.replace("==(85 if phase=='controls' else 88)","==(37 if phase=='controls' else 40)")
            start=text.index('    sources=[Path(__file__)');end=text.index("    if phase=='scores':",start)
            text=text[:start]+'''    sources=[Path(__file__),A/'nonflag_HGB40_plan_20261007.json',
      A/'prepare_nonflag_HGB40_complete_routes_v2_20261007.py',A/'nonflag_HGB40_complete_routes_source_preparation_v2_20261007.json',
      A/'run_nonflag_HGB40_official_comparison_v2_20261007.py',
      A/'prepare_nonflag_HGB40_selected_candidate_v2_20261007.py',A/'seal_nonflag_HGB40_selected_candidate_v2_20261007.py',
      A/'prepare_nonflag_HGB40_round120_sources_v2_20261007.py',A/'verify_nonflag_HGB40_round120_sources_v2_20261007.py',
      A/'run_nonflag_HGB40_round120_full_registration_v2_20261007.py',A/'predict_nonflag_residual_HGB_complete_scheme_20261007.py',
      A/'nonflag_residual_HGB_native_stage_20261007.py',A/'nonflag_residual_HGB_CDF_transform_20261007.py',
      A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'resolve_sealed_scientific_protocol_20261007.py',
      A/'nonflag_residual_HGB_native_hook3_preflight_20261007/verification.json',
      A/'nonflag_HGB10_actual_controls_github_20261007/receipt.json',
      *folder.glob('*.json'),*science.glob('*.json'),*science.glob('*.log'),
      *list((A/'nonflag_residual_HGB_native_hook3_preflight_20261007').glob('*.json')),
      *list((A/'local_118_119_publication_contract_v5_actual_handoff_20261007').glob('*.json'))]
'''+text[end:]
            start=text.index("            if phase=='scores':\n                target=A/");end=text.index('    finally:',start)
            text=text[:start]+text[end:]
            text=text.replace('validation_sync/quantile_HGB88_{phase}_20261007','validation_sync/nonflag_HGB40_{phase}_20261007')
            text=text.replace('published_actual_quantile_HGB88_','published_actual_nonflag_HGB40_')
            text=text.replace("'actual_full_control_cases':85,'actual_cold_prefix_cases':255","'actual_full_control_cases':37,'actual_cold_prefix_cases':111")
            text=text.replace('full119_not_yet_qualified','full120_not_yet_qualified')
            start=text.index("            payload[(prefix/'README.md').as_posix()]=(");end=text.index('            scope.reverify()',start)
            text=text[:start]+"            payload[(prefix/'README.md').as_posix()]=('非涨停残差HGB：两个单模型及其等权集成，各12幅度，加三个合格锚点及消融，共40项。实际10年度成熟模型；37全量和111冷前缀核对；最终候选需冻结、完整重放及QA31。仅main。\\n').encode('utf8')\n"+text[end:]
        if old.startswith('run_') and 'full_registration' in old:
            text=text.replace('预定88项完整官方比较：三个合格锚点、84项分位数HGB和一个消融','预定40项完整官方比较：三个合格锚点、36项非涨停残差HGB和一个消融')
            text=text.replace('完整父方案的分位数HGB补充','完整父方案的非涨停残差HGB补充')
        compile(text,str(A/new),'exec');generated[new]=text
    for n in generated:assert not (A/n).exists(),n
    for n,text in generated.items():
        with (A/n).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'nonflag_HGB40_complete_routes_source_preparation_v2_20261007.json',{
      'status':'compiled_correct_nonflag_candidate_path_replay_proof37_40_and_single_publication_receipt',
      'input_sha256':{str(A/n):sha(A/n) for n in generated},'new_quality_scores':0,'new_native_fits':0,
      'future120_complete_admission_not_claimed':True,'test_labels_read':False})

if __name__=='__main__':main()
