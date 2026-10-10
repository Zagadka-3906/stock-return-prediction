"""Preserve the failed prototype; add required decay=None in fresh exclusive outputs."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    old='actual_stock_rank60_fixed_leading_case17_native14_v1_20261011'
    folder=A/'service_owned_workflows_20261006'/old
    assert read(folder/'service_execution.json')['status']=='failed' and not owned(read(folder/'native_launch.json'))
    source=A/'verify_stock_rank60_fixed_leading_case17_native14_v1_20261011.py'
    target=A/'verify_stock_rank60_fixed_leading_case17_native14_v2_20261011.py'
    text=source.read_text(encoding='utf8')
    needle="'anchor_round':183,'first2020_active':True"
    assert text.count(needle)==1;text=text.replace(needle,"'anchor_round':183,'decay':None,'first2020_active':True")
    text=text.replace('stock_rank60_fixed_leading_case17_native14_v1_20261011','stock_rank60_fixed_leading_case17_native14_v2_20261011')
    text=text.replace('actual_stock_rank60_fixed_leading_case17_native14_location_v1_20261011','actual_stock_rank60_fixed_leading_case17_native14_location_v2_20261011')
    proof=A/'stock_rank60_fixed_case17_decay_none_recovery_v2_20261011.json'
    text=text.replace('stock_rank60_fixed_leading_case17_native14_preparation_v1_20261011.json',proof.name)
    ast.parse(text);assert not target.exists();target.write_text(text,encoding='utf8')
    pins={str(p):sha(p) for p in [Path(__file__),source,target,folder/'service_execution.json',folder/'stderr.log']}
    create(proof,{'status':'new_exclusive_fixed_case17_native_controls_required_decay_none_added',
      'input_sha256':pins,'failed_prototype_preserved':True,'new_scientific_parameters':False,
      'configuration_decay':None,'fixed_case':17,'search_winner_not_claimed':True,
      'new_fits':0,'new_scores':0,'test_labels_read':False})
    pubsource=A/'publish_shared_report_controls_and_fixed60_case17_main_v1_20261011.py'
    pubtarget=A/'publish_shared_report_controls_and_fixed60_case17_main_v2_20261011.py'
    pub=pubsource.read_text(encoding='utf8').replace('actual_stock_rank60_fixed_leading_case17_native14_v1_20261011','actual_stock_rank60_fixed_leading_case17_native14_v2_20261011')
    pub=pub.replace('actual_stock_rank60_fixed_leading_case17_native14_location_v1_20261011','actual_stock_rank60_fixed_leading_case17_native14_location_v2_20261011')
    pub=pub.replace('verify_stock_rank60_fixed_leading_case17_native14_v1_20261011.py',target.name)
    pub=pub.replace("label='Shared_report_controls_and_fixed60_case17'","label='Shared_report_controls_and_fixed60_case17_v2'")
    pub=pub.replace('publish_frozen_shared_report_controls_and_fixed60_case17_main_v1_20261011.py','publish_frozen_shared_report_controls_and_fixed60_case17_main_v2_20261011.py')
    pub=pub.replace('stock_rank60_fixed_leading_case17_native14_preparation_v1_20261011.json',proof.name)
    ast.parse(pub);assert not pubtarget.exists();pubtarget.write_text(pub,encoding='utf8')
    from start_fast_completed_owned_service_v1_20261011 import start_service
    assert allowed()
    print(start_service('actual_stock_rank60_fixed_leading_case17_native14_v2_20261011',target.name,[],{**pins,str(proof):sha(proof)}),flush=True)
    assert allowed()
    print(start_service('actual_shared_report_controls_and_fixed60_case17_main_v2_20261011',pubtarget.name,[],{str(pubtarget):sha(pubtarget),str(proof):sha(proof)}),flush=True)

if __name__=='__main__':main()
