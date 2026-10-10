"""Prospective role/standalone rounds for the five matched CatBoost variants."""
from pathlib import Path
import ast
import hashlib
import json
import re
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def adapt(text,pairs):
    return re.sub('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)),lambda match:pairs[match.group()],text)


def main():
    before={};after={}
    assert not any((HERE/f'optimization_20261003_r{n}/protocol.json').exists() for n in (37,38))
    assert not any((HERE/f'{stem}/verification.json').exists() for stem in ('final_roles_round37_preflight_v2','standalone_round38_preflight_v2','catboost_tuning_round_baselines_qa_20261004'))
    roles=['optimize_training_round35.py','finalize_training_round35.py','run_training_round35_pipeline.py',
           'predict_final_roles_round35.py','verify_methods_round35.py','preflight_final_roles_round35_v2.py']
    pure=['optimize_training_round36.py','finalize_training_round36.py','run_training_round36_pipeline.py',
          'predict_standalone_round36.py','reuse_candidate_round36.py','verify_methods_round36.py','preflight_standalone_round36_v2.py']
    for kind,files,pairs in (
        ('roles',roles,{'round35':'round37','round34':'round36','r35':'r37','r34':'r36','Round35':'Round37','Round34':'Round36','162':'169','163':'170','164':'171','165':'172'}),
        ('pure',pure,{'round36':'round38','round35':'round37','r36':'r38','r35':'r37','Round36':'Round38','Round35':'Round37','166':'173','167':'174','168':'175'})):
        for filename in files:
            source=HERE/filename;text=adapt(source.read_text(encoding='utf-8'),pairs)
            text=text.replace('neural_tuning_model_sources_20261004','catboost_tuning_model_sources_20261004')
            text=text.replace('train_neural_tuning_bank_20261004','train_catboost_tuning_bank_20261004')
            text=text.replace('verify_neural_tuning_20261004','verify_catboost_tuning_20261004')
            text=text.replace('neural_tuning_preflight_20261004','catboost_tuning_preflight_20261004')
            text=text.replace('neural_tuning_bank_20261004/oof_audit.json','catboost_tuning_bank_20261004/oof_audit.json')
            text=text.replace('verify_neural_tuning_round_baselines_20261004','verify_catboost_tuning_round_baselines_20261004')
            text=text.replace('neural_tuning_round_baselines_qa_20261004','catboost_tuning_round_baselines_qa_20261004')
            if kind=='roles':
                text=text.replace('neural_tuning_augmentation','catboost_tuning_augmentation').replace('neural_tuning_limit_delta','catboost_tuning_limit_delta')
                text=text.replace('neural_tuning_role_causal_checks','catboost_tuning_role_causal_checks')
                text=text.replace('waiting_for_previous_round_and_neural_tuning_bank','waiting_for_previous_round_and_catboost_tuning_bank')
                if filename.startswith(('optimize_','predict_')):
                    marker=".get('stacking_limit_delta',0.)";assert marker in text,filename
                    text=text.replace(marker,marker+'+'+('self._foundation_configuration' if filename.startswith('optimize_') else 'winner')+".get('neural_tuning_limit_delta',0.)")
                text=text.replace("'complete_output_foundation_round':34","'complete_output_foundation_round':36")
                if filename.startswith('run_'):
                    text=text.replace("publish(35,","publish(37,").replace("'round':35","'round':37")
                    text=text.replace('标签中心与学习率对照的完整输出增量集成','CatBoost学习率预算正则与深度的完整输出增量集成').replace('5种标签中心与学习率模型独立用途比较','5种CatBoost匹配模型独立用途比较')
            else:
                if filename.startswith('optimize_'):
                    marker="    cfg['neural_tuning_augmentation']=deepcopy(cfg['final_augmentation']);cfg['neural_tuning_limit_delta']=0.\n";assert marker in text
                    text=text.replace(marker,marker+"    cfg['catboost_tuning_augmentation']=deepcopy(cfg['final_augmentation']);cfg['catboost_tuning_limit_delta']=0.\n")
                    text=text.replace('neural_tuning_role_causal_checks','catboost_tuning_role_causal_checks')
                    text=text.replace('matched rank512 target-offset/learning-rate backbones','matched CatBoost learning-rate/budget/regularization/depth backbones')
                if filename.startswith('run_'):
                    text=text.replace("publish(36,","publish(38,").replace("'round':36","'round':38")
                    text=text.replace('neural_tuning_role_causal_checks','catboost_tuning_role_causal_checks')
                    text=text.replace('标签中心与学习率对照的独立完整主模型比较','CatBoost学习率预算正则与深度的独立完整主模型比较').replace('5个标签中心与学习率主模型独立平滑与辅助信号比较','5个CatBoost匹配主模型独立平滑与辅助信号比较')
            target=HERE/adapt(filename,pairs);ast.parse(text,filename=str(target))
            if target.exists():assert target.read_text(encoding='utf-8')==text,target
            else:target.write_text(text,encoding='utf-8',newline='\n')
            before[str(source.resolve())]=hashlib.sha256(source.read_bytes()).hexdigest()
            after[str(target.resolve())]=hashlib.sha256(target.read_bytes()).hexdigest()
    record={'status':'sources_prepared_before_scoring','rounds':[37,38],'expected_records':{'37':92,'38':118},
        'new_annual_fits':25,'new_configurations':5,
        'construction':'Reuse fully tested complete-output role/standalone algorithms. Role foundation shifts include prior neural tuning; standalone replacements clear all eight augmentation groups.',
        'test_labels_read':False,'source_templates_sha256':before,'generated_sources_sha256':after}
    destination=HERE/'catboost_tuning_rounds_prepared_20261004.json';payload=json.dumps(record,ensure_ascii=False,indent=2)+'\n'
    if destination.exists():assert destination.read_text(encoding='utf-8')==payload
    else:destination.write_text(payload,encoding='utf-8',newline='\n')
    # Independent diagnostics and runtime observer get their own source files.
    baseline=(HERE/'verify_neural_tuning_round_baselines_20261004.py').read_text(encoding='utf-8')
    baseline=adapt(baseline,{'round35':'round37','round36':'round38','Round35':'Round37','Round36':'Round38'})
    baseline=baseline.replace('neural_tuning_round_baselines_qa_20261004','catboost_tuning_round_baselines_qa_20261004').replace('neural_tuning_rounds_prepared_20261004','catboost_tuning_rounds_prepared_20261004')
    baseline=baseline.replace("'neural_tuning_augmentation':empty_roles(),'neural_tuning_limit_delta':0.}","'neural_tuning_augmentation':empty_roles(),'neural_tuning_limit_delta':0.,\n         'catboost_tuning_augmentation':empty_roles(),'catboost_tuning_limit_delta':0.}")
    baseline=baseline.replace("'stacking_limit_delta'),(.01,-.02,.03,.04)","'stacking_limit_delta','neural_tuning_limit_delta'),(.01,-.02,.03,.04,.05)")
    baseline=baseline.replace("+shifted['stacking_limit_delta']","+shifted['stacking_limit_delta']+shifted['neural_tuning_limit_delta']")
    baseline=baseline.replace("'neural_tuning_augmentation'):","'neural_tuning_augmentation','catboost_tuning_augmentation'):")
    baseline=baseline.replace("'neural_tuning_limit_delta'):assert","'neural_tuning_limit_delta','catboost_tuning_limit_delta'):assert")
    baseline=baseline.replace('all_five_foundation_limit_shift_components_forwarded','all_six_foundation_limit_shift_components_forwarded').replace('standalone_clears_all_seven_augmentation_groups','standalone_clears_all_eight_augmentation_groups')
    checks=(HERE/'prepare_neural_tuning_checks_20261004.py').read_text(encoding='utf-8')
    checks=adapt(checks,{'round35':'round37','round36':'round38'}).replace('neural_tuning_bank_20261004','catboost_tuning_bank_20261004').replace('neural-tuning','CatBoost-tuning')
    observer=(HERE/'observe_neural_tuning_resources_20261004.py').read_text(encoding='utf-8')
    observer=observer.replace('neural_tuning_','catboost_tuning_').replace('neural_training_root_pid','catboost_training_root_pid')
    for filename,text in [('verify_catboost_tuning_round_baselines_20261004.py',baseline),('prepare_catboost_tuning_checks_20261004.py',checks),('observe_catboost_tuning_resources_20261004.py',observer)]:
        ast.parse(text,filename=filename);path=HERE/filename
        if path.exists():assert path.read_text(encoding='utf-8')==text,path
        else:path.write_text(text,encoding='utf-8',newline='\n')
    print(json.dumps({'status':record['status'],'prediction_and_pipeline_files':len(after),'auxiliary_files':3,'expected_records':record['expected_records']}))


if __name__=='__main__':main()
