"""Summarize the repaired complete optimization; preserve prior experiment evidence."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round7 import OUT,ENSEMBLES,WAVES,read,dump,sha
import json


def main():
    selection=read(OUT/'selection.json');winner=selection['winner']
    validation=read(OUT/'causal_validation.json');csv=read(OUT/'calibrated_csv_official.json')
    candidate=ROOT/'candidates/optimization_20261003_r7';prediction=read(candidate/'verification.json')
    assert validation['status']==csv['status']==prediction['status']=='passed'
    assert sha(candidate/'submission.csv')==prediction['csv_sha256']
    assert prediction['old_delivery_pointer_unchanged']
    baseline=read(OUT/'wave59_results.json')['results']['five_fold_local_membership0.0125']['metrics']
    change={key:winner['metrics'][key]-baseline[key] for key in ('ic_mean','annual_excess','mean_turnover')}
    contribution={'RankIC':.4*change['ic_mean'],'annual_excess':.3*change['annual_excess'],'turnover':-.3*change['mean_turnover']}
    assert abs(sum(contribution.values())-selection['score_gain'])<1e-12
    counts={str(w):len(read(OUT/f'wave{w}_results.json')['results']) for w in WAVES}
    result={'status':'complete','scope':'waves59–61','winner':winner,'baseline_score':selection['baseline_score'],
            'score_gain':selection['score_gain'],'historical_uncorrected_validation_score':selection['historical_uncorrected_score'],
            'historical_score_is_not_a_compliant_baseline':True,
            'scored_records':sum(counts.values()),'records_per_wave':counts,
            'total_scored_records_including_repeats':1156+sum(counts.values()),
            'new_fold_models_trained':0,'ensemble_components':ENSEMBLES[winner['ensemble_name']],
            'feature_selection_dependency_repaired':True,'component_audit':read(OUT/'component_audit.json'),
            'metric_change_vs_repaired_baseline':change,'score_contributions_vs_repaired_baseline':contribution,
            'validation':validation,'calibrated_written_csv':csv,'prediction':prediction,
            'candidate_submission':str(candidate/'submission.csv'),'test_labels_read_this_round':False,
            'test_score_of_this_candidate':None,'old_deliveries_preserved':True,
            'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
            'block_prefix_controls':read(OUT/'block_prefix_controls.json'),
            'repair_amendment':read(OUT/'repair_amendment.json'),
            'followup_directions':['Re-optimize checkpoint mixture and TopK finishing on the pruning-free orderer.',
                                  'Test member weights inside the pruning-free tree/GRU ensemble.',
                                  'Re-evaluate drop/add retention scores against the repaired complete pipeline.']}
    dump(ROOT/'results/optimization_20261003_r7.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r7.json',{'status':'complete','ranking':selection['ranking']})
    dump(candidate/'manifest.json',{'status':'passed','files':{p.relative_to(candidate).as_posix():
         {'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(candidate.rglob('*')) if p.is_file() and p.name!='manifest.json'}})
    readme=ROOT/'README.md';heading='### 第七轮：验证来源修正与无剪枝集成（波59–61）'
    text=readme.read_text(encoding='utf-8-sig')
    if heading not in text:
        note=f'''\n\n{heading}\n\n旧W5a含基于全时期重要性的剪枝成员，因此此前R1–R6验证最高分0.447406500保留为历史诊断，不再作为本轮合规比较基准。来源证据与逐年修正检查见 `results/validation_provenance_erratum_20261003.json`。\n\n本轮完成{sum(counts.values())}条完整方案评分。修正后的同设置基准为{selection['baseline_score']:.12f}，最高分为 **{winner['connected_final_score']:.12f}**，提高 **{selection['score_gain']:.12f}**。选中 `{winner['ensemble_name']}`，成员混合权重{winner['membership_w5a_weight']:g}，Top组排序slow16权重{winner['top_slow_weight']:g}，其余股票权重{winner['slow16_weight']:g}，留存{winner['retention']:g}，涨停偏移{winner['limit_up_delta']:g}。\n\n年度连续评分、只用成熟过去标签的收益校准、实际验证CSV官方评分、未来追加前缀不变性、测试X预测重放及CSV秩往返检查均通过。新候选为 `candidates/optimization_20261003_r7/submission.csv`；本轮未读取测试标签，旧正式交付指针保留。完整更新榜见 `results/all_model_rankings_20261003.html`。\n'''
        readme.write_text(text.rstrip()+note,encoding='utf-8')
    print(json.dumps({'score':winner['connected_final_score'],'gain_vs_repaired_baseline':selection['score_gain'],
                      'records':sum(counts.values()),'candidate':str(candidate/'submission.csv')},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
