from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('registered13_StockRank20Embedding182_complete63_family_v6_20261010')
 receipt=A/'github_validation_sync_main_20261005/round182_receipt.json';full=A/'optimization_20261003_r182/full_registration_execution.json';candidate=ROOT/'candidates/optimization_20261003_r182'
 assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['scored_records']==63
 assert read(full)['status']=='passed';pred=read(candidate/'verification.json');assert pred['status']=='passed' and len(pred['models'])==34
 assert sha(candidate/'submission.csv')==pred['csv_sha256']
 for m in pred['models'].values():assert sha(m['path'])==m['sha256']
 create(A/'actual182_qualified_parent_prefix_bridge_verification_v1_20261011.json',{'status':'passed_actual_existing_182_full_registration_main_CSV34_native_model_rehash_only','input_sha256':{str(p):sha(p) for p in [Path(__file__),receipt,full,candidate/'verification.json',candidate/'submission.csv']},'literal_dependency_alias_only':True,'new_full_registration_or_inference_claimed':False,'original_complete_family_preserved':True,'test_labels_read':False})
if __name__=='__main__':main()
