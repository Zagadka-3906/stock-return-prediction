"""Wait for136 full qualification, freeze the best complete parent and admit exact49/147 controls."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/HuberIRLS64_49_current_parent_v4_20261008')


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    closed('HuberIRLS64_18_native_historical_hooks_v3_20261008')
    closed('HuberIRLS64_historical_controls_main_publication_v2_20261008')
    closed('CrossFamily94_round136_full_registration_v4_20261008')
    plan_path=A/'HuberIRLS64_52_round137_plan_v2_20261008.json';plan=read(plan_path);baselines={}
    sources=[Path(__file__),plan_path,A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',
        A/'HuberIRLS64_historical_controls_main_v2_20261008/receipt.json']
    for number in plan['anchors']:
        folder=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        assert read(folder/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        metrics=read(folder/'calibrated_csv_official.json')['metrics'];prediction=read(candidate/'verification.json')
        assert prediction['status']=='passed' and read(candidate/'selection.json')['winner']['metrics']==metrics
        baselines[number]={'metrics':metrics,'physical_models':len(prediction['models'])}
        sources += [folder/name for name in ('selected_validation.npy','selection.json','calibrated_csv_official.json','full_registration_execution.json')]
        sources += [candidate/'verification.json',candidate/'manifest.json',receipt]
    parent=min(baselines,key=lambda n:(-baselines[n]['metrics']['final_score'],baselines[n]['physical_models'],n));assert parent in (134,135,136)
    old=Path(read(A/'actual_HuberIRLS64_49_parent134_location_v2_20261008.json')['output'])/'verification.json';old_proof=read(old)
    assert (old_proof['actual_full_cases'],old_proof['actual_cold_cases'])==(49,147)
    sources.append(old);pins={str(p):sha(p) for p in sources};assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_current_complete_parent.json',{'input_sha256':pins,'actual_parent_round':parent,'baselines':baselines,
        'qualified_original_official_scores_only':True,'actual_official_scores':0,'future_X_and_Y_read':False})
    if parent==134:
        for path,digest in old_proof['input_sha256'].items():assert sha(path)==digest,path
        assert sha(A/'optimization_20261003_r134/selected_validation.npy')==old_proof['parent_array_sha256']
        proof=deepcopy(old_proof);proof['controls_execution_mode']='exact_existing_parent134_49_full147cold_all_inputs_rehashed'
        proof['new_full_CDF_executions_by_current_parent_admission']=0;original=old
    else:
        source=A/'verify_HuberIRLS64_49_parent134_historical_v2_20261008.py';text=source.read_text(encoding='utf8')
        mapping={'_r134':f'_r{parent}','round134_receipt.json':f'round{parent}_receipt.json',
            'HuberIRLS64_49_parent134_historical_v2_20261008':'HuberIRLS64_49_current_parent_full_v4_20261008',
            'actual_HuberIRLS64_49_parent134_location_v2_20261008':'actual_HuberIRLS64_49_current_parent_full_location_v4_20261008',
            'passed_actual49_parent134_HuberIRLS64_full_CDF_and147_cold_controls':f'passed_actual49_parent{parent}_HuberIRLS64_full_CDF_and147_cold_controls',
            "'actual_historical_parent':134":f"'actual_historical_parent':{parent}","'actual_parent_round':134":f"'actual_parent_round':{parent}"}
        generated=text
        for before,after in mapping.items():generated=generated.replace(before,after)
        tree=ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node,ast.Constant) and isinstance(node.value,str):
                for before,after in mapping.items():node.value=node.value.replace(before,after)
            if isinstance(node,ast.Dict):
                for key,value in zip(node.keys,node.values):
                    if isinstance(key,ast.Constant) and key.value in ('actual_historical_parent','actual_parent_round') and isinstance(value,ast.Constant) and value.value==134:value.value=parent
        assert ast.dump(tree)==ast.dump(ast.parse(generated))
        create(OUT/'frozen_current_receiver_constants.json',{'original_source_sha256':sha(source),
            'generated_source_sha256':hashlib.sha256(generated.encode()).hexdigest(),'constant_mapping':mapping,'AST_math_and_control_flow_unchanged':True})
        target=OUT/f'actual_parent{parent}_receiver.py';target.write_text(generated,encoding='utf8',newline='\n')
        namespace={'__file__':str(source),'__name__':'actual_current_complete_parent_Huber49_controls'}
        exec(compile(generated,str(target),'exec'),namespace);namespace['main']()
        original=Path(read(A/'actual_HuberIRLS64_49_current_parent_full_location_v4_20261008.json')['output'])/'verification.json'
        proof=read(original);assert proof['actual_parent_round']==parent
        proof['controls_execution_mode']='new_actual49_full147cold_on_exact_qualified_complete_parent'
        proof['new_full_CDF_executions_by_current_parent_admission']=49
    for path,digest in pins.items():assert sha(path)==digest,path
    proof.update(status='passed_actual49_current_complete_parent_HuberIRLS64_CDF_and147_cold_controls',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),actual_comparison_parent_round=parent,actual_scheme_base_round=parent,
        baseline_metrics={n:row['metrics'] for n,row in baselines.items()},original_actual_controls_source=str(original),
        current_complete_parent_graph_sha256=sha(ROOT/f'candidates/optimization_20261003_r{parent}/verification.json'),
        input_sha256={**proof['input_sha256'],**pins,str(original):sha(original)},final137_exact_current_parent_controls_fulfilled=True,
        exact_current137_parent_controls_still_required_after136_qualification=False,actual_official_scores=0)
    create(OUT/'verification.json',proof)
    create(A/'actual_HuberIRLS64_49_current_parent_location_v4_20261008.json',{
        'status':'passed_actual_current_complete_parent49_Huber_CDF147cold_controls_on_E','output':str(OUT),
        'verification_sha256':sha(OUT/'verification.json'),'actual_comparison_parent_round':parent,'actual_quality_scores':0})


if __name__=='__main__':main()
