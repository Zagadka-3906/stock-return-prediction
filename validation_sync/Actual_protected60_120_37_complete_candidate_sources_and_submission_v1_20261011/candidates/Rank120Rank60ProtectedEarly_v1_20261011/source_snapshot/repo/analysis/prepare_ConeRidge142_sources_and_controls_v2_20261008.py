"""Finish declared142 registry routes and actual eight-backend adapter evidence before quality."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_ConeRidge142_complete_receivers_v1_20261008 import adapt

def save(path,text):
    assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    inputs=[Path(__file__),A/'prepare_ConeRidge142_complete_receivers_v1_20261008.py'];outputs=[]
    old=A/'prepare_KrylovGram52_round141_sources_v2_20261008.py';inputs.append(old)
    text=adapt(old.read_text(encoding='utf8').replace('run_SpectralGram52_round140_full_registration_v3_20261008.py','run_KrylovGram52_round141_full_registration_v2_20261008.py'))
    first=text.index('from prepare_ConeRidge141_parent_set_recovery') if 'from prepare_ConeRidge141_parent_set_recovery' in text else text.index('from prepare_ConeRidge142_parent_set_recovery')
    last=text.index('\ndef main():',first)
    middle='''from prepare_ConeRidge142_complete_receivers_v1_20261008 import adapt
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
'''
    text=text[:first]+middle+text[last:]
    outputs.append(save(A/'prepare_ConeRidge52_round142_sources_v1_20261008.py',text))
    old=A/'prepare_KrylovGram141_native_preflight_actual_v1_20261008.py';inputs.append(old)
    text=adapt(old.read_text(encoding='utf8'));last=text.index("    source=A/'verify_multiyear_residual_native_calendar_v1_20261008.py'")
    text=text[:last]+'''    assert len(records)==8
    create(A/'ConeRidge142_native_receiver_preflight_v1_20261008.json',{
        'status':'passed_eight_actual_inserted_adapter_contracts_before_quality',
        'input_sha256':{str(p):sha(p) for p in sources},'adapter_controls':records,'backend_priority_cases':8,
        'new_fits':0,'new_official_scores':0,'new_actual_future_inference_claimed':False,'test_labels_read':False})
    print('Eight actual complete-parent adapter contracts passed; no actual future features read.',flush=True)

if __name__=='__main__':main()
'''
    needle="('nonflag_CPU_SpectralGram64_complete_parent_CDF','SpectralGram64')]";assert text.count(needle)==1
    text=text.replace(needle,"('nonflag_CPU_SpectralGram64_complete_parent_CDF','SpectralGram64'),('nonflag_CPU_KrylovGram64_complete_parent_CDF','KrylovGram64')]")
    outputs.append(save(A/'prepare_ConeRidge142_native_preflight_v1_20261008.py',text))
    old=A/'publish_KrylovGram141_historical_causal_v1_20261008.py';inputs.append(old);text=adapt(old.read_text(encoding='utf8'))
    for before,after in (
        ('ConeRidge142_causal_preflight_main_publication_v1_20261008','ConeRidge64_controls_main_publication_v1_20261008'),
        ('actual_ConeRidge20_causal_refit_hidden_launch_v2_20261008','actual_ConeRidge20_causal_refit_hidden_launch_v1_20261008'),
        ('actual_ConeRidge52_plan_preparation_hidden_launch_v1_20261008','ConeRidge142_plan_controls_preparation_hidden_launch_v1_20261008'),
        ('nonflag_ConeRidge64_controls_main_v2_20261008','ConeRidge64_controls_main_v1_20261008'),
        ("len(native['adapter_controls'])==7 and native['backend_priority_cases']==7","len(native['adapter_controls'])==8 and native['backend_priority_cases']==8"),
        ("'actual_adapter_contracts':7","'actual_adapter_contracts':8"),('actual_seven_adapter_contracts','actual_eight_adapter_contracts')):text=text.replace(before,after)
    outputs.append(save(A/'publish_ConeRidge142_historical_causal_v1_20261008.py',text))
    old=A/'verify_KrylovGram52_prospective_routes_v2_20261008.py';inputs.append(old);text=adapt(old.read_text(encoding='utf8'))
    # Eight complete graph kinds: actual134 plus all seven later CPU/neural stage branches.
    needle="'nonflag_CPU_HuberCrossFamily_complete_parent_CDF','nonflag_CPU_SpectralGram64_complete_parent_CDF')";assert text.count(needle)==1
    text=text.replace(needle,"'nonflag_CPU_HuberCrossFamily_complete_parent_CDF','nonflag_CPU_SpectralGram64_complete_parent_CDF','nonflag_CPU_KrylovGram64_complete_parent_CDF')")
    text=text.replace('==1029','==1176')
    outputs.append(save(A/'verify_ConeRidge52_prospective_routes_v1_20261008.py',text))
    create(A/'ConeRidge142_source_receivers_preparation_v2_20261008.json',{
        'status':'prepared52_science_and_eight_canonical_registration_routes_before_quality',
        'input_sha256':{str(p):sha(p) for p in [*inputs,*outputs]},'new_official_scores':0,'test_labels_read':False})
    print('Independent142 canonical source generator, eight adapters, historical publisher and prospective verifier compiled.',flush=True)

if __name__=='__main__':main()
