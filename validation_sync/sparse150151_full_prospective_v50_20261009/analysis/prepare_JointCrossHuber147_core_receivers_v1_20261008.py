"""Prepare complete candidate/sealer/full and storage prototypes for ordered185; admission remains pending."""
from pathlib import Path
import io,tokenize,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def adapt(text):
 text=text.replace('CrossFamilyFine125_round145_full_registration_v2_20261008','__PREVIOUS_ACTUAL146_FULL__')
 text=text.replace('KrylovGram52_round141_full_registration_v18_20261008','__PREVIOUS_ACTUAL146_FULL__')
 text=text.replace('HuberCrossFamilyFine146','JointCrossHuber147').replace('HuberCrossFamilyFine125','JointCrossHuberOrder185')
 text=text.replace('HuberCrossFamilyFine_complete_parent_CDF_v1_20261008','JointCrossHuber_ordered_CDF_v1_20261008')
 text=text.replace('predict_HuberCrossFamilyFine_complete_parent_scheme_v1_20261008','predict_JointCrossHuber_complete_parent_scheme_v1_20261008')
 text=text.replace('HuberCrossFamily_complete_parent_native_replay_verification','JointCrossHuber_complete_parent_native_replay_verification')
 text=text.replace('passed_actual_complete_parent_and_HuberCrossFamily_two_full_native_independent_replays_and_cold80','passed_actual_complete_parent_and_JointCrossHuber_two_full_native_independent_replays_and_cold80')
 text=text.replace('nonflag_CPU_HuberCrossFamily_complete_parent_CDF','nonflag_CPU_joint_Cross_Huber_ordered_complete_parent_CDF')
 for old,new in [('round146','round147'),('full146','full147'),('actual146','actual147'),('prospective146','prospective147'),('_r146','_r147'),('第146轮','第147轮'),('qa_v57','qa_v58'),('qa57','qa58'),('QA57','QA58'),('wave429','wave430')]:text=text.replace(old,new)
 tokens=list(tokenize.generate_tokens(io.StringIO(text).readline))
 text=tokenize.untokenize([t._replace(string={'146':'147','125':'185','57':'58','429':'430','136':'134'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
 for old,new in [('actual125','actual185'),('anchor125','anchor185'),('all125','all185'),('125项','185项')]:text=text.replace(old,new)
 import re
 text=re.sub(r'(JointCrossHuberOrder185_[A-Za-z0-9_]+)_v[23]_20261008',r'\1_v1_20261008',text)
 text=text.replace('actual_registration_v3_20261008','actual_registration_v1_20261008')
 text=text.replace('full_registration_v3_file_IO_20261008','full_registration_v1_file_IO_20261008')
 text=text.replace('(134,139,141,145)','(134,139,141,145,146)').replace('(134, 139, 141, 145)','(134, 139, 141, 145, 146)')
 text=text.replace('__PREVIOUS_ACTUAL146_FULL__','HuberCrossFamilyFine125_round146_full_registration_v2_20261008')
 return text
def save(name,text):
 p=A/name;compile(text,str(p),'exec')
 with p.open('x',encoding='utf8',newline='') as f:f.write(text)
 return p
def main():
 import subprocess
 proposal=A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json';plan=read(proposal)
 assert len(plan['new_cases'])==181 and plan['expected_official_cases']==185
 plan.update(status='frozen185_ordered_joint_parameters_before_quality_complete_receivers_still_require_admission',round=147,QA_version=58,wave=430,
  fixed_scientific_stage_base_round=134,expected_scored_cases=185,existing_saved_native_heads=35,actual_full_OOF_heads=7,
  final_selection_rule='official_S_desc_unique_physical_model_SHA_count_asc_sum_absolute_amplitudes_asc_case_asc',
  comparison_parent_rule='official_S_desc_unique_physical_model_SHA_count_asc_round_asc',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),original_proposal_sha256=sha(proposal))
 create(A/'JointCrossHuberOrder185_round147_plan_v1_20261008.json',plan)
 originals=[];products=[]
 for old,new in [('HuberCrossFamilyFine146_storage_v1_20261008.py','JointCrossHuber147_storage_v1_20261008.py'),
  ('verify_HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.py','verify_JointCrossHuber147_D_scoring_scope_v1_20261008.py'),
  ('seal_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py','seal_JointCrossHuberOrder185_selected_candidate_v1_20261008.py'),
  ('run_HuberCrossFamilyFine125_round146_full_registration_v3_20261008.py','run_JointCrossHuberOrder185_round147_full_registration_v1_20261008.py')]:
  p=A/old;originals.append(p);s=adapt(p.read_text(encoding='utf8'))
  if new.startswith('run_'):s=s.replace("'passed_actual185_sealed_candidate_and_admitted_full147_QA58_sources'","'passed_actual185_sealed_candidate_and_admitted_full147_QA58_sources'")
  products.append(save(new,s))
 source=A/'prepare_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py';originals.append(source);s=adapt(source.read_text(encoding='utf8'))
 s=s.replace('from JointCrossHuber_ordered_CDF_v1_20261008 import transform,mixture,GROUPS','from JointCrossHuber_ordered_CDF_v1_20261008 import transform,required')
 s=s.replace("assert parent_number==134 and 0.<abs(cfg['weight'])<=.00325", "assert parent_number==134 and 0.<abs(cfg['weight'])<=.0065")
 s=s.replace("for head in dict.fromkeys(h for names,sign in GROUPS[cfg['group']] for h in names):", "for head in required(cfg['configuration']):")
 before="        residual=mixture(arrays,cfg['group'],cfg['share'])\n        selected=transform(raw,residual,dates,flags,valid,cfg['weight'])"
 assert s.count(before)==1;s=s.replace(before,"        selected=transform(raw,arrays,dates,flags,valid,cfg['configuration'])")
 begin=s.index("        graph[GRAPH_KEY]={**cfg,");end=s.index('        winner=deepcopy',begin)
 s=s[:begin]+"""        graph[GRAPH_KEY]={**cfg,'configuration':cfg['configuration'],'total_absolute_amplitude':cfg['weight'],
            'universe':'all_current_raw_forecasts','first2020_identity':True,'position':'ordered_composite_after_complete_qualified134_parent',
            'ordered_native_components':components,'teacher_feature':'qualified106_current_forecast_average_rank_over_N',
            'transformation':'explicit_order_two_current_all_universe_inverseCDF_stages_each_with_its_original_saved_residual_heads',
            'original_complete_parent_round':134,'original_complete_parent_graph_preserved':True}
"""+s[end:]
 s=s.replace('actual15_existing_native_and121_fixed_base_controls','actual35_existing_native_and181_fixed_base_controls')
 products.append(save('prepare_JointCrossHuberOrder185_selected_candidate_v1_20261008.py',s))
 # Six E-backed output folders are admitted only while still empty.
 import importlib
 storage=importlib.import_module('JointCrossHuber147_storage_v1_20261008')
 rows=[]
 for path,target in storage.OUTPUTS.items():
  assert path.is_relative_to(ROOT) and target.is_relative_to(Path('E:/赛题五_本机临时/第147轮_20261008'))
  assert not path.exists();path.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True,exist_ok=False)
  def literal(p):return "'"+str(p).replace("'","''")+"'"
  cmd="$ErrorActionPreference='Stop'\nNew-Item -ItemType Junction -Path "+literal(path)+' -Target '+literal(target)+' | Out-Null'
  r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',cmd],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
  assert r.returncode==0,r.stderr.decode('utf8',errors='replace');storage.empty(path);rows.append({'access':str(path),'physical_E':str(target)})
 products.append(A/'run_JointCrossHuberOrder185_official_comparison_v1_20261008.py')
 proof=A/'JointCrossHuber147_core_receiver_preparation_v1_20261008.json'
 create(proof,{'status':'prepared_candidate_sealer_full_and_D_scope_prototypes_with_original_complete_native_replays_and_QA_not_admitted',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),proposal,*originals,*products]},
  'E_output_folders':rows,'models_35_already_existing_not_new_fits':True,'official_cases_planned':185,'QA_version':58,
  'canonical_generator_source_admission_phase_publisher_dispatch_and_full_prospective_controls_still_to_prepare':True,
  'new_official_scores':0,'new_future_inference':0,'test_labels_read':False})
 print('Core147 candidate/sealer/full prototypes and six verified empty E-backed outputs prepared; quality not admitted.',flush=True)
if __name__=='__main__':main()
