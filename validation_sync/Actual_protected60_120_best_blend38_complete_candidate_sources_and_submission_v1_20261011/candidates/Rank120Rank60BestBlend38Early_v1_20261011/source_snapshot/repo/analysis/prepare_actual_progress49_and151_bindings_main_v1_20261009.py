"""Record the actual151 controls, current draft limits and live148-to150 progress."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    s=(A/'monitor_actual_chronological_optimization_progress_v48_20261009.py').read_text(encoding='utf8')
    s=s.replace('optimization_live_progress_v48_20261009','optimization_live_progress_v49_20261009')
    marker="    write(A/'optimization_live_progress_v49_20261009.json'"
    addition="""    rff151=Path('E:/赛题五_本机临时/RFFSparse55_parent134_historical_v1_20261009')
    state['rff_sparse151_frontier']={'expected_quality_cases':59,'existing_saved_annual_states':20,
        'native72':status('RFFSparse72_native_historical_calendar_controls_v1_20261009'),
        'full55':status('RFFSparse55_full_historical_controls_v1_20261009'),
        'actual_full_control_records':len(list(rff151.glob('case*.json'))),
        'historical_main':status('RFFSparse151_historical_main_publication_v1_20261009'),
        'draft_bindings55_and_six_empty_E_outputs_passed':(A/'RFFSparse151_draft_control_bindings_v1_20261009.json').is_file(),
        'complete_quality_receivers_and_duplicate_audit_still_required':True,'inherited_full150_status_labels_require_normalization_before_admission':True,
        'actual151_official_scores':0,'actual151_future_inference':0,'new_native_fits':0,'actual150_full_required_before_quality':True}
"""
    assert s.count(marker)==1;s=s.replace(marker,addition+marker)
    marker="    write(A/'optimization_live_progress_v49_20261009.md',text)"
    addition="""    text+=f"\\n第151轮RFF与稀疏残差混合：55合成/165截断及20状态元数据已通过，原生72项{state['rff_sparse151_frontier']['native72']['status']}，完整55项{state['rff_sparse151_frontier']['full55']['status']}，历史证据main同步{state['rff_sparse151_frontier']['historical_main']['status']}；六份评分与推理草稿及55项控制绑定已检查，还需完整32代码检查与去重，尚无质量分或测试推理。\\n"
"""
    assert s.count(marker)==1;s=s.replace(marker,addition+marker)
    save('monitor_actual_chronological_optimization_progress_v49_20261009.py',s)
    s=(A/'publish_RFFSparse151_historical_main_v1_20261009.py').read_text(encoding='utf8')
    s=s.replace("'HuberSparse150_prospective_main_publication_v2_20261009'):closed(name)","'HuberSparse150_prospective_main_publication_v2_20261009','RFFSparse151_historical_main_publication_v1_20261009'):closed(name)")
    s=s.replace('RFFSparse151_historical_main_v1_20261009','RFFSparse151_historical_main_v2_20261009')
    s=s.replace('validation_sync/RFFSparse151_historical_v1_20261009','validation_sync/RFFSparse151_historical_v2_20261009')
    s=s.replace('RFFSparse151_historical_main_v1_receipt_20261009','RFFSparse151_historical_main_v2_receipt_20261009')
    marker='    sources=list(dict.fromkeys(sources))'
    addition="""    binding=A/'RFFSparse151_draft_control_bindings_v1_20261009.json';draft=read(binding)
    assert draft['actual_control_bindings']==55 and draft['compiled_drafts']==6 and draft['verified_empty_E_outputs']==6
    for path,digest in draft['input_sha256'].items():assert sha(path)==digest,path
    sources.extend([binding,A/'verify_RFFSparse151_draft_control_bindings_v1_20261009.py',
        A/'monitor_actual_chronological_optimization_progress_v49_20261009.py',A/'prepare_actual_progress49_and151_bindings_main_v1_20261009.py',
        A/'actual_old_progress47_retired_after48_v1_20261009.json'])
"""
    assert s.count(marker)==1;s=s.replace(marker,addition+marker)
    s=s.replace("'own32_quality_receivers_and_duplicate_audit_still_required':True", "'own32_quality_receivers_and_duplicate_audit_still_required':True,'actual55_control_bindings_and_six_draft_parse_and_empty_E_outputs_passed':True,'inherited_full150_status_labels_need_normalization_before_quality_admission':True")
    s=s.replace('同步第151轮RFF与稀疏残差55完整165冷检查72原生实际证据','同步第151轮55控制与六份草稿接收绑定及质量准入待办')
    save('publish_RFFSparse151_historical_main_v2_20261009.py',s)
if __name__=='__main__':main()
