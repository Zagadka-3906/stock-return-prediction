"""Create an unfrozen standalone linear round from the checked standalone workflow."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]


def replace_once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new)


def main():
    names=('optimize_training_round','finalize_training_round','verify_methods_round',
           'predict_standalone_round','reuse_candidate_round','preflight_standalone_round',
           'run_training_round')
    for prefix in names:
        suffix='_pipeline' if prefix=='run_training_round' else ''
        target=ROOT/f'analysis/{prefix}28{suffix}.py'
        assert not target.exists(),target
        text=(ROOT/f'analysis/{prefix}27{suffix}.py').read_text(encoding='utf-8')
        text=text.replace('Round27','Round28').replace('round27','round28')
        text=text.replace('_r27','_r28').replace('_r26','_r27')
        text=text.replace('round26','round27').replace('round":27','round":28').replace("'round':27","'round':28")
        text=text.replace('round": 27','round": 28').replace("'round': 27","'round': 28")
        text=text.replace('pairwise_model_sources_20261003','linear_model_sources_20261003')
        text=text.replace('train_pairwise_bank_20261003','train_linear_bank_20261003')
        text=text.replace('pairwise_bank_20261003','linear_bank_20261003')
        text=text.replace('market_regime_causal_checks.json','standalone_causal_checks.json')
        for old,new in ((135,138),(136,139),(137,140)):
            text=text.replace(str(old),str(new))
        if prefix=='optimize_training_round':
            text=text.replace("FIELDS=previous.FIELDS+('standalone_replacement',)",'FIELDS=previous.FIELDS')
            text=text.replace("'expected_scored_records':98,'new_model_training':False,'new_fold_models_trained':0",
                              "'expected_scored_records':138,'new_model_training':True,'new_fold_models_trained':30")
            text=text.replace('all four new RankNet backbones','all six one-day linear backbones')
            text=replace_once(text,"return promote if self.standalone_replacement else super().donor(promote,rerank_weight)","return promote")
            text=replace_once(text,"if not self.standalone_replacement:return super().predict(donor,weight,retention,delta)",
                "if not self.standalone_replacement:\n            assert configuration(self._current_cfg)==baseline()\n            pred=np.load(PREVIOUS/'selected_validation.npy',mmap_mode='r')[:len(self.dates)].copy()\n            return pred,deepcopy(read(PREVIOUS/'selection.json')['winner']['construction'])")
            old="super().configure(cfg);self.standalone=deepcopy(cfg.get('standalone'));self.standalone_replacement=cfg.get('standalone_replacement',False)"
            text=replace_once(text,old,old+";self._current_cfg=deepcopy(cfg)")
            text=text.replace("PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',PREVIOUS/'standalone_causal_checks.json',",
                "PREVIOUS/'selected_validation.npy',PREVIOUS/'promote_baseline.npy',PREVIOUS/'standalone_causal_checks.json',\n             ROOT/'analysis/train_diverse_backbones_20261003.py',\n             ROOT/'analysis/linear_bank_preflight_20261003/verification.json',")
            text=text.replace("'models_trained':0,'test_data_read':False","'models_trained':30,'test_data_read':False")
        elif prefix=='preflight_standalone_round':
            text=replace_once(text,"for name in ('pair_rank256_e32','pair_rank512_e32','pair_rank128_t005_e32','pair_rank128_t020_e32'):",
                              "for name in m.MODELS:")
        elif prefix=='run_training_round':
            text=text.replace("state('publication_and_ranking_qa')\n    result=publish(27,", "state('publication_and_ranking_qa')\n    result=publish(28,")
            text=text.replace('成对排序容量与温度变体的独立主模型比较','未来一日线性秩与收益模型的独立完整比较')
            text=text.replace('4个成对排序主模型独立平滑与辅助信号比较','6个一日线性主模型独立平滑与辅助信号比较')
        ast.parse(text,filename=str(target))
        target.write_text(text,encoding='utf-8',newline='\n')
        print(target)


if __name__=='__main__':main()
