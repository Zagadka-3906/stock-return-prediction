from pathlib import Path
import sys,ast,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 proofs=[A/n for n in ['verified_canonical_publication_failed_chain38_routes_v1_20261011.json','canonical_publication_resume186_isolated39_admission_v1_20261011.json','actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json','rank120_actual_restart_order_recovery_v2_20261011.json','observer121_actual_admission_v1_20261011.json']]
 paths=[Path(__file__),*proofs]
 for proof in proofs:
  for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p;paths.append(Path(p))
 for name in ['actual186_registered_QA_main_resume39_v1_20261011','actual186_complete_parent_bridge40_v1_20261011','actual_stock_rank120_own6_full5_native42_direct33_queue_v2_20261011',*[n for n,d in read(proofs[2])['tasks']]]:
  paths += [A/'service_owned_workflows_20261006'/name/p for p in ('job_definition.json','native_launch.json')]
 for name in ('actual_stock_rank120_embedding_small512_restart_v1_20261011','StockRank120EmbeddingSmall512_independent_small_CPU_v1_20261011'):
  f=A/'service_owned_workflows_20261006'/name;assert read(f/'service_execution.json')['status']=='passed';paths.append(f/'service_execution.json')
 template=A/'publish_frozen_Actual183_parent37_and_mixed60_49_sources_main_v1_20261011.py';paths.append(template)
 lines=template.read_text(encoding='utf8').replace('Actual183_parent37_and_mixed60_49_sources','Actual_chain40_rank120_order2_sources').splitlines()
 i=next(i for i,s in enumerate(lines) if s.strip().startswith('paths=[Path(__file__)'));lines[i]='    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]'
 i=next(i for i,s in enumerate(lines) if "payload[(prefix/'manifest.json')" in s)
 manifest={'status':'actual186_resumed_after_registration_and_fresh43_dependents_and_rank120_restart_order_fixed','dynamic_canonical_publication_module_aliases':30,'actual186_original_registration_reused':True,'actual186_QA_main_pending':True,'actual_failed_dependents_fresh_identities':43,'actual_rank120_restart_small32_and_wide2_passed':True,'actual_rank120_small_CPU_independent_replay_passed':True,'actual_scientific_workers_terminated':0,'new_fits_or_scores_by_publication':0,'future_full_qualification_pending':True,'test_labels_read':False}
 assert len(read(proofs[0])['canonical_publication_module_aliases'])==30
 lines[i]="    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})"
 i=next(i for i,s in enumerate(lines) if "'commit','-m'" in s);lines[i]="            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','实际186发布模块映射恢复及43个失败依赖新任务；120日重启顺序修复且CPU独立重放通过，未重训已有模型',timeout=180)"
 p=A/'publish_frozen_Actual_chain40_rank120_order2_sources_main_v1_20261011.py';text='\n'.join(lines)+'\n';ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
