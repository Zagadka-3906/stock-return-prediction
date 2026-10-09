"""Prepare unadmitted157 candidate, sealing, full68 QA and E storage around the frozen22 grid."""
from pathlib import Path
import sys,ast,tokenize,io,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def route(s):
    exact={
        'actual_BF16Seed10_155_full73_training_location_v1_20261009':'actual_BF16FlagAfter15217_full_training_location_v1_20261009',
        'actual_BF16Seed10_155_native42_calendar_location_v1_20261009':'actual_BF16FlagAfter152157_native14_calendar_location_v1_20261009',
        'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009':'actual_BF16Medium153_full5_independent_location_v1_20261009',
        'BF16_medium2048_seed10_complete_parent_rank_CDF':'BF16_flag_after152157_complete_parent_rank_CDF',
        'BF16Seed10_155_complete_parent_native_replay_verification':'BF16FlagAfter152157_complete_parent_native_replay_verification',
        'passed_actual_complete148_and_seed10_155_two_full_native_independent_replays_and_cold80':'passed_actual_complete152_and_medium153_two_full_native_independent_replays_and_cold80',
        'passed_actual80_BF16_medium2048_seed10_complete_parent_rank_CDF_full_official_comparisons':'passed_actual22_complete152_flag_neural_training_only_official_comparisons',
        'BF16Medium153_complete_parent_rank_CDF_v1_20261009':'__SHARED_SIGNED_CODEC__'}
    for old,new in exact.items():s=s.replace(old,new)
    s=s.replace('BF16Seed10_155','BF16FlagAfter152157').replace('BF16Seed10_80','BF16FlagAfter15222')
    s=s.replace('round155','round157').replace('full155','full157').replace('actual155','actual157').replace('_r155','_r157')
    s=s.replace('seed10','seed09').replace('第155轮','第157轮').replace('QA66','QA68').replace('qa66','qa68').replace('qa_v66','qa_v68').replace('wave438','wave440')
    s=s.replace('all80','all22').replace('actual80','actual22').replace('anchor80','anchor22').replace('80项','22项')
    s=s.replace('passed_actual_complete148_and_seed09_155_two_full_native_independent_replays_and_cold80','passed_actual_complete152_and_medium153_two_full_native_independent_replays_and_cold80')
    nums={'80':'22','155':'157','66':'68','438':'440'}
    s=tokenize.untokenize([t._replace(string=nums.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
    return s.replace('__SHARED_SIGNED_CODEC__','BF16Medium153_complete_parent_rank_CDF_v1_20261009')
def write(name,text):
    ast.parse(text);p=A/name
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p
def main():
    proposal=A/'BF16FlagAfter15217_train_only_proposal_v1_20261009.json';p=read(proposal)
    plan={**p,'round':157,'QA_version':68,'wave':440,'actual_annual_bank':p['native_bank'],
        'qualified_anchor_rounds':list(range(152,157)),'anchor_rounds':list(range(152,157)),
        'expected_scored_records':22,'expected_official_cases':22,'graph_key':'BF16_flag_after152157_complete_parent_rank_CDF',
        'roles':['flag_valid'],'weights':[.001,.002,.003,.004,.006,.008,.012,.016],
        'status':'prepared_unadmitted157_complete152_flag_neural_candidate_and_full_QA68_drafts'}
    planpath=A/'BF16FlagAfter15222_round157_plan_v1_20261009.json';create(planpath,plan)
    pairs=[('BF16Seed10_155_storage_v1_20261009.py','BF16FlagAfter152157_storage_v1_20261009.py'),
        ('verify_BF16Seed10_155_D_scoring_scope_v1_20261009.py','verify_BF16FlagAfter152157_D_scoring_scope_v1_20261009.py'),
        ('prepare_BF16Seed10_80_selected_candidate_v1_20261009.py','prepare_BF16FlagAfter15222_selected_candidate_v1_20261009.py'),
        ('seal_BF16Seed10_80_selected_candidate_v1_20261009.py','seal_BF16FlagAfter15222_selected_candidate_v1_20261009.py'),
        ('run_BF16Seed10_80_round155_full_registration_v2_20261009.py','run_BF16FlagAfter15222_round157_full_registration_v1_20261009.py')]
    files=[Path(__file__),proposal,planpath];outputs=[]
    for old,new in pairs:
        src=A/old;s=route(src.read_text(encoding='utf8'))
        if new.startswith('prepare_BF16Flag'):
            s=s.replace("assert parent_number in (148,149,150,151,152,153,154)","assert parent_number in (152,153,154,155,156)")
            s=s.replace('assert parent_number==148','assert parent_number==152')
            s=s.replace("closed('BF16FlagAfter15222_official_comparison_v1_20261009')","closed('BF16FlagAfter15222_official_comparison_v3_20261009')")
            s=s.replace("A/'BF16FlagAfter15222_round157_source_admission_v1_20261009.json'","A/'BF16FlagAfter15222_round157_source_admission_v1_20261009.json'")
            s=s.replace("A/'prepare_BF16FlagAfter15222_round157_sources_v1_20261009.py'","A/'prepare_BF16FlagAfter15222_round157_sources_v1_20261009.py'")
            s=s.replace("A/'BF16FlagAfter152157_D_scoring_v1_20261009/selected/scoring_validation_only'","A/'BF16FlagAfter152157_D_scoring_v1_20261009/selected/scoring_validation_only'")
        if new.startswith('seal_'):
            s=s.replace('passed_actual_complete148_and_seed10_155_two_full_native_independent_replays_and_cold80','passed_actual_complete152_and_medium153_two_full_native_independent_replays_and_cold80')
            s=s.replace('passed_actual_complete148_and_seed09_155_two_full_native_independent_replays_and_cold80','passed_actual_complete152_and_medium153_two_full_native_independent_replays_and_cold80')
        if new.startswith('run_'):
            s=s.replace('BF16TwoSeed79_round154_full_registration_v2_20261009','BF16Drop05_81_round156_full_registration_v1_20261009')
            s=s.replace("'BF16FlagAfter15222_official_comparison_v1_20261009'","'BF16FlagAfter15222_official_comparison_v3_20261009'")
            s=s.replace('assert parent_number in (148, 149, 150, 151, 152, 153, 154)','assert parent_number in (152, 153, 154, 155, 156)')
            s=s.replace('BF16FlagAfter15222_round157_actual_registration_v3_20261009','BF16FlagAfter15222_round157_actual_registration_v1_20261009')
        if new.startswith('BF16Flag'):
            s=s.replace("EBASE/'official_comparison'","Path('E:/赛题五_本机临时/BF16FlagAfter15222_official_comparison_v1_20261009')")
        dst=write(new,s);files.extend((src,dst));outputs.append(dst)
    import BF16FlagAfter152157_storage_v1_20261009 as storage
    assert len(storage.OUTPUTS)==6
    bindings=[]
    for access,target in storage.OUTPUTS.items():
        assert access.is_relative_to(ROOT) and target.drive.upper()=='E:' and not access.exists() and not target.exists(),(access,target)
    for access,target in storage.OUTPUTS.items():
        access.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True,exist_ok=False)
        q=lambda x:"'"+str(x).replace("'","''")+"'"
        r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command','New-Item -ItemType Junction -Path '+q(access)+' -Target '+q(target)+' | Out-Null'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert r.returncode==0,r.stderr;storage.empty(access);bindings.append({'access':str(access),'physical_E':str(target)})
    create(A/'BF16FlagAfter152157_core_preparation_v62_20261009.json',{'status':'prepared157_five_core_receivers_and6_empty_E_outputs',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in files},
        'outputs':bindings,'fixed_stage_base_round':152,'comparison_anchors':list(range(152,157)),
        'expected_quality_cases':22,'QA_version':68,'wave':440,'quality3_empty_E_admission_and_full_prospective_controls_still_required':True,
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'core_receivers':5,'E_outputs':6,'quality_cases':22},flush=True)
if __name__=='__main__':main()
