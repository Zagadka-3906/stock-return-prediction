"""Derive further fully audited train-only frontiers from the admitted157 contracts."""
from pathlib import Path
import argparse,ast,io,tokenize,json,sys,subprocess,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def build(number,recipe,role,grid=0):
    assert 158<=number<=1000 and recipe in ('seed09','seed10','drop05','topweightedhuber010') and role in ('flag_valid','nonflag_valid','all_valid')
    predecessor=number-1;anchors=(list(range(152,number)) if number==158 else [152,predecessor]);count=len(anchors)+17;qa=number-89
    tag=f'ReusedNN{number}'
    bankname={'seed09':'neural_BF16_medium2048_seed09_e64_bank6_v1_20261009',
        'seed10':'neural_BF16_medium2048_seed10_e64_bank6_v1_20261009',
        'drop05':'neural_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009','topweightedhuber010':'neural_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009'}[recipe]
    bank=Path('E:/赛题五_本机临时')/bankname
    full5={'seed09':'actual_BF16Medium153_full5_independent_location_v1_20261009',
        'seed10':'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009',
        'drop05':'actual_BF16Drop05_156_full5_independent_location_v1_20261009','topweightedhuber010':'actual_BF16TopWeightedHuber010165_full5_independent_location_v1_20261009'}[recipe]
    native42={'seed09':'actual_BF16Medium153_native42_calendar_location_v1_20261009',
        'seed10':'actual_BF16Seed10_155_native42_calendar_location_v1_20261009',
        'drop05':'actual_BF16Drop05_156_native42_calendar_location_v1_20261009','topweightedhuber010':'actual_BF16TopWeightedHuber010165_native42_calendar_location_v1_20261009'}[recipe]
    native_module={'seed09':'neural_BF16_medium2048_seed09_e64_native_v1_20261009',
        'seed10':'neural_BF16_medium2048_seed10_e64_native_v1_20261009',
        'drop05':'neural_BF16_medium2048_drop05_seed09_e64_native_v1_20261009','topweightedhuber010':'neural_BF16_medium2048_topweightedhuber010_seed09_e64_native_v1_20261009'}[recipe]
    decoder={'seed09':'neural_BF16_medium2048_seed09_independent_forward_v1_20261009',
        'seed10':'neural_BF16_medium2048_seed10_independent_forward_v1_20261009',
        'drop05':'neural_BF16_medium2048_drop05_seed09_independent_forward_v1_20261009','topweightedhuber010':'neural_BF16_medium2048_topweightedhuber010_seed09_independent_forward_v1_20261009'}[recipe]
    location={'seed09':'actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009',
        'seed10':'actual_BF16_medium2048_seed10_e64_bank6_location_v1_20261009',
        'drop05':'actual_BF16_medium2048_drop05_seed09_e64_bank6_location_v1_20261009','topweightedhuber010':'actual_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_location_v1_20261009'}[recipe]
    prior_count=23 if predecessor==158 else 19
    previous_service=('BF16FlagAfter15222_round157_full_registration_v1_20261009' if predecessor==157 else f'ReusedNN{predecessor}Quality{prior_count}_round{predecessor}_full_registration_v1_20261009')
    def transform(s,numeric=True):
        # Replace only the original native leaf pointers; the validated CDF codec remains shared.
        for old,new in [('actual_BF16Medium153_full5_independent_location_v1_20261009',full5),
            ('actual_BF16Medium153_native42_calendar_location_v1_20261009',native42),
            ('neural_BF16_medium2048_seed09_e64_native_v1_20261009',native_module),
            ('neural_BF16_medium2048_seed09_independent_forward_v1_20261009',decoder),
            ('actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009',location),
            ('neural_BF16_medium2048_seed09_e64_bank6_v1_20261009',bankname)]:s=s.replace(old,new)
        for old,new in [('BF16FlagAfter152157',tag+'Stage'),('BF16FlagAfter15222',tag+'Quality'+str(count)),
            ('BF16FlagAfter15217',tag+'Full17'),('BF16_flag_after152157','reusedNN'+str(number)),
            ('round157','round'+str(number)),('_r157','_r'+str(number)),('第157轮','第'+str(number)+'轮'),
            ('full157','full'+str(number)),('actual157','actual'+str(number)),
            ('QA68','QA'+str(qa)),('qa_v68','qa_v'+str(qa)),('qa68','qa'+str(qa)),('wave440','wave'+str(number+283)),
            ('passed_actual22_','passed_actual'+str(count)+'_'),('all22','all'+str(count)),('actual22_selected','actual'+str(count)+'_selected'),
            ('actual22_sealed','actual'+str(count)+'_sealed'),('anchor22','anchor'+str(count)),('actual22_score','actual'+str(count)+'_score'),
            ('len(pilot[\'records\'])==22','len(pilot[\'records\'])=='+str(count)),
            ('BF16Drop05_81_round156_full_registration_v1_20261009',previous_service)]:s=s.replace(old,new)
        if numeric:
            nums={'157':str(number),'68':str(qa),'440':str(number+283),'22':str(count)}
            s=tokenize.untokenize([t._replace(string=nums.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
            if number>158:s=s.replace(f'range(152,{number})',repr(tuple(anchors)))
        s=s.replace('[152,153,154,155,156]',repr(anchors)).replace('(152,153,154,155,156)',repr(tuple(anchors)))
        s=s.replace('(152, 153, 154, 155, 156)',repr(tuple(anchors)))
        if recipe=='seed10':s=s.replace('rank_MLP2048_BF16_seed09_e64','rank_MLP2048_BF16_seed10_e64')
        elif recipe=='drop05':s=s.replace('rank_MLP2048_BF16_seed09_e64','rank_MLP2048_BF16_drop05_seed09_e64')
        elif recipe=='topweightedhuber010':s=s.replace('rank_MLP2048_BF16_seed09_e64','rank_MLP2048_BF16_topweightedhuber010_seed09_e64')
        return s
    names=[
        'prepare_BF16FlagAfter152157_core_v62_20261009.py','prepare_BF16FlagAfter152157_core_drafts_v1_20261009.py',
        'prepare_BF16FlagAfter15222_round157_sources_v1_20261009.py','BF16FlagAfter152157_storage_v1_20261009.py',
        'verify_BF16FlagAfter152157_D_scoring_scope_v1_20261009.py','BF16FlagAfter152157_complete_parent_native_stage_v1_20261009.py',
        'predict_BF16FlagAfter152157_complete_parent_scheme_v1_20261009.py','verify_BF16FlagAfter15217_full_training_v1_20261009.py',
        'verify_BF16FlagAfter152157_native14_calendar_v1_20261009.py','run_BF16FlagAfter15222_official_comparison_v3_20261009.py',
        'prepare_BF16FlagAfter15222_selected_candidate_v1_20261009.py','seal_BF16FlagAfter15222_selected_candidate_v1_20261009.py',
        'run_BF16FlagAfter15222_round157_full_registration_v1_20261009.py','run_BF16FlagAfter152157_safe_registration_v1_20261010.py',
        'verify_BF16FlagAfter15222_prospective_routes_v2_20261010.py','verify_BF16FlagAfter15222_round157_sources_v1_20261010.py',
        'publish_BF16FlagAfter15222_evidence_v1_20261009.py',
    ]
    created=[]
    for name in names:
        src=A/name;target=A/transform(name,False);assert not target.exists()
        numeric=not any(w in name for w in ('native_stage','predict_','full_training','native14_calendar'))
        text=transform(src.read_text(encoding='utf8'),numeric)
        text=text.replace('actual_QA_collector_path_runtime_v43_20261009','actual_QA_collector_path_runtime_v44_20261010')
        if 'core_v62' in name:
            for old,new in [("'80':'22'",f"'80':'{count}'"),("'155':'157'",f"'155':'{number}'"),("'66':'68'",f"'66':'{qa}'"),("'438':'440'",f"'438':'{number+283}'")]:text=text.replace(old,new)
            text=text.replace("'actual22'",f"'actual{count}'")
        if 'official_comparison' in name:text=text.replace('i-5','i-'+str(len(anchors)))
        if 'native14_calendar' in name:text=text.replace("[('flag_valid',.008)]",repr([(role,.008)]))
        if 'prospective_routes' in name:
            for old,new in [('len(outputs)==5','len(outputs)=='+str(len(anchors))),('==40','=='+str(8*len(anchors))),
                ('==380','=='+str(76*len(anchors))),('len(baselines)==15','len(baselines)=='+str(3*len(anchors))),('len(sorts)==10','len(sorts)=='+str(2*len(anchors))),
                ("'prospective_sources':40","'prospective_sources':"+str(8*len(anchors))),
                ("'graph_controls':380","'graph_controls':"+str(76*len(anchors))),
                ("'baselines':15","'baselines':"+str(3*len(anchors))),
                ("'physical_model_ties':10","'physical_model_ties':"+str(2*len(anchors))),
                ('collect(157, 68, 22)',f'collect({number}, {qa}, {count})'),
                ("actual_full_QA_version': 68",f"actual_full_QA_version': {qa}"),
                ("namespace['snapshot'](157)",f"namespace['snapshot']({number})")]:text=text.replace(old,new)
        if 'round157_sources_v1_20261010' in name:
            text=text.replace('(40,380,15,10)',str((8*len(anchors),76*len(anchors),3*len(anchors),2*len(anchors))))
        if name.startswith('publish_'):
            text=text.replace("with safe(log),serial(log/'serial_mutex.json'),git_io(log/'file_backed_git'):",
                "with serial(log/'serial_mutex.json') as mutex,safe(log),git_io(log/'file_backed_git'):\n        mutex.acquire()")
        if name.startswith('seal_'):text=text.replace('actual22_day_prefix_model_controls','actual80_day_prefix_model_controls')
        if 'safe_registration_' in name:
            helper="    from contextlib import nullcontext\n    from run_dependency_queue_v3_20261006 import read as read_speed_proof\n    proof_path=A/'byte_exact_ranking_stream_benchmark_v1_20261010.json'\n    accelerated_writer=nullcontext()\n    if proof_path.is_file() and read_speed_proof(proof_path).get('adopt'):\n        from byte_exact_ranking_stream_runtime_v1_20261010 import installed as stream_writer\n        accelerated_writer=stream_writer()\n"
            point=text.index('    count=int(')
            text=text[:point]+helper+text[point:]
            helper_pub="    publication_encoder=nullcontext()\n    publication_proof_path=A/'full_ranking_JSON_decoder_benchmark_v2_20261010.json'\n    if publication_proof_path.is_file() and read_speed_proof(publication_proof_path).get('adopt_parameter_encoder'):\n        from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encode_publication\n        publication_encoder=encode_publication()\n"
            point=text.index('    count=int(');text=text[:point]+helper_pub+text[point:]
            text=text.replace('installed_transfer(),qa_paths():','installed_transfer(),qa_paths(),accelerated_writer,publication_encoder:')
            needle_sources='def main():\n'
            augmentation=f"    import prepare_{tag}Quality{count}_round{number}_sources_v1_20261009 as source_generator\n    original_sources=source_generator.source_paths\n    source_generator.source_paths=lambda:list(dict.fromkeys([*original_sources(),Path(__file__),A/'actual_QA_collector_path_runtime_v44_20261010.py',A/'actual_QA_collector_path_controls_v44_20261010.json',A/'byte_exact_ranking_stream_runtime_v1_20261010.py',A/'byte_exact_publication_encoder_runtime_v1_20261010.py',A/'byte_exact_publication_encoder_controls_v1_20261010.json',*([publication_proof_path] if publication_proof_path.is_file() else []),*([proof_path] if proof_path.is_file() else [])]))\n"
            text=text.replace(needle_sources,needle_sources+augmentation)

        if 'safe_registration_' in name:
            text=text.replace('from contextlib import nullcontext','from contextlib import nullcontext\n    from owned_idle_publication_wait_runtime_v1_20261010 import installed as idle_waiters')
            text=text.replace('accelerated_writer,publication_encoder:','accelerated_writer,publication_encoder,idle_waiters(log/\'owned_idle_watcher_waits.json\'):')
            text=text.replace("A/'byte_exact_publication_encoder_controls_v1_20261010.json'","A/'byte_exact_publication_encoder_controls_v1_20261010.json',A/'owned_idle_publication_wait_runtime_v1_20261010.py'")
        compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');created.append(target)
    plan=read(A/'BF16FlagAfter15222_round157_plan_v1_20261009.json')
    if grid==10:weights=[.004,.016,.064,.125,.25,.5,.75,1.]
    elif grid==0:weights=[.001,.002,.003,.004,.006,.008,.012,.016]
    elif grid==1:weights=[.000125,.00025,.0005,.024,.032,.048,.064,.096]
    elif grid==2:weights=[.00001,.00002,.00004,.00008,.125,.25,.5,1.]
    else:
        # Distinct bounded weights fixed before each new round; no test target or future forecast is consulted.
        fraction=(grid-2)/(grid+2)
        weights=sorted(set([.00003*fraction,.00007*fraction,.0003*fraction,.0007*fraction,.0035*fraction,.035*fraction,.35*fraction,.7*fraction]))
    cases=[{'role':role,'weight':0.,'sign':1.}]+[{'role':role,'weight':w,'sign':s} for s in (1.,-1.) for w in weights]
    model_name={'seed09':'rank_MLP2048_BF16_seed09_e64','seed10':'rank_MLP2048_BF16_seed10_e64','drop05':'rank_MLP2048_BF16_drop05_seed09_e64','topweightedhuber010':'rank_MLP2048_BF16_topweightedhuber010_seed09_e64'}[recipe]
    pins={str(A/'optimization_20261003_r152/full_registration_execution.json'):sha(A/'optimization_20261003_r152/full_registration_execution.json')}
    for year in range(2020,2026):
        for filename in ('info.json','model.joblib'):p=bank/str(year)/filename;pins[str(p)]=sha(p)
    plan.update(round=number,QA_version=qa,wave=number+283,new_cases=cases,qualified_anchor_rounds=anchors,anchor_rounds=anchors,
        expected_scored_records=count,expected_official_cases=count,model_name=model_name,native_bank=str(bank),actual_annual_bank=str(bank),
        graph_key='reusedNN'+str(number)+'_complete_parent_rank_CDF',configuration=read(bank/'2025/info.json')['configuration'],
        roles=[role],weights=weights,input_sha256=pins,status='frozen_training_only_reused_neural_frontier_before_own_quality')
    for old in ('BF16FlagAfter15222_round157_plan_v1_20261009.json','BF16FlagAfter15217_train_only_proposal_v1_20261009.json'):
        p=A/transform(old,False);create(p,plan);created.append(p)
    # Existing synthetic17 is only an algebraic route proof; actual full17 and own native14 remain mandatory.
    p=A/transform('BF16FlagAfter15217_synthetic17_cold51_v1_20261009.json',False)
    create(p,{'status':'reused_signed_rank_CDF_algebra_only_actual_full_and_native_checks_pending',
        'input_sha256':{str(A/'BF16FlagAfter15217_synthetic17_cold51_v1_20261009.json'):sha(A/'BF16FlagAfter15217_synthetic17_cold51_v1_20261009.json')},
        'actual_cases':17,'actual_cold_cases':51,'reused_not_new_controls':True});created.append(p)
    # The quality59 capsule pins the generated source; it has no score or candidate inference.
    quality=A/transform('run_BF16FlagAfter15222_official_comparison_v3_20261009.py',False)
    p=A/transform('BF16FlagAfter15222_quality_preparation_v59_20261009.json',False)
    create(p,{'status':'frozen_reused_neural_quality_sources_before_own_scores','input_sha256':{str(quality):sha(quality)}});created.append(p)
    p=A/transform('BF16FlagAfter152157_complete_native_predictor_preparation_v58_20261009.json',False)
    source_pins={str(p):sha(p) for p in created if p.suffix=='.py'}
    create(p,{'status':'prepared_derived_native_interface_actual_native14_and_full17_required','input_sha256':source_pins,
        'actual_future_X_read':False,'new_native_fits':0,'test_labels_read':False});created.append(p)
    p=A/transform('BF16FlagAfter152157_core_preparation_v62_20261009.json',False)
    create(p,{'status':'prepared_derived_full_candidate_seal_QA_receivers_without_quality_or_future_X','input_sha256':source_pins});created.append(p)
    module_name=transform('BF16FlagAfter152157_storage_v1_20261009',False)
    storage=__import__(module_name)
    for access,target in storage.OUTPUTS.items():
        assert not access.exists() and not target.exists()
        access.parent.mkdir(parents=True,exist_ok=True);target.mkdir(parents=True,exist_ok=False)
        quote=lambda value:"'"+str(value).replace("'","''")+"'"
        result=subprocess.run(['pwsh','-NoProfile','-NonInteractive','-Command',
            'New-Item -ItemType Junction -Path '+quote(access)+' -Target '+quote(target)+' | Out-Null'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr;storage.empty(access)
    for filename in ('verify_BF16FlagAfter152157_D_scoring_scope_v1_20261009.py','verify_BF16FlagAfter15222_prospective_routes_v2_20261010.py'):
        target=A/transform(filename,False)
        result=subprocess.run([sys.executable,'-B','-X','utf8',str(target)],cwd=ROOT,capture_output=True,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW)
        create(A/f'{tag}_{target.stem}_actual_preflight.json',{'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
        assert result.returncode==0,result.stderr
    return {'round':number,'count':count,'QA':qa,'tag':tag,'recipe':recipe,'role':role,'grid':grid,'predecessor':previous_service,
        'full17_driver':transform('verify_BF16FlagAfter15217_full_training_v1_20261009.py',False),
        'native14_driver':transform('verify_BF16FlagAfter152157_native14_calendar_v1_20261009.py',False),
        'created_source_sha256':{str(p):sha(p) for p in created},'new_native_fits':0,'test_labels_read':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--round',type=int,required=True);parser.add_argument('--recipe',required=True);parser.add_argument('--role',required=True);parser.add_argument('--grid',type=int,default=0)
    args=parser.parse_args();value=build(args.round,args.recipe,args.role,args.grid)
    create(A/f'ReusedNN{args.round}_prepared_frontier_v1_20261010.json',value);print(value['round'],value['count'],value['recipe'],value['role'],flush=True)
if __name__=='__main__':main()
