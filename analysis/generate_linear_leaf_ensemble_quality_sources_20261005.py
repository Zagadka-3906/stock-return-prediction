"""Generate full declared composite-scheme searches without changing frozen predecessors."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'
def remap(text):
    text=text.replace('linear_leaf','linear_leaf_ensemble').replace('train_linear_leaf_ensemble_bank','build_linear_leaf_ensemble_bank')
    mapping={69:71,70:72,283:290,284:291,285:292,286:293,287:294,288:295,289:296}
    return re.sub(r'(?<![0-9])(?:69|70|283|284|285|286|287|288|289)(?![0-9])',lambda match:str(mapping[int(match[0])]),text)
def create(name,text):
    path=HERE/name;compile(text,str(path),'exec')
    with path.open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)
    return str(path),hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    generated,originals={},{}
    names=['scheme_runtime','search_engine_v2','predict_linear_leaf_scheme','predict_linear_leaf_scheme_v2','check_linear_leaf_scheme','verify_linear_leaf_search_generators_v2','run_linear_leaf_round_v2']
    files=['linear_leaf_scheme_runtime_20261005.py','linear_leaf_search_engine_v2_20261005.py',
           'predict_linear_leaf_scheme_20261005.py','predict_linear_leaf_scheme_v2_20261005.py',
           'check_linear_leaf_scheme_20261005.py','verify_linear_leaf_search_generators_v2_20261005.py','run_linear_leaf_round_v2_20261005.py']
    for filename in files:
        path=HERE/filename;originals[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        target=filename.replace('linear_leaf','linear_leaf_ensemble');text=remap(path.read_text(encoding='utf-8'))
        if 'search_engine' in target:
            text=text.replace("cfg.get('kind')=='neural_ensemble'","cfg.get('kind') in ('neural_ensemble','linear_leaf_ensemble')")
            text=text.replace("proof=ROOT/'analysis/linear_leaf_ensemble_preflight_20261005/verification.json'","proof=bank.OUT/'oof_audit.json'")
            text=text.replace("assert ns.read(proof)['status']=='passed_actual_linear_leaf_ensemble_maturity_native_reload_and_prefix_controls'","assert ns.read(proof)['status']=='passed' and ns.read(proof)['actual_virtual_annual_outputs']==40 and ns.read(proof)['actual_annual_fits']==0")
            text=text.replace("gates=[bank.OUT/'oof_audit.json',", "gates=[bank.OUT/'construction_execution_scope.json',bank.OUT/'oof_audit.json',")
            text=text.replace('124 if number==71 else 138','148 if number==71 else 178')
            text=text.replace('[73,8,18,25] if number==71 else [37,84,17]','[97,8,18,25] if number==71 else [49,112,17]')
            text=text.replace("'previous_linear_leaf_ensemble_bank_actual_annual_fits':30,'new_native_model_configurations':6", "'previous_linear_leaf_ensemble_bank_actual_annual_fits':0,'previous_linear_leaf_ensemble_bank_virtual_annual_outputs':40,'actual_native_parent_annual_fits':30,'new_virtual_model_configurations':8")
            text=text.replace('all6_new_native_models','all8_new_virtual_models')
            text=text.replace('matched constant andlinear leaf complete graph','fixed weight composite complete graph')
            text=text.replace("ROOT/'analysis/linear_leaf_ensemble_future_codec_adapter_20261005.py',", "ROOT/'analysis/linear_leaf_ensemble_future_codec_adapter_20261005.py',ROOT/'analysis/linear_leaf_future_codec_adapter_20261005.py',")
            text=text.replace("for path in gates:assert ns.read(path)['status']=='passed',path", "for path in gates:assert ns.read(path)['status']=='passed',path\n        assert ns.read(gates[2])['actual_virtual_final_artifacts']==8 and ns.read(gates[2])['actual_new_final_fits']==0")
        if 'run_linear_leaf_ensemble_round' in target:
            text=text.replace('actual30_annual6_final','actual40_virtual_annual8_virtual_final')
            text=text.replace("'native_configs': 6", "'virtual_configs': 8,'new_model_fits':0,'actual_parent_annual_fits':30")
            text=text.replace('普通树叶与线性树叶模型','普通树与线性树固定权重集成')
            text=text.replace('匹配参数的普通树叶与线性树叶LightGBM完整方案','成熟普通树与线性树固定权重集成完整方案')
        if target=='predict_linear_leaf_ensemble_scheme_20261005.py':
            text=text.replace("'linear_leaf_ensemble_future_codec_adapter_20261005.py',", "'linear_leaf_ensemble_future_codec_adapter_20261005.py', 'linear_leaf_future_codec_adapter_20261005.py',")
        if 'check_linear_leaf_ensemble' in target:text=text.replace('all6_new_models_checked','all8_new_virtual_models_checked')
        if 'verify_linear_leaf_ensemble_search_generators' in target:
            text=text.replace('[73, 8, 18, 25] if number == 71 else [37, 84, 17]','[97, 8, 18, 25] if number == 71 else [49, 112, 17]')
            text=text.replace('124 if number == 71 else 138','148 if number == 71 else 178')
            text=text.replace('actual_R68_and_R71','actual_R70_and_R71')
        generated.update([create(target,text)])
    for number in (71,72):
        previous=number-1
        wrapper=f'import sys\nimport optimize_training_round{previous}_v2 as previous\nsys.modules["optimize_training_round{previous}"] = previous\nfrom linear_leaf_ensemble_search_engine_v2_20261005 import install\ninstall({number}, globals())\n'
        generated.update([create(f'optimize_training_round{number}_v2.py',wrapper)])
        generated.update([create(f'optimize_training_round{number}.py',f'from optimize_training_round{number}_v2 import *\n')])
        generated.update([create(f'run_training_round{number}_v2_pipeline.py',f'from run_linear_leaf_ensemble_round_v2_20261005 import main\nif __name__=="__main__":main({number})\n')])
        generated.update([create(f'finalize_training_round{number}.py',remap((HERE/f'finalize_training_round{number-2}.py').read_text(encoding='utf-8')))])
    plan=HERE/'linear_leaf_ensemble_complete_search_plan_20261005.json'
    assert json.loads(plan.read_text(encoding='utf-8'))['expected_total_records']=={'71':148,'72':178}
    with (HERE/'linear_leaf_ensemble_source_generation_20261005.json').open('x',encoding='utf-8') as stream:
        json.dump({'status':'prepared_complete_grid_before_actual_official_quality','original_sources_preserved_sha256':originals,'generated_source_sha256':generated,'existing_frozen_plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'planned_virtual_annual_artifacts':40,'planned_new_annual_fits':0,'planned_quality_records':326,'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'generated_before_actual_quality','generated_files':len(generated),'expected_records':{'71':148,'72':178}},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
