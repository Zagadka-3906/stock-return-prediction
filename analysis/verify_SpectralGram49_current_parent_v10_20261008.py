"""Control the exact fully qualified parent of139 using only training validation arrays."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/SpectralGram49_current_parent_v10_20261008')


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    for name in ('SpectralGram24_native_historical_hooks_v2_20261008',
        'SpectralGram140_historical_causal_main_publication_v1_20261008',
        'HuberCrossFamily112_round139_full_registration_v10_20261008'):closed(name)
    plan_path=A/'SpectralGram52_round140_plan_v1_20261008.json';plan=read(plan_path)
    sources=[Path(__file__),plan_path,A/'SpectralGram64_complete_parent_CDF_v1_20261008.py'];baselines={}
    for number in plan['anchors']:
        folder=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        assert read(folder/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        metrics=read(folder/'calibrated_csv_official.json')['metrics'];prediction=read(candidate/'verification.json')
        assert prediction['status']=='passed' and read(candidate/'selection.json')['winner']['metrics']==metrics
        assert len(prediction['models'])==len({row['sha256'] for row in prediction['models'].values()})
        baselines[number]={'metrics':metrics,'physical_models':len(prediction['models'])}
        sources += [folder/name for name in ('selected_validation.npy','selection.json','calibrated_csv_official.json','full_registration_execution.json')]
        sources += [candidate/'verification.json',candidate/'manifest.json',receipt]
    parent=min(baselines,key=lambda n:(-baselines[n]['metrics']['final_score'],baselines[n]['physical_models'],n))
    old=Path(read(A/'actual_SpectralGram49_parent134_location_v1_20261008.json')['output'])/'verification.json'
    old_proof=read(old);assert old_proof['actual_full_cases']==49 and old_proof['actual_cold_cases']==147;sources.append(old)
    pins={str(p):sha(p) for p in sources};assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_current_parent_before_actual_controls.json',{'input_sha256':pins,'actual_parent_round':parent,
        'baselines':baselines,'official_S_then_physical_SHA_count_parent_selection':True,'actual_future_X_and_Y_read':False})
    if sha(A/f'optimization_20261003_r{parent}/selected_validation.npy')==old_proof['parent_array_sha256']:
        for path,digest in old_proof['input_sha256'].items():assert sha(path)==digest,path
        proof=deepcopy(old_proof);original=old
        proof['controls_execution_mode']='reused_actual49_147_transform_controls_on_bit_identical_parent_array_with_all_inputs_rehashed'
        proof['new_full_CDF_executions_by_current_parent_admission']=0
        proof['current_parent_native_candidate_not_reused_by_this_math_check']=True
    else:
        source=A/'verify_SpectralGram49_parent134_historical_v1_20261008.py';text=source.read_text(encoding='utf8')
        mapping={'_r134':f'_r{parent}','round134_receipt.json':f'round{parent}_receipt.json',
            'SpectralGram49_parent134_historical_v1_20261008':'SpectralGram49_current_parent_full_v10_20261008',
            'actual_SpectralGram49_parent134_location_v1_20261008':'actual_SpectralGram49_current_parent_full_location_v10_20261008',
            'parent134':f'parent{parent}',"'actual_parent_round':134":f"'actual_parent_round':{parent}"}
        generated=text
        for before,after in mapping.items():generated=generated.replace(before,after)
        def normalize(tree):
            for node in ast.walk(tree):
                if isinstance(node,ast.Constant) and isinstance(node.value,str):
                    for before,after in mapping.items():node.value=node.value.replace(before,after)
                if isinstance(node,ast.Dict):
                    for key,value in zip(node.keys,node.values):
                        if isinstance(key,ast.Constant) and key.value=='actual_parent_round' and isinstance(value,ast.Constant) and value.value==134:value.value=parent
            return ast.dump(tree)
        assert normalize(ast.parse(text))==ast.dump(ast.parse(generated))
        create(OUT/'frozen_actual_current_parent_receiver.json',{'original_source_sha256':sha(source),
            'generated_source_sha256':hashlib.sha256(generated.encode()).hexdigest(),'constant_mapping':mapping,'AST_math_and_control_flow_unchanged':True})
        target=OUT/'actual_current_parent_receiver.py';target.write_text(generated,encoding='utf8',newline='\n')
        namespace={'__file__':str(source),'__name__':'actual_current_parent109_full_CDF_controls'}
        exec(compile(generated,str(target),'exec'),namespace);namespace['main']()
        original=Path(read(A/'actual_SpectralGram49_current_parent_full_location_v10_20261008.json')['output'])/'verification.json'
        proof=read(original);assert proof['actual_parent_round']==parent
        proof['controls_execution_mode']='new_actual49_current_parent_full_and147_cold_controls'
        proof['new_full_CDF_executions_by_current_parent_admission']=49
    for path,digest in pins.items():assert sha(path)==digest,path
    proof.update(status='passed_actual49_current_parent_SpectralGram_CDF_and147_cold_controls',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        actual_comparison_parent_round=parent,actual_scheme_base_round=parent,baseline_metrics={n:row['metrics'] for n,row in baselines.items()},
        original_actual_controls_source=str(original),input_sha256={**proof['input_sha256'],**pins,str(original):sha(original)},
        final140_exact_current_parent_controls_fulfilled=True,final140_current_parent_controls_still_required_after139_is_qualified=False,
        actual_official_scores=0)
    create(OUT/'verification.json',proof)
    create(A/'actual_SpectralGram49_current_parent_location_v10_20261008.json',{'status':'passed_current_parent49_147_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_comparison_parent_round':parent,'actual_quality_scores':0})
    print('Exact qualified140 parent admitted by completed49/147 controls: '+str(parent),flush=True)


if __name__=='__main__':main()
