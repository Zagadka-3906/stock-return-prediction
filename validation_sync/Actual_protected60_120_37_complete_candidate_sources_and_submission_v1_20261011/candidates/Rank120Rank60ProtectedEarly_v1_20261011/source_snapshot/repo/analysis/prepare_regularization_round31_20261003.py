"""Prepare regularization role additions after complete-layer refinement."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]


def main():
    for prefix,suffix in (('optimize_training_round',''),('finalize_training_round',''),
            ('verify_methods_round',''),('predict_final_roles_round',''),
            ('preflight_final_roles_round',''),('run_training_round','_pipeline')):
        target=ROOT/f'analysis/{prefix}31{suffix}.py';assert not target.exists()
        text=(ROOT/f'analysis/{prefix}29{suffix}.py').read_text(encoding='utf-8')
        text=text.replace('Round29','Round31').replace('round29','round31').replace('_r29','_r31')
        text=text.replace('round28','round30').replace('_r28','_r30')
        text=text.replace("'round':29","'round':31").replace('publish(29,','publish(31,')
        text=text.replace('linear_model_sources_20261003','regularization_model_sources_20261003')
        text=text.replace('train_linear_bank_20261003','train_neural_regularization_bank_20261003')
        text=text.replace('linear_bank_20261003','neural_regularization_bank_20261003')
        text=text.replace('linear_augmentation','regularization_augmentation')
        text=text.replace('linear_limit_delta','regularization_limit_delta')
        text=text.replace('linear_role_causal_checks.json','regularization_role_causal_checks.json')
        text=text.replace('standalone_causal_checks.json','complete_scheme_causal_checks.json')
        text=text.replace('waiting_for_previous_round_and_linear_bank','waiting_for_previous_round_and_regularization_bank')
        for old,new in ((141,148),(142,149),(143,150),(144,151)):text=text.replace(str(old),str(new))
        if prefix=='optimize_training_round':
            text=text.replace("'expected_scored_records':104,'new_model_training':False,'new_fold_models_trained':0",
                              "'expected_scored_records':80,'new_model_training':True,'new_fold_models_trained':20")
            text=text.replace("'complete_output_foundation_round':28","'complete_output_foundation_round':30")
            text=text.replace("delta=delta+self._foundation_configuration.get('final_limit_delta',0.)",
                "delta=delta+self._foundation_configuration.get('final_limit_delta',0.)+self._foundation_configuration.get('linear_limit_delta',0.)")
            text=text.replace("'models_trained':0","'models_trained':20")
        elif prefix=='predict_final_roles_round':
            text=text.replace("winner['limit_up_delta']+winner.get('final_limit_delta',0.)",
                              "winner['limit_up_delta']+winner.get('final_limit_delta',0.)+winner.get('linear_limit_delta',0.)")
        elif prefix=='run_training_round':
            text=text.replace('未来一日线性信号的完整输出增量集成','匹配神经网络正则化变体的完整输出增量集成')
            text=text.replace('6种线性信号独立用途比较','4种正则化变体独立用途比较')
        elif prefix=='preflight_final_roles_round':text=text.replace('All18','All12')
        ast.parse(text,filename=str(target));target.write_text(text,encoding='utf-8',newline='\n');print(target)


if __name__=='__main__':main()
