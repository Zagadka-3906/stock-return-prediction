"""Prepare standalone regularization comparisons without preserving prior output layers."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]


def main():
    for prefix,suffix in (('optimize_training_round',''),('finalize_training_round',''),
            ('verify_methods_round',''),('predict_standalone_round',''),('reuse_candidate_round',''),
            ('preflight_standalone_round',''),('run_training_round','_pipeline')):
        target=ROOT/f'analysis/{prefix}32{suffix}.py';assert not target.exists()
        text=(ROOT/f'analysis/{prefix}28{suffix}.py').read_text(encoding='utf-8')
        text=text.replace('Round28','Round32').replace('round28','round32').replace('_r28','_r32')
        text=text.replace('round27','round31').replace('_r27','_r31')
        text=text.replace("'round':28","'round':32").replace('publish(28,','publish(32,')
        text=text.replace('linear_model_sources_20261003','regularization_model_sources_20261003')
        text=text.replace('train_linear_bank_20261003','train_neural_regularization_bank_20261003')
        text=text.replace('linear_bank_20261003','neural_regularization_bank_20261003')
        text=text.replace('linear_bank_preflight_20261003','neural_regularization_bank_20261003')
        for old,new in ((138,152),(139,153),(140,154)):text=text.replace(str(old),str(new))
        if prefix=='optimize_training_round':
            text=text.replace("PREVIOUS/'standalone_causal_checks.json'","PREVIOUS/'regularization_role_causal_checks.json'")
            text=text.replace("ROOT/'analysis/neural_regularization_bank_20261003/verification.json'",
                              "ROOT/'analysis/neural_regularization_bank_20261003/oof_audit.json'")
            text=text.replace("'expected_scored_records':152,'new_model_training':True,'new_fold_models_trained':30",
                              "'expected_scored_records':98,'new_model_training':False,'new_fold_models_trained':0")
            text=text.replace("'models_trained':30","'models_trained':0")
            needle="    cfg['standalone_replacement']=True;cfg['final_augmentation']={r:{'model':'none','weight':0.} for r in ('membership','top','rest')};cfg['final_limit_delta']=0."
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n    cfg['linear_augmentation']=deepcopy(cfg['final_augmentation']);cfg['linear_limit_delta']=0.\n    cfg['regularization_augmentation']=deepcopy(cfg['final_augmentation']);cfg['regularization_limit_delta']=0.")
            text=text.replace('all six one-day linear backbones','all four matched neural regularization backbones')
        elif prefix=='run_training_round':
            text=text.replace("optimization_20261003_r31/standalone_causal_checks.json","optimization_20261003_r31/regularization_role_causal_checks.json")
            text=text.replace('未来一日线性秩与收益模型的独立完整比较','匹配神经网络正则化变体的独立完整主模型比较')
            text=text.replace('6个一日线性主模型独立平滑与辅助信号比较','4个正则化主模型独立平滑与辅助信号比较')
        ast.parse(text,filename=str(target));target.write_text(text,encoding='utf-8',newline='\n');print(target)


if __name__=='__main__':main()
