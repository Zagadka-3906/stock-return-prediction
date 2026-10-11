"""Match actual large29 service provenance without changing its scientific output folder."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import retire,start_service
def main():
    assert allowed();source=A/'publish_stock_forward5_embedding_after171_large29_completion_v70_20261010.py';target=A/'publish_stock_forward5_embedding_after171_large29_completion_v71_20261010.py'
    text=source.read_text(encoding='utf8');old='service_owned_workflows_20261006/actual_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010';assert text.count(old)==1
    text=text.replace(old,old.replace('_v1_','_v2_'));assert 'StockForward5EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010' in text
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    assert not Path('E:/赛题五_本机临时/stock_forward5_embedding29_after171_completion_main_v68_20261010').exists()
    oldrow=read(A/'service_owned_workflows_20261006/actual_stock_forward5_embedding_after171_large29_completion_main_v70_20261010/native_launch.json')
    retire(oldrow,'Match exact future large29 v2 service provenance before any publisher output; preserve E screen_v1 location, score recipe, receipt68 and frozen48 plan')
    proof=A/'stock_forward5_embedding_large29_exact_service_receipt_admission_v71_20261010.json'
    create(proof,{'status':'compiled_exact_actual_large29_v2_service_pointer_Escreen_v1_and_receipt68_consistent_before_scores','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target]},'no_scoring_or_native_math_changed':True,'new_quality_scores':0,'test_labels_read':False})
    row=start_service('actual_stock_forward5_embedding_after171_large29_completion_main_v71_20261010',target.name,[],{str(target):sha(target),str(proof):sha(proof)});create(A/'actual_forward5_large29_exact_service_receipt_activation_v71_20261010.json',row)
    print({'actual_large29_v2_service_receipt68_publisher71_admitted':True},flush=True)
if __name__=='__main__':main()
