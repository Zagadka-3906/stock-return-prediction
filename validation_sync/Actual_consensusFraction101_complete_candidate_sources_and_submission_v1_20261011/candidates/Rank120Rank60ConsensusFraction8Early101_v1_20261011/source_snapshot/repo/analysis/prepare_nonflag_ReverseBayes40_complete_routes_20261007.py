"""Prepare signed40 complete132 routes only; official scoring requires later real parent admission."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_ReverseBayes40_round132_mapping_20261007 import convert

def main():
    originals=[
      'run_nonflag_EmpiricalBayes40_official_comparison_v4_20261007.py','run_nonflag_EmpiricalBayes40_admitted_comparison_v5_20261007.py',
      'prepare_nonflag_EmpiricalBayes40_selected_candidate_v4_20261007.py','seal_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py',
      'publish_nonflag_EmpiricalBayes40_evidence_v4_20261007.py','run_nonflag_EmpiricalBayes40_round130_full_registration_v1_20261007.py',
      'verify_nonflag_EmpiricalBayes40_round130_sources_v4_20261007.py','predict_nonflag_residual_EmpiricalBayes_complete_scheme_20261007.py',
      'nonflag_residual_EmpiricalBayes_compatible_parent_20261007.py','verify_nonflag_EmpiricalBayes40_prospective_routes_v3_20261007.py']
    sources=[Path(__file__),A/'nonflag_ReverseBayes40_round132_mapping_20261007.py',A/'prepare_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',
      A/'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json']
    signed=read(sources[-1]);assert signed['status']=='passed_actual_signed_native3_full37_independent_CDF_and111_cold_controls'
    plan=read(A/'nonflag_ReverseBayes40_control_plan_20261007.json')
    plan={k:v for k,v in plan.items() if k not in ['proposed_round','proposed_future_qualified_anchor_rounds','actual_qualified_preflight_parent','selection','at_local']}
    plan.update(status='frozen_negative_Bayes40_before_official_scores_complete_future_schema_pending_actual_parents',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
      round=132,wave=415,after_round=131,qualified_anchor_rounds=[112,130,131],selection='highest_whole_connected_official_score_after_actual131_main_and_source_admission',
      full_future_candidate_native_replays_and_QA43_required=True,original_full_future_source_schema_not_yet_admitted=True,
      input_sha256={str(p):sha(p) for p in [Path(__file__),sources[-1],A/'nonflag_ReverseBayes40_control_plan_20261007.json']})
    path=A/'nonflag_ReverseBayes40_plan_20261007.json';create(path,plan);sources.append(path)
    for name in originals:
        old=A/name;new=A/convert(name);text=convert(old.read_text(encoding='utf8'))
        if name.startswith('run_nonflag_EmpiricalBayes40_official'):
            needle="    assert len(cases)==plan['expected_scored_records']==40";assert text.count(needle)==1
            text=text.replace(needle,"    assert plan['residual_sign']==-1\n    for case in cases:\n        if case['model'] is not None:case['residual_sign']=-1\n"+needle)
            needle="        prepared=prepare(reference,dates,flags,valid,plan['universe'])";assert text.count(needle)==1
            text=text.replace(needle,"        head={name:-np.asarray(values) for name,values in head.items()}\n"+needle)
        if name.startswith('prepare_nonflag_EmpiricalBayes40_selected'):
            needle="        selected=transform(raw,reference,dates,flags,valid,residual,cfg['weight'],cfg['universe'])";assert text.count(needle)==1
            text=text.replace(needle,"        assert cfg['residual_sign']==-1\n        residual*=cfg['residual_sign']\n"+needle)
        if name.startswith('verify_nonflag_EmpiricalBayes40'):
            text=text.replace("'universe':plan['universe']}","'universe':plan['universe'],'residual_sign':-1}")
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old':'remove'}", "'nonflag_CPU_HGB_residual_CDF':{'old':'remove'},'nonflag_CPU_EmpiricalBayes64_residual_CDF':{'old_positive':'remove'}")
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}", "'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_EmpiricalBayes64_residual_CDF':{'old_positive':'remove'}")
            text=text.replace("assert graph['nonflag_CPU_ReverseBayes64_residual_CDF']['ordered_equal_mean_components']==names", "assert graph['nonflag_CPU_ReverseBayes64_residual_CDF']['ordered_equal_mean_components']==names and graph['nonflag_CPU_ReverseBayes64_residual_CDF']['residual_sign']==-1")
            if name.startswith('verify_nonflag_EmpiricalBayes40_prospective'):
                needle='    graph_controls=[];generated_hashes={};path_controls=[];issues=[]';assert text.count(needle)==1
                text=text.replace(needle,"    future |= {A/f'github_validation_sync_main_20261005/round{n}_receipt.json' for n in (130,131)}\n"+needle)
        if name.startswith('verify_nonflag_EmpiricalBayes40_round') or name.startswith('publish_'):
            needle='    for p in sources:' if name.startswith('verify_') else "    if phase=='scores':\n        for row in proof['records']:"
            assert text.count(needle)==1
            text=text.replace(needle,"    sources += [A/'prepare_nonflag_ReverseBayes40_complete_routes_20261007.py',A/'nonflag_ReverseBayes40_control_source_preparation_20261007.json',A/'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json',A/'nonflag_ReverseBayes40_prospective_routes_v1_20261007.json']\n"+needle)
        compile(text,str(new),'exec');assert not new.exists(),new;new.write_text(text,encoding='utf8',newline='\n');sources.extend((old,new))
    create(A/'nonflag_ReverseBayes40_science_route_preparation_v1_20261007.json',{
      'status':'compiled_fresh_signed40_complete132_QA43_routes_before_any_official_scores','input_sha256':{str(p):sha(p) for p in sources},
      'actual_negative_native3_full37_and111_controls_passed':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    from verify_nonflag_ReverseBayes40_prospective_routes_v1_20261007 import main as prospective
    prospective()

if __name__=='__main__':main()
