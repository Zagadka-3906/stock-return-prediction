"""Prepare own two/three/five-head real controls after148, retaining full zero-Ridge reference verification."""
from pathlib import Path
import sys,time,json,io,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
def adapt(s):
 s=s.replace('JointCrossHuberOrder185_round147_proposal_v1_20261008','PureRFFHuber128_round149_proposal_v1_20261008')
 s=s.replace('JointCrossHuber_ordered_CDF_v1_20261008','PureRFFHuber_ordered_CDF_v2_20261008').replace('JointCrossHuber_ordered_native_stage_v1_20261008','PureRFFHuber_ordered_native_stage_v2_20261008')
 s=s.replace('actual_JointCrossHuber35_existing_native_location_v1_20261008','actual_PureRFFHuber25_existing_native_location_v1_20261008')
 s=s.replace('JointCrossHuber181','PureRFFHuber124').replace('JointCrossHuber80','PureRFFHuber80')
 s=s.replace('actual_PureRFFHuber124_synthetic_location_v1_20261008','actual_PureRFFHuber124_synthetic_location_v2_20261008')
 s=s.replace('PureRFFHuber124_actual_synthetic_controls_v1_20261008','PureRFFHuber124_actual_synthetic_controls_v2_20261008')
 s=s.replace('PureRFFHuber80_native_historical_calendar_controls_v2_20261008','PureRFFHuber80_native_historical_calendar_controls_v1_20261008')
 s=s.replace('PureRFFHuber80_native_historical_calendar_v2_20261008','PureRFFHuber80_native_historical_calendar_v1_20261008').replace('actual_PureRFFHuber80_native_calendar_location_v2_20261008','actual_PureRFFHuber80_native_calendar_location_v1_20261008')
 s=s.replace("existing['actual_saved_model_count']==35","existing['actual_saved_model_count']==25").replace("existing['actual_full_OOF_heads']==7","existing['actual_full_OOF_heads']==5")
 return s
