"""Prepare67-member stacking role and standalone rounds before any scoring."""
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
    text=text.replace('verify_fourier_ridge_bank_20261004','verify_nonlinear_stacking_20261004')
    return text.replace('fourier_ridge','nonlinear_stacking').replace('固定随机傅里叶特征Ridge','67成员样本外学习集成').replace('傅里叶Ridge','67成员学习集成')


def main():
    assert not any((HERE/f'optimization_20261003_r{n}/protocol.json').exists() for n in (45,46))
    assert not any((HERE/name/'verification.json').exists() for name in ('final_roles_round45_preflight_v2','standalone_round46_preflight_v2','nonlinear_stacking_round_baselines_qa_20261004'))
    originals={};generated={}
    roles=['optimize_training_round43.py','finalize_training_round43.py','run_training_round43_pipeline.py','predict_final_roles_round43.py','verify_methods_round43.py','preflight_final_roles_round43_v2.py']
    pure=['optimize_training_round44.py','finalize_training_round44.py','run_training_round44_pipeline.py','predict_standalone_round44.py','reuse_candidate_round44.py','verify_methods_round44.py','preflight_standalone_round44_v2.py']
    for kind,files,pairs in (
        ('roles',roles,{'round43':'round45','round42':'round44','r43':'r45','r42':'r44','Round43':'Round45','Round42':'Round44','190':'197','191':'198','192':'199','193':'200'}),
        ('pure',pure,{'round44':'round46','round43':'round45','r44':'r46','r43':'r45','Round44':'Round46','Round43':'Round45','194':'201','195':'202','196':'203'})):
        for filename in files:
            source=HERE/filename;text=method(adapt(source.read_text(encoding='utf-8'),pairs))
            if kind=='roles':
                if filename.startswith(('optimize_','predict_')):
                    marker=".get('additive_ridge_limit_delta',0.)";assert marker in text
                    prefix='self._foundation_configuration' if filename.startswith('optimize_') else 'winner'
                    text=text.replace(marker,marker+'+'+prefix+".get('fourier_ridge_limit_delta',0.)")
                text=text.replace("'complete_output_foundation_round':42","'complete_output_foundation_round':44")
                text=text.replace("'expected_scored_records':104","'expected_scored_records':176")
                text=text.replace("'new_fold_models_trained':30","'new_fold_models_trained':24").replace("'models_trained':30","'models_trained':24")
                text=text.replace('All18 generic complete-output role','All36 generic complete-output role').replace('6种67成员学习集成','12种67成员学习集成')
                if filename.startswith('run_'):text=text.replace('publish(43,','publish(45,').replace("'round':43","'round':45")
            else:
                if filename.startswith('optimize_'):
                    marker="    cfg['nonlinear_stacking_augmentation']=deepcopy(cfg['final_augmentation']);cfg['nonlinear_stacking_limit_delta']=0.\n";assert marker in text
                    text=text.replace(marker,"    cfg['fourier_ridge_augmentation']=deepcopy(cfg['final_augmentation']);cfg['fourier_ridge_limit_delta']=0.\n"+marker)
                    text=text.replace("'expected_scored_records':138","'expected_scored_records':258")
                text=text.replace('six fixed hinge-basis one-day additive ridge backbones','twelve67-parent learned stacking and paired first-year policies').replace('6个67成员学习集成','12个67成员学习集成')
                if filename.startswith('run_'):text=text.replace('publish(44,','publish(46,').replace("'round':44","'round':46")
            target=save(adapt(filename,pairs),text)
            originals[str(source.resolve())]=hashlib.sha256(source.read_bytes()).hexdigest();generated[str(target.resolve())]=hashlib.sha256(target.read_bytes()).hexdigest()
    baseline=method(adapt((HERE/'verify_fourier_ridge_round_baselines_20261004.py').read_text(encoding='utf-8'),{'round43':'round45','round44':'round46','Round43':'Round45','Round44':'Round46'}))
    marker="'nonlinear_stacking_augmentation':empty_roles(),'nonlinear_stacking_limit_delta':0.}"
    assert marker in baseline
    baseline=baseline.replace(marker,"'fourier_ridge_augmentation':empty_roles(),'fourier_ridge_limit_delta':0.,\n         "+marker)
    marker="'additive_ridge_limit_delta'),(.01,-.02,.03,.04,.05,-.06,.07,-.08)";assert marker in baseline
    baseline=baseline.replace(marker,"'additive_ridge_limit_delta','fourier_ridge_limit_delta'),(.01,-.02,.03,.04,.05,-.06,.07,-.08,.09)")
    baseline=baseline.replace("+shifted['additive_ridge_limit_delta']","+shifted['additive_ridge_limit_delta']+shifted['fourier_ridge_limit_delta']")
    baseline=baseline.replace("'nonlinear_stacking_augmentation'):","'fourier_ridge_augmentation','nonlinear_stacking_augmentation'):")
    baseline=baseline.replace("'nonlinear_stacking_limit_delta'):assert","'fourier_ridge_limit_delta','nonlinear_stacking_limit_delta'):assert")
    baseline=baseline.replace('all_nine_foundation_limit_shift_components_forwarded','all_ten_foundation_limit_shift_components_forwarded').replace('standalone_clears_all_eleven_augmentation_groups','standalone_clears_all_twelve_augmentation_groups')
    save('verify_nonlinear_stacking_round_baselines_20261004.py',baseline)
    checks=method(adapt((HERE/'prepare_fourier_ridge_checks_20261004.py').read_text(encoding='utf-8'),{'round43':'round45','round44':'round46'}))
    checks=checks.replace('all30 mature annual Fourier-ridge fits','all60 annual artifacts and24 distinct67-member fits').replace('Fourier-ridge','67-member stacking')
    save('prepare_nonlinear_stacking_checks_20261004.py',checks)
    record={'status':'sources_prepared_before_scoring','rounds':[45,46],'expected_records':{'45':176,'46':258},
        'new_annual_fits':24,'new_scheme_configurations':12,'annual_forecast_artifacts':60,'test_data_read':False,
        'construction':'Same complete-output algorithms; cumulative shift includes Fourier ridge. Standalone clears all12 augmentation groups.',
        'source_templates_sha256':originals,'generated_sources_sha256':generated}
    (HERE/'nonlinear_stacking_rounds_prepared_20261004.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':record['status'],'files':len(generated),'expected_records':record['expected_records']}))


if __name__=='__main__':main()
