"""Prepare isolated Fourier-ridge role and standalone searches from frozen templates."""
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
    assert not any((HERE/f'optimization_20261003_r{n}/protocol.json').exists() for n in (43,44))
    assert not any((HERE/name/'verification.json').exists() for name in ('final_roles_round43_preflight_v2','standalone_round44_preflight_v2','fourier_ridge_round_baselines_qa_20261004'))
    before={};after={}
    roles=['optimize_training_round41.py','finalize_training_round41.py','run_training_round41_pipeline.py',
           'predict_final_roles_round41.py','verify_methods_round41.py','preflight_final_roles_round41_v2.py']
    pure=['optimize_training_round42.py','finalize_training_round42.py','run_training_round42_pipeline.py',
          'predict_standalone_round42.py','reuse_candidate_round42.py','verify_methods_round42.py','preflight_standalone_round42_v2.py']
    for kind,files,pairs in (
        ('roles',roles,{'round41':'round43','round40':'round42','r41':'r43','r40':'r42','Round41':'Round43','Round40':'Round42','183':'190','184':'191','185':'192','186':'193'}),
        ('pure',pure,{'round42':'round44','round41':'round43','r42':'r44','r41':'r43','Round42':'Round44','Round41':'Round43','187':'194','188':'195','189':'196'})):
        for filename in files:
            source=HERE/filename;text=adapt(source.read_text(encoding='utf-8'),pairs)
            for old,new in (
                ('additive_ridge_model_sources_20261004','fourier_ridge_model_sources_20261004'),
                ('train_additive_ridge_bank_20261004','train_fourier_ridge_bank_20261004'),
                ('verify_additive_ridge_bank_20261004','verify_fourier_ridge_bank_20261004'),
                ('additive_ridge_preflight_20261004','fourier_ridge_preflight_20261004'),
                ('additive_ridge_bank_20261004/oof_audit.json','fourier_ridge_bank_20261004/oof_audit.json'),
                ('verify_additive_ridge_round_baselines_20261004','verify_fourier_ridge_round_baselines_20261004'),
                ('additive_ridge_round_baselines_qa_20261004','fourier_ridge_round_baselines_qa_20261004')):
                text=text.replace(old,new)
            text=text.replace('固定分段基函数加性Ridge','固定随机傅里叶特征Ridge').replace('加性Ridge','傅里叶Ridge')
            text=text.replace('fixed hinge-basis one-day additive ridge backbones','fixed raw-plus-Fourier one-day ridge backbones')
            if kind=='roles':
                text=text.replace('additive_ridge_augmentation','fourier_ridge_augmentation').replace('additive_ridge_limit_delta','fourier_ridge_limit_delta')
                text=text.replace('additive_ridge_role_causal_checks','fourier_ridge_role_causal_checks')
                text=text.replace('waiting_for_previous_round_and_additive_ridge_bank','waiting_for_previous_round_and_fourier_ridge_bank')
                if filename.startswith(('optimize_','predict_')):
                    marker=".get('expanded_stacking_limit_delta',0.)";assert marker in text
                    text=text.replace(marker,marker+'+'+('self._foundation_configuration' if filename.startswith('optimize_') else 'winner')+".get('additive_ridge_limit_delta',0.)")
                text=text.replace("'complete_output_foundation_round':40","'complete_output_foundation_round':42")
                text=text.replace("'expected_scored_records':104","'expected_scored_records':104").replace("'new_fold_models_trained':24","'new_fold_models_trained':30").replace("'models_trained':24","'models_trained':30")
                if filename.startswith('run_'):text=text.replace("publish(41,","publish(43,").replace("'round':41","'round':43")
                text=text.replace('55模型样本外学习集成与首年回退对照的完整输出增量集成','固定随机傅里叶特征Ridge的完整输出增量集成').replace('12种55模型学习集成与首年回退独立用途比较','6种傅里叶Ridge独立用途比较')
                text=text.replace('All36 generic complete-output role','All18 generic complete-output role')
            else:
                text=re.sub(r'connected_topk0\d+_20261003','connected_topk0175_20261003',text)
                text=re.sub(r'len\(parsed\)==\d+','len(parsed)==1599600',text)
                if filename.startswith('optimize_'):
                    marker="    cfg['additive_ridge_augmentation']=deepcopy(cfg['final_augmentation']);cfg['additive_ridge_limit_delta']=0.\n";assert marker in text
                    text=text.replace(marker,marker+"    cfg['fourier_ridge_augmentation']=deepcopy(cfg['final_augmentation']);cfg['fourier_ridge_limit_delta']=0.\n")
                    text=text.replace("'expected_scored_records':258","'expected_scored_records':138")
                    text=text.replace('twelve55-parent learned stacking and first-year fallback schemes','six fixed hinge-basis one-day additive ridge backbones')
                text=text.replace('additive_ridge_role_causal_checks','fourier_ridge_role_causal_checks')
                if filename.startswith('run_'):text=text.replace("publish(42,","publish(44,").replace("'round':42","'round':44")
                text=text.replace('55模型样本外学习集成与首年回退对照的独立完整主模型比较','固定随机傅里叶特征Ridge的独立完整主模型比较').replace('12个55模型学习集成与首年回退主方案独立平滑与辅助信号比较','6个傅里叶Ridge主方案独立平滑与辅助信号比较')
            target=save(adapt(filename,pairs),text)
            before[str(source.resolve())]=hashlib.sha256(source.read_bytes()).hexdigest()
            after[str(target.resolve())]=hashlib.sha256(target.read_bytes()).hexdigest()
    record={'status':'sources_prepared_before_scoring','rounds':[43,44],'expected_records':{'43':104,'44':138},
        'new_annual_fits':30,'new_configurations':6,'test_labels_read':False,
        'construction':'Same complete-output role/standalone algorithms; foundation shift includes additive ridge, standalone clears all eleven augmentation groups.',
        'source_templates_sha256':before,'generated_sources_sha256':after}
    path=HERE/'fourier_ridge_rounds_prepared_20261004.json';payload=json.dumps(record,ensure_ascii=False,indent=2)+'\n'
    path.write_text(payload,encoding='utf-8',newline='\n')
    baseline=(HERE/'verify_additive_ridge_round_baselines_20261004.py').read_text(encoding='utf-8')
    baseline=adapt(baseline,{'round41':'round43','round42':'round44','Round41':'Round43','Round42':'Round44'})
    baseline=baseline.replace('additive_ridge_round_baselines_qa_20261004','fourier_ridge_round_baselines_qa_20261004').replace('additive_ridge_rounds_prepared_20261004','fourier_ridge_rounds_prepared_20261004')
    baseline=baseline.replace("'additive_ridge_augmentation':empty_roles(),'additive_ridge_limit_delta':0.}","'additive_ridge_augmentation':empty_roles(),'additive_ridge_limit_delta':0.,\n         'fourier_ridge_augmentation':empty_roles(),'fourier_ridge_limit_delta':0.}")
    baseline=baseline.replace("'expanded_stacking_limit_delta'),(.01,-.02,.03,.04,.05,-.06,.07)","'expanded_stacking_limit_delta','additive_ridge_limit_delta'),(.01,-.02,.03,.04,.05,-.06,.07,-.08)")
    baseline=baseline.replace("+shifted['expanded_stacking_limit_delta']","+shifted['expanded_stacking_limit_delta']+shifted['additive_ridge_limit_delta']")
    baseline=baseline.replace("'additive_ridge_augmentation'):","'additive_ridge_augmentation','fourier_ridge_augmentation'):")
    baseline=baseline.replace("'additive_ridge_limit_delta'):assert","'additive_ridge_limit_delta','fourier_ridge_limit_delta'):assert")
    baseline=baseline.replace('all_eight_foundation_limit_shift_components_forwarded','all_nine_foundation_limit_shift_components_forwarded').replace('standalone_clears_all_ten_augmentation_groups','standalone_clears_all_eleven_augmentation_groups')
    save('verify_fourier_ridge_round_baselines_20261004.py',baseline)
    checks=(HERE/'prepare_additive_ridge_checks_20261004.py').read_text(encoding='utf-8')
    checks=adapt(checks,{'round41':'round43','round42':'round44'}).replace('additive_ridge_bank_20261004','fourier_ridge_bank_20261004').replace('expanded-stacking','Fourier-ridge').replace('all60 annual forecast artifacts and24 distinct learned fits','all30 mature annual Fourier-ridge fits')
    checks=checks.replace('verify_additive_ridge_round_baselines_20261004','verify_fourier_ridge_round_baselines_20261004').replace('additive_ridge_round_baselines_qa_20261004','fourier_ridge_round_baselines_qa_20261004').replace('additive-ridge','Fourier-ridge')
    save('prepare_fourier_ridge_checks_20261004.py',checks)
    print(json.dumps({'status':record['status'],'files':len(after),'expected_records':record['expected_records']}))


if __name__=='__main__':main()
