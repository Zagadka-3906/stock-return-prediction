"""Prepare independent linear role additions to a frozen complete R28 foundation."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]


def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new)


def main():
    for prefix,suffix in (('optimize_training_round',''),('finalize_training_round',''),
            ('verify_methods_round',''),('predict_final_roles_round',''),
            ('preflight_final_roles_round',''),('run_training_round','_pipeline')):
        target=ROOT/f'analysis/{prefix}29{suffix}.py';assert not target.exists()
        text=(ROOT/f'analysis/{prefix}25{suffix}.py').read_text(encoding='utf-8')
        text=text.replace('Round25','Round29').replace('round25','round29').replace('_r25','_r29')
        text=text.replace('round24','round28').replace('_r24','_r28')
        text=text.replace("'round':25","'round':29").replace('publish(25,','publish(29,')
        text=text.replace('pairwise_model_sources_20261003','linear_model_sources_20261003')
        text=text.replace('train_pairwise_bank_20261003','train_linear_bank_20261003')
        text=text.replace('pairwise_bank_20261003','linear_bank_20261003')
        text=text.replace('final_augmentation','linear_augmentation').replace('final_limit_delta','linear_limit_delta')
        text=text.replace('final_role_causal_checks.json','linear_role_causal_checks.json')
        for old,new in ((127,141),(128,142),(129,143),(130,144)):
            text=text.replace(str(old),str(new))
        if prefix=='optimize_training_round':
            text=once(text,'MODELS=tuple(trainer.CONFIGS)','MODELS=tuple(trainer.NEW_CONFIGS)')
            text=once(text,"base,original=super().predict(donor,weight,retention,delta)",
                "import numpy as np\n        assert self._foundation_configuration==previous.configuration(baseline())\n        base=np.load(FOUNDATION/'selected_validation.npy',mmap_mode='r')[:len(self.dates)].copy()\n        original=deepcopy(read(FOUNDATION/'selection.json')['winner']['construction'])\n        delta=delta+self._foundation_configuration.get('final_limit_delta',0.)")
            text=text.replace("'expected_scored_records':452,'new_model_training':True,'new_fold_models_trained':20",
                              "'expected_scored_records':104,'new_model_training':False,'new_fold_models_trained':0")
            text=text.replace("'complete_output_foundation_round':24","'complete_output_foundation_round':28")
            text=text.replace("'models_trained':20","'models_trained':0")
        elif prefix=='predict_final_roles_round':
            text=text.replace("ctx.finish_output(base,winner['retention'],winner['limit_up_delta'])",
                "ctx.finish_output(base,winner['retention'],winner['limit_up_delta']+winner.get('final_limit_delta',0.))")
            text=text.replace("ctx.finish_output(np.load(source_base),winner['retention'],winner['limit_up_delta'])",
                "ctx.finish_output(np.load(source_base),winner['retention'],winner['limit_up_delta']+winner.get('final_limit_delta',0.))")
        elif prefix=='preflight_final_roles_round':
            text=once(text,"for name in ('pair_rank256_e32','pair_rank512_e32','rank512_window2_e32','nn_capacity_all5_rankmean'):",
                      "for name in m.MODELS:")
            text=text.replace('All12','All18')
        elif prefix=='run_training_round':
            text=text.replace('通用完整输出用途集成与成对排序容量变体','未来一日线性信号的完整输出增量集成')
        ast.parse(text,filename=str(target));target.write_text(text,encoding='utf-8',newline='\n')
        print(target)


if __name__=='__main__':main()
