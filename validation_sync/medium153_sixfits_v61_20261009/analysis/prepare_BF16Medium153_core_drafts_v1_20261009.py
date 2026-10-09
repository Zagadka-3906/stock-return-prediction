"""Prepare unadmitted neural153 receivers with explicit own bank, signed grid and148 stage."""
from pathlib import Path
import sys,re,io,tokenize,ast,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def route(s):
    mapping={
      'BF16_reverse_complete_parent_rank_CDF_v1_20261008':'BF16Medium153_complete_parent_rank_CDF_v1_20261009',
      'BF16_reverse_complete_parent_native_stage_v1_20261008':'BF16Medium153_complete_parent_native_stage_v1_20261009',
      'predict_BF16_reverse_complete_parent_scheme_v1_20261008':'predict_BF16Medium153_complete_parent_scheme_v1_20261009',
      'BF16_reverse_complete_parent_native_replay_verification.json':'BF16Medium153_complete_parent_native_replay_verification.json',
      'BF16_reverse_complete_parent_rank_CDF':'BF16_medium2048_seed09_complete_parent_rank_CDF',
      'passed_actual_complete_parent_and_reverse_BF16_two_full_native_independent_replays_and_cold80':'passed_actual_complete148_and_medium153_two_full_native_independent_replays_and_cold80',
      'neural_BF16_micro8192_native_v1_20261008':'neural_BF16_medium2048_seed09_e64_native_v1_20261009',
      'actual_BF16_micro8192_bank6_location_v2_20261008':'actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009',
      'actual_BF16_reverse_rank_CDF_full37_location_v1_20261008':'actual_BF16Medium153_full73_training_location_v1_20261009',
      'actual_BF16_full5_independent_location_v2_20261008':'actual_BF16Medium153_full5_independent_location_v1_20261009',
      'passed_actual37_full5635800_reverse_BF16_CDF_independent_and111_cold_controls':'passed_actual73_full5635800_medium153_signed_rank_mix_and219_cold_prefixes',
      'passed_actual_full5_5635800_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes':'passed_actual_full5_5635800_medium2048_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes',
      'prepare_BF16reverse138_complete_receivers_v1_20261008':'prepare_BF16Medium153_core_drafts_v1_20261009',
      'exact138_connected_API_publication_reconciliation_v2_20261008':'BF16Medium78_scores_main_publication_v1_20261009',
      'BF16reverse40_scores_github_v3_20261008':'BF16Medium78_scores_github_v1_20261009',
      '第138轮_20261008':'第153轮_20261009',
      'lossless_ranking_display_qa_v49_20261007':'lossless_ranking_display_qa_v64_20261009',
      'main_publisher_v8_20261008':'main_publisher_v9_20261009'}
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    s=pattern.sub(lambda m:mapping[m[0]],s)
    for old,new in [('BF16reverse40','BF16Medium78'),('BF16reverse138','BF16Medium153'),('round138','round153'),
      ('full138','full153'),('actual138','actual153'),('prospective138','prospective153'),('_r138','_r153'),
      ('qa49','qa64'),('QA49','QA64'),('qa_v49','qa_v64'),('wave421','wave436'),('actual40','actual78'),('all40','all78'),
      ('anchor40','anchor78'),('all37','all73'),('40项','78项')]:s=s.replace(old,new)
    s=re.sub(r'(BF16Medium(?:78|153)[A-Za-z0-9_/{}.-]*?)_v(?:1|3|14|17)_20261008',r'\1_v1_20261009',s)
    s=re.sub(r'(BF16Medium(?:78|153)[A-Za-z0-9_/{}.-]*?)_20261008',r'\1_20261009',s)
    s=s.replace('(135,136,137)','(148,149,150,151,152)').replace('(135, 136, 137)','(148,149,150,151,152)')
    nums={'40':'78','37':'73','111':'219','138':'153','49':'64','421':'436'}
    s=tokenize.untokenize([t._replace(string=nums.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
    return s

def best_key(row):
    return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])

def exact_replace(s,before,after):
    assert before in s,before
    return s.replace(before,after)

def main():
    proposal=A/'BF16Medium78_round153_proposal_v1_20261009.json';p=read(proposal)
    plan={**p,'round':153,'QA_version':64,'wave':436,'model_name':'rank_MLP2048_BF16_seed09_e64',
      'actual_annual_bank':p['native_bank'],'qualified_anchor_rounds':p['anchor_rounds'],'expected_scored_records':78,
      'roles':['all_valid','nonflag_valid','flag_valid'],'weights':[.0005,.001,.002,.004,.008,.016,.032,.064,.125,.25,.5,1.],
      'graph_key':'BF16_medium2048_seed09_complete_parent_rank_CDF','status':'prepared_unadmitted_medium153_complete_core_drafts'}
    planpath=A/'BF16Medium78_round153_plan_v1_20261009.json';assert not planpath.exists()
    pairs=[('BF16reverse138_storage_v1_20261008.py','BF16Medium153_storage_v1_20261009.py'),
      ('verify_BF16reverse138_D_scoring_scope_v1_20261008.py','verify_BF16Medium153_D_scoring_scope_v1_20261009.py'),
      ('run_BF16reverse40_official_comparison_v14_20261008.py','run_BF16Medium78_official_comparison_v1_20261009.py'),
      ('prepare_BF16reverse40_selected_candidate_v17_20261008.py','prepare_BF16Medium78_selected_candidate_v1_20261009.py'),
      ('seal_BF16reverse40_selected_candidate_v17_20261008.py','seal_BF16Medium78_selected_candidate_v1_20261009.py'),
      ('run_BF16reverse40_round138_full_registration_v17_20261008.py','run_BF16Medium78_round153_full_registration_v1_20261009.py')]
    changes=[];inputs=[Path(__file__),proposal]
    for old,new in pairs:
        source=A/old;inputs.append(source);s=route(source.read_text(encoding='utf8'))
        if old.startswith('run_BF16reverse40_official'):
            s=exact_replace(s,'    scheme_base=comparison_parent','    scheme_base=148')
            s=exact_replace(s,"assert scheme_base==control['actual_parent_round'] and scheme_base in (148,149,150,151,152)","assert scheme_base==control['actual_parent_round']==148")
            start=s.index('    cases += [');end=s.index('    assert len(cases)',start)
            s=s[:start]+"    cases += [{\"anchor_round\":148,\"model\":plan['model_name'] if c['weight'] else 'zero_BF16_rank_identity',\"role\":c['role'],\"weight\":c['weight'],\"sign\":c['sign'],\"universe\":plan['rank_universe']} for c in plan['new_cases']]\n"+s[end:]
            s=exact_replace(s,"neural=neural_frame['pred_raw'].to_numpy();prepared=codec.prepare(parent,neural,dates,flags,valid)","neural=neural_frame['pred_raw'].to_numpy();prepared={sign:codec.prepare(parent,neural,dates,flags,valid,sign) for sign in (1.,-1.)}")
            s=exact_replace(s,"cfg['role'],cfg['weight'],prepared)","cfg['role'],cfg['weight'],prepared[cfg['sign']])")
            s=exact_replace(s,"cfg['role'],cfg['weight'])","cfg['role'],cfg['weight'],cfg['sign'])")
        if old.startswith('prepare_BF16reverse40_selected'):
            s=exact_replace(s,"assert parent_number in (148,149,150,151,152) and 0.<cfg['weight']<=1.","assert parent_number==148 and 0.<cfg['weight']<=1. and cfg['sign'] in (-1.,1.)")
            s=exact_replace(s,"cfg['role'],cfg['weight'])","cfg['role'],cfg['weight'],cfg['sign'])")
            s=exact_replace(s,"'signal_sign_on_valid_rows':-1.,'invalid_signal_bits_preserved':True","'sign':cfg['sign'],'invalid_signal_bits_preserved':True")
        compile(s,str(A/new),'exec');ast.parse(s);changes.append((A/new,s))
    assert all(not x.exists() for x,_ in changes)
    for path,s in changes:
        with path.open('x',encoding='utf8') as f:f.write(s)
        inputs.append(path)
    create(planpath,plan);inputs.append(planpath)
    import BF16Medium153_storage_v1_20261009 as storage
    base=Path('E:/赛题五_本机临时/第153轮_20261009');folders=[]
    assert len(storage.OUTPUTS)==6
    for access,target in storage.OUTPUTS.items():
        assert access.is_relative_to(ROOT) and target.is_relative_to(base)
        assert not access.exists() and not target.exists()
    for access,target in storage.OUTPUTS.items():
        access.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True)
        q=lambda x:"'"+str(x).replace("'","''")+"'"
        r=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',"New-Item -ItemType Junction -Path "+q(access)+' -Target '+q(target)+' | Out-Null'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert r.returncode==0,r.stderr;storage.empty(access);folders.append({'access':str(access),'physical_E':str(target)})
    create(A/'BF16Medium153_core_draft_preparation_v1_20261009.json',{'status':'prepared_six_medium153_unadmitted_core_drafts_and6_empty_E_outputs',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(x):sha(x) for x in inputs},'E_outputs':folders,
      'actual_stage_base_round':148,'quality_anchor_rounds':[148,149,150,151,152],'expected_quality_cases':78,
      'QA_version':64,'wave':436,'signed_signal_on_valid_rows_only':True,'source_generator_40_prospective_and_duplicates_and_full_admission_still_required':True,
      'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'core_drafts':6,'empty_E_outputs':6,'official_scoring_admitted':False},flush=True)

if __name__=='__main__':main()
