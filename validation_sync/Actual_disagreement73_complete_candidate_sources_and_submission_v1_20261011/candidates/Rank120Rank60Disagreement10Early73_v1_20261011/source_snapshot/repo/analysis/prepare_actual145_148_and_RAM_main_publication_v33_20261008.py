"""Publish actual145 closure,148 prospective and optional RAM boundary after main31; hold only idle publishers."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 original=A/'publish_actual_joint147_preparation_and_storage_main_v31_20261008.py';s=original.read_text(encoding='utf8')
 s=s.replace('actual_joint147_preparation_and_storage_main_v31_20261008','actual145_148_and_RAM_main_v33_20261008')
 s=s.replace('actual_joint147_preparation_and_verified_storage_v31_20261008','actual145_joint148_and_RAM_boundary_v33_20261008')
 s=s.replace('actual_joint147_preparation_and_storage_main_v31_receipt_20261008','actual145_148_and_RAM_main_v33_receipt_20261008')
 s=s.replace('actual_fine146_historical_controls_main_publication_v30_20261008','actual_joint147_preparation_and_storage_main_publication_v31_20261008')
 s=s.replace('Git_publisher_exact_nine_index_refresh_verified_E_relocation_v10_20261008\'):closed(n)','CrossFamilyFine125_round145_full_registration_v3_20261008\'):closed(n)')
 s=s.replace('datetime.datetime(2026,10,8,19,9)','datetime.datetime(2026,10,8,21,32)')
 s=s.replace("  sources.extend(p for p in A.iterdir()", "  sources += [A/'actual_optimization_checkpoint_v35_20261008.json',A/'optimization_20261003_r145/full_registration_execution.json',A/'github_validation_sync_main_20261005/round145_receipt.json',A/'latest_verified_submission_delivery_v2_20261008.json',A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json',A/'actual_deferred_serialization_RAM_boundary_v3_20261008.json']\n  sources.extend(p for p in A.iterdir()")
 s=s.replace("'actual_JointCrossHuber181_synthetic_location_v1_20261008.json'):","'actual_JointCrossHuber181_synthetic_location_v1_20261008.json','actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008.json'):")
 s=s.replace('full_board_deferred_resource_budget_v2_20261008','full_board_deferred_resource_budget_v3_20261008')
 needle="  payload[(prefix/'manifest.json').as_posix()]=sync.encoded({"
 assert s.count(needle)==1
 s=s.replace(needle,"  qualified=read(A/'github_validation_sync_main_20261005/round145_receipt.json');prosp=read(A/'AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.json');resource_proof=read(resource/'verification.json')\n"+needle)
 s=s.replace("'actual147_full_historical_and_native_jobs_have_their_own_actual_statuses':True", "'actual145_qualified_main_commit':qualified['commit'],'actual145_qualified_score':qualified['official_score'],'actual145_qualified_physical_models':22,'connected_records_at145':14405,'actual148_prospective_sources':prosp['actual_prospective_sources'],'actual148_prospective_graph_controls':prosp['actual_graph_controls'],'actual_optional_RAM_boundary':resource_proof,'actual147_full_historical_and_native_jobs_have_their_own_actual_statuses':True")
 s=s.replace('同步147轮联合权重顺序验证准备与E盘迁移核验，保留失败记录','同步145轮正式最佳、148轮完整预检及实际内存边界，保留失败记录')
 target=save('publish_actual145_148_and_RAM_main_v33_20261008.py',s)
 meta=A/'actual145_148_and_RAM_main_preparation_v33_20261008.json'
 create(meta,{'status':'prepared_serial_main_publication_after_actual31_and145_qualification_with_completed148_controls_and_RAM_boundary',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,target]},'new_quality_scores':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('actual145_148_and_RAM_main_publication_v33_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target,meta]})
 create(A/'actual145_148_and_RAM_main_hidden_launch_v33_20261008.json',row);print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
