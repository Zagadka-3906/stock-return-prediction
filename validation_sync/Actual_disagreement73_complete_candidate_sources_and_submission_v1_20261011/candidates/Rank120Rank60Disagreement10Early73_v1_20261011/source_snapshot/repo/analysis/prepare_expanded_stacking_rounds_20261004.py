"""Prepare55-parent stacking role/standalone rounds without changing predecessors."""
from pathlib import Path
import ast
import hashlib
import json
import re
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def adapt(text,pairs):
    return re.sub('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)),lambda m:pairs[m.group()],text)


def main():
    before={};after={}
    assert not any((HERE/f'optimization_20261003_r{n}/protocol.json').exists() for n in (39,40))
    roles=['optimize_training_round37.py','finalize_training_round37.py','run_training_round37_pipeline.py',
           'predict_final_roles_round37.py','verify_methods_round37.py','preflight_final_roles_round37_v2.py']
    pure=['optimize_training_round38.py','finalize_training_round38.py','run_training_round38_pipeline.py',
          'predict_standalone_round38.py','reuse_candidate_round38.py','verify_methods_round38.py','preflight_standalone_round38_v2.py']
    for kind,files,pairs in (
        ('roles',roles,{'round37':'round39','round36':'round38','r37':'r39','r36':'r38','Round37':'Round39','Round36':'Round38','169':'176','170':'177','171':'178','172':'179'}),
        ('pure',pure,{'round38':'round40','round37':'round39','r38':'r40','r37':'r39','Round38':'Round40','Round37':'Round39','173':'180','174':'181','175':'182'})):
        for filename in files:
            source=HERE/filename;text=adapt(source.read_text(encoding='utf-8'),pairs)
            text=text.replace('catboost_tuning_model_sources_20261004','expanded_stacking_model_sources_20261004')
            text=text.replace('train_catboost_tuning_bank_20261004','train_expanded_stacking_bank_20261004')
            text=text.replace('verify_catboost_tuning_20261004','verify_expanded_stacking_20261004')
            text=text.replace('catboost_tuning_preflight_20261004','expanded_stacking_preflight_20261004')
            text=text.replace('catboost_tuning_bank_20261004/oof_audit.json','expanded_stacking_bank_20261004/oof_audit.json')
            text=text.replace('verify_catboost_tuning_round_baselines_20261004','verify_expanded_stacking_round_baselines_20261004')
            text=text.replace('catboost_tuning_round_baselines_qa_20261004','expanded_stacking_round_baselines_qa_20261004')
            if kind=='roles':
                text=text.replace('catboost_tuning_augmentation','expanded_stacking_augmentation').replace('catboost_tuning_limit_delta','expanded_stacking_limit_delta')
                text=text.replace('catboost_tuning_role_causal_checks','expanded_stacking_role_causal_checks')
                text=text.replace('waiting_for_previous_round_and_catboost_tuning_bank','waiting_for_previous_round_and_expanded_stacking_bank')
                if filename.startswith(('optimize_','predict_')):
                    marker=".get('neural_tuning_limit_delta',0.)";assert marker in text
                    text=text.replace(marker,marker+'+'+('self._foundation_configuration' if filename.startswith('optimize_') else 'winner')+".get('catboost_tuning_limit_delta',0.)")
                text=text.replace("'complete_output_foundation_round':36","'complete_output_foundation_round':38")
                text=text.replace("'expected_scored_records':92","'expected_scored_records':176").replace("'new_fold_models_trained':25","'new_fold_models_trained':24").replace("'models_trained':25","'models_trained':24")
                if filename.startswith('run_'):
                    text=text.replace("publish(37,","publish(39,").replace("'round':37","'round':39")
                    text=text.replace('CatBoost学习率预算正则与深度的完整输出增量集成','55模型样本外学习集成与首年回退对照的完整输出增量集成').replace('5种CatBoost匹配模型独立用途比较','12种55模型学习集成与首年回退独立用途比较')
                text=text.replace('All15 generic complete-output role','All36 generic complete-output role')
            else:
                if filename.startswith('optimize_'):
                    marker="    cfg['catboost_tuning_augmentation']=deepcopy(cfg['final_augmentation']);cfg['catboost_tuning_limit_delta']=0.\n";assert marker in text
                    text=text.replace(marker,marker+"    cfg['expanded_stacking_augmentation']=deepcopy(cfg['final_augmentation']);cfg['expanded_stacking_limit_delta']=0.\n")
                    text=text.replace('catboost_tuning_role_causal_checks','expanded_stacking_role_causal_checks')
                    text=text.replace("'expected_scored_records':118","'expected_scored_records':258")
                    text=text.replace('five matched CatBoost learning-rate/budget/regularization/depth backbones','twelve55-parent learned stacking and first-year fallback schemes')
                if filename.startswith('run_'):
                    text=text.replace("publish(38,","publish(40,").replace("'round':38","'round':40")
                    text=text.replace('catboost_tuning_role_causal_checks','expanded_stacking_role_causal_checks')
                    text=text.replace('CatBoost学习率预算正则与深度的独立完整主模型比较','55模型样本外学习集成与首年回退对照的独立完整主模型比较').replace('5个CatBoost匹配主模型独立平滑与辅助信号比较','12个55模型学习集成与首年回退主方案独立平滑与辅助信号比较')
            target=HERE/adapt(filename,pairs);ast.parse(text,filename=str(target))
            if target.exists():assert target.read_text(encoding='utf-8')==text,target
            else:target.write_text(text,encoding='utf-8',newline='\n')
            before[str(source.resolve())]=hashlib.sha256(source.read_bytes()).hexdigest();after[str(target.resolve())]=hashlib.sha256(target.read_bytes()).hexdigest()
    record={'status':'sources_prepared_before_scoring','rounds':[39,40],'expected_records':{'39':176,'40':258},
        'new_annual_fits':24,'new_scheme_configurations':12,'annual_forecast_artifacts':60,
        'paired_later_year_reused_fits':24,'fixed_first_year_artifacts':12,
        'construction':'Unchanged complete-output role/standalone algorithms; cumulative foundation shift includes CatBoost tuning. Standalone replacements clear all nine augmentation groups.',
        'test_labels_read':False,'source_templates_sha256':before,'generated_sources_sha256':after}
    destination=HERE/'expanded_stacking_rounds_prepared_20261004.json';payload=json.dumps(record,ensure_ascii=False,indent=2)+'\n'
    if destination.exists():assert destination.read_text(encoding='utf-8')==payload
    else:destination.write_text(payload,encoding='utf-8',newline='\n')
    baseline=(HERE/'verify_catboost_tuning_round_baselines_20261004.py').read_text(encoding='utf-8')
    baseline=adapt(baseline,{'round37':'round39','round38':'round40','Round37':'Round39','Round38':'Round40'})
    baseline=baseline.replace('catboost_tuning_round_baselines_qa_20261004','expanded_stacking_round_baselines_qa_20261004').replace('catboost_tuning_rounds_prepared_20261004','expanded_stacking_rounds_prepared_20261004')
    baseline=baseline.replace("'catboost_tuning_augmentation':empty_roles(),'catboost_tuning_limit_delta':0.}","'catboost_tuning_augmentation':empty_roles(),'catboost_tuning_limit_delta':0.,\n         'expanded_stacking_augmentation':empty_roles(),'expanded_stacking_limit_delta':0.}")
    baseline=baseline.replace("'neural_tuning_limit_delta'),(.01,-.02,.03,.04,.05)","'neural_tuning_limit_delta','catboost_tuning_limit_delta'),(.01,-.02,.03,.04,.05,-.06)")
    baseline=baseline.replace("+shifted['neural_tuning_limit_delta']","+shifted['neural_tuning_limit_delta']+shifted['catboost_tuning_limit_delta']")
    baseline=baseline.replace("'catboost_tuning_augmentation'):","'catboost_tuning_augmentation','expanded_stacking_augmentation'):")
    baseline=baseline.replace("'catboost_tuning_limit_delta'):assert","'catboost_tuning_limit_delta','expanded_stacking_limit_delta'):assert")
    baseline=baseline.replace('all_six_foundation_limit_shift_components_forwarded','all_seven_foundation_limit_shift_components_forwarded').replace('standalone_clears_all_eight_augmentation_groups','standalone_clears_all_nine_augmentation_groups')
    checks=(HERE/'prepare_catboost_tuning_checks_20261004.py').read_text(encoding='utf-8')
    checks=adapt(checks,{'round37':'round39','round38':'round40'}).replace('catboost_tuning_bank_20261004','expanded_stacking_bank_20261004').replace('CatBoost-tuning','expanded-stacking').replace('all25 mature annual models','all60 annual forecast artifacts and24 distinct learned fits')
    observer=(HERE/'observe_catboost_tuning_resources_20261004.py').read_text(encoding='utf-8').replace('catboost_tuning_','expanded_stacking_').replace('catboost_training_root_pid','expanded_training_root_pid').replace('completed_tuning_annual_models','completed_expanded_annual_artifacts')
    for filename,text in [('verify_expanded_stacking_round_baselines_20261004.py',baseline),('prepare_expanded_stacking_checks_20261004.py',checks),('observe_expanded_stacking_resources_20261004.py',observer)]:
        ast.parse(text,filename=filename);path=HERE/filename
        if path.exists():assert path.read_text(encoding='utf-8')==text,path
        else:path.write_text(text,encoding='utf-8',newline='\n')
    print(json.dumps({'status':record['status'],'files':len(after),'auxiliary_files':3,'expected_records':record['expected_records']}))


if __name__=='__main__':main()
