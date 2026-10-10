"""Predeclare all eight141 registry, full-QA53 and main sources for each eligible parent."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_ConeRidge142_complete_receivers_v1_20261008 import adapt
import prepare_KrylovGram52_round141_sources_v2_20261008 as original
NAMES={name:name.replace('KrylovGram','ConeRidge').replace('round141','round142').replace('qa52','qa53') for name in original.NAMES.values()}

def source_paths():
    names=[Path(__file__).name,'prepare_ConeRidge142_complete_receivers_v1_20261008.py','prepare_ConeRidge142_sources_and_controls_v1_20261008.py',
        'ConeRidge142_receiver_drafts_v1_20261008.json','ConeRidge142_receiver_preparation_v1_20261008.json',
        'ConeRidge52_round142_plan_v1_20261008.json','ConeRidge142_storage_v1_20261008.py',
        'ConeRidge64_complete_parent_CDF_v1_20261008.py','ConeRidge64_complete_parent_native_stage_v1_20261008.py',
        'predict_ConeRidge64_complete_parent_scheme_v1_20261008.py','nonflag_ConeRidge64_streamed_v1_20261008.py',
        'run_ConeRidge52_official_comparison_v1_20261008.py','prepare_ConeRidge52_selected_candidate_v1_20261008.py',
        'seal_ConeRidge52_selected_candidate_v1_20261008.py','run_ConeRidge52_round142_full_registration_v1_20261008.py',
        'verify_ConeRidge52_round142_sources_v1_20261008.py','verify_ConeRidge52_prospective_routes_v1_20261008.py',
        'publish_ConeRidge52_evidence_v1_20261008.py','queue_ConeRidge142_complete_pipeline_v1_20261008.py',
        'verify_ConeRidge49_current_parent_v1_20261008.py','verify_ConeRidge142_D_scoring_scope_v1_20261008.py',
        'ConeRidge142_D_scoring_scope_v1_20261008.json','ConeRidge52_prospective_routes_v1_20261008.json',
        'ConeRidge52_actual_controls_index_v1_20261008.json','ConeRidge52_round142_source_admission_v1_20261008.json',
        'ConeRidge52_round142_source_preparation_v1_20261008.json',
        'ConeRidge52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'ConeRidge52_scores_github_v1_20261008/receipt.json','verify_ConeRidge49_parent134_historical_v1_20261008.py',
        'verify_ConeRidge24_native_historical_hooks_v1_20261008.py','verify_ConeRidge_multiyear_native_calendar_v1_20261008.py',
        'verify_ConeRidge20_causal_refit_v1_20261008.py','ConeRidge142_native_receiver_preflight_v1_20261008.json',
        'prepare_ConeRidge142_native_preflight_v1_20261008.py','publish_ConeRidge142_historical_causal_v1_20261008.py',
        'ConeRidge142_historical_causal_main_v1_20261008/receipt.json',
        'create_ConeRidge142_output_junctions_v1_20261008.py','ConeRidge142_output_junction_admission_v1_20261008.json',
        'prepare_ConeRidge52_round142_plan_controls_v1_20261008.py','nonflag_ConeRidge64_bank20_plan_v1_20261008.json',
        'train_nonflag_ConeRidge64_bank20_v1_20261008.py','publish_ConeRidge64_controls_v1_20261008.py',
        'ConeRidge64_controls_main_v1_20261008/causal/receipt.json']
    # Only existing immutable template dependencies; unfinished135141 generated products are unnecessary.
    templates=[p for p in original.source_paths() if p.is_file()]
    return list(dict.fromkeys([*[A/name for name in [*names,*NAMES.values()]],*templates]))

def generate(parent):
    assert parent in (132,133,134);outputs={}
    from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
    for old_name,old_text in original.generate(138).items():
        name=NAMES[old_name];value=adapt(old_text)
        value=substitute(value,{'_r138':f'_r{parent}','round138_receipt.json':f'round{parent}_receipt.json',
            'PREVIOUS_NUMBER = 138':f'PREVIOUS_NUMBER = {parent}',"'explicit_parent_round': 138":f"'explicit_parent_round': {parent}",
            'explicit_comparison_parent_round=138':f'explicit_comparison_parent_round={parent}'})
        if name.startswith('publish_'):
            first=value.index("    payload[(prefix/'README.md').as_posix()] += (");last=value.index('    previous = ',first)
            value=value[:first]+"    payload[(prefix/'README.md').as_posix()] += ('\\n本轮52项：已合格132、133、134三个锚点，四种系数约束岭回归的正负变换，六种幅度共48项及恒等对照。自身成熟窗口20个年度模型、独立BVLS/KKT、完整OOF、后续训练标签扰动20次、49完整及147冷、24原生及24跨年检查已实际通过。完整图保留八类父分支；按官方S及物理SHA计数选优。新方案冻结后两次完整1599600行推理及冷80；锚点如实复用且零新推理。完整榜六视图45秒QA53及仅main。无需等待135至141完成；未读取实际测试标签，未证明优化穷尽。\\n').encode('utf8')\n"+value[last:]
        compile(value,str(A/name),'exec');outputs[name]=value
    assert len(outputs)==8;return outputs

def main():
    ready_path=A/'ConeRidge52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual52_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'ConeRidge52_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==52 and pilot['best']==ready['best']
    proof_path=A/'ConeRidge52_round142_source_admission_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual20_heads49_current_CDF147cold24hooks_and24_prospective142_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'ConeRidge52_round142_source_preparation_v1_20261008.json',{
        'status':'passed_actual52_sealed_candidate_and_admitted_full142_QA53_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':142,'scored_records':52,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
