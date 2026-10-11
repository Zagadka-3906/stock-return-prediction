"""Prepare unadmitted80 individual-seed receivers from the verified complete148 neural route."""
from pathlib import Path
import sys,io,tokenize,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_BF16Seed10_155_scientific_frontier_v1_20261009 import route as scientific_route
def best_key(row):return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])
def route(s):
    s=scientific_route(s)
    s=s.replace('round153','round155').replace('full153','full155').replace('actual153','actual155').replace('_r153','_r155')
    s=s.replace('第153轮','第155轮').replace('QA64','QA66').replace('qa64','qa66').replace('qa_v64','qa_v66').replace('wave436','wave438')
    s=s.replace('main_publisher_v9_20261009','main_publisher_v10_20261009')
    s=s.replace('actual78','actual80').replace('all78','all80').replace('anchor78','anchor80').replace('78项','80项')
    numbers={'78':'80','153':'155','436':'438'}
    s=tokenize.untokenize([t._replace(string=numbers.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
    s=s.replace('(148,149,150,151,152)','(148,149,150,151,152,153,154)')
    s=s.replace('run_BF16Seed10_80_official_comparison_v2_20261009','run_BF16Seed10_80_official_comparison_v1_20261009')
    s=s.replace('run_BF16Seed10_80_round155_full_registration_v3_20261009','run_BF16Seed10_80_round155_full_registration_v1_20261009')
    s=s.replace('publish_BF16Seed10_80_evidence_v2_20261009','publish_BF16Seed10_80_evidence_v1_20261009')
    s=s.replace('BF16Seed10_155_actual_receiver_bindings_v2_20261009','BF16Seed10_155_actual_receiver_bindings_v1_20261009')
    return s
def main():
    proposal=A/'BF16Seed10_80_round155_proposal_v1_20261009.json';p=read(proposal)
    plan={**p,'round':155,'QA_version':66,'wave':438,'actual_annual_bank':p['native_bank'],
        'qualified_anchor_rounds':p['anchor_rounds'],'expected_scored_records':80,'roles':['all_valid','nonflag_valid','flag_valid'],
        'weights':[.0005,.001,.002,.004,.008,.016,.032,.064,.125,.25,.5,1.],
        'status':'prepared_unadmitted_individual_seed10_155_complete_core_drafts'}
    planpath=A/'BF16Seed10_80_round155_plan_v1_20261009.json';assert not planpath.exists()
    pairs=[('BF16Medium153_storage_v1_20261009.py','BF16Seed10_155_storage_v1_20261009.py'),
        ('verify_BF16Medium153_D_scoring_scope_v1_20261009.py','verify_BF16Seed10_155_D_scoring_scope_v1_20261009.py'),
        ('run_BF16Medium78_official_comparison_v2_20261009.py','run_BF16Seed10_80_official_comparison_v1_20261009.py'),
        ('prepare_BF16Medium78_selected_candidate_v1_20261009.py','prepare_BF16Seed10_80_selected_candidate_v1_20261009.py'),
        ('seal_BF16Medium78_selected_candidate_v1_20261009.py','seal_BF16Seed10_80_selected_candidate_v1_20261009.py'),
        ('run_BF16Medium78_round153_full_registration_v3_20261009.py','run_BF16Seed10_80_round155_full_registration_v1_20261009.py')]
    inputs=[Path(__file__),proposal];drafts=[]
    for old,new in pairs:
        source=A/old;text=route(source.read_text(encoding='utf8'))
        if old.startswith('run_BF16Medium78_round153_full'):
            text=text.replace('SparseAfter14829_round152_full_registration_v1_20261009','BF16TwoSeed79_round154_full_registration_v1_20261009')
            text=text.replace('passed_actual29','passed_actual80').replace('五个合格锚点','七个合格锚点')
        if old.startswith('run_BF16Medium78_official'):
            # The existing independent proof is for this actual seed10 bank; its
            # generic medium2048 status is unchanged from the verified decoder.
            assert 'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009' in text
        compile(text,str(A/new),'exec');drafts.append((A/new,text));inputs.append(source)
    assert all(not dst.exists() for dst,_ in drafts)
    for dst,text in drafts:dst.write_text(text,encoding='utf8');inputs.append(dst)
    create(planpath,plan);inputs.append(planpath)
    import BF16Seed10_155_storage_v1_20261009 as storage
    assert len(storage.OUTPUTS)==6;folders=[];base=Path('E:/赛题五_本机临时/第155轮_20261009')
    for access,target in storage.OUTPUTS.items():assert access.is_relative_to(ROOT) and target.is_relative_to(base) and not access.exists() and not target.exists()
    for access,target in storage.OUTPUTS.items():
        access.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True)
        q=lambda x:"'"+str(x).replace("'","''")+"'"
        result=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command','New-Item -ItemType Junction -Path '+q(access)+' -Target '+q(target)+' | Out-Null'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr;storage.empty(access);folders.append({'access':str(access),'physical_E':str(target)})
    create(A/'BF16Seed10_155_core_draft_preparation_v1_20261009.json',{
        'status':'prepared_six_unadmitted_individual_seed10_155_receivers_and6_empty_E_outputs',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'E_outputs':folders,
        'stage_base_round':148,'quality_anchor_rounds':list(range(148,155)),'expected_quality_cases':80,'QA_version':66,'wave':438,
        'full_prospective56_routes_actual_full73_duplicate_audit_and_full154_still_required':True,
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'unadmitted_receivers':6,'quality_cases_proposed':80,'empty_E_outputs':6},flush=True)
if __name__=='__main__':main()
