"""Prepare all242 official/candidate/QA59 receivers with explicit report paths and own0.125 codec controls."""
from pathlib import Path
import io,tokenize,re,sys,time,json,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def convert(s):
 s=s.replace('JointCrossHuberOrder185_round147_full_registration_v1_20261008','__ACTUAL_UPSTREAM147_FULL__')
 s=s.replace('HuberCrossFamilyFine125_round146_full_registration_v2_20261008','__ACTUAL_UPSTREAM147_FULL__')
 s=s.replace('actual_JointCrossHuber35_existing_native_location_v1_20261008','__EXISTING35_POINTER__')
 s=s.replace('JointCrossHuber_ordered_CDF_v1_20261008','AdaptiveJointCrossHuber_ordered_CDF_v2_20261008')
 s=s.replace('JointCrossHuber_ordered_native_stage_v1_20261008','AdaptiveJointCrossHuber_ordered_native_stage_v2_20261008')
 s=s.replace('JointCrossHuberOrder185','AdaptiveJointCrossHuber242').replace('JointCrossHuber147','AdaptiveJointCrossHuber148')
 s=s.replace('JointCrossHuber181','AdaptiveJointCrossHuber238').replace('JointCrossHuber80','AdaptiveJointCrossHuber80')
 s=s.replace('predict_JointCrossHuber','predict_AdaptiveJointCrossHuber').replace('_JointCrossHuber_teacher','_AdaptiveJointCrossHuber_teacher')
 s=s.replace('JointCrossHuber_complete_parent','AdaptiveJointCrossHuber_complete_parent')
 s=s.replace('nonflag_CPU_joint_Cross_Huber_ordered_complete_parent_CDF','nonflag_CPU_joint_Cross_Huber_adaptive_complete_parent_CDF')
 for old,new in [('round147','round148'),('full147','full148'),('actual147','actual148'),('prospective147','prospective148'),('_r147','_r148'),('第147轮','第148轮'),('qa_v58','qa_v59'),('qa58','qa59'),('QA58','QA59'),('wave430','wave431')]:s=s.replace(old,new)
 tokens=list(tokenize.generate_tokens(io.StringIO(s).readline))
 s=tokenize.untokenize([t._replace(string={'147':'148','185':'242','181':'238','543':'714','81':'108','58':'59','430':'431'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
 for old,new in [('actual185','actual242'),('all185','all242'),('185项','242项'),('181项','238项'),('181full','238full'),('543cold','714cold'),('181_fixed','238_fixed'),('32_prospective147','32_prospective148')]:s=s.replace(old,new)
 s=s.replace('(134,139,141,145,146)','(134,139,145,146,147)').replace('(139,141,145,146)','(139,145,146,147)').replace('[139,141,145,146]','[139,145,146,147]')
 s=s.replace('=={134,136,139}','=={134,136,139,145}')
 s=re.sub(r'(AdaptiveJointCrossHuber(?:242|148)_[A-Za-z0-9_]+)_v[2345]_20261008',r'\1_v1_20261008',s)
 s=s.replace('actual_registration_v5_20261008','actual_registration_v1_20261008').replace('full_registration_v5_file_IO_20261008','full_registration_v1_file_IO_20261008')
 for kind in ('synthetic_controls','full_historical_controls'):
  s=s.replace('AdaptiveJointCrossHuber238_actual_'+kind+'_v1_20261008','AdaptiveJointCrossHuber238_actual_'+kind+'_v2_20261008')
 s=s.replace('actual_AdaptiveJointCrossHuber238_synthetic_location_v1_20261008','actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008').replace('actual_AdaptiveJointCrossHuber238_parent134_location_v1_20261008','actual_AdaptiveJointCrossHuber238_parent134_location_v2_20261008')
 s=s.replace('__EXISTING35_POINTER__','actual_JointCrossHuber35_existing_native_location_v1_20261008')
 return s.replace('__ACTUAL_UPSTREAM147_FULL__','JointCrossHuberOrder185_round147_full_registration_v1_20261008')
def main():
 import subprocess,importlib
 proposal=A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json';plan=read(proposal)
 assert len(plan['new_cases'])==238 and len(plan['heads'])==7 and plan['anchor_rounds']==[139,145,146,147]
 plan.update(round=148,QA_version=59,wave=431,fixed_scientific_stage_base_round=134,expected_scored_cases=242,
  status='frozen242_expanded_Cross_share_joint_parameters_before_quality',comparison_parent_rule='official_S_desc_unique_physical_model_SHA_count_asc_round_asc',original_proposal_sha256=sha(proposal))
 create(A/'AdaptiveJointCrossHuber242_round148_plan_v1_20261008.json',plan)
 originals=[];products=[]
 pairs=[('JointCrossHuber147_storage_v1_20261008.py','AdaptiveJointCrossHuber148_storage_v1_20261008.py'),
  ('verify_JointCrossHuber147_D_scoring_scope_v1_20261008.py','verify_AdaptiveJointCrossHuber148_D_scoring_scope_v1_20261008.py'),
  ('run_JointCrossHuberOrder185_official_comparison_v1_20261008.py','run_AdaptiveJointCrossHuber242_official_comparison_v1_20261008.py'),
  ('prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py','prepare_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py'),
  ('seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py','seal_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py'),
  ('run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py','run_AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008.py'),
  ('publish_JointCrossHuberOrder185_evidence_v4_20261008.py','publish_AdaptiveJointCrossHuber242_evidence_v1_20261008.py'),
  ('verify_JointCrossHuberOrder185_round147_sources_v2_20261008.py','verify_AdaptiveJointCrossHuber242_round148_sources_v1_20261008.py'),
  ('verify_JointCrossHuberOrder185_prospective_routes_v2_20261008.py','verify_AdaptiveJointCrossHuber242_prospective_routes_v1_20261008.py'),
  ('dispatch_JointCrossHuber147_complete_pipeline_v2_20261008.py','dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v1_20261008.py'),
  ('predict_JointCrossHuber_complete_parent_scheme_v1_20261008.py','predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008.py')]
 for old,new in pairs:
  p=A/old;originals.append(p);s=convert(p.read_text(encoding='utf8'))
  s=s.replace('cross_volume_byte_probe_v2','cross_volume_byte_probe_v1')
  s=s.replace("A/'JointCrossHuber147_core_receiver_preparation_v1_20261008.json'","A/'AdaptiveJointCrossHuber148_complete_receiver_preparation_v1_20261008.json'")
  # Generic147 receiver metadata becomes the actual single fresh148 preparation proof.
  s=s.replace('AdaptiveJointCrossHuber148_core_receiver_preparation_v1_20261008.json','AdaptiveJointCrossHuber148_complete_receiver_preparation_v1_20261008.json')
  products.append(save(new,s))
 import prepare_JointCrossHuberOrder185_round147_sources_v4_20261008 as prior
 inherited=[p.relative_to(A).as_posix() for p in prior.source_paths() if p.is_file() and p.suffix=='.py']
 own=[p.name for p in products]+[Path(__file__).name,'AdaptiveJointCrossHuber148_complete_receiver_preparation_v1_20261008.json',
  'AdaptiveJointCrossHuber242_round148_plan_v1_20261008.json',proposal.name,
  'prepare_AdaptiveJointCrossHuber242_frontier_v1_20261008.py','recover_AdaptiveJointCrossHuber148_import_boundaries_v2_20261008.py',
  'AdaptiveJointCrossHuber148_import_boundary_recovery_v2_20261008.json','AdaptiveJointCrossHuber148_historical_receiver_preparation_v1_20261008.json',
  'AdaptiveJointCrossHuber_ordered_CDF_v2_20261008.py','AdaptiveJointCrossHuber_ordered_native_stage_v2_20261008.py',
  'AdaptiveCrossFamily_complete_parent_CDF_v1_20261008.py','AdaptiveCrossFamily_complete_parent_native_stage_v1_20261008.py',
  'verify_AdaptiveJointCrossHuber238_synthetic_controls_v2_20261008.py','verify_AdaptiveJointCrossHuber80_native_historical_calendar_v2_20261008.py',
  'verify_AdaptiveJointCrossHuber238_full_historical_controls_v2_20261008.py','actual_JointCrossHuber35_existing_native_location_v1_20261008.json',
  'actual_AdaptiveJointCrossHuber238_synthetic_location_v2_20261008.json','actual_AdaptiveJointCrossHuber80_native_calendar_location_v2_20261008.json',
  'actual_AdaptiveJointCrossHuber238_parent134_location_v2_20261008.json','AdaptiveJointCrossHuber148_D_scoring_scope_v1_20261008.json',
  'AdaptiveJointCrossHuber242_prospective_routes_v1_20261008.json','AdaptiveJointCrossHuber242_actual_controls_index_v1_20261008.json',
  'AdaptiveJointCrossHuber242_round148_source_admission_v1_20261008.json','AdaptiveJointCrossHuber242_round148_source_preparation_v1_20261008.json',
  'AdaptiveJointCrossHuber242_selected_release_v1_20261008/selected_candidate_ready_for_registration.json','AdaptiveJointCrossHuber242_scores_github_v1_20261008/receipt.json']
 names={n:convert(n) for n in prior.NAMES.values()}
 header='''"""Predeclare32 complete242 receiver routes, fixed134 mathematical base and explicit comparison parent."""
from pathlib import Path
import sys,time,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_AdaptiveJointCrossHuber148_complete_receivers_v1_20261008 import convert
import prepare_JointCrossHuberOrder185_round147_sources_v4_20261008 as original
'''+f'NAMES={names!r}\nSOURCE_NAMES={list(dict.fromkeys([*own,*inherited]))!r}\n'+'''
def source_paths():return list(dict.fromkeys([Path(__file__),*(A/n for n in SOURCE_NAMES),*(A/n for n in NAMES.values())]))
def generate(parent):
 assert parent in (139,145,146,147)
 result={convert(n):convert(s) for n,s in original.generate(139).items()}
 for n,s in result.items():
  s=s.replace('_r139/',f'_r{parent}/').replace('PREVIOUS_NUMBER = 139',f'PREVIOUS_NUMBER = {parent}')
  s=s.replace("'explicit_parent_round': 139",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=139',f'explicit_comparison_parent_round={parent}')
  if n=='optimize_training_round148.py':
   t=ast.parse(s);assignment=next(x for x in t.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PREVIOUS' for a in x.targets))
   literal=ast.get_source_segment(s,assignment.value.right);assert s.count(literal)==1;s=s.replace(literal,repr('analysis/optimization_20261003_r'+str(parent)))
  if n.startswith('publish_'):
   s=s.replace('139、141、145、146','139、145、146、147').replace('181完整/543冷前缀','238完整/714冷前缀')
  compile(s,str(A/n),'exec');result[n]=s
 assert len(result)==8;return result
'''
 g2=A/'prepare_JointCrossHuberOrder185_round147_sources_v2_20261008.py';originals.append(g2);body=g2.read_text(encoding='utf8');body=body[body.index('def main():'):]
 header+=convert(body)
 products.append(save('prepare_AdaptiveJointCrossHuber242_round148_sources_v1_20261008.py',header))
 storage=importlib.import_module('AdaptiveJointCrossHuber148_storage_v1_20261008');rows=[]
 for path,target in storage.OUTPUTS.items():
  assert path.is_relative_to(ROOT) and target.is_relative_to(Path('E:/赛题五_本机临时/第148轮_20261008')) and not path.exists()
  path.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True,exist_ok=False)
  def literal(p):return "'"+str(p).replace("'","''")+"'"
  r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',"$ErrorActionPreference='Stop'\nNew-Item -ItemType Junction -Path "+literal(path)+' -Target '+literal(target)+' | Out-Null'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
  assert r.returncode==0,r.stderr.decode('utf8',errors='replace');storage.empty(path);rows.append({'access':str(path),'physical_E':str(target)})
 create(A/'AdaptiveJointCrossHuber148_complete_receiver_preparation_v1_20261008.json',{'status':'prepared_all242_scoring_candidate_registry_full_QA59_and_main_receivers_before_actual_prospective_controls',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),proposal,*originals,*products]},
  'E_output_folders':rows,'existing_saved_native_models':35,'expected_quality_cases':242,'QA_version':59,
  'own_native80_and_full238714cold_and_actual147_closure_required_before_quality':True,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
 print('All242 scoring/candidate/full QA59 receiver prototypes and32 generator routes prepared; prospective checks next.',flush=True)
if __name__=='__main__':main()
