"""Execute32 generated joint147 routes before admitting any official quality score."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def module(nodes):return ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]))
def main():
 import prepare_PureRFFHuber128_round149_sources_v2_20261008 as generator
 from PureRFFHuber149_storage_v1_20261008 import OUTPUTS,empty,installed_transfer,EBASE
 from PureRFFHuber_ordered_CDF_v2_20261008 import required,GRAPH_KEY
 from run_PureRFFHuber128_official_comparison_v1_20261008 import best_key,STATUS
 proof_path=A/'PureRFFHuber128_prospective_routes_v2_20261008.json';assert not proof_path.exists()
 plan_path=A/'PureRFFHuber128_round149_plan_v1_20261008.json';plan=read(plan_path)
 assert plan['anchor_rounds']==[145,146,147,148] and plan['fixed_scientific_stage_base_round']==134 and len(plan['new_cases'])==124
 assert plan['final_selection_rule']=='official_S_desc_unique_physical_model_SHA_count_asc_sum_absolute_amplitudes_asc_case_asc'
 for path in OUTPUTS:empty(path)
 paths=generator.source_paths();future={p for p in paths if not p.is_file()}
 allowed={A/n for n in generator.NAMES.values()}|{proof_path,A/'PureRFFHuber128_actual_controls_index_v1_20261008.json',
  A/'PureRFFHuber128_round149_source_admission_v1_20261008.json',A/'PureRFFHuber128_round149_source_preparation_v1_20261008.json',
  A/'PureRFFHuber128_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',A/'PureRFFHuber128_scores_github_v1_20261008/receipt.json',
  A/'actual_PureRFFHuber80_native_calendar_location_v2_20261008.json',A/'actual_PureRFFHuber124_parent134_location_v2_20261008.json'}
 assert future<=allowed,future-allowed
 inputs=[Path(__file__),plan_path,*(p for p in paths if p.is_file()),ROOT/'evaluate.py',ROOT/'后续选模标准.md',
  A/'optimization_20261003_r134/selection.json',ROOT/'candidates/optimization_20261003_r134/verification.json']
 for p in inputs:
  if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
 assert sha(ROOT/'evaluate.py')=='72dc59987e92ba8ae6b506e114dfe8591b5608c9beccd0769d5d1f778f9189c2'
 scorer=A/'run_PureRFFHuber128_official_comparison_v1_20261008.py';tree=ast.parse(scorer.read_text(encoding='utf8'))
 item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets))
 schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
 count_node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='expected_models' for t in n.targets) and 'model_sha' in ast.unparse(n.value))
 counts=[]
 for base,heads in (({'a'},[]),({'a'},['h0']),({'a','b'},['h0','h1']),({'a'},['h0','h1','h2']),({'a','b','c'},['h0','h0','h2']),
  ({'a'},['h0','h1','h2','h3']),({'a','c'},['h0','h1','h2','h3','h4','h5','h6']),({'a','b','c'},['h0','h1','h2','h3','h4','h5','h6'])):
  infos={f'h{i}':{'native_model_sha256':v} for i,v in enumerate(('a','b','c','d','e','f','g'))};ns={'model_sha':base,'components':heads,'infos':infos}
  exec(compile(module([count_node]),str(scorer),'exec'),ns);assert ns['expected_models']==len(base|{infos[h]['native_model_sha256'] for h in heads})
  counts.append({'base_SHA':sorted(base),'heads':heads,'actual_union_models':ns['expected_models']})
 metrics=read(A/'optimization_20261003_r134/selection.json')['winner']['metrics'];base=read(ROOT/'candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']
 assert GRAPH_KEY not in base and 'nonflag_CPU_CrossFamily_complete_parent_CDF' not in base and 'nonflag_CPU_HuberCrossFamily_complete_parent_CDF' not in base
 augmented=deepcopy(base);augmented['prospective_complete_parent_preservation_sentinel']={'nested':[{'values':[0,None,'中文',True]}]}
 outputs={};graphs=[];baselines=[];ties=[];collectors=[];paths_checked=[]
 for parent in plan['anchor_rounds']:
  generated=generator.generate(parent);assert len(generated)==8
  registry=ast.parse(generated['optimize_training_round149.py'])
  previous=next(ast.literal_eval(x.value.right) for x in registry.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PREVIOUS' for a in x.targets))
  declared=next(ast.literal_eval(x.value) for x in registry.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PREVIOUS_NUMBER' for a in x.targets))
  assert previous=='analysis/optimization_20261003_r'+str(parent) and declared==parent
  outputs[str(parent)]={n:hashlib.sha256(s.encode()).hexdigest() for n,s in generated.items()}
  for n,s in generated.items():assert not (A/n).exists();compile(s,str(A/n),'exec')
  name='register_PureRFFHuber128_round149_artifacts_20261008.py';text=generated[name];t=ast.parse(text)
  measured_keys={n.slice.value for n in ast.walk(t) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
  assert measured_keys<=schema,measured_keys-schema
  guard=next(n for n in ast.walk(t) if isinstance(n,ast.Compare) and ast.unparse(n.left)=="pilot['status']");assert guard.comparators[0].value==STATUS
  assert 'from prepare_PureRFFHuber128_round149_sources_v2_20261008 import source_paths' in text
  assert ':03d}_official.json' in text and ':02d}_official.json' not in text
  first=text.index("        if measured['case'] == pilot['best']['case']:");last=text.index('        row = ',first);code=compile('if True:\n'+text[first:last],name,'exec')
  for kind,parent_graph in (('actual134',base),('augmented_complete_parent',augmented)):
   for index,cfg0 in enumerate(plan['new_cases']):
    cfg={'anchor_round':134,'model':'JointCrossHuber_ordered_case'+str(index),'configuration':cfg0,
     'weight':sum(abs(cfg0[n]['amplitude']) for n in ('cross','huber')),'role':'nonflag_valid_2021_onward','universe':'all_current_raw_forecasts'}
    heads=required(cfg0);measured={'case':7,'ordered_native_components':heads,'native_bank_source':'prospective_actual25_saved_states','first2020_identity':True};requested=[]
    def base_read(p):
     assert Path(p)==ROOT/'candidates/optimization_20261003_r134/verification.json';requested.append(str(p));return {'whole_scheme_graph':deepcopy(parent_graph)}
    ns={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':134,'actual_comparison_parent_round':parent},'deepcopy':deepcopy,'ROOT':ROOT,'read':base_read}
    exec(code,ns);graph=ns['graph'];stage=graph.pop(GRAPH_KEY,None);assert graph==parent_graph and len(requested)==1
    if cfg['weight']:
     assert stage['configuration']==cfg0 and stage['ordered_native_component_heads']==heads
     assert stage['position']=='ordered_composite_after_complete_qualified134_parent' and stage['original_complete_parent_round']==134 and stage['first2020_identity']
     assert stage['total_absolute_amplitude']==cfg['weight']
    else:assert stage is None
    graphs.append({'parent':parent,'stage_base':134,'graph_kind':kind,'case':index,'explicit_order':cfg0['order'],'heads':heads,'all_parent_values_preserved_once':True})
  for anchor in plan['anchor_rounds']:
   existing=deepcopy(augmented);existing[GRAPH_KEY]={'existing_qualified_anchor_stage':True};requested=[]
   def anchor_read(p):
    assert Path(p)==ROOT/f'candidates/optimization_20261003_r{anchor}/verification.json';requested.append(str(p));return {'whole_scheme_graph':deepcopy(existing)}
   ns={'cfg':{'anchor_round':anchor,'model':None,'weight':0.},'measured':{'case':7},'pilot':{'best':{'case':8},'actual_scheme_base_round':134},'deepcopy':deepcopy,'ROOT':ROOT,'read':anchor_read}
   exec(code,ns);assert ns['graph']==existing and len(requested)==1
  ns={'cfg':{},'measured':{'case':8},'pilot':{'best':{'case':8}},'actual':{'whole_scheme_graph':augmented},'deepcopy':deepcopy}
  exec(code,ns);assert ns['graph']==augmented and ns['graph'] is not augmented
  body=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
  baseline=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='comparison_baseline' for k in n.targets))
  update=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='selection.update')
  sorting=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='records.sort')
  for delta in (0.,1e-8,-4e-5):
   requested=[];expected=A/f'optimization_20261003_r{parent}/selection.json'
   def expected_read(p):
    assert Path(p)==expected;requested.append(str(p));return {'winner':{'metrics':metrics}}
   ns={'A':A,'ROOT':ROOT,'read':expected_read,'sha':sha,'selection':{},'winner':{'connected_final_score':metrics['final_score']+delta},'records':[],
    'pilot':{'actual_scheme_base_round':134},'selection_source':A/'optimization_20261003_r134/selection.json','GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
   exec(compile(module([baseline,update]),name,'exec'),ns)
   assert len(requested)==1 and ns['selection']['baseline_score']==metrics['final_score'] and ns['selection']['score_gain']==ns['winner']['connected_final_score']-metrics['final_score']
   assert ns['selection']['explicit_comparison_parent_round']==parent and ns['selection']['actual_scheme_base_round']==134
   baselines.append({'parent':parent,'delta':delta,'exact_comparison_parent_read':True})
  for advantage in (0.,1e-8):
   samples=[{'connected_final_score':metrics['final_score']+(advantage if case==4 else 0.),'direct_rank_comparison_configuration':{'weight':w},'original_comparison_case':case,
    'actual_full_conditional_residual_control':{'expected_unique_native_models':m}} for case,w,m in ((0,.0065,18),(1,.001,20),(2,.001,18),(3,0.,18),(4,.0065,22))]
   ns={'records':samples};exec(compile(module([sorting]),name,'exec'),ns);assert samples[0]['original_comparison_case']==(4 if advantage else 3)
   scores=[{'connected_final_score':r['connected_final_score'],'expected_unique_native_models':r['actual_full_conditional_residual_control']['expected_unique_native_models'],'configuration':r['direct_rank_comparison_configuration'],'case':r['original_comparison_case']} for r in samples]
   assert min(scores,key=best_key)['case']==samples[0]['original_comparison_case'];ties.append({'parent':parent,'advantage':advantage,'physical_SHA_then_total_absolute_amplitude':True})
  collector=next(s for n,s in generated.items() if n.startswith('collect_full_'));ct=ast.parse(collector);fn=next(n for n in ct.body if isinstance(n,ast.FunctionDef) and n.name=='collect');forwarded=[]
  ns={'namespace':{'collect':lambda *args:forwarded.append(args)}};exec(compile(module([fn]),'<147_collector>','exec'),ns);ns['collect'](149,60,128);assert forwarded==[(149,60,128)]
  collectors.append({'parent':parent,'contract':[149,60,128]})
  pub=generated['publish_PureRFFHuber128_round149_full_validation_20261008.py']
  assert 'collect(149, 60, 128)' in pub and "namespace['snapshot'](149)" in pub and "== full['scored_records'] == 128" in pub
  assert 'from prepare_PureRFFHuber128_round149_sources_v2_20261008 import source_paths' in pub
  paths_checked.append({'parent':parent,'all128_scored_records_QA60_and_main':True})
 producer=A/'publish_PureRFFHuber128_evidence_v2_20261008.py';pt=ast.parse(producer.read_text(encoding='utf8'))
 expression=next(n.value for n in ast.walk(pt) if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='out' for k in n.targets))
 for phase,consumer in (('controls',scorer),('scores',A/'prepare_PureRFFHuber128_selected_candidate_v1_20261008.py')):
  out=eval(compile(ast.Expression(body=expression),'<147_phase>','eval'),{'__builtins__':{},'A':A,'phase':phase})
  assert out==A/f'PureRFFHuber128_{phase}_github_v1_20261008' and out.name+'/receipt.json' in consumer.read_text(encoding='utf8')
 scope=read(A/'PureRFFHuber149_D_scoring_scope_v1_20261008.json');assert scope['original_cache_functions_and_official_script_unmodified']
 source=A/'PureRFFHuber149_cross_volume_byte_probe_v2.bin';target=EBASE/'cross_volume_byte_probe_v2.bin'
 assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*7)
 import os
 with installed_transfer():os.link(source,target)
 assert source.read_bytes()==target.read_bytes() and sha(source)==sha(target);inputs.append(source)
 pins={str(p):sha(p) for p in dict.fromkeys(inputs)}
 create(proof_path,{'status':'passed_actual32_prospective149_sources_ordered_joint_graphs_baselines_status_paths_SHA_unions_ties_and_cross_volume_bytes',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,'actual_prospective_sources':32,
  'actual_graph_controls':len(graphs),'graph_controls':graphs,'baseline_controls':baselines,'same_score_sort_controls':ties,
  'path_controls':paths_checked,'collector_controls':collectors,'physical_SHA_count_controls':counts,
  'actual_future_anchor_quality_or_inference_not_claimed':True,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
 print('32 prospective sources, '+str(len(graphs))+' ordered graphs,12 baselines,8 ties and4 original collector contracts passed.',flush=True)
if __name__=='__main__':main()
