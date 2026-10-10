"""Bind immutable actual recovery publication to the predeclared score-family receipt slot."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('actual_reboot_routes_protected37_capsules_main_v1_20261011')
    path=A/'reboot_routes_and_protected37_main_receipt_v1_20261011.json';receipt=read(path)
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    proof=Path('E:/赛题五_本机临时/StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011/verification.json')
    assert len(read(proof)['records'])==37
    native=Path('E:/赛题五_本机临时/rank20_two_seed_protected_selected_native14_v1_20261011/verification.json');assert native.is_file()
    for target in ['Rank20_two_seed_protected37_official37_main_receipt_v1_20261011.json','Rank20_two_seed_protected37_selected14_main_receipt_v1_20261011.json']:
        create(A/target,{**receipt,'publication_route':'recovery_publication_not_original_failed_publisher','actual_recovery_receipt':str(path),'actual_recovery_receipt_sha256':sha(path),'official37_verification_sha256':sha(proof),'selected_native_verification_sha256':sha(native),'original_failed_publishers_preserved':True})
if __name__=='__main__':main()
