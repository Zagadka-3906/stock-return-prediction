"""Admit the exact complete current parent after135 closes, with honest original134 control reuse."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/CrossFamily91_current_parent_v2_20261008')


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    closed('CrossFamily15_native_historical_hooks_v1_20261008')
    closed('CrossFamily_preliminary_controls_main_publication_v1_20261008')
    closed('BF16wide40_round135_full_registration_v7_20261008')
    plan_path=A/'CrossFamily94_round136_plan_v1_20261008.json';plan=read(plan_path)
    baselines={};sources=[Path(__file__),plan_path,A/'CrossFamily_complete_parent_CDF_v1_20261008.py',
        A/'CrossFamily_preliminary_controls_main_v1_20261008/historical/receipt.json']
    for number in plan['anchor_rounds']:
        folder=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        assert read(folder/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        metrics=read(folder/'calibrated_csv_official.json')['metrics'];prediction=read(candidate/'verification.json')
        assert prediction['status']=='passed' and read(candidate/'selection.json')['winner']['metrics']==metrics
        baselines[number]={'metrics':metrics,'physical_models':len(prediction['models'])}
        sources += [folder/name for name in ('selected_validation.npy','selection.json','calibrated_csv_official.json','full_registration_execution.json')]
        sources += [candidate/'verification.json',candidate/'manifest.json',receipt]
    parent=min(baselines,key=lambda n:(-baselines[n]['metrics']['final_score'],baselines[n]['physical_models'],n))
    assert parent in (134,135) and baselines[parent]['metrics']['final_score']>=baselines[134]['metrics']['final_score']
    old=Path(read(A/'actual_CrossFamily91_parent134_location_v1_20261008.json')['output'])/'verification.json'
    old_proof=read(old);assert old_proof['actual_full_cases']==91 and old_proof['actual_cold_cases']==273
    sources.append(old)
    pins={str(p):sha(p) for p in sources}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_current_parent_before_actual_controls.json',{'input_sha256':pins,'actual_parent_round':parent,'baselines':baselines,
        'parent_selection_uses_only_qualified_official_training_scores':True,'actual_future_X_and_labels_read':False,'new_quality_scores':0})
    if parent==134:
        for path,digest in old_proof['input_sha256'].items():assert sha(path)==digest,path
        assert sha(A/'optimization_20261003_r134/selected_validation.npy')==old_proof['parent_array_sha256']
        proof=deepcopy(old_proof);proof['controls_execution_mode']='reused_actual91_parent134_full_and273_cold_controls_with_all_inputs_rehashed'
        proof['new_full_CDF_executions_by_current_parent_admission']=0
        original=old
    else:
        # Execute the same immutable full91 arithmetic/CDF receiver with only exact parent/output constants adapted.
        source=A/'verify_CrossFamily91_parent134_historical_v1_20261008.py';text=source.read_text(encoding='utf8')
        mapping={'_r134':'_r135','round134_receipt.json':'round135_receipt.json',
            'CrossFamily91_parent134_historical_v1_20261008':'CrossFamily91_current_parent_full_v2_20261008',
            'actual_CrossFamily91_parent134_location_v1_20261008':'actual_CrossFamily91_current_parent_full_location_v2_20261008',
            'passed_actual91_full_parent134_historical_crossfamily_CDF_and273_cold_controls':'passed_actual91_full_parent135_historical_crossfamily_CDF_and273_cold_controls',
            "'parent_round':134":"'parent_round':135","'actual_parent_round':134":"'actual_parent_round':135"}
        generated=text
        for before,after in mapping.items():generated=generated.replace(before,after)
        original_ast=ast.parse(text);adapted_ast=ast.parse(generated)
        # Every changed AST node is a declared parent/output constant; no math or control-flow changes.
        def normalize(tree):
            for node in ast.walk(tree):
                if isinstance(node,ast.Constant) and isinstance(node.value,str):
                    for before,after in mapping.items():node.value=node.value.replace(before,after)
                if isinstance(node,ast.Dict):
                    for key,value in zip(node.keys,node.values):
                        if isinstance(key,ast.Constant) and key.value in ('parent_round','actual_parent_round') and isinstance(value,ast.Constant) and value.value==134:value.value=135
            return ast.dump(tree)
        assert normalize(original_ast)==ast.dump(adapted_ast)
        create(OUT/'frozen_actual_parent135_receiver.json',{'original_source':str(source),'original_source_sha256':sha(source),
            'generated_source_sha256':hashlib.sha256(generated.encode()).hexdigest(),'constant_mapping':mapping,'AST_math_and_control_flow_unchanged':True})
        (OUT/'actual_parent135_receiver.py').write_text(generated,encoding='utf8',newline='\n')
        namespace={'__file__':str(source),'__name__':'actual_current_parent135_full_CDF_controls'}
        exec(compile(generated,str(OUT/'actual_parent135_receiver.py'),'exec'),namespace);namespace['main']()
        original=Path(read(A/'actual_CrossFamily91_current_parent_full_location_v2_20261008.json')['output'])/'verification.json'
        proof=read(original);proof['controls_execution_mode']='new_actual91_parent135_full_and273_cold_controls'
        proof['new_full_CDF_executions_by_current_parent_admission']=91
        assert proof['actual_parent_round']==135
    for path,digest in pins.items():assert sha(path)==digest,path
    proof.update(status='passed_actual91_current_parent_CrossFamily_CDF_and273_cold_controls',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        actual_comparison_parent_round=parent,actual_scheme_base_round=parent,baseline_metrics={n:row['metrics'] for n,row in baselines.items()},
        original_actual_controls_source=str(original),current_complete_parent_graph_sha256=sha(ROOT/f'candidates/optimization_20261003_r{parent}/verification.json'),
        input_sha256={**proof['input_sha256'],**pins,str(original):sha(original)},final136_exact_current_parent_controls_fulfilled=True,
        final136_current_parent_controls_still_required_after135_is_qualified=False,actual_official_scores=0)
    create(OUT/'verification.json',proof)
    create(A/'actual_CrossFamily91_current_parent_location_v2_20261008.json',{'status':'passed_actual_current_parent91_CDF273_cold_controls_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_comparison_parent_round':parent,'actual_quality_scores':0})
    print(f'Exact qualified current parent{parent}:91 actual full CDF/273 cold controls admitted before136 scoring.',flush=True)


if __name__=='__main__':main()
