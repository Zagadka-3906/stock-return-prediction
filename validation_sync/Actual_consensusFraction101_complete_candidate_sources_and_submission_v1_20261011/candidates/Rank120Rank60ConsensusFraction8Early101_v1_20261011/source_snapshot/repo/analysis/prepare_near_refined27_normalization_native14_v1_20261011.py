"""Normalize25 new CDF cases against actual qualified175/190, then replay the selected native pair."""
from pathlib import Path
from datetime import datetime
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
NORMAL='normalize_completed_near_refined27_after190_v1_20261011'
QUAL='qualify_near_refined27_selected_native14_v1_20261011'
PLAN='near_refined_complete27_after190_plan_v1_20261011.json'

def route(text):
    mappings={'normalize_completed_near_protected39_after189_v1_20261011':NORMAL,
              'compute_near_protected39_selected_native14_v1_20261011':QUAL,
              'near_protected_complete39_after189':'near_refined_complete27_after190',
              'near_protected39_selected_native14':'near_refined27_selected_native14',
              'near_protected_stage_selector_and_CPU11_sources_admission_v1_20261011':'three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011',
              'near_protected_actual_eleven_parent_callbacks_CPU_controls_v1_20261011':'three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011',
              'actual_near_protected39_after189_normalization_v1_20261011':'actual_near_refined27_after190_normalization_v1_20261011',
              'selected_near_protected39':'selected_near_refined27','fully_qualified_anchor39':'fully_qualified_anchor27',
              'pilot39':'pilot27','normalized39':'normalized27','complete39':'complete27',
              'full190':'full191'}
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mappings,key=len,reverse=True)))
    text=pattern.sub(lambda m:mappings[m.group()],text)
    return re.sub(r'(?<![A-Za-z0-9_])(189|39|37|36|108)(?![A-Za-z0-9_])',
                  lambda m:{'189':'190','39':'27','37':'25','36':'24','108':'72'}[m.group()],text)

def main():
    assert allowed()
    oldplan=A/'near_protected_complete39_after189_plan_v1_20261011.json'
    plan=read(oldplan);plan.update(status='predeclared27_refined25_normalization_without_rescoring_future_parent190_not_yet_claimed_qualified',
            at_local=datetime.now().isoformat(),expected_records=27,fully_qualified_anchors=[175,190],
            actual_previous_complete_family='MixedProtected190_complete39_family_v1_20261011')
    plan.pop('full190_factory_not_yet_created');plan['full191_factory_not_yet_created']=True
    family=plan['families'][0];family.update(name='near_refined25',actual_service='actual_rank5_rank20_after175_near_refined25_screen_v1_20261011',
            main_receipt='near_refined25_official25_main_receipt_v1_20261011.json',
            output='E:/赛题五_本机临时/Rank5Rank20_after175_near_refined25_screen_v1_20261011',
            native_stage_module='rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011',
            stage_kind='rank5_rank20_mixed_raw_average',signal_name='near_refined_two_horizon_raw_average')
    create(A/PLAN,plan)
    originals=[A/'normalize_completed_near_protected39_after189_v1_20261011.py',A/'compute_near_protected39_selected_native14_v1_20261011.py']
    targets=[A/(NORMAL+'.py'),A/(QUAL+'.py')]
    for source,target in zip(originals,targets):
        text=route(source.read_text(encoding='utf8'))
        text=text.replace("cfg['kind'] in ('valid_pool_protection_v1','official_Top_protection_v2')","cfg['kind']=='CDF'")
        assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    norm=targets[0].read_text(encoding='utf8');qual=targets[1].read_text(encoding='utf8')
    assert 'pilot39.json' not in norm+qual
    assert "closed('actual_near_refined27_after190_normalization_v1_20261011')" in qual
    assert 'passed_selected_near_refined27_six_pairs14_native14_cold7_prefit_refusals' in qual
    assert '[175,190]' in norm and "PLAN=A/'"+PLAN+"'" in norm
    pins={str(p):sha(p) for p in [Path(__file__),oldplan,*originals,*targets,A/PLAN,
           A/'near_refined25_sources_and_dispatch_admission_v1_20261011.json',
           A/'three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011.json']}
    proof=A/'near_refined27_normalization_native14_sources_admission_v1_20261011.json'
    create(proof,{'status':'compiled27_refined25_CDF_actual190_parent_routes_before_future_and_native',
            'input_sha256':pins,'expected_records':27,'expected_full_controls':24,'expected_prefix_controls':72,
            'native14_only_if_selected_new_scheme':True,'actual190_complete_not_yet_claimed':True,
            'full191_factory_not_yet_created':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    for name,driver in [('actual_near_refined27_after190_normalization_v1_20261011',targets[0].name),
                        ('actual_near_refined27_selected_native14_v1_20261011',targets[1].name)]:
        assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(proof):sha(proof)})
        create(A/(name+'_activation.json'),row)
    print({'actual27_normalization_and_selected_native14_queued':True,'new_fits':0,'full191_not_created':True},flush=True)

if __name__=='__main__':main()
