"""Own144 source package; three admitted parents and exact100-case QA55 collector contract."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_ConeRidgeFine68_round143_sources_v1_20261008 as original
from prepare_ConeRidgeAlpha144_complete_receivers_v1_20261008 import adapt as original_adapt
from complete_ConeRidgeAlpha144_metadata_and_queue_v2_20261008 import corrected
def adapt(text):return corrected(original_adapt(text))
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
            value=value[:first]+"    payload[(prefix/'README.md').as_posix()] += ('\\n本轮100项：三个合格锚点132、134、143，新增四种岭参数的八个系数方向模型，16种正负变换乘六种幅度共96项及零幅度恒等对照。40个自身成熟年度模型和40次因果重新拟合；完整图保留包括原Cone143在内九类父分支，以独立外层Alpha图键追加。全部TRAIN内部连续评分，按官方S及物理SHA数选优。新方案冻结后两次完整1599600行推理和冷80；完整六视图45秒QA55，仅main。未读取实际测试标签，未证明优化穷尽。\\n').encode('utf8')\n"+value[last:]
        outputs[adapt(name)]=value
        compile(value,adapt(name),'exec')
    assert len(outputs)==8
    return outputs
def source_paths():
    current=list(A.glob('*ConeRidgeAlpha*.py'))+list(A.glob('*ConeRidgeAlpha*.json'))
    current=[p for p in current if p.name!='actual_stage.json']
    dependencies=[p for p in original.source_paths() if p.is_file()]
    required=['ConeRidgeAlpha100_round144_source_admission_v2_20261008.json',
        'ConeRidgeAlpha100_actual_controls_index_v1_20261008.json','ConeRidgeAlpha100_round144_source_preparation_v2_20261008.json',
        'ConeRidgeAlpha100_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'ConeRidgeAlpha100_scores_github_v1_20261008/receipt.json',
        'ConeRidgeAlpha8_completed_controls_main_v1_20261008/receipt.json']
    return list(dict.fromkeys([Path(corrected(str(p))) for p in [Path(__file__),*dependencies,*current,*[A/p for p in required],*[A/name for name in NAMES.values()]]]))
def main():
    ready_path=A/'ConeRidgeAlpha100_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual100_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'ConeRidgeAlpha100_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==100 and pilot['best']==ready['best']
    proof_path=A/'ConeRidgeAlpha100_round144_source_admission_v2_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual40_heads97_current_CDF291cold48hooks_and24_prospective144_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'ConeRidgeAlpha100_round144_source_preparation_v2_20261008.json',{
        'status':'passed_actual100_sealed_candidate_and_admitted_full144_QA55_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':144,'scored_records':100,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
