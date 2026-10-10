"""Prepare unadmitted152 prototypes with explicit counts, parent routing and E outputs."""
from pathlib import Path
import io,re,sys,time,tokenize,importlib,subprocess,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
NATIVE_STATUS='passed_actual_complete148_and_sparse_two_full_native_independent_replays_and_cold80'
def route(s):
 replacements={
  'PureRFFHuber128_round149_full_registration_v1_20261008':'RFFSparse59_round151_full_registration_v1_20261009',
  'HuberSparse150_storage_v1_20261008':'SparseAfter148152_storage_v1_20261009',
  'predict_HuberSparse_complete_parent_scheme_v1_20261008':'predict_SparseAfter148_complete_parent_scheme_v1_20261009',
  'HuberSparse_complete_parent_CDF_v1_20261008':'SparseAfter148_complete_parent_CDF_v1_20261009',
  'HuberSparse_complete_parent_native_stage_v1_20261008':'SparseAfter148_complete_parent_native_stage_v1_20261009',
  'prepare_HuberSparse59_round150_sources_v2_20261009':'prepare_SparseAfter14829_round152_sources_v1_20261009',
  'prepare_HuberSparse59_round150_sources_v1_20261008':'prepare_SparseAfter14829_round152_sources_v1_20261009',
  'passed_actual_complete_parent_and_HuberSparse_two_full_native_independent_replays_and_cold80':NATIVE_STATUS,
  'passed_actual55_HuberSparse_full_training_CDF_and165_cold_controls_with_exact134_identity':'passed_actual25_SparseAfter148_full_training_CDF_and75_cold_controls_with_exact148_identity',
  'actual_HuberSparse55_parent134_location_v1_20261008':'actual_SparseAfter14825_parent148_location_v1_20261009',
  '第150轮_20261008':'第152轮_20261009',
  'lossless_ranking_display_qa_v61_20261007':'lossless_ranking_display_qa_v63_20261009',
  'qa_v{qa_version}_20261007':'qa_v{qa_version}_20261009',
  'main_publisher_v8_20261008':'main_publisher_v9_20261009'}
 # Replace all original literals once; a newly produced148 is never rerouted to150.
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)))
 s=pattern.sub(lambda m:replacements[m.group()],s)
 parent_paths={134:148,146:148,147:149,148:150,149:151}
 s=re.sub(r'(_r|round)(134|146|147|148|149)(?=[/_.\s\x27\x22])',lambda m:m[1]+str(parent_paths[int(m[2])]),s)
 s=s.replace('HuberSparse59','SparseAfter14829').replace('HuberSparse150','SparseAfter148152').replace('HuberSparse','SparseAfter148')
 for k,v in [('round150','round152'),('full150','full152'),('actual150','actual152'),('_r150','_r152'),
  ('第150轮','第152轮'),('qa61','qa63'),('QA61','QA63'),('wave433','wave435')]:s=s.replace(k,v)
 s=re.sub(r'(SparseAfter148[A-Za-z0-9_/{}.-]*?)_v[12]_2026100[89]',r'\1_v1_20261009',s)
 s=re.sub(r'(SparseAfter148[A-Za-z0-9_/{}.-]*?)_20261008',r'\1_20261009',s)
 s=s.replace('round152_qa63_20261007','round152_qa63_20261009')
 nums={'134':'148','146':'148','147':'149','148':'150','149':'151','150':'152',
  '59':'29','55':'25','54':'24','165':'75','20':'10','61':'63','433':'435'}
 tokens=list(tokenize.generate_tokens(io.StringIO(s).readline))
 s=tokenize.untokenize([t._replace(string=nums.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
 for k,v in [('in (3,4)','in (1,2)'),('in (3, 4)','in (1, 2)'),("len(plan['heads'])==4","len(plan['heads'])==2"),
  ('actual59','actual29'),('all59','all29'),('anchor59','anchor29'),('59项','29项'),
  ('full150_QA61','full152_QA63')]:s=s.replace(k,v)
 return s

def main():
 proposal=A/'SparseAfter14829_round152_proposal_v1_20261009.json';original=read(proposal)
 assert len(original['new_cases'])==25 and original['new_cases'][0]['amplitude']==0.
 plan={**original,'new_cases':original['new_cases'][1:],'original_proposal_sha256':sha(proposal),
  'status':'frozen29_core_receiver_drafts_before_any_quality_source_admission','round':152,'QA_version':63,'wave':435,
  'expected_scored_cases':29,'existing_saved_native_heads':10,'actual_full_OOF_heads':2,
  'graph_key':'nonflag_CPU_SparseAfter148_complete_parent_CDF'}
 planpath=A/'SparseAfter14829_round152_plan_v1_20261009.json';assert not planpath.exists()
 pairs=[('HuberSparse150_storage_v1_20261008.py','SparseAfter148152_storage_v1_20261009.py'),
  ('verify_HuberSparse150_D_scoring_scope_v1_20261008.py','verify_SparseAfter148152_D_scoring_scope_v1_20261009.py'),
  ('run_HuberSparse59_official_comparison_v2_20261009.py','run_SparseAfter14829_official_comparison_v1_20261009.py'),
  ('prepare_HuberSparse59_selected_candidate_v2_20261009.py','prepare_SparseAfter14829_selected_candidate_v1_20261009.py'),
  ('seal_HuberSparse59_selected_candidate_v2_20261009.py','seal_SparseAfter14829_selected_candidate_v1_20261009.py'),
  ('run_HuberSparse59_round150_full_registration_v2_20261009.py','run_SparseAfter14829_round152_full_registration_v1_20261009.py')]
 transformed=[];inputs=[Path(__file__),proposal]
 for old,new in pairs:
  p=A/old;inputs.append(p);s=route(p.read_text(encoding='utf8'))
  # The current152 predictor preserves the entire148 parent and reports this exact status.
  if old.startswith('seal_'):
   assert NATIVE_STATUS in s
  compile(s,str(A/new),'exec');ast.parse(s);transformed.append((A/new,s))
 assert all(not p.exists() for p,_ in transformed)
 for p,s in transformed:
  with p.open('x',encoding='utf8') as f:f.write(s)
  inputs.append(p)
 create(planpath,plan);inputs.append(planpath)
 storage=importlib.import_module('SparseAfter148152_storage_v1_20261009')
 base=Path('E:/赛题五_本机临时/第152轮_20261009');folders=[]
 assert len(storage.OUTPUTS)==6
 for access,target in storage.OUTPUTS.items():
  assert access.is_relative_to(ROOT) and target.is_relative_to(base),(access,target)
  assert not access.exists() and not target.exists(),(access,target)
 for access,target in storage.OUTPUTS.items():
  access.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True)
  q=lambda p:"'"+str(p).replace("'","''")+"'"
  r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',
   "New-Item -ItemType Junction -Path "+q(access)+' -Target '+q(target)+' | Out-Null'],
   capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
  assert r.returncode==0,r.stderr
  storage.empty(access);folders.append({'access':str(access),'physical_E':str(target)})
 # Every executable152 prediction entry must resolve before a future-feature worker can be admitted.
 candidate=dict(transformed)[A/'prepare_SparseAfter14829_selected_candidate_v1_20261009.py']
 assert 'from predict_SparseAfter148_complete_parent_scheme_v1_20261009 import predict' in candidate
 assert (A/'predict_SparseAfter148_complete_parent_scheme_v1_20261009.py').is_file()
 assert "assert parent_number==148" in candidate
 create(A/'SparseAfter148152_core_draft_preparation_v1_20261009.json',{
  'status':'prepared_six152_core_drafts_and6_empty_E_outputs_not_admitted_or_scored',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},
  'stage_base_round':148,'anchor_rounds':[148,149,150,151],'quality_cases':29,'QA_version':63,'wave':435,
  'physical_component_guards_allow1_or2':True,'native_kind_and_linear_storage_kind_separate':True,
  'current152_predictor_entry_exists_and_complete148_native_stage_status_exact':True,
  'E_outputs':folders,'complete_prospective_32_routes_and_duplicate_bindings_and_admission_still_required':True,
  'new_native_fits':0,'new_official_scores':0,'new_future_inference':0,'test_labels_read':False})
 print({'core_drafts':6,'empty_E_outputs':6,'actual_quality_admitted':False},flush=True)
if __name__=='__main__':main()
