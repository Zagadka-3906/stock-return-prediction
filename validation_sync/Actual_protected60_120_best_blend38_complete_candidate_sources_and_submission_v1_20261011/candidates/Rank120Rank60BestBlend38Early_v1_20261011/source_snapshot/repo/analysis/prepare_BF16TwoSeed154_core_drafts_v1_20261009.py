"""Build unadmitted two-seed receivers; preserve complete148 and official scoring contracts."""
from pathlib import Path
import sys,ast,re,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
NAMES=['rank_MLP2048_BF16_seed09_e64','rank_MLP2048_BF16_seed10_e64']
def best_key(row):
    return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])
def replace(s,before,after,count=1):
    assert s.count(before)==count,(before,s.count(before),count)
    return s.replace(before,after)
def route(s):
    # Reuse the verified scalar CDF arithmetic; only the input is a frozen two-seed mean.
    s=s.replace('BF16Medium153_complete_parent_rank_CDF_v1_20261009','__SHARED_CODEC__')
    s=s.replace('BF16Medium153','BF16TwoSeed154').replace('BF16Medium78','BF16TwoSeed79')
    s=s.replace('BF16_medium2048_seed09_complete_parent_rank_CDF','BF16_two_seed09_seed10_equal_mean_complete_parent_rank_CDF')
    s=s.replace('medium153_two_full','two_seed154_two_full')
    s=s.replace('__SHARED_CODEC__','BF16Medium153_complete_parent_rank_CDF_v1_20261009')
    s=s.replace('round153','round154').replace('full153','full154').replace('actual153','actual154').replace('_r153','_r154')
    s=s.replace('第153轮','第154轮').replace('QA64','QA65').replace('qa64','qa65').replace('qa_v64','qa_v65')
    s=s.replace('wave436','wave437').replace('main_publisher_v9_20261009','main_publisher_v10_20261009')
    s=s.replace('(148,149,150,151,152)','(148,149,150,151,152,153)')
    s=s.replace('actual78','actual79').replace('all78','all79').replace('anchor78','anchor79').replace('78项','79项')
    # Integer tokens used as round/case numbers, never change training epoch literals.
    import tokenize,io
    numbers={'78':'79','153':'154','436':'437'}
    s=tokenize.untokenize([t._replace(string=numbers.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
    return s
def main():
    ppath=A/'BF16TwoSeed79_round154_proposal_v1_20261009.json';proposal=read(ppath)
    previous=A/'BF16Medium78_round153_plan_v1_20261009.json'
    banks=[str(Path(read(A/f'actual_BF16_medium2048_seed{s}_e64_bank6_location_v1_20261009.json')['output'])) for s in ('09','10')]
    plan={**read(previous),**proposal,'status':'prepared_unadmitted_two_seed154_complete_core_drafts',
        'round':154,'QA_version':65,'wave':437,'model_name':'fixed_equal_seed09_seed10_mean','native_component_names':NAMES,
        'actual_annual_banks':banks,'qualified_anchor_rounds':proposal['quality_anchor_rounds'],
        'new_cases':proposal['scientific_cases'],'expected_scored_records':79,'expected_official_cases':79,
        'graph_key':'BF16_two_seed09_seed10_equal_mean_complete_parent_rank_CDF','seed_weights':[.5,.5],
        'actual_scheme_base_round':148,'native_saved_states':12,'input_sha256':{str(ppath):sha(ppath),str(previous):sha(previous)}}
    for key in ('actual_annual_bank','native_bank'):plan.pop(key,None)
    assert len(plan['new_cases'])==73 and plan['qualified_anchor_rounds']==list(range(148,154))
    pairs=[('BF16Medium153_storage_v1_20261009.py','BF16TwoSeed154_storage_v1_20261009.py'),
        ('verify_BF16Medium153_D_scoring_scope_v1_20261009.py','verify_BF16TwoSeed154_D_scoring_scope_v1_20261009.py'),
        ('run_BF16Medium78_official_comparison_v2_20261009.py','run_BF16TwoSeed79_official_comparison_v1_20261009.py'),
        ('prepare_BF16Medium78_selected_candidate_v1_20261009.py','prepare_BF16TwoSeed79_selected_candidate_v1_20261009.py'),
        ('seal_BF16Medium78_selected_candidate_v1_20261009.py','seal_BF16TwoSeed79_selected_candidate_v1_20261009.py'),
        ('run_BF16Medium78_round153_full_registration_v3_20261009.py','run_BF16TwoSeed79_round154_full_registration_v1_20261009.py')]
    paths=[Path(__file__),ppath,previous];drafts=[]
    for old,new in pairs:
        source=A/old;paths.append(source);s=route(source.read_text(encoding='utf8'))
        if old.startswith('run_BF16Medium78_official'):
            s=replace(s,"final_info=read(Path(plan['actual_annual_bank'])/'2025/info.json');neural_sha=final_info['model_sha256']",
                "final_infos=[read(Path(bank)/'2025/info.json') for bank in plan['actual_annual_banks']];neural_shas={info['model_sha256'] for info in final_infos};assert len(neural_shas)==2")
            s=replace(s,'actual_BF16TwoSeed154_full5_independent_location_v1_20261009','actual_BF16TwoSeed154_equal_mean_full5_location_v1_20261009')
            s=replace(s,'passed_actual_full5_5635800_medium2048_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes',
                'passed_actual_two_independent_seeds5635800_equal_mean_and10_annual_prefixes')
            s=replace(s,'passed_actual73_full5635800_medium153_signed_rank_mix_and219_cold_prefixes',
                'passed_actual73_full5635800_two_seed154_signed_rank_mix_and219_cold_prefixes')
            s=replace(s,"else [plan['model_name']]","else plan['native_component_names']")
            s=replace(s,"'components':{plan['model_name']:[plan['model_name']]}","'components':{plan['model_name']:plan['native_component_names']}")
            s=replace(s,'({neural_sha} if','(neural_shas if')
            s=replace(s,"'native_bank_fits':6","'native_bank_fits':12")
            s=replace(s,"'existing_native_bank_fits':6","'existing_native_bank_fits':12")
        elif old.startswith('prepare_BF16Medium78_selected'):
            begin=s.index("    bank=Path(read(A/'actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009.json')")
            end=s.index('    freeze=Path(',begin)
            s=s[:begin]+'''    components=[]
    from neural_BF16_medium2048_seed10_e64_native_v1_20261009 import CONFIG as CONFIG10
    for seed,name,config in zip(('09','10'),NAMES,(CONFIG,CONFIG10)):
        bank=Path(read(A/f'actual_BF16_medium2048_seed{seed}_e64_bank6_location_v1_20261009.json')['output'])
        info=read(bank/'2025/info.json');meta=info['training_meta']
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and info['year']==2025
        assert info['configuration']==config
        import joblib
        bundle=joblib.load(bank/'2025/model.joblib');assert bundle['config']==config and len(bundle['training_losses'])==64;del bundle
        assert meta['last']<meta['cutoff_exclusive']==fold_cutoff(2025) and meta['last_label_end']<=meta['cutoff_exclusive']
        component={'name':name,'source_path':str(bank/'2025/model.joblib'),'path':str(CANDIDATE/(name+'_final2025.joblib')),
            'sha256':info['model_sha256'],'configuration':config,'training_info':info}
        assert sha(component['source_path'])==component['sha256']
        pins[component['source_path']]=component['sha256'];pins[str(bank/'2025/info.json')]=sha(bank/'2025/info.json')
        components.append(component)
    assert len({c['sha256'] for c in components})==2
''' +s[end:]
            s=replace(s,"neural_folder=Path(read(A/'actual_BF16TwoSeed154_full5_independent_location_v1_20261009.json')['output'])",
                "neural_folder=Path(read(A/'actual_BF16TwoSeed154_equal_mean_full5_location_v1_20261009.json')['output'])")
            s=replace(s,"'native_component':component","'native_components':components,'seed_weights':[.5,.5],'seed_values':[20261009,20261010]")
            s=replace(s,"|{component['sha256']}","|{c['sha256'] for c in components}")
            s=replace(s,"*([cfg['model']] if component['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()} else [])",
                "*[c['name'] for c in components if c['sha256'] not in {m['sha256'] for m in parent_prediction['models'].values()}]")
            s=replace(s,"'actual6_mature_native_and_full_independent_controls'","'actual12_mature_native_and_full_independent_controls'")
            s=s.replace("GRAPH_KEY='", "NAMES=['rank_MLP2048_BF16_seed09_e64','rank_MLP2048_BF16_seed10_e64']\nGRAPH_KEY='")
        elif old.startswith('run_BF16Medium78_round153_full'):
            s=s.replace('SparseAfter14829_round152_full_registration_v1_20261009','BF16Medium78_round153_full_registration_v1_20261009')
            s=s.replace('passed_actual29','passed_actual79')
        compile(s,str(A/new),'exec');ast.parse(s);drafts.append((A/new,s))
    planpath=A/'BF16TwoSeed79_round154_plan_v1_20261009.json'
    assert not planpath.exists() and all(not path.exists() for path,_ in drafts)
    for path,s in drafts:
        with path.open('x',encoding='utf8') as f:f.write(s)
        paths.append(path)
    create(planpath,plan);paths.append(planpath)
    import BF16TwoSeed154_storage_v1_20261009 as storage
    base=Path('E:/赛题五_本机临时/第154轮_20261009');folders=[]
    assert len(storage.OUTPUTS)==6
    for access,target in storage.OUTPUTS.items():assert access.is_relative_to(ROOT) and target.is_relative_to(base) and not access.exists() and not target.exists()
    for access,target in storage.OUTPUTS.items():
        access.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True)
        q=lambda x:"'"+str(x).replace("'","''")+"'"
        result=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command','New-Item -ItemType Junction -Path '+q(access)+' -Target '+q(target)+' | Out-Null'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr
        storage.empty(access);folders.append({'access':str(access),'physical_E':str(target)})
    create(A/'BF16TwoSeed154_core_draft_preparation_v1_20261009.json',{'status':'prepared_six_unadmitted_two_seed154_core_drafts_and6_empty_E_outputs',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},'E_outputs':folders,
        'actual_stage_base_round':148,'quality_anchor_rounds':list(range(148,154)),'expected_quality_cases':79,
        'native_component_names':NAMES,'actual_saved_annual_states_required':12,'QA_version':65,'wave':437,
        'all_full_prospective_routes_duplicates_source_admission_and153_full_registration_still_required':True,
        'official_scoring_admitted':False,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'core_drafts':6,'empty_E_outputs':6,'official_scoring_admitted':False},flush=True)
if __name__=='__main__':main()
