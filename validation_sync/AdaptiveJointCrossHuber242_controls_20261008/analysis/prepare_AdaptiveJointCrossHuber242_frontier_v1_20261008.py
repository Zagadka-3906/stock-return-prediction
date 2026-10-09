"""Freeze an expanded Cross share frontier from actual145 scores; prepare controls before quality."""
from pathlib import Path
import sys,time,json,re,io,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def renamed(s):
 # Existing35 audit is reused honestly; its path and actual original proof remain immutable.
 marker='__EXISTING35_ORIGINAL_JOINT__'
 s=s.replace('actual_JointCrossHuber35_existing_native_location_v1_20261008',marker)
 s=s.replace('JointCrossHuberOrder185_round147','AdaptiveJointCrossHuber242_round148')
 s=s.replace('JointCrossHuber181','AdaptiveJointCrossHuber238').replace('JointCrossHuber80','AdaptiveJointCrossHuber80')
 s=s.replace('JointCrossHuber_ordered','AdaptiveJointCrossHuber_ordered')
 s=s.replace('nonflag_CPU_joint_Cross_Huber_ordered_complete_parent_CDF','nonflag_CPU_joint_Cross_Huber_adaptive_complete_parent_CDF')
 s=s.replace(marker,'actual_JointCrossHuber35_existing_native_location_v1_20261008')
 return s
