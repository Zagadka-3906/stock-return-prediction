"""Bind actual generator3 in every canonical route after all legacy token conversions."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 originals=[];products=[]
 header='''"""Bind the actual complete ordered185 source receiver after immutable legacy conversion."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_JointCrossHuberOrder185_round147_sources_v2_20261008 as original
NAMES=original.NAMES
ORIGINAL_GENERATE=original.generate
def source_paths():
 out=[]
 for p in original.source_paths():
  if p.name=='run_JointCrossHuberOrder185_round147_full_registration_v3_20261008.py':p=A/'run_JointCrossHuberOrder185_round147_full_registration_v4_20261008.py'
  if p.name=='publish_JointCrossHuberOrder185_evidence_v2_20261008.py':p=A/'publish_JointCrossHuberOrder185_evidence_v3_20261008.py'
  out.append(p)
 out += [Path(__file__),Path(original.__file__),A/'bind_JointCrossHuber147_actual_generator_v3_20261008.py',A/'JointCrossHuber147_actual_generator_binding_v3_20261008.json']
 return list(dict.fromkeys(out))
def generate(parent):
 result={}
 for n,s in ORIGINAL_GENERATE(parent).items():
  for version in (1,2):s=s.replace('prepare_JointCrossHuberOrder185_round147_sources_v'+str(version)+'_20261008','prepare_JointCrossHuberOrder185_round147_sources_v3_20261008')
  compile(s,str(A/n),'exec');result[n]=s
 return result
def main():
 original.generate=generate
 original.main()
if __name__=='__main__':main()
'''
 products.append(save('prepare_JointCrossHuberOrder185_round147_sources_v3_20261008.py',header))
 for old,new in [('run_JointCrossHuberOrder185_round147_full_registration_v3_20261008.py','run_JointCrossHuberOrder185_round147_full_registration_v4_20261008.py'),('publish_JointCrossHuberOrder185_evidence_v2_20261008.py','publish_JointCrossHuberOrder185_evidence_v3_20261008.py')]:
  p=A/old;originals.append(p);s=p.read_text(encoding='utf8').replace('prepare_JointCrossHuberOrder185_round147_sources_v2_20261008','prepare_JointCrossHuberOrder185_round147_sources_v3_20261008')
  if new.startswith('run_'):s=s.replace('actual_registration_v3_20261008','actual_registration_v4_20261008').replace('full_registration_v3_file_IO_20261008','full_registration_v4_file_IO_20261008')
  products.append(save(new,s))
 create(A/'JointCrossHuber147_actual_generator_binding_v3_20261008.json',{'status':'bound_actual_generator3_after_complete_legacy_conversion_before_prospective_or_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},'all_prototypes_preserved':True,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
 print('Actual generator3, publisher3 and full4 bound; original scientific arithmetic preserved.',flush=True)
if __name__=='__main__':main()
