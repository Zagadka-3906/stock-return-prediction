"""Prepare matched Fourier controls as complete role and standalone schemes."""
from pathlib import Path
import ast
import json
import hashlib
from prepare_fourier_ridge_rounds_20261004 import adapt
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def save(name,text):
    ast.parse(text,filename=name);path=HERE/name;path.write_text(text,encoding='utf-8',newline='\n');return path


def method(text):
    text=text.replace('verify_nonlinear_stacking_20261004','verify_fourier_tuning_bank_20261004')
    return text.replace('nonlinear_stacking','fourier_tuning').replace('67成员样本外学习集成','傅里叶容量正则与种子匹配对照').replace('67成员学习集成','傅里叶匹配对照')


def main():
    assert not any((HERE/f'optimization_20261003_r{n}/protocol.json').exists() for n in (47,48))
    assert not any((HERE/name/'verification.json').exists() for name in ('final_roles_round47_preflight_v2','standalone_round48_preflight_v2','fourier_tuning_round_baselines_qa_20261004'))
    originals={};generated={}
    roles=['optimize_training_round45.py','finalize_training_round45.py','run_training_round45_pipeline.py','predict_final_roles_round45.py','verify_methods_round45.py','preflight_final_roles_round45_v2.py']
    pure=['optimize_training_round46.py','finalize_training_round46.py','run_training_round46_pipeline.py','predict_standalone_round46.py','reuse_candidate_round46.py','verify_methods_round46.py','preflight_standalone_round46_v2.py']
    for kind,files,pairs in (
        ('roles',roles,{'round45':'round47','round44':'round46','r45':'r47','r44':'r46','Round45':'Round47','Round44':'Round46','197':'204','198':'205','199':'206','200':'207'}),
        ('pure',pure,{'round46':'round48','round45':'round47','r46':'r48','r45':'r47','Round46':'Round48','Round45':'Round47','201':'208','202':'209','203':'210'})):
        for filename in files:
            source=HERE/filename;text=method(adapt(source.read_text(encoding='utf-8'),pairs))
            if kind=='roles':
                if filename.startswith(('optimize_','predict_')):
                    marker=".get('fourier_ridge_limit_delta',0.)";assert marker in text
                    prefix='self._foundation_configuration' if filename.startswith('optimize_') else 'winner'
                    text=text.replace(marker,marker+'+'+prefix+".get('nonlinear_stacking_limit_delta',0.)")
                text=text.replace("'complete_output_foundation_round':44","'complete_output_foundation_round':46")
                text=text.replace("'expected_scored_records':176","'expected_scored_records':152")
                text=text.replace("'new_fold_models_trained':24","'new_fold_models_trained':50").replace("'models_trained':24","'models_trained':50")
                text=text.replace('All36 generic complete-output role','All30 generic complete-output role').replace('12种傅里叶匹配对照','10种傅里叶匹配对照')
                if filename.startswith('run_'):text=text.replace('publish(45,','publish(47,').replace("'round':45","'round':47")
            else:
                if filename.startswith('optimize_'):
                    marker="    cfg['fourier_tuning_augmentation']=deepcopy(cfg['final_augmentation']);cfg['fourier_tuning_limit_delta']=0.\n";assert marker in text
                    text=text.replace(marker,"    cfg['nonlinear_stacking_augmentation']=deepcopy(cfg['final_augmentation']);cfg['nonlinear_stacking_limit_delta']=0.\n"+marker)
                    text=text.replace("'expected_scored_records':258","'expected_scored_records':218")
                text=text.replace('twelve67-parent learned stacking and paired first-year policies','ten Fourier capacity/penalty/seed one-day backbones').replace('12个傅里叶匹配对照','10个傅里叶匹配对照')
                if filename.startswith('run_'):text=text.replace('publish(46,','publish(48,').replace("'round':46","'round':48")
            target=save(adapt(filename,pairs),text)
            originals[str(source.resolve())]=hashlib.sha256(source.read_bytes()).hexdigest();generated[str(target.resolve())]=hashlib.sha256(target.read_bytes()).hexdigest()
    baseline=method(adapt((HERE/'verify_nonlinear_stacking_round_baselines_20261004.py').read_text(encoding='utf-8'),{'round45':'round47','round46':'round48','Round45':'Round47','Round46':'Round48'}))
    marker="'fourier_tuning_augmentation':empty_roles(),'fourier_tuning_limit_delta':0.}";assert marker in baseline
    baseline=baseline.replace(marker,"'nonlinear_stacking_augmentation':empty_roles(),'nonlinear_stacking_limit_delta':0.,\n         "+marker)
    marker="'fourier_ridge_limit_delta'),(.01,-.02,.03,.04,.05,-.06,.07,-.08,.09)";assert marker in baseline
    baseline=baseline.replace(marker,"'fourier_ridge_limit_delta','nonlinear_stacking_limit_delta'),(.01,-.02,.03,.04,.05,-.06,.07,-.08,.09,-.1)")
    baseline=baseline.replace("+shifted['fourier_ridge_limit_delta']","+shifted['fourier_ridge_limit_delta']+shifted['nonlinear_stacking_limit_delta']")
    baseline=baseline.replace("'fourier_tuning_augmentation'):","'nonlinear_stacking_augmentation','fourier_tuning_augmentation'):")
    baseline=baseline.replace("'fourier_tuning_limit_delta'):assert","'nonlinear_stacking_limit_delta','fourier_tuning_limit_delta'):assert")
    baseline=baseline.replace('all_ten_foundation_limit_shift_components_forwarded','all_eleven_foundation_limit_shift_components_forwarded').replace('standalone_clears_all_twelve_augmentation_groups','standalone_clears_all_thirteen_augmentation_groups')
    save('verify_fourier_tuning_round_baselines_20261004.py',baseline)
    checks=method(adapt((HERE/'prepare_nonlinear_stacking_checks_20261004.py').read_text(encoding='utf-8'),{'round45':'round47','round46':'round48'}))
    checks=checks.replace('all60 annual artifacts and24 distinct67-member fits','all50 matched Fourier annual fits').replace('67-member stacking','Fourier tuning')
    save('prepare_fourier_tuning_checks_20261004.py',checks)
    record={'status':'sources_prepared_before_scoring','rounds':[47,48],'expected_records':{'47':152,'48':218},
        'new_annual_fits':50,'new_configurations':10,'test_data_read':False,
        'construction':'Same complete-output algorithms; cumulative shift includes67-parent stacking. Standalone clears all13 augmentation groups.',
        'source_templates_sha256':originals,'generated_sources_sha256':generated}
    (HERE/'fourier_tuning_rounds_prepared_20261004.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':record['status'],'files':len(generated),'expected_records':record['expected_records']}))


if __name__=='__main__':main()
