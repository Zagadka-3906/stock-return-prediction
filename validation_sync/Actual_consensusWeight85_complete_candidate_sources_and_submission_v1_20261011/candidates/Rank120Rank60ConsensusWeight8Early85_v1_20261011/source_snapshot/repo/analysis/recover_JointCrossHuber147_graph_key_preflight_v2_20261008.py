"""Preserve failed prototype; bind the already converted ordered graph key before scoring."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 g=A/'prepare_JointCrossHuberOrder185_round147_sources_v1_20261008.py';s=g.read_text(encoding='utf8')
 original='start=s.index("            assert \'nonflag_CPU_HuberCrossFamily_complete_parent_CDF\' not in graph")'
 assert s.count(original)==1
 s=s.replace(original,'start=s.index("            assert \'nonflag_CPU_joint_Cross_Huber_ordered_complete_parent_CDF\' not in graph")')
 replacements={
 'prepare_JointCrossHuberOrder185_round147_sources_v1_20261008':'prepare_JointCrossHuberOrder185_round147_sources_v2_20261008',
 'prepare_JointCrossHuberOrder185_selected_candidate_v2_20261008':'prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008',
 'run_JointCrossHuberOrder185_round147_full_registration_v2_20261008':'run_JointCrossHuberOrder185_round147_full_registration_v3_20261008',
 'publish_JointCrossHuberOrder185_evidence_v1_20261008':'publish_JointCrossHuberOrder185_evidence_v2_20261008'}
 for old,new in replacements.items():s=s.replace(old,new)
 s=s.replace('original.generate(139).items()', 'original.generate(139).items()')
 s=s.replace("return list(dict.fromkeys([Path(__file__),", "return list(dict.fromkeys([Path(__file__),A/'recover_JointCrossHuber147_graph_key_preflight_v2_20261008.py',A/'JointCrossHuber147_graph_key_preflight_recovery_v2_20261008.json',")
 products=[save('prepare_JointCrossHuberOrder185_round147_sources_v2_20261008.py',s)];originals=[g]
 for old,new in replacements.items():
  if old.startswith('prepare_JointCrossHuberOrder185_round147_sources'):continue
  p=A/(old+'.py');originals.append(p);t=p.read_text(encoding='utf8')
  t=t.replace('prepare_JointCrossHuberOrder185_round147_sources_v1_20261008','prepare_JointCrossHuberOrder185_round147_sources_v2_20261008')
  if old.startswith('run_'):t=t.replace('actual_registration_v2_20261008','actual_registration_v3_20261008').replace('full_registration_v2_file_IO_20261008','full_registration_v3_file_IO_20261008')
  products.append(save(new+'.py',t))
 create(A/'JointCrossHuber147_graph_key_preflight_recovery_v2_20261008.json',{'status':'recovered_static_prototype_graph_key_after_actual_conversion_before_any147_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_prototype_failure':'ValueError: substring not found: legacy Huber key had already been converted to Joint key',
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},'all_original_sources_preserved':True,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
 print('Recovered generator2 and actual candidate3/full3/publisher2; no scored cases.',flush=True)
if __name__=='__main__':main()