def main():
 pilot=A/'CrossFamilyFine125_official_comparison_v1_20261008/verification.json';q=read(pilot);best=q['best']
 assert len(q['records'])==125 and best['configuration']['group']==4 and best['configuration']['share']==.25 and best['configuration']['weight']==.002
 prior=A/'JointCrossHuberOrder185_round147_proposal_v1_20261008.json';p=read(prior)
 cross=[{'group':4,'share':s,'amplitude':w} for s in (.125,.25,.375,.5) for w in (.0015,.002,.0025)]
 huber=[{'group':4,'share':s,'amplitude':w} for s in (.375,.5,.625) for w in (.001,.0025,.00325)]
 zero={'group':4,'share':.5,'amplitude':0.}
 cases=[{'order':['cross','huber'],'cross':zero,'huber':zero}]
 cases += [{'order':['cross','huber'],'cross':c,'huber':zero} for c in cross]
 cases += [{'order':['cross','huber'],'cross':zero,'huber':h} for h in huber]
 cases += [{'order':order,'cross':c,'huber':h} for order in (['cross','huber'],['huber','cross']) for c in cross for h in huber]
 assert len(cases)==238 and len({json.dumps(c,sort_keys=True) for c in cases})==238
 previous={json.dumps(c,sort_keys=True) for c in p['new_cases']};new=sum(json.dumps(c,sort_keys=True) not in previous for c in cases)
 proposal=A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json'
 sources=[Path(__file__),pilot,prior,A/'CrossFamilyFine_complete_parent_CDF_v1_20261008.py',A/'CrossFamilyFine_complete_parent_native_stage_v1_20261008.py',
  A/'JointCrossHuber_ordered_CDF_v1_20261008.py',A/'JointCrossHuber_ordered_native_stage_v1_20261008.py',ROOT/'evaluate.py',ROOT/'后续选模标准.md']
 create(proposal,{'status':'frozen242_adaptive_joint_proposal_and_controls_only_quality_receivers_not_yet_prepared',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':148,'deadline_local':'2026-10-10T23:59:00+08:00',
  'scientific_stage_base_round':134,'anchor_rounds':[139,145,146,147],'expected_official_cases':242,'new_case_count':238,'new_cases':cases,'heads':p['heads'],
  'graph_key':'nonflag_CPU_joint_Cross_Huber_adaptive_complete_parent_CDF','actual145_all125_training_score_winner':best,
  'actual145_winner_not_claimed_fully_qualified_at_proposal':True,'distinct_cases_outside_frozen147_grid':new,
  'why_uncovered':'Actual145 winner share0.25 amplitude0.002 lies outside frozen147 joint grid; expand share downward to0.125 and pair both orders with Huber.',
  'existing_native_heads':35,'full_OOF_heads':7,'new_native_fits_needed':0,
  'known_134_136_139_145_numeric_and_all8_metric_controls_required':True,
  'final_selection_rule':'official_S_desc_unique_physical_model_SHA_count_asc_sum_absolute_amplitudes_asc_case_asc',
  'required_before_quality':['actual147_full_qualification_and_main_receipt','actual238_full_Pandas_and714cold_controls','own80_native_and80cold_controls',
   'complete148_source_receivers_and32_prospective_routes','original_train_only_mature_mapping_and_original_official_scoring'],
  'required_after_selection':['source_and_parameters_frozen_before_futureX','two_full1599600_reload_independent_CSV_and_cold80_or_exact_qualified_anchor_reuse',
   'all_original_six_view_full_board_QA59_and_main_receipt'],
  'training_grid_selection_bias_uncorrected':True,'new_official_scores':0,'new_future_inference':0,'test_labels_read':False,
  'global_feasible_direction_or_compute_exhaustion_claimed':False,'input_sha256':{str(f):sha(f) for f in sources}})
 products=[]
 cf=save('AdaptiveCrossFamily_complete_parent_CDF_v1_20261008.py',sources[3].read_text(encoding='utf8').replace('share in (.25, .375, .5, .625, .75)','share in (.125, .25, .375, .5)'))
 products.append(cf)
 sn=sources[4].read_text(encoding='utf8').replace('CrossFamilyFine_complete_parent_CDF_v1_20261008','AdaptiveCrossFamily_complete_parent_CDF_v1_20261008').replace('spec[\'share\'] in (.25,.375,.5,.625,.75)',"spec['share'] in (.125,.25,.375,.5)")
 products.append(save('AdaptiveCrossFamily_complete_parent_native_stage_v1_20261008.py',sn))
 sc=renamed(sources[5].read_text(encoding='utf8')).replace('CrossFamilyFine_complete_parent_CDF_v1_20261008','AdaptiveCrossFamily_complete_parent_CDF_v1_20261008')
 begin=sc.index('def check(case):');end=sc.index('def required(case):',begin)
 sc=sc[:begin]+'''def check(case):
 assert case['order'] in (['cross','huber'],['huber','cross'])
 for name in ('cross','huber'):
  spec=case[name];assert spec['group']==4
  assert spec['share'] in ((.125,.25,.375,.5) if name=='cross' else (.375,.5,.625))
  assert spec['amplitude'] in ((0.,.0015,.002,.0025) if name=='cross' else (0.,.001,.0025,.00325))
'''+sc[end:]
 products.append(save('AdaptiveJointCrossHuber_ordered_CDF_v1_20261008.py',sc))
 stage=renamed(sources[6].read_text(encoding='utf8')).replace('CrossFamilyFine_complete_parent_native_stage_v1_20261008','AdaptiveCrossFamily_complete_parent_native_stage_v1_20261008')
 products.append(save('AdaptiveJointCrossHuber_ordered_native_stage_v1_20261008.py',stage))
 originals=[]
 synthetic=A/'verify_JointCrossHuber181_synthetic_controls_v1_20261008.py';originals.append(synthetic);s=renamed(synthetic.read_text(encoding='utf8'))
 for old,new_value in [('181','238'),('543','714'),('81','108')]:
  tokens=list(tokenize.generate_tokens(io.StringIO(s).readline));s=tokenize.untokenize([t._replace(string=new_value) if t.type==tokenize.NUMBER and t.string==old else t for t in tokens])
 s=s.replace('actual181','actual238').replace('and543','and714').replace('all181','all238')
 products.append(save('verify_AdaptiveJointCrossHuber238_synthetic_controls_v1_20261008.py',s))
 native=A/'verify_JointCrossHuber80_native_historical_calendar_v2_20261008.py';originals.append(native);s=renamed(native.read_text(encoding='utf8'))
 s=s.replace("closed('HuberCrossFamilyFine125_round146_full_registration_v2_20261008')","closed('JointCrossHuberOrder185_round147_full_registration_v1_20261008')")
 s=s.replace('AdaptiveJointCrossHuber80_native_historical_calendar_v2_20261008','AdaptiveJointCrossHuber80_native_historical_calendar_v1_20261008').replace('actual_AdaptiveJointCrossHuber80_native_calendar_location_v2_20261008','actual_AdaptiveJointCrossHuber80_native_calendar_location_v1_20261008')
 s=s.replace('CrossFamilyFine_complete_parent_native_stage_v1_20261008','AdaptiveCrossFamily_complete_parent_native_stage_v1_20261008').replace('CrossFamilyFine_complete_parent_CDF_v1_20261008','AdaptiveCrossFamily_complete_parent_CDF_v1_20261008')
 s=s.replace('shares=[(.375,.375),(.5,.5),(.625,.625),(.375,.625),(.625,.375)]','shares=[(.125,.375),(.25,.5),(.375,.625),(.5,.5),(.125,.625)]')
 s=s.replace('((.001,.00325),(.00325,.001))','((.0015,.00325),(.0025,.001))')
 s=s.replace('Path(__file__).parent/\'prepare_JointCrossHuber35_reused_evidence_and_native80_v2_20261008.py\'',"A/'prepare_AdaptiveJointCrossHuber242_frontier_v1_20261008.py'")
 products.append(save('verify_AdaptiveJointCrossHuber80_native_historical_calendar_v1_20261008.py',s))
 full=A/'verify_JointCrossHuber181_full_historical_controls_v1_20261008.py';originals.append(full);s=renamed(full.read_text(encoding='utf8'))
 s=s.replace('AdaptiveJointCrossHuber80_native_historical_calendar_controls_v2_20261008','AdaptiveJointCrossHuber80_native_historical_calendar_controls_v1_20261008').replace('actual_AdaptiveJointCrossHuber80_native_calendar_location_v2_20261008','actual_AdaptiveJointCrossHuber80_native_calendar_location_v1_20261008')
 tokens=list(tokenize.generate_tokens(io.StringIO(s).readline));s=tokenize.untokenize([t._replace(string={'181':'238','543':'714'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
 s=s.replace('actual181','actual238').replace('and543','and714').replace('actual185','actual242').replace('all185','all242').replace('147_freeze','148_freeze')
 s=s.replace('for number in (134,136,139):','for number in (134,136,139,145):')
 s=s.replace("for name in ('cross','huber') for share in (.375,.5,.625)","for name in ('cross','huber') for share in sorted({case[name]['share'] for case in plan['new_cases'] if case[name]['amplitude']})")
 needle="   if anchor is not None:\n";assert s.count(needle)==1
 s=s.replace(needle,"   if case['cross']=={'group':4,'share':.25,'amplitude':.002} and not case['huber']['amplitude']:anchor=145\n"+needle)
 s=s.replace("=={134,136,139}","=={134,136,139,145}")
 products.append(save('verify_AdaptiveJointCrossHuber238_full_historical_controls_v1_20261008.py',s))
 create(A/'AdaptiveJointCrossHuber148_historical_receiver_preparation_v1_20261008.json',{'status':'prepared_expanded_share_codecs_and_238synthetic_80native_238full_control_receivers_before_any148_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in [Path(__file__),proposal,*originals,*products]},
  'actual_source_range_extended_to_Cross_share0_125_requires_new_own_native_controls':True,'actual148_scoring_registry_candidate_and_full_QA_receivers_still_to_prepare':True,
  'new_quality_scores':0,'new_future_inference':0,'new_model_fits':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(f):sha(f) for f in [Path(__file__),proposal,*products,A/'AdaptiveJointCrossHuber148_historical_receiver_preparation_v1_20261008.json']}
 specs=[('AdaptiveJointCrossHuber238_actual_synthetic_controls_v1_20261008','verify_AdaptiveJointCrossHuber238_synthetic_controls_v1_20261008.py'),
  ('AdaptiveJointCrossHuber80_native_historical_calendar_controls_v1_20261008','verify_AdaptiveJointCrossHuber80_native_historical_calendar_v1_20261008.py'),
  ('AdaptiveJointCrossHuber238_actual_full_historical_controls_v1_20261008','verify_AdaptiveJointCrossHuber238_full_historical_controls_v1_20261008.py')]
 rows={n:start(n,d,[],pins) for n,d in specs}
 create(A/'AdaptiveJointCrossHuber148_historical_hidden_launches_v1_20261008.json',{'launches':rows,'input_sha256':pins,'native_and_full_wait_for_actual147_closure':True,'new_quality_scores':0})
 print(json.dumps({'round':148,'planned_cases':242,'different_from147':new,'controls_started_or_queued':{n:r['owned_worker_pid'] for n,r in rows.items()}}),flush=True)
if __name__=='__main__':main()
