"""Restore the complete35 alias namespace; preserve the actual fixed14 proof bytes."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    native='actual_stock_rank60_fixed_leading_case17_native14_v2_20261011'
    f=A/'service_owned_workflows_20261006'/native
    assert read(f/'service_execution.json')['status']=='passed' and not owned(read(f/'native_launch.json'))
    original=A/'actual_stock_rank60_direct_embedding35_selected_native14_location_v1_20261011.json'
    target=A/'actual_stock_rank60_fixed_leading_case17_native14_location_v2_20261011.json'
    assert original.parent.resolve()==A.resolve() and target.parent.resolve()==A.resolve()
    value=read(original)
    expected=Path('E:/赛题五_本机临时/stock_rank60_fixed_leading_case17_native14_v2_20261011')
    assert Path(value['output']).resolve()==expected.resolve()
    proof=expected/'verification.json'
    assert sha(proof)==value['verification_sha256']
    assert read(proof)['status']=='passed_fixed_case17_six_states14_native_and14_cold_and7_prefit_rejections'
    digest=sha(original);assert not target.exists()
    original.rename(target);assert sha(target)==digest and not original.exists()
    source=A/'publish_shared_report_controls_and_fixed60_case17_main_v2_20261011.py'
    driver=A/'publish_shared_report_controls_and_fixed60_case17_main_v3_20261011.py'
    text=source.read_text(encoding='utf8').replace("label='Shared_report_controls_and_fixed60_case17_v2'","label='Shared_report_controls_and_fixed60_case17_v3'")
    text=text.replace('publish_frozen_shared_report_controls_and_fixed60_case17_main_v2_20261011.py','publish_frozen_shared_report_controls_and_fixed60_case17_main_v3_20261011.py')
    ast.parse(text);assert not driver.exists();driver.write_text(text,encoding='utf8')
    receipt=A/'fixed_case17_actual14_receipt_namespace_repair_v3_20261011.json'
    pins={str(p):sha(p) for p in [Path(__file__),source,driver,target,proof]}
    create(receipt,{'status':'fixed_case14_actual_receipt_moved_byte_exact_out_of_complete35_namespace',
      'input_sha256':pins,'original_misnamed_receipt':str(original),'correct_fixed_case_receipt':str(target),
      'actual14_control_bytes_preserved':True,'complete35_not_claimed':True,
      'no_model_or_score_restarted':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
    from start_fast_completed_owned_service_v1_20261011 import start_service
    assert allowed()
    print(start_service('actual_shared_report_controls_and_fixed60_case17_main_v3_20261011',driver.name,[],{**pins,str(receipt):sha(receipt)}),flush=True)

if __name__=='__main__':main()
