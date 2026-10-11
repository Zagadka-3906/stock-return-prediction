"""Declare independent100-case Alpha CPU pipeline; preserve inner Cone143 and all nine parent backends."""
from pathlib import Path
import io,sys,time,tokenize,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_ConeRidgeAlpha144_actual_auxiliary_controls_v1_20261008 import adapt as base_adapt

def adapt(text):
    text=base_adapt(text)
    for before,after in (
        ('ConeRidgeAlpha97_current_parent_controls_v1','ConeRidgeAlpha97_current_parent_controls_v2'),
        ('ConeRidgeAlpha144_historical_causal_main_publication_v1','ConeRidgeAlpha8_completed_controls_main_publication_v1'),
        ('ConeRidgeAlpha144_historical_causal_main_v1','ConeRidgeAlpha8_completed_controls_main_v1'),
        ('nonflag_ConeRidge64_streamed_v1','nonflag_ConeRidgeAlpha8_64_streamed_v1'),
        ('prepare_ConeRidgeFine143_complete_receivers_v3','prepare_ConeRidgeAlpha144_complete_receivers_v1'),
        ('prepare_ConeRidgeAlpha144_complete_receivers_v3','prepare_ConeRidgeAlpha144_complete_receivers_v1'),
        ('qa_version, expected_records) == (144, 54, 100)','qa_version, expected_records) == (144, 55, 100)'),
        ('collect(144, 100, 54)','collect(144, 100, 55)'),
        ('actual_complete_QA_version=54','actual_complete_QA_version=55'),
        ("'actual_full_QA_version': 54","'actual_full_QA_version': 55"),
        ('wave=426','wave=427'),('WAVES = (426,)','WAVES = (427,)'),
        ('wave426_results','wave427_results'),("'waves': [426]","'waves': [427]"),
        ('len(plan[\'heads\'])==4',"len(plan['heads'])==8"),
        ('actual_existing_own_mature_annual_models\']==20',"actual_existing_own_mature_annual_models']==40"),
        ("'existing_saved_native_heads':20","'existing_saved_native_heads':40"),
        ("'actual_existing_native_model_audits':20","'actual_existing_native_model_audits':40"),
        ("'actual_existing_native_head_audits':20","'actual_existing_native_head_audits':40"),
        ("'actual_full_OOF_heads':4","'actual_full_OOF_heads':8"),
        ("'actual_full_native_OOF_heads':4","'actual_full_native_OOF_heads':8"),
        ('actual_causal_same_configuration_refit_controls\']==20',"actual_causal_same_configuration_refit_controls']==40"),
        ("==proofs['hooks']['actual_cold_hooks']==24","==proofs['hooks']['actual_cold_hooks']==48"),
        ("proofs['calendar']['actual_calendar_cases']==24","proofs['calendar']['actual_calendar_cases']==48"),
        ("proofs['calendar']['actual_whole_day_controls']==64","proofs['calendar']['actual_whole_day_controls']==96"),
        ("'actual_historical_native_hooks':24","'actual_historical_native_hooks':48"),
        ("'actual_calendar_cases':24","'actual_calendar_cases':48"),
        ('cold24hooks','cold48hooks'),('cold24_historical','cold48_historical'),
        ('new_stage_ConeRidge64','new_stage_ConeRidgeAlpha8_64'),
        ('actual20_existing_native','actual40_existing_native'),
        ('actual_all52_official_controls','actual_all100_official_controls'),
        ('selected_by_all52_actual_official_scores','selected_by_all100_actual_official_scores'),
        ('passed_exact_selected_anchor52_candidate_reuse','passed_exact_selected_anchor100_candidate_reuse'),
    ):text=text.replace(before,after)
    return text

