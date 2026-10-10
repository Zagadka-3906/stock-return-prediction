"""Execute preserved167 receiver with exact predecessor, cleanup, and proven late encoder binding."""
from pathlib import Path
from types import SimpleNamespace
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
def main():
    import prepare_protected167_full_registry_sources_v1_20261010 as routes
    old=routes.source_paths
    routes.source_paths=lambda:list(dict.fromkeys([*old(),Path(__file__),A/'run_Return167_complete_family_admitted_v2_20261010.py',A/'verify_Return167_complete67_preflight_v1_20261010.py',A/'protected167_full_family_preflight_v1_20261010.json',A/'prepare_protected167_selected_candidate_v3_20261010.py',A/'predict_protected_Return_after163_complete_scheme_v4_20261010.py',A/'Return167_actual_parent163_source_and_callback_controls_v2_20261010.json',A/'late_bound_dynamic_snapshot_encoder_runtime_v1_20261010.py',A/'late_bound_snapshot_encoder_actual_CPU_controls_v1_20261010.json']))
    source=A/'run_protected167_full_registration_v1_20261010.py';text=source.read_text(encoding='utf8')
    needle="closed('ReusedNN166Quality19_round165_full_registration_v1_20261009')";assert text.count(needle)==1
    text=text.replace(needle,"closed('ReusedNN166Quality19_round166_full_registration_v1_20261009')")
    needle="            create(folder/'full_registration_execution.json'";assert text.count(needle)==1
    text=text.replace(needle,"            assert restore_ranking is not None\n            restore_ranking();restore_ranking=None\n"+needle)
    text=text.replace('verified_TLS_Git_retry_runtime_v2_20261008','verified_TLS_Git_retry_runtime_v3_20261010')
    text=text.replace('完整157之后保护高分头部的成熟神经排序置换','完整163之后追加成熟直接收益率网络的保护排序置换')
    text=text.replace('预定两类保护头部方案各37项，以及两个已合格锚点，共76项；连续官方S优先','已实际完成直接收益率65项连接验证，加合格165/166锚点，共67条；连续官方S优先')
    namespace={'__file__':str(source),'__name__':'actual_Return167_registration_receiver'}
    exec(compile(text,str(source),'exec'),namespace)
    receiver=SimpleNamespace(**namespace)
    from late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 import installed
    with installed(receiver,'publish_ReturnProtected167_round167_full_validation_20261010',Path('E:/赛题五_本机临时/第167轮_20261010/late_snapshot_encoder_import.json')):
        receiver.main()
if __name__=='__main__':main()
