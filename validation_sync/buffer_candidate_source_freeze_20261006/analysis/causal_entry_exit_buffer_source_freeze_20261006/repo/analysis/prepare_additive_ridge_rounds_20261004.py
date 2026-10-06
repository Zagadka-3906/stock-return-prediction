"""Prepare isolated additive-ridge role and standalone searches from frozen templates."""
from pathlib import Path
import ast
import hashlib
import json
import re
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def adapt(text,pairs):
    pattern='|'.join(('(?<![0-9.])'+re.escape(k)+'(?![0-9])') if k.isdigit() else re.escape(k) for k in sorted(pairs,key=len,reverse=True))
    return re.sub(pattern,lambda m:pairs[m.group()],text)


def save(name,text):
    ast.parse(text,filename=name);path=HERE/name
    path.write_text(text,encoding='utf-8',newline='\n')
    return path


def main():
    assert not any((HERE/f'optimization_20261003_r{n}/protocol.json').exists() for n in (41,42))
    assert not any((HERE/name/'verification.json').exists() for name in ('final_roles_round41_preflight_v2','standalone_round42_preflight_v2','additive_ridge_round_baselines_qa_20261004'))
    before={};after={}
    roles=['optimize_training_round39.py','finalize_training_round39.py','run_training_round39_pipeline.py',
           'predict_final_roles_round39.py','verify_methods_round39.py','preflight_final_roles_round39_v2.py']
    pure=['optimize_training_round40.py','finalize_training_round40.py','run_training_round40_pipeline.py',
          'predict_standalone_round40.py','reuse_candidate_round40.py','verify_methods_round40.py','preflight_standalone_round40_v2.py']
    for kind,files,pairs in (
        ('roles',roles,{'round39':'round41','round38':'round40','r39':'r41','r38':'r40','Round39':'Round41','Round38':'Round40','176':'183','177':'184','178':'185','179':'186'}),
        ('pure',pure,{'round40':'round42','round39':'round41','r40':'r42','r39':'r41','Round40':'Round42','Round39':'Round41','180':'187','181':'188','182':'189'})):
        for filename in files:
            source=HERE/filename;text=adapt(source.read_text(encoding='utf-8'),pairs)
            for old,new in (
                ('expanded_stacking_model_sources_20261004','additive_ridge_model_sources_20261004'),
                ('train_expanded_stacking_bank_20261004','train_additive_ridge_bank_20261004'),
                ('verify_expanded_stacking_20261004','verify_additive_ridge_bank_20261004'),
                ('expanded_stacking_preflight_20261004','additive_ridge_preflight_20261004'),
                ('expanded_stacking_bank_20261004/oof_audit.json','additive_ridge_bank_20261004/oof_audit.json'),
                ('verify_expanded_stacking_round_baselines_20261004','verify_additive_ridge_round_baselines_20261004'),
                ('expanded_stacking_round_baselines_qa_20261004','additive_ridge_round_baselines_qa_20261004')):
                text=text.replace(old,new)
            if kind=='roles':
                text=text.replace('expanded_stacking_augmentation','additive_ridge_augmentation').replace('expanded_stacking_limit_delta','additive_ridge_limit_delta')
                text=text.replace('expanded_stacking_role_causal_checks','additive_ridge_role_causal_checks')
                text=text.replace('waiting_for_previous_round_and_expanded_stacking_bank','waiting_for_previous_round_and_additive_ridge_bank')
                if filename.startswith(('optimize_','predict_')):
                    marker=".get('catboost_tuning_limit_delta',0.)";assert marker in text
                    text=text.replace(marker,marker+'+'+('self._foundation_configuration' if filename.startswith('optimize_') else 'winner')+".get('expanded_stacking_limit_delta',0.)")
                text=text.replace("'complete_output_foundation_round':38","'complete_output_foundation_round':40")
                text=text.replace("'expected_scored_records':183","'expected_scored_records':104").replace("'new_fold_models_trained':24","'new_fold_models_trained':30").replace("'models_trained':24","'models_trained':30")
                if filename.startswith('run_'):text=text.replace("publish(39,","publish(41,").replace("'round':39","'round':41")
                text=text.replace('55模型样本外学习集成与首年回退对照的完整输出增量集成','固定分段基函数加性Ridge的完整输出增量集成').replace('12种55模型学习集成与首年回退独立用途比较','6种加性Ridge独立用途比较')
                text=text.replace('All36 generic complete-output role','All18 generic complete-output role')
            else:
                text=re.sub(r'connected_topk0\d+_20261003','connected_topk0175_20261003',text)
                text=re.sub(r'len\(parsed\)==\d+','len(parsed)==1599600',text)
                if filename.startswith('optimize_'):
                    marker="    cfg['expanded_stacking_augmentation']=deepcopy(cfg['final_augmentation']);cfg['expanded_stacking_limit_delta']=0.\n";assert marker in text
                    text=text.replace(marker,marker+"    cfg['additive_ridge_augmentation']=deepcopy(cfg['final_augmentation']);cfg['additive_ridge_limit_delta']=0.\n")
                    text=text.replace("'expected_scored_records':258","'expected_scored_records':138")
                    text=text.replace('twelve55-parent learned stacking and first-year fallback schemes','six fixed hinge-basis one-day additive ridge backbones')
                text=text.replace('expanded_stacking_role_causal_checks','additive_ridge_role_causal_checks')
                if filename.startswith('run_'):text=text.replace("publish(40,","publish(42,").replace("'round':40","'round':42")
                text=text.replace('55模型样本外学习集成与首年回退对照的独立完整主模型比较','固定分段基函数加性Ridge的独立完整主模型比较').replace('12个55模型学习集成与首年回退主方案独立平滑与辅助信号比较','6个加性Ridge主方案独立平滑与辅助信号比较')
            target=save(adapt(filename,pairs),text)
            before[str(source.resolve())]=hashlib.sha256(source.read_bytes()).hexdigest()
            after[str(target.resolve())]=hashlib.sha256(target.read_bytes()).hexdigest()
    record={'status':'sources_prepared_before_scoring','rounds':[41,42],'expected_records':{'41':104,'42':138},
        'new_annual_fits':30,'new_configurations':6,'test_labels_read':False,
        'construction':'Same complete-output role/standalone algorithms; foundation shift includes expanded stacking, standalone clears all ten augmentation groups.',
        'source_templates_sha256':before,'generated_sources_sha256':after}
    path=HERE/'additive_ridge_rounds_prepared_20261004.json';payload=json.dumps(record,ensure_ascii=False,indent=2)+'\n'
    path.write_text(payload,encoding='utf-8',newline='\n')
    baseline=(HERE/'verify_expanded_stacking_round_baselines_20261004.py').read_text(encoding='utf-8')
    baseline=adapt(baseline,{'round39':'round41','round40':'round42','Round39':'Round41','Round40':'Round42'})
    baseline=baseline.replace('expanded_stacking_round_baselines_qa_20261004','additive_ridge_round_baselines_qa_20261004').replace('expanded_stacking_rounds_prepared_20261004','additive_ridge_rounds_prepared_20261004')
    baseline=baseline.replace("'expanded_stacking_augmentation':empty_roles(),'expanded_stacking_limit_delta':0.}","'expanded_stacking_augmentation':empty_roles(),'expanded_stacking_limit_delta':0.,\n         'additive_ridge_augmentation':empty_roles(),'additive_ridge_limit_delta':0.}")
    baseline=baseline.replace("'catboost_tuning_limit_delta'),(.01,-.02,.03,.04,.05,-.06)","'catboost_tuning_limit_delta','expanded_stacking_limit_delta'),(.01,-.02,.03,.04,.05,-.06,.07)")
    baseline=baseline.replace("+shifted['catboost_tuning_limit_delta']","+shifted['catboost_tuning_limit_delta']+shifted['expanded_stacking_limit_delta']")
    baseline=baseline.replace("'expanded_stacking_augmentation'):","'expanded_stacking_augmentation','additive_ridge_augmentation'):")
    baseline=baseline.replace("'expanded_stacking_limit_delta'):assert","'expanded_stacking_limit_delta','additive_ridge_limit_delta'):assert")
    baseline=baseline.replace('all_seven_foundation_limit_shift_components_forwarded','all_eight_foundation_limit_shift_components_forwarded').replace('standalone_clears_all_nine_augmentation_groups','standalone_clears_all_ten_augmentation_groups')
    save('verify_additive_ridge_round_baselines_20261004.py',baseline)
    checks=(HERE/'prepare_expanded_stacking_checks_20261004.py').read_text(encoding='utf-8')
    checks=adapt(checks,{'round39':'round41','round40':'round42'}).replace('expanded_stacking_bank_20261004','additive_ridge_bank_20261004').replace('expanded-stacking','additive-ridge').replace('all60 annual forecast artifacts and24 distinct learned fits','all30 mature annual additive-ridge fits')
    checks=checks.replace("for script,proof_name in (","for script,proof_name in (\n        ('verify_additive_ridge_round_baselines_20261004.py','additive_ridge_round_baselines_qa_20261004'),")
    save('prepare_additive_ridge_checks_20261004.py',checks)
    print(json.dumps({'status':record['status'],'files':len(after),'expected_records':record['expected_records']}))


if __name__=='__main__':main()
