"""Prepare a fresh byte-preserving main publication of two completed annual models and the full135 handoff."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    original=A/'publish_actual_BF16wide135_receiver_preflight_v1_20261008.py'
    text=original.read_text(encoding='utf8')
    marker='    sources=list(dict.fromkeys(sources));pins={str(p):sha(p) for p in sources}'
    assert text.count(marker)==1
    text=text.replace(marker,"""    closed=A/'service_owned_workflows_20261006/actual_BF16wide135_receiver_preflight_main_publication_v1_20261008'
    assert read(closed/'service_execution.json')['status']=='passed'
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    sources += [A/'actual_optimization_handoff_v2_20261008.json',A/'record_actual_optimization_handoff_v2_20261008.py',
        A/'monitor_BF16wide135_progress_v1_20261008.py',A/'actual_BF16wide135_live_progress_monitor_launch_v1_20261008.json',
        A/'actual_BF16wide135_receiver_preflight_main_v1_20261008/receipt.json',
        A/'prepare_actual_BF16_two_year_handoff_publisher_v1_20261008.py',bank/'protocol.json',
        *[bank/str(year)/name for year in (2020,2021) for name in ('info.json','frozen_training_inputs.json')]]
    weight_pins={}
    for year in (2020,2021):
        info=read(bank/str(year)/'info.json');model=bank/str(year)/'model.joblib'
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
        assert info['actual_full_annual_reload_prediction_bits_exact'] and info['actual_cold80_prefix_bits_exact']
        assert sha(model)==info['model_sha256'];weight_pins[str(model)]=info['model_sha256']
    sources=list(dict.fromkeys(sources));pins={**weight_pins,**{str(p):sha(p) for p in sources}}""")
    text=text.replace("A/'actual_BF16wide135_receiver_preflight_main_v1_20261008';assert not out.exists()",
        "A/'actual_BF16_two_year_handoff_main_v1_20261008';assert not out.exists()")
    text=text.replace("Path('validation_sync/actual_BF16wide135_receiver_preflight_20261008')",
        "Path('validation_sync/actual_BF16_two_year_training_and135_handoff_20261008')")
    text=text.replace("target=(prefix/source.relative_to(ROOT)).as_posix();targets[target]=data\n                bindings[source.relative_to(ROOT).as_posix()]",
        "relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(hashlib.sha256(data).hexdigest()+'_'+source.name)\n                target=(prefix/relative).as_posix();targets[target]=data\n                bindings[str(source)]")
    text=text.replace("'actual_cross_volume_probe_bytes':proof['cross_volume_transfer_bytes'],",
        "'actual_cross_volume_probe_bytes':proof['cross_volume_transfer_bytes'],'actual_completed_annual_years':[2020,2021],'completed_model_sha256':weight_pins,'remaining_full_bank_and_quality_pending':True,")
    text=text.replace('同步第135轮实际24项方案接收器检查与完整排队流程','同步实际BF16前两年度训练验证与第135轮完整流程交接')
    text=text.replace('Actual24 receiver checks and lazy135 dispatch published to main: ','Actual two complete annual models and full135 handoff published to main: ')
    target=A/'publish_actual_BF16_two_year_handoff_v1_20261008.py';assert not target.exists();compile(text,str(target),'exec')
    target.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual_BF16_two_year_handoff_publisher_preparation_v1_20261008.json',{'status':'prepared_fresh_completed_training2_and_full135_handoff_main_publisher',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),original,target)},'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
