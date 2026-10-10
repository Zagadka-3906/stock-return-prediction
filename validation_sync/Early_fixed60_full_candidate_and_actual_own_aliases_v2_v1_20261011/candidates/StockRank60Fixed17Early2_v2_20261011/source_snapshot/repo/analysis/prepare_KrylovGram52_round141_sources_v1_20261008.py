"""Predeclare all eight141 registry, full-QA52 and main sources for each eligible parent."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_KrylovGram141_complete_receivers_v1_20261008 import adapt
import prepare_SpectralGram52_round140_sources_v2_20261008 as original
NAMES={name:name.replace('SpectralGram52','KrylovGram52').replace('round140','round141').replace('qa51','qa52') for name in original.NAMES.values()}

def source_paths():
    names=[Path(__file__).name,'prepare_KrylovGram141_complete_receivers_v1_20261008.py','KrylovGram141_receiver_drafts_v1_20261008.json',
        'KrylovGram141_receiver_preparation_v1_20261008.json','KrylovGram52_round141_plan_v1_20261008.json','KrylovGram141_storage_v1_20261008.py',
        'KrylovGram64_complete_parent_CDF_v1_20261008.py','KrylovGram64_complete_parent_native_stage_v1_20261008.py',
        'predict_KrylovGram64_complete_parent_scheme_v1_20261008.py','nonflag_KrylovGram64_streamed_v2_20261008.py',
        'run_KrylovGram52_official_comparison_v1_20261008.py','prepare_KrylovGram52_selected_candidate_v1_20261008.py',
        'seal_KrylovGram52_selected_candidate_v1_20261008.py','run_KrylovGram52_round141_full_registration_v1_20261008.py',
        'verify_KrylovGram52_round141_sources_v1_20261008.py','verify_KrylovGram52_prospective_routes_v1_20261008.py',
        'publish_KrylovGram52_evidence_v1_20261008.py','queue_KrylovGram141_complete_pipeline_v1_20261008.py',
        'verify_KrylovGram49_current_parent_v1_20261008.py','verify_KrylovGram141_D_scoring_scope_v1_20261008.py',
        'KrylovGram141_D_scoring_scope_v1_20261008.json','KrylovGram52_prospective_routes_v1_20261008.json',
        'KrylovGram52_actual_controls_index_v1_20261008.json','KrylovGram52_round141_source_admission_v1_20261008.json',
        'KrylovGram52_round141_source_preparation_v1_20261008.json','KrylovGram52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'KrylovGram52_scores_github_v1_20261008/receipt.json','verify_KrylovGram49_parent134_historical_v1_20261008.py',
        'verify_KrylovGram24_native_historical_hooks_v1_20261008.py','verify_KrylovGram_multiyear_native_calendar_v1_20261008.py',
        'verify_KrylovGram20_causal_refit_v2_20261008.py','KrylovGram141_native_receiver_preflight_v1_20261008.json',
        'prepare_KrylovGram141_native_preflight_v1_20261008.py','prepare_KrylovGram141_native_preflight_actual_v1_20261008.py',
        'KrylovGram141_native_preflight_lineage_v1_20261008.json','publish_KrylovGram141_historical_causal_v1_20261008.py',
        'KrylovGram141_historical_causal_main_v1_20261008/receipt.json','create_KrylovGram141_output_junctions_v1_20261008.py',
        'KrylovGram141_output_junction_admission_v1_20261008.json',
        'prepare_KrylovGram52_round141_plan_controls_v1_20261008.py','nonflag_KrylovGram64_bank20_plan_v3_20261008.json',
        'train_nonflag_KrylovGram64_bank20_v3_20261008.py','recover_KrylovGram64_bank20_paths_v3_20261008.py',
        'KrylovGram64_reorthogonalized_source_preparation_v2_20261008.json','KrylovGram64_bank20_admin_path_preparation_v3_20261008.json',
        'prepare_nonflag_KrylovGram64_bank20_v2_20261008.py','prepare_nonflag_KrylovGram64_bank20_actual_v2_20261008.py',
        'nonflag_HuberIRLS64_own_window_v1_20261008.py','nonflag_residual_HGB_preprocessing_20261007.py',
        'memory_bounded_numeric_preparation_20261007.py','nonflag_residual_Ridge_codec_20261007.py',
        'predict_SpectralGram64_complete_parent_scheme_v1_20261008.py','SpectralGram64_complete_parent_native_stage_v1_20261008.py',
        'SpectralGram64_complete_parent_CDF_v1_20261008.py','run_SpectralGram52_round140_full_registration_v3_20261008.py']
    return list(dict.fromkeys([*[A/name for name in [*names,*NAMES.values()]],*original.source_paths()]))

def generate(parent):
    assert parent in (138,139,140);outputs={}
    for old_name,old_text in original.generate(137).items():
        name=NAMES[old_name];text=adapt(old_text)
        if name.startswith('publish_'):
            first=text.index("    payload[(prefix/'README.md').as_posix()] += (");last=text.index('    previous = ',first)
            text=text[:first]+'''    payload[(prefix/'README.md').as_posix()] += ('\\n本轮52项：138、139、140三个完整合格锚点；2/4/8/16步重正交共轭梯度岭回归的正负方向，六种幅度共48项及零幅度恒等对照。'
        '20个自身成熟年度模型，各训练窗口共享Gram；全部统计量、停止条件、提供目标和预处理均限制在自身成熟训练窗口。'
        '12小样本、4实际20万行独立投影求解及保存后推理、4完整OOF复核通过；5成熟窗口及20次后续训练标签扰动重训练逐位一致。'
        '49完整5635800行及147冷前缀，24历史原生/24冷、冻结2025模型24跨年/48按日检查通过。'
        '新变换位于完整父方案之后并保留全部七类已有分支；原官方S及八指标选优，同分按唯一物理SHA、幅度和case。'
        '选中新方案先冻结完整源/图/映射，再两次1599600行原生与独立推理及冷80；锚点明确记录零新推理。'
        '完整榜六视图45秒QA52、仅main；未读取实际测试标签，有限网格不证明方向及资源穷尽。\\n').encode('utf8')
'''+text[last:]
        text=substitute(text,{'_r137':f'_r{parent}','round137_receipt.json':f'round{parent}_receipt.json',
            'PREVIOUS_NUMBER = 137':f'PREVIOUS_NUMBER = {parent}',"'explicit_parent_round': 137":f"'explicit_parent_round': {parent}",
            'explicit_comparison_parent_round=137':f'explicit_comparison_parent_round={parent}'})
        compile(text,str(A/name),'exec');outputs[name]=text
    assert len(outputs)==8;return outputs

def main():
    ready_path=A/'KrylovGram52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual52_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'KrylovGram52_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==52 and pilot['best']==ready['best']
    proof_path=A/'KrylovGram52_round141_source_admission_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual20_heads49_current_CDF147cold24hooks_and24_prospective141_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'KrylovGram52_round141_source_preparation_v1_20261008.json',{
        'status':'passed_actual52_sealed_candidate_and_admitted_full141_QA52_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':141,'scored_records':52,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
