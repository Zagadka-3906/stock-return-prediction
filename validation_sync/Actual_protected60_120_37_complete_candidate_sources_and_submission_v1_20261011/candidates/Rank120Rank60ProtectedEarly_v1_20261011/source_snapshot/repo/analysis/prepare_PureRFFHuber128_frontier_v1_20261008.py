"""Freeze a lower physical-model frontier and execute small controls; no quality or native inference claimed."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def main():
 source=A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json';prior=read(source)
 receipt=A/'github_validation_sync_main_20261005/round145_receipt.json';r=read(receipt);assert r['status']=='pushed_and_remote_head_verified'
 cross=[{'group':4,'share':0.,'amplitude':w} for w in (.001,.0015,.002,.0025,.003,.00325)]
 huber=[{'group':4,'share':s,'amplitude':w} for s in (.375,.5,.625) for w in (.001,.0025,.00325)]
 zc={'group':4,'share':0.,'amplitude':0.};zh={'group':4,'share':.5,'amplitude':0.}
 cases=[{'order':['cross','huber'],'cross':zc,'huber':zh}]
 cases += [{'order':['cross','huber'],'cross':c,'huber':zh} for c in cross]
 cases += [{'order':['cross','huber'],'cross':zc,'huber':h} for h in huber]
 cases += [{'order':order,'cross':c,'huber':h} for order in (['cross','huber'],['huber','cross']) for c in cross for h in huber]
 assert len(cases)==124 and len({json.dumps(c,sort_keys=True) for c in cases})==124
 heads={h:prior['heads'][h] for h in ('rff_g00625','rff_g0125','huber_d010','huber_d025','bayes_diagonal')}
 pointer=A/'actual_JointCrossHuber35_existing_native_location_v1_20261008.json';bank_path=Path(read(pointer)['output'])/'verification.json';bank=read(bank_path)
 relevant=[row for row in bank['records'] if row['head'] in heads];assert len(relevant)==25
 proposal=A/'PureRFFHuber128_round149_proposal_v1_20261008.json'
 originals=[source,receipt,pointer,bank_path,A/'CrossFamilyFine_complete_parent_native_stage_v1_20261008.py',A/'JointCrossHuber_ordered_CDF_v1_20261008.py',
  A/'JointCrossHuber_ordered_native_stage_v1_20261008.py',A/'verify_JointCrossHuber181_synthetic_controls_v1_20261008.py']
 create(proposal,{'status':'frozen128_lower_physical_model_proposal_and_synthetic_controls_only_not_admitted_for_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':149,'deadline_local':'2026-10-10T23:59:00+08:00',
  'scientific_stage_base_round':134,'anchor_rounds':[145,146,147,148],'expected_official_cases':128,'new_case_count':124,'new_cases':cases,'heads':heads,
  'graph_key':'nonflag_CPU_PureRFF_Huber_ordered_complete_parent_CDF','existing_native_heads':25,'full_OOF_heads':5,
  'actual145_qualified_score':r['official_score'],'why_this_frontier':'145 winner prefers RFF-dominant mixture; zero Ridge share may permit two fewer physical saved models.',
  'each_case_required_heads':{'pure_RFF_only':2,'Huber_only':3,'both_stages':5,'zero_identity':0},
  'zero_coefficient_Ridge_heads_not_used_or_claimed_as_predicted_models':True,'new_native_fits_needed':0,
  'all_prior_qualified_complete_graph_duplicate_audit_required_before_quality':True,
  'required_before_quality':['actual148_full_and_main_closure','own25_mature_saved_state_rehashes_not_new_replay_claims',
   'actual124_full_and372cold_independent_Pandas_controls','own_historical_native_reload_independent_and_final2025_multiyear_controls',
   'pure_mean_and_reference_zero_Ridge_weight_full_forecast_bit_equivalence','all128_scoring_freeze_candidate_registry_QA60_main_receivers_prospectively_verified'],
  'required_after_selection':['freeze_models_parameters_sources_mapping_before_future_X','two_full1599600_native_independent_reload_CSV_and_cold80_or_exact_qualified_anchor_reuse',
   'all_original_six_view_full_board_QA60_and_actual_main_receipt'],
  'final_selection_rule':'official_S_desc_unique_physical_model_SHA_count_asc_sum_absolute_amplitudes_asc_case_asc',
  'training_grid_selection_bias_uncorrected':True,'new_quality_scores':0,'new_inference':0,'test_labels_read':False,'global_exhaustion_claimed':False,
  'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals]}})
 codec='''"""Pure mean of two saved RFF heads; all CDF arithmetic retains the original current-day complete universe."""
import numpy as np
from CrossFamilyFine_complete_parent_CDF_v1_20261008 import prepare,selected,apply_prepared,transform,pandas_oracle
HEADS=('rff_g00625','rff_g0125')
GROUPS=((),(),(),(),((HEADS,1.),))
def mixture(raw,group,share):
 assert group==4 and share==0.
 value=np.array(raw[HEADS[0]],dtype=np.float64,copy=True)
 value+=np.asarray(raw[HEADS[1]],dtype=np.float64);value/=2.
 assert np.isfinite(value).all();return value
def independent_mixture(raw,group,share):
 assert group==4 and share==0.
 return np.divide(np.add(np.asarray(raw[HEADS[0]],dtype=np.float64),np.asarray(raw[HEADS[1]],dtype=np.float64)),2.)
'''
 products=[save('PureRFFMean_complete_parent_CDF_v1_20261008.py',codec)]
 native=originals[4].read_text(encoding='utf8').replace('CrossFamilyFine_complete_parent_CDF_v1_20261008','PureRFFMean_complete_parent_CDF_v1_20261008')
 native=native.replace("spec['share'] in (.25,.375,.5,.625,.75)","spec['share']==0.").replace('nonflag_CPU_CrossFamily_complete_parent_CDF','nonflag_CPU_PureRFFMean_complete_parent_CDF')
 products.append(save('PureRFFMean_complete_parent_native_stage_v1_20261008.py',native))
 joint=originals[5].read_text(encoding='utf8').replace('CrossFamilyFine_complete_parent_CDF_v1_20261008','PureRFFMean_complete_parent_CDF_v1_20261008').replace('nonflag_CPU_joint_Cross_Huber_ordered_complete_parent_CDF','nonflag_CPU_PureRFF_Huber_ordered_complete_parent_CDF')
 begin=joint.index('def check(case):');end=joint.index('def required(case):',begin)
 joint=joint[:begin]+'''def check(case):
 assert case['order'] in (['cross','huber'],['huber','cross'])
 for name in ('cross','huber'):
  spec=case[name];assert spec['group']==4
  assert spec['share']==0. if name=='cross' else spec['share'] in (.375,.5,.625)
  assert spec['amplitude'] in ((0.,.001,.0015,.002,.0025,.003,.00325) if name=='cross' else (0.,.001,.0025,.00325))
'''+joint[end:]
 products.append(save('PureRFFHuber_ordered_CDF_v1_20261008.py',joint))
 stage=originals[6].read_text(encoding='utf8').replace('JointCrossHuber_ordered_CDF_v1_20261008','PureRFFHuber_ordered_CDF_v1_20261008')
 # Match the full import statement so the Huber module name cannot be changed accidentally.
 stage=stage.replace('import CrossFamilyFine_complete_parent_native_stage_v1_20261008 as cross','import PureRFFMean_complete_parent_native_stage_v1_20261008 as cross')
 products.append(save('PureRFFHuber_ordered_native_stage_v1_20261008.py',stage))
 synthetic=originals[7].read_text(encoding='utf8').replace('JointCrossHuber_ordered_CDF_v1_20261008','PureRFFHuber_ordered_CDF_v1_20261008')
 synthetic=synthetic.replace('JointCrossHuberOrder185_round147_proposal_v1_20261008','PureRFFHuber128_round149_proposal_v1_20261008')
 synthetic=synthetic.replace('JointCrossHuber181_synthetic_v1_20261008','PureRFFHuber124_synthetic_v1_20261008').replace('actual_JointCrossHuber181_synthetic_location_v1_20261008','actual_PureRFFHuber124_synthetic_location_v1_20261008')
 synthetic=synthetic.replace('==181','==124').replace('==7','==5').replace('==81','==54')
 synthetic=synthetic.replace('(7 if all(case[n]', '(5 if all(case[n]').replace('(4 if case[\'cross\']',"(2 if case['cross']")
 synthetic=synthetic.replace("'actual_cold_cases':543","'actual_cold_cases':372").replace("'actual_double_stage_order_pairs':81","'actual_double_stage_order_pairs':54").replace("'cold_cases':543","'cold_cases':372")
 synthetic=synthetic.replace('actual181','actual124').replace('and543','and372').replace('all181','all124').replace('declared_cases\':181',"declared_cases':124")
 products.append(save('verify_PureRFFHuber124_synthetic_controls_v1_20261008.py',synthetic))
 meta=A/'PureRFFHuber149_mathematical_receiver_preparation_v1_20261008.json'
 create(meta,{'status':'prepared_five_head25_state_reduced_physical_model_codecs_and124_synthetic_controls_before_quality',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),proposal,*originals,*products]},
  'own_full_native_calendar_scoring_candidate_registry_and_QA_receivers_still_pending':True,'new_quality_scores':0,'new_model_fits':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p) for p in [Path(__file__),proposal,meta,*products]}
 row=start('PureRFFHuber124_actual_synthetic_controls_v1_20261008',products[-1].name,[],pins)
 create(A/'PureRFFHuber149_synthetic_hidden_launch_v1_20261008.json',{'launch':row,'input_sha256':pins,'new_quality_scores':0});print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
