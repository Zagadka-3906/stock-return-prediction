"""Prospectively extend frozen R33/R34 construction to the matched neural grid."""
from pathlib import Path
import ast
import hashlib
import json
import re
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def adapt(text,pairs):
    return re.sub('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)),
                  lambda match:pairs[match.group()],text)


def trainer_sources(text):
    first=text.index('             Path(trainer.__file__),')
    end=text.index("             ROOT/'analysis/score_calibrated_candidates_20261003.py'",first)
    return text[:first]+"             Path(trainer.__file__),ROOT/'analysis/train_neural_tuning_bank_20261004.py',\n             ROOT/'analysis/verify_neural_tuning_20261004.py',ROOT/'analysis/neural_tuning_preflight_20261004/verification.json',\n             trainer.OUT/'protocol.json',trainer.OUT/'oof_audit.json',\n"+text[end:]


def main():
    generated={};before={}
    prepared=HERE/'neural_tuning_rounds_prepared_20261004.json'
    old_prepared=json.loads(prepared.read_text(encoding='utf-8')) if prepared.exists() else None
    assert not any((HERE/f'optimization_20261003_r{n}/protocol.json').exists() for n in (35,36))
    assert not any((HERE/f'{stem}/verification.json').exists() for stem in ('final_roles_round35_preflight_v2','standalone_round36_preflight_v2','neural_tuning_round_baselines_qa_20261004'))
    roles=['optimize_training_round33.py','finalize_training_round33.py','run_training_round33_pipeline.py',
           'predict_final_roles_round33.py','verify_methods_round33.py','preflight_final_roles_round33_v2.py']
    pure=['optimize_training_round34.py','finalize_training_round34.py','run_training_round34_pipeline.py',
          'predict_standalone_round34.py','reuse_candidate_round34.py','verify_methods_round34.py',
          'preflight_standalone_round34_v2.py']
    for kind,files,pairs in (
        ('roles',roles,{'round33':'round35','round32':'round34','r33':'r35','r32':'r34',
                       'Round33':'Round35','Round32':'Round34','155':'162','156':'163','157':'164','158':'165'}),
        ('pure',pure,{'round34':'round36','round33':'round35','r34':'r36','r33':'r35',
                      'Round34':'Round36','Round33':'Round35','159':'166','160':'167','161':'168'})):
        for filename in files:
            source=HERE/filename;original=source.read_text(encoding='utf-8');text=original
            if filename.startswith('optimize_'):text=trainer_sources(text)
            text=adapt(text,pairs).replace('stacking_model_sources_20261004','neural_tuning_model_sources_20261004')
            text=text.replace('oof_stacking_bank_20261004/oof_audit.json','neural_tuning_bank_20261004/oof_audit.json')
            text=text.replace('verify_stacking_round_baselines_20261004_v2.py','verify_neural_tuning_round_baselines_20261004.py').replace('stacking_round_baselines_qa_20261004_v2/verification.json','neural_tuning_round_baselines_qa_20261004/verification.json')
            if kind=='roles':
                text=text.replace('stacking_augmentation','neural_tuning_augmentation').replace('stacking_limit_delta','neural_tuning_limit_delta')
                text=text.replace('stacking_role_causal_checks','neural_tuning_role_causal_checks')
                if filename.startswith(('optimize_','predict_')):
                    marker=".get('regularization_limit_delta',0.)"
                    assert marker in text,filename
                    text=text.replace(marker,marker+"+"+("self._foundation_configuration" if filename.startswith('optimize_') else 'winner')+".get('stacking_limit_delta',0.)")
                if filename.startswith('optimize_'):
                    text=text.replace("'expected_scored_records':104","'expected_scored_records':92")
                    text=text.replace("'new_fold_models_trained':24","'new_fold_models_trained':25").replace("'models_trained':24","'models_trained':25")
                    text=text.replace("'complete_output_foundation_round':32","'complete_output_foundation_round':34")
                if filename.startswith('run_'):
                    text=text.replace("publish(33,","publish(35,")
                    text=text.replace("'round':33","'round':35")
                    text=text.replace('历史样本外学习集成的完整输出增量集成','标签中心与学习率对照的完整输出增量集成').replace('6种历史样本外学习集成独立用途比较','5种标签中心与学习率模型独立用途比较')
                    text=text.replace('waiting_for_previous_round_and_stacking_bank','waiting_for_previous_round_and_neural_tuning_bank')
                    text=text.replace("    last_notice=time.monotonic()","    gates += [ROOT/'analysis/final_roles_round35_preflight_v2/verification.json',ROOT/'analysis/neural_tuning_round_baselines_qa_20261004/verification.json']\n    last_notice=time.monotonic()",1)
                text=text.replace('All18 generic complete-output role','All15 generic complete-output role')
            else:
                if filename.startswith('optimize_'):
                    marker="    cfg['stacking_augmentation']=deepcopy(cfg['final_augmentation']);cfg['stacking_limit_delta']=0.\n"
                    assert marker in text
                    text=text.replace(marker,marker+"    cfg['neural_tuning_augmentation']=deepcopy(cfg['final_augmentation']);cfg['neural_tuning_limit_delta']=0.\n")
                    text=text.replace("'expected_scored_records':138","'expected_scored_records':118")
                    text=text.replace('Waves166–168: compare complete standalone outputs of all six mature past-OOF learned stacking backbones.','Waves166–168: compare five matched rank512 target-offset/learning-rate backbones.')
                    text=text.replace('stacking_role_causal_checks','neural_tuning_role_causal_checks')
                if filename.startswith('run_'):
                    text=text.replace("publish(34,","publish(36,").replace("'round':34","'round':36")
                    text=text.replace('stacking_role_causal_checks','neural_tuning_role_causal_checks')
                    text=text.replace('历史样本外学习集成的独立完整主模型比较','标签中心与学习率对照的独立完整主模型比较').replace('6个学习集成主模型独立平滑与辅助信号比较','5个标签中心与学习率主模型独立平滑与辅助信号比较')
                    text=text.replace("    last_notice=time.monotonic()","    gates += [ROOT/'analysis/standalone_round36_preflight_v2/verification.json',ROOT/'analysis/neural_tuning_round_baselines_qa_20261004/verification.json']\n    last_notice=time.monotonic()",1)
            target=HERE/adapt(filename,pairs)
            ast.parse(text,filename=str(target))
            if target.exists() and target.read_text(encoding='utf-8')!=text:
                assert old_prepared and hashlib.sha256(target.read_bytes()).hexdigest()==old_prepared['generated_sources_sha256'][str(target.resolve())],target
            target.write_text(text,encoding='utf-8',newline='\n')
            before[str(source.resolve())]=hashlib.sha256(source.read_bytes()).hexdigest()
            generated[str(target.resolve())]=hashlib.sha256(target.read_bytes()).hexdigest()
    record={'status':'sources_prepared_before_scoring','new_rounds':[35,36],
            'new_model_names':['rank512_o05_lr0005_e32','rank512_o05_lr002_e32','rank512_o0_lr0005_e32','rank512_o0_lr001_e32','rank512_o0_lr002_e32'],
            'expected_records':{'35':92,'36':118},'new_annual_fits':25,
            'construction':'Same complete-output role and standalone algorithms as R33/R34, with all prior groups retained in the frozen baseline and cleared for standalone replacements. Foundation cumulative limit shifts include stacking.',
            'test_labels_read':False,'source_templates_sha256':before,'generated_sources_sha256':generated}
    destination=HERE/'neural_tuning_rounds_prepared_20261004.json'
    payload=json.dumps(record,ensure_ascii=False,indent=2)+'\n'
    destination.write_text(payload,encoding='utf-8',newline='\n')
    print(json.dumps({'status':record['status'],'files':len(generated),'expected_records':record['expected_records']},ensure_ascii=False))


if __name__=='__main__':main()