def main():
 audit=A/'actual_PureRFFHuber25_existing_native_location_v1_20261008.json';assert read(Path(read(audit)['output'])/'verification.json')['actual_saved_model_count']==25
 originals=[];products=[]
 source=A/'verify_JointCrossHuber80_native_historical_calendar_v2_20261008.py';originals.append(source);s=adapt(source.read_text(encoding='utf8'))
 s=s.replace("closed('HuberCrossFamilyFine125_round146_full_registration_v2_20261008')","closed('AdaptiveJointCrossHuber242_round148_full_registration_v1_20261008')")
 s=s.replace("sources=[Path(__file__),", "sources=[A/'prepare_PureRFFHuber149_native80_and_full124_v1_20261008.py',A/'PureRFFHuber149_real_control_preparation_v1_20261008.json',A/'PureRFFMean_complete_parent_CDF_v1_20261008.py',A/'PureRFFMean_complete_parent_native_stage_v1_20261008.py',Path(__file__),")
 begin=s.index(' shares=[');end=s.index(' assert len(cases)==20',begin)
 s=s[:begin]+''' zc={'group':4,'share':0.,'amplitude':0.};zh={'group':4,'share':.5,'amplitude':0.}
 settings=[({'group':4,'share':0.,'amplitude':cw},{'group':4,'share':hs,'amplitude':hw}) for hs in (.375,.5,.625) for cw,hw in ((.001,.00325),(.00325,.001))]
 settings += [({'group':4,'share':0.,'amplitude':w},zh) for w in (.001,.00325)]
 settings += [(zc,{'group':4,'share':.5,'amplitude':w}) for w in (.001,.00325)]
 cases=[{'order':order,'cross':c,'huber':h} for order in (['cross','huber'],['huber','cross']) for c,h in settings]
 assert len({json.dumps(c,sort_keys=True) for c in cases})==20
'''+s[end:]
 products.append(save('verify_PureRFFHuber80_native_historical_calendar_v1_20261008.py',s))
 source=A/'verify_JointCrossHuber181_full_historical_controls_v1_20261008.py';originals.append(source);s=adapt(source.read_text(encoding='utf8'))
 tokens=list(tokenize.generate_tokens(io.StringIO(s).readline));s=tokenize.untokenize([t._replace(string={'181':'124','543':'372'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokens])
 s=s.replace('actual181','actual124').replace('and543','and372').replace('actual185','actual128').replace('all185','all128').replace('147_freeze','149_freeze').replace('existing35_saved','existing25_saved')
 s=s.replace('for number in (134,136,139):','for number in (134,):').replace('=={134,136,139}','=={134}')
 s=s.replace("for name in ('cross','huber') for share in (.375,.5,.625)","for name in ('cross','huber') for share in sorted({case[name]['share'] for case in plan['new_cases'] if case[name]['amplitude']})")
 s=s.replace(" import PureRFFHuber_ordered_CDF_v2_20261008 as codec\n", " import PureRFFHuber_ordered_CDF_v2_20261008 as codec\n import CrossFamilyFine_complete_parent_CDF_v1_20261008 as zero_ridge_reference\n")
 needle=' pins={str(p):sha(p) for p in dict.fromkeys(sources)};OUT.mkdir(exist_ok=False)';assert s.count(needle)==1
 s=s.replace(needle," reference_plan=read(A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json');reference_paths={h:Path(reference_plan['heads'][h]['oof']) for h in ('ridge_l001','ridge_l025')}\n sources += [Path(zero_ridge_reference.__file__),A/'AdaptiveJointCrossHuber242_round148_proposal_v1_20261008.json',*reference_paths.values()]\n"+needle)
 needle="  raw={h:np.load(r['oof'],mmap_mode='r') for h,r in plan['heads'].items()};assert all(x.dtype==np.float64 and x.shape==base.shape for x in raw.values())\n";assert s.count(needle)==1
 s=s.replace(needle,needle+"  reference_raw={**raw,**{h:np.load(p,mmap_mode='r') for h,p in reference_paths.items()}}\n  reference_residual=zero_ridge_reference.independent_mixture(reference_raw,4,0.)\n")
 needle='   exact(value[preserved],np.asarray(base)[preserved])\n';assert s.count(needle)==1
 s=s.replace(needle,needle+'''   reference=np.array(base,dtype=np.float64,copy=True)
   for stage in case['order']:
    cfg=case[stage]
    if not cfg['amplitude']:continue
    module=zero_ridge_reference if stage=='cross' else codec.huber
    residual=reference_residual if stage=='cross' else independent[('huber',cfg['share'])]
    reference=module.pandas_oracle(reference,residual,dates,flags,valid,cfg['amplitude'])
   exact(value,reference);del reference
''')
 s=s.replace("'existing25_saved_native_models_reused_not_new_fits':True", "'actual124_full_zero_Ridge_reference_forecast_bits_equal':True,'existing25_saved_native_models_reused_not_new_fits':True")
 products.append(save('verify_PureRFFHuber124_full_historical_controls_v1_20261008.py',s))
 meta=A/'PureRFFHuber149_real_control_preparation_v1_20261008.json'
 create(meta,{'status':'prepared_own80_native_calendar_and124_full372cold_with_zero_Ridge_reference_controls_after148_closure',
  'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),audit,*originals,*products]},
  'native_cases_include_Cross_only_Huber_only_and_both_in_both_orders':True,'actual149_quality_receivers_and_historical_graph_duplicate_audit_still_pending':True,
  'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 pins={str(p):sha(p) for p in [Path(__file__),meta,*products,A/'PureRFFHuber128_round149_proposal_v1_20261008.json']}
 n=start('PureRFFHuber80_native_historical_calendar_controls_v1_20261008',products[0].name,[],pins)
 f=start('PureRFFHuber124_actual_full_historical_controls_v1_20261008',products[1].name,[],pins)
 create(A/'PureRFFHuber149_real_control_hidden_launches_v1_20261008.json',{'native':n,'full':f,'input_sha256':pins,'actual80_and_full124_not_yet_performed':True})
 print(json.dumps({'native80':n['owned_worker_pid'],'full124':f['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