def save(name,text):
    path=A/name;assert not path.exists(),path;compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    originals=[
        'run_ConeRidgeFine68_official_comparison_v1_20261008.py',
        'prepare_ConeRidgeFine68_selected_candidate_v1_20261008.py',
        'seal_ConeRidgeFine68_selected_candidate_v2_20261008.py',
        'run_ConeRidgeFine68_round143_full_registration_v1_20261008.py',
        'publish_ConeRidgeFine68_evidence_v1_20261008.py',
        'verify_ConeRidgeFine68_round143_sources_v1_20261008.py',
        'ConeRidgeFine143_storage_v1_20261008.py',
        'create_ConeRidgeFine143_output_junctions_v1_20261008.py',
        'verify_ConeRidgeFine143_D_scoring_scope_v1_20261008.py',
        'verify_ConeRidgeFine68_prospective_routes_v2_20261008.py',
        'archive_ConeRidgeFine143_completed_scoring_CSV_v1_20261008.py',
    ]
    sources=[Path(__file__),A/'prepare_ConeRidgeAlpha144_actual_auxiliary_controls_v1_20261008.py',
        A/'ConeRidgeAlpha100_round144_plan_v1_20261008.json',A/'ConeRidgeAlpha144_native_receiver_preflight_v1_20261008.json']
    outputs=[]
    for original in originals:
        source=A/original;sources.append(source);text=adapt(source.read_text(encoding='utf8'));name=adapt(original)
        if 'seal_'==original[:5]:
            name=name.replace('_v2_','_v1_')
        if original.startswith('verify_ConeRidgeFine68_round143_sources'):
            text=text.replace('actual40_heads97_current_CDF291cold24hooks','actual40_heads97_current_CDF291cold48hooks')
            text=text.replace('actual40_heads97_current_CDF291cold24_historical','actual40_heads97_current_CDF291cold48_historical')
        if original.startswith('verify_ConeRidgeFine68_prospective'):
            text=text.replace("'actual134':deepcopy(original_graph)","'actual143':deepcopy(original_graph)")
            text=text.replace("candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']", "candidates/optimization_20261003_r143/verification.json')['whole_scheme_graph']")
            end="'nonflag_CPU_KrylovGram64_complete_parent_CDF'):"
            assert end in text;text=text.replace(end,"'nonflag_CPU_KrylovGram64_complete_parent_CDF','nonflag_CPU_ConeRidge64_complete_parent_CDF'):")
            text=text.replace("len(plan['new_cases'])==64","len(plan['new_cases'])==96")
            text=text.replace("assert forwarded==[(144,54,100)]", "assert forwarded==[(144,55,100)]")
            text=text.replace('(144,54,100),(144,67,54)', '(144,55,100),(144,99,55)')
            text=text.replace('(142,100,54),(144,54,100),(144,67,54)', '(143,100,55),(144,55,100),(144,99,55)')
            text=text.replace('(142,100,54),(144,54,100),(144,67,54)', '(143,100,55),(144,55,100),(144,99,55)')
        if original.startswith('run_ConeRidgeFine68_round143_full_registration'):
            text=text.replace('68项','100项').replace('48项正负系数约束岭回归','96项新增参数约束岭回归')
        outputs.append(save(name,text))
    generator_source=A/'prepare_ConeRidgeFine68_round143_sources_v1_20261008.py';sources.append(generator_source)
    tail=adapt(generator_source.read_text(encoding='utf8').split('\ndef main():',1)[1])
    generator='''"""Own144 source package; three admitted parents and exact100-case QA55 collector contract."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_ConeRidgeFine68_round143_sources_v1_20261008 as original
from prepare_ConeRidgeAlpha144_complete_receivers_v1_20261008 import adapt
ROOT=original.ROOT;A=original.A
NAMES={name:adapt(name) for name in original.NAMES.values()}
def generate(parent):
    assert parent in (132,134,143)
    template_parent=134 if parent==143 else parent
    outputs={}
    for name,text in original.generate(template_parent).items():
        value=adapt(text)
        if parent==143:
            for before,after in (('_r134','_r143'),('round134_receipt.json','round143_receipt.json'),
                ('PREVIOUS_NUMBER = 134','PREVIOUS_NUMBER = 143'),("'explicit_parent_round': 134","'explicit_parent_round': 143"),
                ('explicit_comparison_parent_round=134','explicit_comparison_parent_round=143')):
                value=value.replace(before,after)
        if name.startswith('publish_'):
            first=value.index("    payload[(prefix/'README.md').as_posix()] += (");last=value.index('    previous = ',first)
            value=value[:first]+"    payload[(prefix/'README.md').as_posix()] += ('\\\\n本轮100项：三个合格锚点132、134、143，新增四种岭参数的八个系数方向模型，16种正负变换乘六种幅度共96项及零幅度恒等对照。40个自身成熟年度模型和40次因果重新拟合；完整图保留包括原Cone143在内九类父分支，以独立外层Alpha图键追加。全部TRAIN内部连续评分，按官方S及物理SHA数选优。新方案冻结后两次完整1599600行推理和冷80；完整六视图45秒QA55，仅main。未读取实际测试标签，未证明优化穷尽。\\\\n').encode('utf8')\\n"+value[last:]
        outputs[adapt(name)]=value
        compile(value,adapt(name),'exec')
    assert len(outputs)==8
    return outputs
def source_paths():
    current=list(A.glob('*ConeRidgeAlpha*.py'))+list(A.glob('*ConeRidgeAlpha*.json'))
    current=[p for p in current if p.name!='actual_stage.json']
    dependencies=[p for p in original.source_paths() if p.is_file()]
    required=['ConeRidgeAlpha100_round144_source_admission_v1_20261008.json',
        'ConeRidgeAlpha100_actual_controls_index_v1_20261008.json','ConeRidgeAlpha100_round144_source_preparation_v1_20261008.json',
        'ConeRidgeAlpha100_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'ConeRidgeAlpha100_scores_github_v1_20261008/receipt.json',
        'ConeRidgeAlpha8_completed_controls_main_v1_20261008/receipt.json']
    return list(dict.fromkeys([Path(__file__),*dependencies,*current,*[A/p for p in required],*[A/name for name in NAMES.values()]]))
def main():'''+tail
    outputs.append(save('prepare_ConeRidgeAlpha100_round144_sources_v1_20261008.py',generator))
    pins={str(p):sha(p) for p in [*sources,*outputs]}
    create(A/'ConeRidgeAlpha144_receiver_drafts_v1_20261008.json',{
        'status':'frozen100_receivers_before_any144_quality','input_sha256':pins,
        'anchors':[132,134,143],'actual_official_scores':0,'new_fits':0,'test_labels_read':False})
    from ConeRidgeAlpha144_storage_v1_20261008 import OUTPUTS,EBASE
    create(A/'ConeRidgeAlpha144_junction_requests_v1_20261008.json',{
        'workspace':str(ROOT),'E_base':str(EBASE),'requests':[{'logical':str(p),'target':str(t)} for p,t in OUTPUTS.items()]})
    from create_ConeRidgeAlpha144_output_junctions_v1_20261008 import main as junctions
    from verify_ConeRidgeAlpha144_D_scoring_scope_v1_20261008 import main as dscope
    junctions();dscope()
    from verify_ConeRidgeAlpha100_prospective_routes_v2_20261008 import main as prospective
    prospective()
    create(A/'ConeRidgeAlpha144_complete_receivers_execution_v1_20261008.json',{
        'status':'passed_own100_receivers_prospective_contracts_before_quality',
        'input_sha256':pins,'actual_quality_scores':0,'test_labels_read':False,
        'actual100_pipeline_dispatch_still_required':True})
    print('Alpha144 complete prospective source controls passed; no actual quality inferred.',flush=True)

if __name__=='__main__':main()
