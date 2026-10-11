from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();source=A/'activate_tiny183_QA94_sources_main_v71_20261010.py';target=A/'activate_verified_seal_routes7_CPU10_sources_main_v73_20261010.py'
    text=source.read_text(encoding='utf8').replace('Tiny183_QA94_actual_sources','Verified_seal175_routes7_CPU10_sources').replace('tiny183_QA94_sources','verified_seal175_routes7_CPU10_sources').replace('v71_20261010','v73_20261010')
    extras=['prepare_Top175_verified_inference_sealing_recovery_v2_20261010.py','Top175_verified_inference_sealing_recovery_v2_20261010.json','seal_StockTop10Embedding175_selected_candidate_recovery_v2_20261010.py','recover_verified_sealing175_and_descendants_routes_v7_20261010.py','Dual25_verified_recovery_exact_dependency_aliases_v7_20261010.json','route_verified_Dual25_recovery_dependencies_v7_20261010.py','finish_StockTop10Embedding175_verified_registration_recovery_v7_20261010.py','verify_sealing_routes7_actual_main_and_cross_drive_CPU_v1_20261010.py','sealing_routes7_actual_main_and_cross_drive_CPU_v1_20261010.json']
    text=text.replace('extras=[','extras='+repr(extras)[:-1]+',',1)
    needle="proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json'";assert text.count(needle)==1
    text=text.replace(needle,"proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v7_20261010.json'")
    text=text.replace("'status':'compiled_exact_full18148_QA92_full18263_QA93_and_actual_routes_CPU111_child9_sources'","'status':'actual_verified175_inference_and_seal_preserved_new_main_context_routes7_and_real_D_to_E_transfer_CPU10_sources'")
    text=text.replace("'actual_route_alias_CPU_cases':111","'actual_original_storage_main_dispatch_CPU_cases':10,'actual_real_D_to_E_transfer_bytes':1064")
    text=text.replace('保存第183轮82项微权重互补与3个合格锚点组成的85项完整流程，QA94与17258项完整榜源码；尚未执行未来推理','保存已完成175推理及封装修复、后续封装原始main上下文和实际跨盘复制10项CPU检查；仅恢复登记与依赖流程')
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    import runpy;runpy.run_path(str(target),run_name='__main__')
if __name__=='__main__':main()
