"""Prepare128 official receivers and QA60 for the frozen five-head frontier; real controls and duplicate audit remain mandatory."""
from pathlib import Path
import ast,io,tokenize,re,sys,time,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def convert(s):
 s=s.replace('JointCrossHuberOrder185_round147_full_registration_v1_20261008','__ACTUAL148_FULL__')
 s=s.replace('actual_JointCrossHuber35_existing_native_location_v1_20261008.json','actual_PureRFFHuber25_existing_native_location_v1_20261008.json')
 s=s.replace('AdaptiveJointCrossHuber_ordered','PureRFFHuber_ordered').replace('AdaptiveCrossFamily_complete_parent','PureRFFMean_complete_parent')
 s=s.replace('AdaptiveJointCrossHuber242','PureRFFHuber128').replace('AdaptiveJointCrossHuber238','PureRFFHuber124').replace('AdaptiveJointCrossHuber80','PureRFFHuber80').replace('AdaptiveJointCrossHuber148','PureRFFHuber149')
 s=s.replace('predict_AdaptiveJointCrossHuber','predict_PureRFFHuber').replace('_AdaptiveJointCrossHuber_teacher','_PureRFFHuber_teacher').replace('AdaptiveJointCrossHuber_complete_parent','PureRFFHuber_complete_parent')
 s=s.replace('nonflag_CPU_joint_Cross_Huber_adaptive_complete_parent_CDF','nonflag_CPU_PureRFF_Huber_ordered_complete_parent_CDF')
 for before,after in [('round148','round149'),('full148','full149'),('actual148','actual149'),('prospective148','prospective149'),('_r148','_r149'),('第148轮','第149轮'),('qa_v59','qa_v60'),('qa59','qa60'),('QA59','QA60'),('wave431','wave432')]:s=s.replace(before,after)
 tokens=list(tokenize.generate_tokens(io.StringIO(s).readline))
 s=tokenize.untokenize([t._replace(string={'148':'149','242':'128','238':'124','714':'372','108':'54','35':'25','59':'60','431':'432'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
 for before,after in [('242','128'),('238','124'),('714','372'),('saved_states35','saved_states25'),('actual35','actual25'),('states35','states25'),('35_states','25_states'),('25_states238','25_states124'),('known_134_136_139_all8','known_134_all8')]:s=s.replace(before,after)
 s=s.replace('[139,145,146,147]','[145,146,147,148]').replace('(139,145,146,147)','(145,146,147,148)').replace('(134,139,145,146,147)','(134,145,146,147,148)')
 s=s.replace('=={134,136,139,145}','=={134}').replace('==7','==5').replace(' == 7',' == 5').replace('in (4,3,7)','in (2,3,5)').replace('in (4, 3, 7)','in (2, 3, 5)')
 s=s.replace("kind=row['state_kind']","kind=row.get('native_stage_state_kind',row['state_kind']);storage_kind=row['state_kind']").replace("info['independent_'+kind+","info['independent_'+storage_kind+")
 s=s.replace('actual_PureRFFHuber124_synthetic_location_v1','actual_PureRFFHuber124_synthetic_location_v2')
 s=re.sub(r'(PureRFFHuber(?:128|149)_[A-Za-z0-9_]+)_v[234]_20261008',r'\1_v1_20261008',s)
 s=s.replace('actual_registration_v2_20261008','actual_registration_v1_20261008').replace('full_registration_v2_file_IO','full_registration_v1_file_IO')
 s=s.replace('PureRFFHuber149_complete_receiver_preparation_v1','Pure149_complete_receiver_preparation_v1')
 return s.replace('__ACTUAL148_FULL__','AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008')

def main():
 import importlib
 proposal=A/'PureRFFHuber128_round149_proposal_v1_20261008.json';plan=read(proposal)
 assert len(plan['new_cases'])==124 and len(plan['heads'])==5 and plan['anchor_rounds']==[145,146,147,148]
 plan.update(round=149,QA_version=60,wave=432,fixed_scientific_stage_base_round=134,expected_scored_cases=128,
  existing_saved_native_heads=25,actual_full_OOF_heads=5,status='frozen128_pure_RFF_Huber_ordered_frontier_before_official_quality',original_proposal_sha256=sha(proposal))
 create(A/'PureRFFHuber128_round149_plan_v1_20261008.json',plan)
 pairs=[('AdaptiveJointCrossHuber148_storage_v1_20261008.py','PureRFFHuber149_storage_v1_20261008.py'),('verify_AdaptiveJointCrossHuber148_D_scoring_scope_v1_20261008.py','verify_PureRFFHuber149_D_scoring_scope_v1_20261008.py'),('run_AdaptiveJointCrossHuber242_official_comparison_v1_20261008.py','run_PureRFFHuber128_official_comparison_v1_20261008.py'),('prepare_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py','prepare_PureRFFHuber128_selected_candidate_v1_20261008.py'),('seal_AdaptiveJointCrossHuber242_selected_candidate_v1_20261008.py','seal_PureRFFHuber128_selected_candidate_v1_20261008.py'),('run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py','run_PureRFFHuber128_round149_full_registration_v1_20261008.py'),('publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py','publish_PureRFFHuber128_evidence_v1_20261008.py'),('verify_AdaptiveJointCrossHuber242_round148_sources_v2_20261008.py','verify_PureRFFHuber128_round149_sources_v1_20261008.py'),('verify_AdaptiveJointCrossHuber242_prospective_routes_v2_20261008.py','verify_PureRFFHuber128_prospective_routes_v1_20261008.py'),('dispatch_AdaptiveJointCrossHuber148_complete_pipeline_v2_20261008.py','dispatch_PureRFFHuber149_complete_pipeline_v1_20261008.py'),('predict_AdaptiveJointCrossHuber_complete_parent_scheme_v1_20261008.py','predict_PureRFFHuber_complete_parent_scheme_v1_20261008.py')]
 originals=[];products=[]
 for old,new in pairs:
  p=A/old;originals.append(p);s=convert(p.read_text(encoding='utf8'))
  if old.startswith('verify_AdaptiveJointCrossHuber242_round'):
   # Native80 and full124 establish the actual decoder/forecast recipe. This audit is only saved-state provenance.
   s=s.replace('not bank[\'new_native_replay_claimed\']','not bank[\'new_native_replay_claimed\']')
   s=s.replace(" for name in (", " for name in ('Pure149_prior_complete_forecast_duplicate_audit_v1_20261008',")
  if old.startswith('run_AdaptiveJointCrossHuber242_official'):
   s=s.replace(" for n in (", " for n in ('Pure149_prior_complete_forecast_duplicate_audit_v1_20261008',",1)
   s=s.replace('existing_saved_native_heads\':35','existing_saved_native_heads\':25')
  if 'prospective_routes' in old:
   s=s.replace("'collect(148, 59, 242)'","'collect(149, 60, 128)'").replace("namespace['snapshot'](148)","namespace['snapshot'](149)")
   s=s.replace("'collect(148, 59, 128)'","'collect(149, 60, 128)'")
  products.append(save(new,s))
 import prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008 as prior
 names={k:convert(v) for k,v in prior.NAMES.items()}
 own=[p.name for p in products]+[Path(__file__).name,'Pure149_complete_receiver_preparation_v1_20261008.json',proposal.name,'PureRFFHuber128_round149_plan_v1_20261008.json',
  'PureRFFMean_complete_parent_CDF_v1_20261008.py','PureRFFMean_complete_parent_native_stage_v1_20261008.py','PureRFFHuber_ordered_CDF_v2_20261008.py','PureRFFHuber_ordered_native_stage_v2_20261008.py',
  'prepare_PureRFFHuber128_frontier_v1_20261008.py','verify_PureRFFHuber124_synthetic_controls_v2_20261008.py','verify_PureRFFHuber25_existing_native_evidence_v1_20261008.py',
  'prepare_Pure149_correct_native_dispatch_v2_20261008.py','Pure149_correct_native_dispatch_preparation_v2_20261008.json','verify_PureRFFHuber80_native_historical_calendar_v2_20261008.py','verify_PureRFFHuber124_full_historical_controls_v2_20261008.py',
  'actual_PureRFFHuber25_existing_native_location_v1_20261008.json','actual_PureRFFHuber124_synthetic_location_v2_20261008.json','actual_PureRFFHuber80_native_calendar_location_v2_20261008.json','actual_PureRFFHuber124_parent134_location_v2_20261008.json',
  'PureRFFHuber149_D_scoring_scope_v1_20261008.json','PureRFFHuber128_prospective_routes_v1_20261008.json','PureRFFHuber128_actual_controls_index_v1_20261008.json','PureRFFHuber128_round149_source_admission_v1_20261008.json','PureRFFHuber128_round149_source_preparation_v1_20261008.json',
  'PureRFFHuber128_selected_release_v1_20261008/selected_candidate_ready_for_registration.json','PureRFFHuber128_scores_github_v1_20261008/receipt.json']
 inherited=[p.relative_to(A).as_posix() for p in prior.source_paths() if p.is_file() and p.suffix=='.py']
 header='''from pathlib import Path
import ast,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_Pure149_complete_receivers_v1_20261008 import convert
import prepare_AdaptiveJointCrossHuber242_round148_sources_v2_20261008 as original
'''+f'NAMES={names!r}\nSOURCE_NAMES={list(dict.fromkeys([*own,*inherited]))!r}\n'+'''
def source_paths():return list(dict.fromkeys([Path(__file__),*(A/n for n in SOURCE_NAMES),*(A/n for n in NAMES.values())]))
def generate(parent):
 assert parent in (145,146,147,148)
 result={convert(n):convert(s) for n,s in original.generate(145).items()}
 for n,s in result.items():
  s=s.replace('prepare_PureRFFHuber128_round149_sources_v2_20261008','prepare_PureRFFHuber128_round149_sources_v1_20261008')
  s=s.replace('_r145/',f'_r{parent}/').replace('PREVIOUS_NUMBER = 145',f'PREVIOUS_NUMBER = {parent}')
  s=s.replace("'explicit_parent_round': 145",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=145',f'explicit_comparison_parent_round={parent}')
  if n=='optimize_training_round149.py':
   tree=ast.parse(s);assignment=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREVIOUS' for t in x.targets))
   literal=ast.get_source_segment(s,assignment.value.right);assert s.count(literal)==1;s=s.replace(literal,repr('analysis/optimization_20261003_r'+str(parent)))
  compile(s,str(A/n),'exec');result[n]=s
 assert len(result)==8;return result
'''
 body=Path(prior.original.__file__).read_text(encoding='utf8');body=body[body.index('def main():'):]
 header+=convert(body).replace('prepare_PureRFFHuber128_round149_sources_v2_20261008','prepare_PureRFFHuber128_round149_sources_v1_20261008')
 products.append(save('prepare_PureRFFHuber128_round149_sources_v1_20261008.py',header))
 storage=importlib.import_module('PureRFFHuber149_storage_v1_20261008');rows=[]
 for access,target in storage.OUTPUTS.items():
  assert access.is_relative_to(ROOT) and target.is_relative_to(Path('E:/赛题五_本机临时/第149轮_20261008')) and not access.exists() and not target.exists()
  target.mkdir(parents=True);q=lambda p:"'"+str(p).replace("'","''")+"'"
  subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command','New-Item -ItemType Junction -Path '+q(access)+' -Target '+q(target)+' | Out-Null'],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  storage.empty(access);rows.append({'access':str(access),'physical_E':str(target)})
 create(A/'Pure149_complete_receiver_preparation_v1_20261008.json',{'status':'prepared128_scoring_candidate_full_QA60_and_main_receivers_not_yet_prospectively_admitted','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),proposal,*originals,*products]},'E_outputs':rows,'existing_saved_native_models':25,'own124_full372_cold80_native_and_prior_duplicate_audit_required':True,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
 print('128 receiver prototypes prepared; prospective and duplicate audits must pass before actual quality.',flush=True)
if __name__=='__main__':main()
